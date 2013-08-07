import sympy
from sympy.abc import *
from .. import not_named_yet
from ..polynomials.linear import request_linear


class AbsoluteValue(object):
    def __init__(self, difficulty):

        c = not_named_yet.randint_no_zero(-4, 4)
        m = not_named_yet.randint_no_zero(-3, 3)
        interior_function = request_linear(difficulty=3).equation
        if difficulty == 1:
            self.equation = sympy.Abs(x) + c
        elif difficulty == 2:
            self.equation = sympy.Abs(interior_function) + c
        elif difficulty == 3:
            m = not_named_yet.randint(-3, 3, exclude=[-1, 0, 1])
            self.equation = sympy.Abs(interior_function)/m + c
