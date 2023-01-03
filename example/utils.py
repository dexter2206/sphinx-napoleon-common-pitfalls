"""Module implementing some utils."""
from example.subpackage.submodule import A


class B:
    """Class B"""
    pass


def func_correct(arg: B) -> A:
    """Return fresh A, without using arg.

    Also, here's some math: :math:`|x + y| \\le |x| + |y|`

    Args:
        arg: some unused arg
          with multiline description
    Returns:
        A new instance of A.
    """
    return A()


def func_incorrect_1(arg: B) -> A:
    """Return fresh A, without using arg.

    Also, here's some math: :math:`|x + y| \\le |x| + |y|`
    Args:
        arg: some unused arg
          with multiline description
    Returns:
        A new instance of A.
    """
    return A()


def func_incorrect_2(arg: B) -> A:
    """Return fresh A, without using arg.

    Also, here's some math: :math:`|x + y| \\le |x| + |y|`

    Args:
        arg: some unused arg
          with multiline description
    Returns:
        A: A new instance of A.
    """
    return A()


def func_incorrect_3(arg: B) -> A:
    """Return fresh A, without using arg.

    Also, here's some math: |x + y| \\le |x| + |y|

    Args:
        arg: some unused arg
          with multiline description
    Returns:
        A new instance of A.
    """
    return A()
