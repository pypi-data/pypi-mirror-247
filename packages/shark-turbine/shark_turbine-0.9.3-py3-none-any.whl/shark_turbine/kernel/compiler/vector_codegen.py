"""Code generation for generating vector-dialect based kernels.

Such kernels operate on global memory at the boundary, scheduling
actual loads/stores/computes to local vectors using PyTorch tensor
level operations executed as threads over a grid.
"""
from typing import Any, Callable, Type, Optional, Sequence, Union

from dataclasses import dataclass
import inspect
import operator as py_operator

import torch
import torch.fx as fx

from .._support.indexing import (
    Grid,
    IndexingContext,
    KernelBuffer,
    SymbolDef,
    is_kernel_buffer_meta_derived,
)

from ..lang import (
    Index,
)

from .. import ops

from .analysis import (
    SliceAnalysis,
)

from .builder import (
    ModuleBuilder,
    ScalarBuilder,
)

from .base import (
    CodegenError,
    ValidationError,
)

from .ir import (
    AffineMap,
    AffineMapAttr,
    FunctionType,
    IndexType,
    InsertionPoint,
    IrType,
    Location,
    MemRefType,
    ShapedType,
    Value,
    VectorType,
    arith_d,
    func_d,
    math_d,
    vector_d,
)

from .kernel_codegen import (
    BoundKernelSignature,
)

from . import op_matchers

ArgTypeUnion = Union[SymbolDef, Type[KernelBuffer]]


@dataclass
class NodeAttrs:
    # By default, integers are assumed signed. We propagate unsigned as graph
    # node attrs.
    unsigned: bool = False

    @staticmethod
    def load(py_value) -> "NodeAttrs":
        if isinstance(py_value, fx.Node):
            return NodeAttrs(unsigned=bool(py_value.meta.get("unsigned")))
        return NodeAttrs()

    def store(self, node: fx.Node):
        node.meta["unsigned"] = self.unsigned


class ThreadEmitter:
    """Emits a 'thread function' as a `func` with a signature derived from the gm."""

    OP_HANDLERS: dict[Any, Callable[["ThreadEmitter", fx.Node], None]] = {}

    def __init__(self, sig: BoundKernelSignature):
        self._node_values: dict[fx.Node, Value] = {}
        self._grid_axis_values: dict[int, Value] = {}
        self._sig = sig
        self.ip = InsertionPoint(sig.entry_block)

    def lookup_node_value(self, node: fx.Node) -> Value:
        value = self._node_values.get(node)
        if value is None:
            value = self._sig.resolve_by_reference(("node", node))
            self._node_values[node] = value
        return value

    def lookup_grid_axis_value(self, grid_axis: int) -> Value:
        value = self._grid_axis_values.get(grid_axis)
        if value is None:
            try:
                value = self._sig.resolve_by_reference(("grid", grid_axis))
            except KeyError:
                raise CodegenError(f"Grid axis {grid_axis} out of bounds")
            self._node_values[grid_axis] = value
        return value

    def bind_node_result(
        self, node: fx.Node, value: Value, *, attrs: Optional[NodeAttrs] = None
    ):
        assert (
            node not in self._node_values
        ), f"Cannot rebind node {node}: already bound"
        if attrs is not None:
            attrs.store(node)
        self._node_values[node] = value

    def emit_graph(self, graph: fx.Graph):
        for node in graph.nodes:
            # TODO: Construct a location for the node.
            with self.ip, Location.unknown():
                if node.op == "call_function":
                    self.emit_function_call_node(node)

    def emit_function_call_node(self, node: fx.Node):
        target_op = node.target
        try:
            handler = self.OP_HANDLERS[target_op]
        except KeyError:
            raise CodegenError(f"No handler registered for op {target_op}")
        handler(self, node)

    def finish(self):
        with self.ip, Location.unknown():
            func_d.ReturnOp([])


def handle_op(op):
    def decorator(f: Callable[["ThreadEmitter", fx.Node], None]):
        ThreadEmitter.OP_HANDLERS[op] = f
        return None

    return decorator


###############################################################################
# Python/scalar ops
###############################################################################

BINARY_ARITHMETIC_OPS = [
    (py_operator.add, "add"),
    (py_operator.mul, "mul"),
    (py_operator.sub, "sub"),
    (py_operator.mod, "mod"),
    (py_operator.floordiv, "floordiv"),
    (py_operator.truediv, "truediv"),
]


