from __future__ import annotations

__all__ = [
    "check_feature_size",
    "check_interval",
    "check_num_examples",
    "check_integer_ge",
    "check_std",
]

from typing import Any


def check_feature_size(value: int | Any, low: int = 1) -> None:
    r"""Checks if the given value is a valid feature size i.e. number of
    features.

    Args:
    ----
        value: Specifies the value to check.
        low (int, optional): Specifies the minimum value (inclusive).
            Default: ``1``

    Raises:
    ------
        TypeError if the input is not an integer.
        RuntimeError if the value is not greater than 0

    Example usage:

    .. code-block:: pycon

        >>> import torch
        >>> from startorch.example.utils import check_feature_size
        >>> check_feature_size(5)
    """
    check_integer_ge(value, name="feature_size", low=low)


def check_interval(value: float | int | Any, low: float, high: float, name: str) -> None:
    r"""Checks if the given value is an interval.

    Args:
    ----
        value: Specifies the value to check.
        low (float): Specifies the minimum value (inclusive).
        high (float): Specifies the maximum value (exclusive).
        name (str): Specifies the variable name.

    Raises:
    ------
        TypeError if the input is not an integer or float.
        RuntimeError if the value is not in the interval

    Example usage:

    .. code-block:: pycon

        >>> import torch
        >>> from startorch.example.utils import check_interval
        >>> check_interval(1, low=-1.0, high=2.0, name="my_variable")
    """
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"Incorrect type for {name}. Expected an integer or float but received {type(value)}"
        )
    if value < low or value >= high:
        raise RuntimeError(
            f"Incorrect value for {name}. Expected a value in interval [{low}, {high}) "
            f"but received {value}"
        )


def check_num_examples(value: int | Any) -> None:
    r"""Checks if the given value is a valid number of examples.

    Args:
    ----
        value: Specifies the value to check.

    Raises:
    ------
        TypeError if the input is not an integer.
        RuntimeError if the value is not greater than 0

    Example usage:

    .. code-block:: pycon

        >>> import torch
        >>> from startorch.example.utils import check_num_examples
        >>> check_num_examples(5)
    """
    check_integer_ge(value, low=1, name="num_examples")


def check_integer_ge(value: int | Any, low: int, name: str) -> None:
    r"""Checks if the given value is a valid positive integer.

    Args:
    ----
        value: Specifies the value to check.
        low (int): Specifies the minimum value (inclusive).
        name (str): Specifies the variable name.

    Raises:
    ------
        TypeError if the input is not an integer.
        RuntimeError if the value is not greater than 0

    Example usage:

    .. code-block:: pycon

        >>> import torch
        >>> from startorch.example.utils import check_integer_ge
        >>> check_integer_ge(5, low=0, name="feature_size")
    """
    if not isinstance(value, int):
        raise TypeError(
            f"Incorrect type for {name}. Expected an integer but received {type(value)}"
        )
    if value < low:
        raise RuntimeError(
            f"Incorrect value for {name}. Expected a value greater or equal to {low} but received {value}"
        )


def check_std(value: float | int | Any, name: str = "std") -> None:
    r"""Checks if the given value is a valid standard deviation.

    Args:
    ----
        value: Specifies the value to check.
        name (str, optional): Specifies the variable name.
            Default: ``'std'``

    Raises:
    ------
        TypeError if the input is not an integer or float.
        RuntimeError if the value is not greater than 0

    Example usage:

    .. code-block:: pycon

        >>> import torch
        >>> from startorch.example.utils import check_std
        >>> check_std(1.2)
    """
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"Incorrect type for {name}. Expected an integer or float but received {type(value)}"
        )
    if value < 0:
        raise RuntimeError(
            f"Incorrect value for {name}. Expected a value greater than 0 but received {value}"
        )
