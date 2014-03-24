from maths.utils import functions
from maths.symbols import *
import sympy
from sympy import oo


def test_is_monotone_increasing():
    assert functions.is_monotone_increasing(sympy.exp(x))
    assert functions.is_monotone_increasing(x**3)

    assert functions.is_monotone_increasing(x**2, sympy.Interval(0, oo, False, True))
    assert functions.is_monotone_increasing(sympy.sin(x), sympy.Interval(0, sympy.pi/2, False, False))

    assert functions.is_monotone_increasing(-1/x)
    assert not functions.is_monotone_increasing(x**4)


def test_is_monotone_decreasing():
    assert functions.is_monotone_decreasing(-sympy.exp(x))
    assert functions.is_monotone_decreasing(-x**3)

    assert functions.is_monotone_decreasing(-x**2, sympy.Interval(0, oo, False, True))
    assert functions.is_monotone_decreasing(-sympy.sin(x), sympy.Interval(0, sympy.pi/2, False, False))

    assert functions.is_monotone_decreasing(1/x)
    assert not functions.is_monotone_decreasing(-x**4)
