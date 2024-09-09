"""Immutable number vars."""

from __future__ import annotations

import dataclasses
import json
import sys
from typing import Any, Callable, TypeVar, Union

from reflex.vars import ImmutableVarData, Var, VarData

from .base import (
    CachedVarOperation,
    CustomVarOperationReturn,
    ImmutableVar,
    LiteralVar,
    cached_property_no_lock,
    unionize,
    var_operation,
    var_operation_return,
)

NUMBER_T = TypeVar("NUMBER_T", int, float, Union[int, float])


class NumberVar(ImmutableVar[NUMBER_T]):
    """Base class for immutable number vars."""

    def __add__(self, other: number_types | boolean_types):
        """Add two numbers.

        Args:
            other: The other number.

        Returns:
            The number addition operation.
        """
        return number_add_operation(self, +other)

    def __radd__(self, other: number_types | boolean_types):
        """Add two numbers.

        Args:
            other: The other number.

        Returns:
            The number addition operation.
        """
        return number_add_operation(+other, self)

    def __sub__(self, other: number_types | boolean_types):
        """Subtract two numbers.

        Args:
            other: The other number.

        Returns:
            The number subtraction operation.
        """
        return number_subtract_operation(self, +other)

    def __rsub__(self, other: number_types | boolean_types):
        """Subtract two numbers.

        Args:
            other: The other number.

        Returns:
            The number subtraction operation.
        """
        return number_subtract_operation(+other, self)

    def __abs__(self):
        """Get the absolute value of the number.

        Returns:
            The number absolute operation.
        """
        return number_abs_operation(self)

    def __mul__(self, other: number_types | boolean_types):
        """Multiply two numbers.

        Args:
            other: The other number.

        Returns:
            The number multiplication operation.
        """
        return number_multiply_operation(self, +other)

    def __rmul__(self, other: number_types | boolean_types):
        """Multiply two numbers.

        Args:
            other: The other number.

        Returns:
            The number multiplication operation.
        """
        return number_multiply_operation(+other, self)

    def __truediv__(self, other: number_types | boolean_types):
        """Divide two numbers.

        Args:
            other: The other number.

        Returns:
            The number true division operation.
        """
        return number_true_division_operation(self, +other)

    def __rtruediv__(self, other: number_types | boolean_types):
        """Divide two numbers.

        Args:
            other: The other number.

        Returns:
            The number true division operation.
        """
        return number_true_division_operation(+other, self)

    def __floordiv__(self, other: number_types | boolean_types):
        """Floor divide two numbers.

        Args:
            other: The other number.

        Returns:
            The number floor division operation.
        """
        return number_floor_division_operation(self, +other)

    def __rfloordiv__(self, other: number_types | boolean_types):
        """Floor divide two numbers.

        Args:
            other: The other number.

        Returns:
            The number floor division operation.
        """
        return number_floor_division_operation(+other, self)

    def __mod__(self, other: number_types | boolean_types):
        """Modulo two numbers.

        Args:
            other: The other number.

        Returns:
            The number modulo operation.
        """
        return number_modulo_operation(self, +other)

    def __rmod__(self, other: number_types | boolean_types):
        """Modulo two numbers.

        Args:
            other: The other number.

        Returns:
            The number modulo operation.
        """
        return number_modulo_operation(+other, self)

    def __pow__(self, other: number_types | boolean_types):
        """Exponentiate two numbers.

        Args:
            other: The other number.

        Returns:
            The number exponent operation.
        """
        return number_exponent_operation(self, +other)

    def __rpow__(self, other: number_types | boolean_types):
        """Exponentiate two numbers.

        Args:
            other: The other number.

        Returns:
            The number exponent operation.
        """
        return number_exponent_operation(+other, self)

    def __neg__(self):
        """Negate the number.

        Returns:
            The number negation operation.
        """
        return number_negate_operation(self)

    def __invert__(self):
        """Boolean NOT the number.

        Returns:
            The boolean NOT operation.
        """
        return boolean_not_operation(self.bool())

    def __pos__(self) -> NumberVar:
        """Positive the number.

        Returns:
            The number.
        """
        return self

    def __round__(self):
        """Round the number.

        Returns:
            The number round operation.
        """
        return number_round_operation(self)

    def __ceil__(self):
        """Ceil the number.

        Returns:
            The number ceil operation.
        """
        return number_ceil_operation(self)

    def __floor__(self):
        """Floor the number.

        Returns:
            The number floor operation.
        """
        return number_floor_operation(self)

    def __trunc__(self):
        """Trunc the number.

        Returns:
            The number trunc operation.
        """
        return number_trunc_operation(self)

    def __lt__(self, other: Any):
        """Less than comparison.

        Args:
            other: The other number.

        Returns:
            The result of the comparison.
        """
        if isinstance(other, (NumberVar, BooleanVar, int, float, bool)):
            return less_than_operation(self, +other)
        return less_than_operation(self, other)

    def __le__(self, other: Any):
        """Less than or equal comparison.

        Args:
            other: The other number.

        Returns:
            The result of the comparison.
        """
        if isinstance(other, (NumberVar, BooleanVar, int, float, bool)):
            return less_than_or_equal_operation(self, +other)
        return less_than_or_equal_operation(self, other)

    def __eq__(self, other: Any):
        """Equal comparison.

        Args:
            other: The other number.

        Returns:
            The result of the comparison.
        """
        if isinstance(other, (NumberVar, BooleanVar, int, float, bool)):
            return equal_operation(self, +other)
        return equal_operation(self, other)

    def __ne__(self, other: Any):
        """Not equal comparison.

        Args:
            other: The other number.

        Returns:
            The result of the comparison.
        """
        if isinstance(other, (NumberVar, BooleanVar, int, float, bool)):
            return not_equal_operation(self, +other)
        return not_equal_operation(self, other)

    def __gt__(self, other: Any):
        """Greater than comparison.

        Args:
            other: The other number.

        Returns:
            The result of the comparison.
        """
        if isinstance(other, (NumberVar, BooleanVar, int, float, bool)):
            return greater_than_operation(self, +other)
        return greater_than_operation(self, other)

    def __ge__(self, other: Any):
        """Greater than or equal comparison.

        Args:
            other: The other number.

        Returns:
            The result of the comparison.
        """
        if isinstance(other, (NumberVar, BooleanVar, int, float, bool)):
            return greater_than_or_equal_operation(self, +other)
        return greater_than_or_equal_operation(self, other)

    def bool(self):
        """Boolean conversion.

        Returns:
            The boolean value of the number.
        """
        return self != 0


