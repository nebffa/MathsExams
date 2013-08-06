from maths.logs_exps import exp
from maths.tests_help import *
import sympy


def test_difficulty_one():
    obj = exp.Exp(difficulty=1)
    match = obj.equation.match(x0*sympy.exp(x1*x + x2) + x3)

    assert match[x0] == 1
    assert match[x1] != 0
    assert match[x2] == 0
    assert match[x3] != 0


def test_difficulty_two():
    obj = exp.Exp(difficulty=2)
    match = obj.equation.match(x0*sympy.exp(x1*x + x2) + x3)

    assert match[x0] != 1
    assert match[x1] != 0
    assert match[x2] == 0
    assert match[x3] != 0


def test_difficulty_three():
    obj = exp.Exp(difficulty=3)
    match = obj.equation.match(x0*sympy.exp(x1*x + x2) + x3)

    assert match[x0] != 1
    assert match[x1] != 0
    assert match[x2] != 0
    assert match[x3] != 0
