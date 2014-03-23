from maths.relations.trigonometry import trig
from maths.symbols import *
import sympy


def test_difficulty_one():
    obj = trig.Cos(difficulty=1)
    match = obj.equation.match(sympy.cos(x0*x + x1))

    assert match[x0] != 0
    assert match[x1] == 0


def test_difficulty_two():
    obj = trig.Cos(difficulty=2)
    match = obj.equation.match(sympy.cos(x0*x + x1))

    assert match[x0] != 0
    assert match[x1] != 0