def binary_number_operation(
    func: Callable[[NumberVar, NumberVar], str],
) -> Callable[[number_types, number_types], NumberVar]:
    """Decorator to create a binary number operation.

    Args:
        func: The binary number operation function.

    Returns:
        The binary number operation.
    """

    @var_operation
    def operation(lhs: NumberVar, rhs: NumberVar):
        return var_operation_return(
            js_expression=func(lhs, rhs),
            var_type=unionize(lhs._var_type, rhs._var_type),
        )

    def wrapper(lhs: number_types, rhs: number_types) -> NumberVar:
        """Create the binary number operation.

        Args:
            lhs: The first number.
            rhs: The second number.

        Returns:
            The binary number operation.
        """
        return operation(lhs, rhs)  # type: ignore

    return wrapper


@binary_number_operation
def number_add_operation(lhs: NumberVar, rhs: NumberVar):
    """Add two numbers.

    Args:
        lhs: The first number.
        rhs: The second number.

    Returns:
        The number addition operation.
    """
    return f"({lhs} + {rhs})"


@binary_number_operation
def number_subtract_operation(lhs: NumberVar, rhs: NumberVar):
    """Subtract two numbers.

    Args:
        lhs: The first number.
        rhs: The second number.

    Returns:
        The number subtraction operation.
    """
    return f"({lhs} - {rhs})"


@var_operation
def number_abs_operation(value: NumberVar):
    """Get the absolute value of the number.

    Args:
        value: The number.

    Returns:
        The number absolute operation.
    """
    return var_operation_return(
        js_expression=f"Math.abs({value})", var_type=value._var_type
    )


