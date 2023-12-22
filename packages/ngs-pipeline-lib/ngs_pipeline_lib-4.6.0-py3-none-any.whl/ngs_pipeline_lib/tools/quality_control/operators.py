from dataclasses import dataclass
from operator import eq, ge, gt, le, lt, ne
from typing import Any, Callable, Protocol


class Comparable(Protocol):
    def __le__(self, other: Any) -> bool:
        """
        Supports less-equal operator
        """

    def __ge__(self, other: Any) -> bool:
        """
        Supports greater-equal operator
        """


def catch_type_error_in_function(func: Callable):
    """
    To support NoneType in comparisons
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError:
            return False

    return inner


def within(value: Comparable, interval: list[Comparable]) -> bool:
    return interval[0] <= value <= interval[1]


def not_within(value: Comparable, interval: list[Comparable]) -> bool:
    return not within(value, interval)


@dataclass
class Operator:
    _function: Callable
    description: str

    @property
    def function(self):
        return catch_type_error_in_function(self._function)

    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("string required")
        if v not in OPERATORS:
            raise TypeError(f"Unknown Operator {v}")
        return OPERATORS[v]


OPERATORS = {
    "EQ": Operator(eq, "is equal to"),
    "NE": Operator(ne, "is not equal to"),
    "LT": Operator(lt, "is less than"),
    "LE": Operator(le, "is less than or equal to"),
    "GE": Operator(ge, "is greater than or equal to"),
    "GT": Operator(gt, "is greater than"),
    "NW": Operator(
        not_within, "is not within"
    ),  # equivalent to : lower_bound < value > upper_bound
    "W": Operator(
        within, "is within"
    ),  # equivalent to : lower_bound <= value <= upper_bound
}
