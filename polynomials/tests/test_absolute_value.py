from .. import absolute_value
from ...symbols import *
from sympy import Abs


def test_difficulty_one():
    obj = absolute_value.AbsoluteValue(difficulty=1)
    match = obj.equation.match(Abs(x0*x + x1)/x2 + x3)

    assert match[x0] == 1
    assert match[x1] == 0
    assert match[x2] == 1
    assert match[x3] != 0


def test_difficulty_two():
    obj = absolute_value.AbsoluteValue(difficulty=2)
    match = obj.equation.match(Abs(x0*x + x1)/x2 + x3)

    assert match[x1] != 0
    assert match[x2] == 1
    assert match[x3] != 0


def test_difficulty_three():
    obj = absolute_value.AbsoluteValue(difficulty=3)
    match = obj.equation.match(Abs(x0*x + x1)/x2 + x3)

    assert match[x1] != 0
    assert match[x2] != 1
    assert match[x3] != 0