@binary_number_operation
def number_multiply_operation(lhs: NumberVar, rhs: NumberVar):
    """Multiply two numbers.

    Args:
        lhs: The first number.
        rhs: The second number.

    Returns:
        The number multiplication operation.
    """
    return f"({lhs} * {rhs})"


@var_operation
def number_negate_operation(
    value: NumberVar[NUMBER_T],
) -> CustomVarOperationReturn[NUMBER_T]:
    """Negate the number.

    Args:
        value: The number.

    Returns:
        The number negation operation.
    """
    return var_operation_return(js_expression=f"-({value})", var_type=value._var_type)


@binary_number_operation
def number_true_division_operation(lhs: NumberVar, rhs: NumberVar):
    """Divide two numbers.

    Args:
        lhs: The first number.
        rhs: The second number.

    Returns:
        The number true division operation.
    """
    return f"({lhs} / {rhs})"


@binary_number_operation
def number_floor_division_operation(lhs: NumberVar, rhs: NumberVar):
    """Floor divide two numbers.

    Args:
        lhs: The first number.
        rhs: The second number.

    Returns:
        The number floor division operation.
    """
    return f"Math.floor({lhs} / {rhs})"


@binary_number_operation
def number_modulo_operation(lhs: NumberVar, rhs: NumberVar):
    """Modulo two numbers.

    Args:
        lhs: The first number.
        rhs: The second number.

    Returns:
        The number modulo operation.
    """
    return f"({lhs} % {rhs})"


@binary_number_operation
def number_exponent_operation(lhs: NumberVar, rhs: NumberVar):
    """Exponentiate two numbers.

    Args:
        lhs: The first number.
        rhs: The second number.

    Returns:
        The number exponent operation.
    """
    return f"({lhs} ** {rhs})"


@var_operation
def number_round_operation(value: NumberVar):
    """Round the number.

    Args:
        value: The number.

    Returns:
        The number round operation.
    """
    return var_operation_return(js_expression=f"Math.round({value})", var_type=int)


@var_operation
def number_ceil_operation(value: NumberVar):
    """Ceil the number.

    Args:
        value: The number.

    Returns:
        The number ceil operation.
    """
    return var_operation_return(js_expression=f"Math.ceil({value})", var_type=int)


@var_operation
def number_floor_operation(value: NumberVar):
    """Floor the number.

    Args:
        value: The number.

    Returns:
        The number floor operation.
    """
    return var_operation_return(js_expression=f"Math.floor({value})", var_type=int)


@var_operation
def number_trunc_operation(value: NumberVar):
    """Trunc the number.

    Args:
        value: The number.

    Returns:
        The number trunc operation.
    """
    return var_operation_return(js_expression=f"Math.trunc({value})", var_type=int)


class BooleanVar(ImmutableVar[bool]):
    """Base class for immutable boolean vars."""

    def __invert__(self):
        """NOT the boolean.

        Returns:
            The boolean NOT operation.
        """
        return boolean_not_operation(self)

    def __int__(self):
        """Convert the boolean to an int.

        Returns:
            The boolean to int operation.
        """
        return boolean_to_number_operation(self)

    def __pos__(self):
        """Convert the boolean to an int.

        Returns:
            The boolean to int operation.
        """
        return boolean_to_number_operation(self)

    def bool(self) -> BooleanVar:
        """Boolean conversion.

        Returns:
            The boolean value of the boolean.
        """
        return self

    def __lt__(self, other: boolean_types | number_types):
        """Less than comparison.

        Args:
            other: The other boolean.

        Returns:
            The result of the comparison.
        """
        return less_than_operation(+self, +other)

    def __le__(self, other: boolean_types | number_types):
        """Less than or equal comparison.

        Args:
            other: The other boolean.

        Returns:
            The result of the comparison.
        """
        return less_than_or_equal_operation(+self, +other)

    def __eq__(self, other: boolean_types | number_types):
        """Equal comparison.

        Args:
            other: The other boolean.

        Returns:
            The result of the comparison.
        """
        return equal_operation(+self, +other)

    def __ne__(self, other: boolean_types | number_types):
        """Not equal comparison.

        Args:
            other: The other boolean.

        Returns:
            The result of the comparison.
        """
        return not_equal_operation(+self, +other)

    def __gt__(self, other: boolean_types | number_types):
        """Greater than comparison.

        Args:
            other: The other boolean.

        Returns:
            The result of the comparison.
        """
        return greater_than_operation(+self, +other)

    def __ge__(self, other: boolean_types | number_types):
        """Greater than or equal comparison.

        Args:
            other: The other boolean.

        Returns:
            The result of the comparison.
        """
        return greater_than_or_equal_operation(+self, +other)


