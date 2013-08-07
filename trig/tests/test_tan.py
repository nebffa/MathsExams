from .. import trig
from ...symbols import *
import sympy


def test_difficulty_one():
    obj = trig.Tan(difficulty=1)
    match = obj.equation.match(sympy.tan(x0*x + x1))

    assert match[x0] != 0
    assert match[x1] == 0


def test_difficulty_two():
    obj = trig.Tan(difficulty=2)
    match = obj.equation.match(sympy.tan(x0*x + x1))

    assert match[x0] != 0
    assert match[x1] != 0
