import sympy
from sympy.abc import *


def transform_set(x, expr, sympy_set):
    """ Transform a sympy_set by an expression

    >>> domain = Interval(-pi, 0, True, True) + Interval(0, pi/2, True, True)
    (0, pi/2) U (-pi, 0)

    >>> transform_set(x, 2*x, domain)
    (0, pi) U (-2*pi, 0)

    >>> transform_set(x, x**2, domain)
    (0, pi**2)
    """
    if isinstance(sympy_set, sympy.Union):
        return sympy.Union(transform_set(x, expr, arg) for arg in sympy_set.args)
    if isinstance(sympy_set, sympy.Intersection):
        return sympy.Intersection(transform_set(x, expr, arg) for arg in sympy_set.args)

    f = sympy.Lambda(x, expr)
    if isinstance(sympy_set, sympy.Interval):
        # TODO: manage left_open and right_open better
        left, right = f(sympy_set.left), f(sympy_set.right)
        return sympy.Interval(sympy.Min(left, right), sympy.Max(left, right),
                              sympy_set.left_open, sympy_set.right_open)
    if isinstance(sympy_set, sympy.FiniteSet):
        return sympy.FiniteSet(list(map(f, sympy_set)))


