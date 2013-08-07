from .. import trig
from ...symbols import *
import sympy


def test_difficulty_one():
    obj = trig.Sin(difficulty=1)
    match = obj.equation.match(sympy.sin(x0*x + x1))

    assert match[x0] != 0
    assert match[x1] == 0


def test_difficulty_two():
    obj = trig.Sin(difficulty=2)
    match = obj.equation.match(sympy.sin(x0*x + x1))

    assert match[x0] != 0
    assert match[x1] != 0