def binary_broadcast(lhs: Value, rhs: Value) -> tuple[bool, Value, Value]:
    lhs_type = lhs.type
    rhs_type = rhs.type
    lhs_is_vector = VectorType.isinstance(lhs_type)
    rhs_is_vector = VectorType.isinstance(rhs_type)
    if not lhs_is_vector and not rhs_is_vector:
        # Not vectors: return as-is.
        return False, lhs, rhs

    # Promote to vector.
    if not lhs_is_vector:
        lhs = vector_d.splat(VectorType([], lhs_type), lhs)
    if not rhs_is_vector:
        rhs = vector_d.splat(VectorType([], rhs_type), rhs)
    lhs_type = VectorType(lhs.type)
    rhs_type = VectorType(rhs.type)

    broadcast_shape = lhs_type.shape
    rhs_shape = rhs_type.shape
    rank = max(len(broadcast_shape), len(rhs_shape))
    while len(broadcast_shape) < rank:
        broadcast_shape.insert(0, 1)
    while len(rhs_shape) < rank:
        rhs_shape.insert(0, 1)

    for i in range(rank):
        a = broadcast_shape[i]
        b = rhs_shape[i]
        if a != b:
            if a != 1 and b != 1:
                raise CodegenError(
                    f"Binary operands are not broadcast compatible: {lhs_type}, {rhs_type}"
                )
            broadcast_shape[i] = rhs_shape[i] = max(a, b)

    lhs_type = VectorType.get(broadcast_shape, lhs_type.element_type)
    rhs_type = VectorType.get(broadcast_shape, rhs_type.element_type)
    if lhs_type != lhs.type:
        lhs = vector_d.broadcast(lhs_type, lhs)
    if rhs_type != rhs.type:
        rhs = vector_d.broadcast(rhs_type, rhs)
    return True, lhs, rhs


def _define_arithmetic_handlers():
    def register(py_operator, mnemonic):
        @handle_op(py_operator)
        def _(emitter: ThreadEmitter, node: fx.Node):
            try:
                lhs, rhs = node.args
            except ValueError as e:
                raise ValidationError("Malformed arguments") from e

            lhs = cast_py_value(emitter, lhs)
            rhs = cast_py_value(emitter, rhs)
            is_vector, lhs, rhs = binary_broadcast(lhs, rhs)
            if is_vector:
                result = ScalarBuilder.binary_vector_arithmetic(mnemonic, lhs, rhs)
            else:
                result = ScalarBuilder.binary_arithmetic(mnemonic, lhs, rhs)
            emitter.bind_node_result(node, result)

    for py_operator, mnemonic in BINARY_ARITHMETIC_OPS:
        # Need to capture these per iteration, not just final value,
        # so call a function.
        register(py_operator, mnemonic)


_define_arithmetic_handlers()

###############################################################################
# Core data movement and indexing ops
###############################################################################


@handle_op(ops.thread_program_id)
def _(emitter: ThreadEmitter, node: fx.Node):
    try:
        (axis,) = node.args
        axis = Index(axis)
    except ValueError as e:
        raise ValidationError("Malformed arguments") from e

    value = emitter.lookup_grid_axis_value(axis)
    emitter.bind_node_result(node, value)


@handle_op(ops.kernel_buffer_getitem)
def _(emitter: ThreadEmitter, node: fx.Node):
    try:
        kb, slice_spec = node.args
    except ValueError as e:
        raise ValidationError("Malformed arguments") from e

    kb_src, kb_ir_type, kb_py_type = cast_kernel_buffer(emitter, kb)
    sa = SliceAnalysis(kb_py_type.symbolic_shape, slice_spec)
    sa.normalize_symbolic_ranges()
    vector_shape = sa.symbolic_shape
    element_type = kb_ir_type.element_type
    vector_type = VectorType.get(vector_shape, element_type)
    pad_attr = ScalarBuilder.zero_attr(element_type)
    indices = cast_indices(emitter, [s.start for s in sa.slices])
    pad_value = arith_d.constant(pad_attr)
    result = vector_d.transfer_read(
        vector_type, kb_src, indices, AffineMap.get_identity(len(indices)), pad_value
    )
    emitter.bind_node_result(node, result)


@handle_op(ops.kernel_buffer_setitem)
def _(emitter: ThreadEmitter, node: fx.Node):
    try:
        kb, slice_spec, item = node.args
    except ValueError as e:
        raise ValidationError("Malformed arguments") from e

    kb_dest, kb_ir_type, kb_py_type = cast_kernel_buffer(emitter, kb)
    dest_rank = kb_ir_type.rank
    sa = SliceAnalysis(kb_py_type.symbolic_shape, slice_spec)
    sa.normalize_symbolic_ranges()
    indices = cast_indices(emitter, [s.start for s in sa.slices])
    if dest_rank != len(indices):
        raise CodegenError(
            f"Mismatched slice assignment: Expected rank {dest_rank}, got {len(indices)}"
        )
    insert_vector = cast_vector(emitter, item, element_type=kb_ir_type.element_type)
    insert_type = VectorType(insert_vector.type)
    insert_rank = insert_type.rank

    # Special case rank-0 broadcast.
    if insert_rank == 0:
        broadcast_type = VectorType.get(dest_rank * [1], kb_ir_type.element_type)
        insert_vector = vector_d.broadcast(broadcast_type, insert_vector)

    permutation_map = AffineMap.get_identity(dest_rank)
    vector_d.transfer_write(
        None, insert_vector, kb_dest, indices, AffineMapAttr.get(permutation_map)
    )


###############################################################################
# Torch and math ops
###############################################################################


@handle_op(torch.exp)
def _(emitter: ThreadEmitter, node: fx.Node):
    args = op_matchers.torch_exp(*node.args, **node.kwargs)
    raw_input = args["input"]
    input = cast_vector(emitter, raw_input)
    result = math_d.exp(input)
    emitter.bind_node_result(node, result)