@var_operation
def boolean_to_number_operation(value: BooleanVar):
    """Convert the boolean to a number.

    Args:
        value: The boolean.

    Returns:
        The boolean to number operation.
    """
    return var_operation_return(js_expression=f"Number({value})", var_type=int)


def comparison_operator(
    func: Callable[[Var, Var], str],
) -> Callable[[Var | Any, Var | Any], BooleanVar]:
    """Decorator to create a comparison operation.

    Args:
        func: The comparison operation function.

    Returns:
        The comparison operation.
    """

    @var_operation
    def operation(lhs: Var, rhs: Var):
        return var_operation_return(
            js_expression=func(lhs, rhs),
            var_type=bool,
        )

    def wrapper(lhs: Var | Any, rhs: Var | Any) -> BooleanVar:
        """Create the comparison operation.

        Args:
            lhs: The first value.
            rhs: The second value.

        Returns:
            The comparison operation.
        """
        return operation(lhs, rhs)

    return wrapper


@comparison_operator
def greater_than_operation(lhs: Var, rhs: Var):
    """Greater than comparison.

    Args:
        lhs: The first value.
        rhs: The second value.

    Returns:
        The result of the comparison.
    """
    return f"({lhs} > {rhs})"


@comparison_operator
def greater_than_or_equal_operation(lhs: Var, rhs: Var):
    """Greater than or equal comparison.

    Args:
        lhs: The first value.
        rhs: The second value.

    Returns:
        The result of the comparison.
    """
    return f"({lhs} >= {rhs})"


@comparison_operator
def less_than_operation(lhs: Var, rhs: Var):
    """Less than comparison.

    Args:
        lhs: The first value.
        rhs: The second value.

    Returns:
        The result of the comparison.
    """
    return f"({lhs} < {rhs})"


@comparison_operator
def less_than_or_equal_operation(lhs: Var, rhs: Var):
    """Less than or equal comparison.

    Args:
        lhs: The first value.
        rhs: The second value.

    Returns:
        The result of the comparison.
    """
    return f"({lhs} <= {rhs})"


@comparison_operator
def equal_operation(lhs: Var, rhs: Var):
    """Equal comparison.

    Args:
        lhs: The first value.
        rhs: The second value.

    Returns:
        The result of the comparison.
    """
    return f"({lhs} === {rhs})"


@comparison_operator
def not_equal_operation(lhs: Var, rhs: Var):
    """Not equal comparison.

    Args:
        lhs: The first value.
        rhs: The second value.

    Returns:
        The result of the comparison.
    """
    return f"({lhs} !== {rhs})"


@var_operation
def boolean_not_operation(value: BooleanVar):
    """Boolean NOT the boolean.

    Args:
        value: The boolean.

    Returns:
        The boolean NOT operation.
    """
    return var_operation_return(js_expression=f"!({value})", var_type=bool)


@dataclasses.dataclass(
    eq=False,
    frozen=True,
    **{"slots": True} if sys.version_info >= (3, 10) else {},
)
class LiteralBooleanVar(LiteralVar, BooleanVar):
    """Base class for immutable literal boolean vars."""

    _var_value: bool = dataclasses.field(default=False)

    def json(self) -> str:
        """Get the JSON representation of the var.

        Returns:
            The JSON representation of the var.
        """
        return "true" if self._var_value else "false"

    def __hash__(self) -> int:
        """Calculate the hash value of the object.

        Returns:
            int: The hash value of the object.
        """
        return hash((self.__class__.__name__, self._var_value))

    @classmethod
    def create(cls, value: bool, _var_data: VarData | None = None):
        """Create the boolean var.

        Args:
            value: The value of the var.
            _var_data: Additional hooks and imports associated with the Var.

        Returns:
            The boolean var.
        """
        return cls(
            _var_name="true" if value else "false",
            _var_type=bool,
            _var_data=ImmutableVarData.merge(_var_data),
            _var_value=value,
        )


