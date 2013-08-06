from maths.polynomials import quadratic
from maths.tests_help import *
import gmpy


def test_difficulty_one():
    obj = quadratic.Quadratic(difficulty=1)
    match = obj.equation.match(x0*x**2 + x1*x + x2)

    assert match[x1] == 0 or match[x2] == 0
    assert obj.discriminant == 0


def test_difficulty_two():
    obj = quadratic.Quadratic(difficulty=2)

    assert obj.discriminant > 0
    assert gmpy.is_square(obj.discriminant)


def test_difficulty_three():
    obj = quadratic.Quadratic(difficulty=3)

    assert obj.discriminant > 0
    assert not gmpy.is_square(obj.discriminant)