@handle_op(torch.max)
def _(emitter: ThreadEmitter, node: fx.Node):
    args = op_matchers.torch_max_unary(
        *node.args, **node.kwargs
    ) or op_matchers.torch_max(*node.args, **node.kwargs)

    def combiner(element_type: IrType, attrs: NodeAttrs) -> vector_d.CombiningKind:
        if ScalarBuilder.is_floating_point_type(element_type):
            # Non-NaN propagating.
            # TODO: Carry a "fastmath" flag on the emitter and choose between this
            # and MAXIMUMF?
            return vector_d.CombiningKind.MAXF
        elif ScalarBuilder.is_integer_type(element_type):
            return (
                vector_d.CombiningKind.MAXUI
                if attrs.unsigned
                else vector_d.CombiningKind.MAXSI
            )

    emit_reduction(emitter, node, args, combiner)


@handle_op(torch.sum)
def _(emitter: ThreadEmitter, node: fx.Node):
    args = op_matchers.torch_sum_unary(
        *node.args, **node.kwargs
    ) or op_matchers.torch_sum(*node.args, **node.kwargs)

    def combiner(element_type: IrType, attrs: NodeAttrs) -> vector_d.CombiningKind:
        return vector_d.CombiningKind.ADD

    emit_reduction(emitter, node, args, combiner)


def emit_reduction(
    emitter: ThreadEmitter,
    node: fx.Node,
    args: dict,
    combiner_callback: Callable[[IrType], vector_d.CombiningKind],
):
    # Setup.
    raw_input = args["input"]
    attrs = NodeAttrs.load(raw_input)
    input = cast_vector(emitter, raw_input)
    vector_type = VectorType(input.type)
    element_type = vector_type.element_type
    rank = vector_type.rank
    zero = arith_d.constant(ScalarBuilder.zero_attr(element_type))
    combiner = combiner_callback(element_type, attrs)

    if len(args) == 1:
        # Reduce to scalar.
        scalar_result = vector_d.multi_reduction(
            combiner, input, zero, list(range(rank))
        )
        result = vector_d.splat(VectorType.get([], element_type), scalar_result)
        emitter.bind_node_result(node, result, attrs=attrs)
    else:
        # Reduce to vector.
        raise CodegenError("NYI: Reduce to vector")


###############################################################################
# Conversion utilities
###############################################################################


def cast_py_value(emitter: ThreadEmitter, value) -> Value:
    if isinstance(value, fx.Node):
        try:
            return emitter.lookup_node_value(value)
        except KeyError:
            raise CodegenError(f"Producer node `{value}` has no IR Value")

    return ScalarBuilder.constant(value)


def cast_py_lvalue(emitter: ThreadEmitter, py_value) -> tuple[Value, fx.Node]:
    if isinstance(py_value, fx.Node):
        try:
            return emitter.lookup_node_value(py_value), py_value
        except KeyError:
            raise CodegenError(f"Producer node `{py_value}` has no IR Value")
    else:
        raise CodegenError(
            f"Required a traced node in the graph. Got: {py_value} (type {type(py_value)})"
        )


def cast_kernel_buffer(
    emitter: ThreadEmitter, kb
) -> tuple[Value, MemRefType, Type[KernelBuffer]]:
    """Casts a Python value of type KernelBuffer, which lowers to a MemRefType'd value."""
    value, node = cast_py_lvalue(emitter, kb)
    ir_type = value.type
    py_type = node.type

    if not MemRefType.isinstance(ir_type):
        raise CodegenError(
            f"Expected a KernelBuffer (aka. `memref`) but got `{ir_type}`"
        )

    if not issubclass(py_type, KernelBuffer):
        raise CodegenError(
            f"Expected an lvalue of type KernelBuffer but got '{py_type}' for node {node}"
        )

    return value, MemRefType(ir_type), py_type


def cast_indices(emitter: ThreadEmitter, slice) -> list[Value]:
    if not isinstance(slice, (tuple, list)):
        slice = (slice,)
    ir_slice = [cast_py_value(emitter, s) for s in slice]
    return ir_slice


def cast_vector(
    emitter: ThreadEmitter, value, *, element_type: Optional[IrType] = None
):
    value = cast_py_value(emitter, value)

    # Promote scalar types correctly first.
    if element_type and not ShapedType.isinstance(value.type):
        # Implicit scalar type promotion.
        value = ScalarBuilder.promote(value, element_type)

    # After scalar promotion, promote to vector.
    if VectorType.isinstance(value.type):
        # Already a vector. Coerce or return.
        if element_type is not None:
            vector_type = VectorType(value.type)
            if vector_type.element_type == element_type:
                return value
            # TODO: Implement vector element type conversion.
            raise CodegenError(
                f"Implicit conversion of vector element types not supported (`{vector_type.element_type}` -> `{element_type}`)"
            )
        # No target element_type.
        return value
    else:
        # Scalar -> vector.
        element_type = value.type
        vector_type = VectorType.get([], element_type)
        return vector_d.splat(vector_type, value)