@dataclasses.dataclass(
    eq=False,
    frozen=True,
    **{"slots": True} if sys.version_info >= (3, 10) else {},
)
class LiteralNumberVar(LiteralVar, NumberVar):
    """Base class for immutable literal number vars."""

    _var_value: float | int = dataclasses.field(default=0)

    def json(self) -> str:
        """Get the JSON representation of the var.

        Returns:
            The JSON representation of the var.
        """
        return json.dumps(self._var_value)

    def __hash__(self) -> int:
        """Calculate the hash value of the object.

        Returns:
            int: The hash value of the object.
        """
        return hash((self.__class__.__name__, self._var_value))

    @classmethod
    def create(cls, value: float | int, _var_data: VarData | None = None):
        """Create the number var.

        Args:
            value: The value of the var.
            _var_data: Additional hooks and imports associated with the Var.

        Returns:
            The number var.
        """
        return cls(
            _var_name=str(value),
            _var_type=type(value),
            _var_data=ImmutableVarData.merge(_var_data),
            _var_value=value,
        )


number_types = Union[NumberVar, int, float]
boolean_types = Union[BooleanVar, bool]


@dataclasses.dataclass(
    eq=False,
    frozen=True,
    **{"slots": True} if sys.version_info >= (3, 10) else {},
)
class ToNumberVarOperation(CachedVarOperation, NumberVar):
    """Base class for immutable number vars that are the result of a number operation."""

    _original_value: Var = dataclasses.field(
        default_factory=lambda: LiteralNumberVar.create(0)
    )

    @cached_property_no_lock
    def _cached_var_name(self) -> str:
        """The name of the var.

        Returns:
            The name of the var.
        """
        return str(self._original_value)

    @classmethod
    def create(
        cls,
        value: Var,
        _var_type: type[int] | type[float] = float,
        _var_data: VarData | None = None,
    ):
        """Create the number var.

        Args:
            value: The value of the var.
            _var_type: The type of the Var.
            _var_data: Additional hooks and imports associated with the Var.

        Returns:
            The number var.
        """
        return cls(
            _var_name="",
            _var_type=_var_type,
            _var_data=ImmutableVarData.merge(_var_data),
            _original_value=value,
        )


@dataclasses.dataclass(
    eq=False,
    frozen=True,
    **{"slots": True} if sys.version_info >= (3, 10) else {},
)
class ToBooleanVarOperation(CachedVarOperation, BooleanVar):
    """Base class for immutable boolean vars that are the result of a boolean operation."""

    _original_value: Var = dataclasses.field(
        default_factory=lambda: LiteralBooleanVar.create(False)
    )

    @cached_property_no_lock
    def _cached_var_name(self) -> str:
        """The name of the var.

        Returns:
            The name of the var.
        """
        return str(self._original_value)

    @classmethod
    def create(
        cls,
        value: Var,
        _var_data: VarData | None = None,
    ):
        """Create the boolean var.

        Args:
            value: The value of the var.
            _var_data: Additional hooks and imports associated with the Var.

        Returns:
            The boolean var.
        """
        return cls(
            _var_name="",
            _var_type=bool,
            _var_data=ImmutableVarData.merge(_var_data),
            _original_value=value,
        )


@var_operation
def boolify(value: Var):
    """Convert the value to a boolean.

    Args:
        value: The value.

    Returns:
        The boolean value.
    """
    return var_operation_return(
        js_expression=f"Boolean({value})",
        var_type=bool,
    )


@var_operation
def ternary_operation(condition: BooleanVar, if_true: Var, if_false: Var):
    """Create a ternary operation.

    Args:
        condition: The condition.
        if_true: The value if the condition is true.
        if_false: The value if the condition is false.

    Returns:
        The ternary operation.
    """
    return var_operation_return(
        js_expression=f"({condition} ? {if_true} : {if_false})",
        var_type=unionize(if_true._var_type, if_false._var_type),
    )