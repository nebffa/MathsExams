from .. import log
from ...symbols import *
import sympy


def test_difficulty_one():
    obj = log.Log(difficulty=1)
    match = obj.equation.match(sympy.log(x0*x + x1)/x2 + x3)

    assert match[x1] == 0
    assert match[x2] == 1
    assert match[x3] != 0


def test_difficulty_two():
    obj = log.Log(difficulty=2)
    match = obj.equation.match(sympy.log(x0*x + x1)/x2 + x3)

    assert match[x1] == 0
    assert match[x2] != 1
    assert match[x3] != 0


def test_difficulty_three():
    obj = log.Log(difficulty=3)
    match = obj.equation.match(sympy.log(x0*x + x1)/x2 + x3)

    assert match[x1] != 0
    assert match[x2] != 1
    assert match[x3] != 0