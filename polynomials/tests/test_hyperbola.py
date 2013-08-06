from maths.polynomials import hyperbola
from maths.symbols import *


def test_difficulty_one():
    obj = hyperbola.Hyperbola(difficulty=1)
    match = obj.equation.match(x0/x1 + x2)
    second_match = match[x1].match(x0*x + x1)

    assert match[x0] in [-1, 1]
    assert second_match[x1] == 0


def test_difficulty_two():
    obj = hyperbola.Hyperbola(difficulty=2)
    match = obj.equation.match(x0/x1 + x2)
    second_match = match[x1].match(x0*x + x1)

    assert match[x0] in [-1, 1]
    assert second_match[x1] != 0


def test_difficulty_three():
    obj = hyperbola.Hyperbola(difficulty=3)
    match = obj.equation.match(x0/x1 + x2)
    second_match = match[x1].match(x0*x + x1)

    assert match[x0] not in [-1, 1]
    assert second_match[x1] != 0
