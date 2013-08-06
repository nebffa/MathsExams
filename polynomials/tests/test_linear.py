from maths.polynomials import linear
from maths.symbols import *


def test_difficulty_one():
    obj = linear.Linear(difficulty=1)
    match = obj.equation.match(x0*x + x1)

    assert match[x0] not in [0, 1]
    assert match[x1] == 0


def test_difficulty_two():
    obj = linear.Linear(difficulty=2)
    match = obj.equation.match(x0*x + x1)

    assert match[x0] == 1
    assert match[x1] != 0


def test_difficulty_three():
    obj = linear.Linear(difficulty=3)
    match = obj.equation.match(x0*x + x1)

    assert match[x0] not in [0, 1]
    assert match[x1] != 0
