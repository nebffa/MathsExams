from ... import not_named_yet
from ...relations.polynomials.linear import request_linear
from ...symbols import *
import sympy


class Exp(object):
    def __init__(self, difficulty):


        a = not_named_yet.randint_no_zero(-3, 2)
        k = not_named_yet.randint_no_zero(-2, 2)
        c = not_named_yet.randint_no_zero(-5, 5)

        if a == 1:
            a += 1

        if difficulty == 1:
            self.equation = sympy.exp(k * x) + c
        elif difficulty == 2:
            self.equation = a * sympy.exp(k * x) + c
        elif difficulty == 3:
            inner_function = request_linear(difficulty=3).equation
            self.equation = a * sympy.exp(inner_function) + c
        else:
            raise ValueError('You have given an invalid difficulty level! Please use difficulty levels 1-3')

        self.domain = sympy.Interval(-sympy.oo, sympy.oo, True, True)
        if a < 0:
            self.range = sympy.Interval(-sympy.oo, c, True, True)
        else:
            self.range = sympy.Interval(c, sympy.oo, True, True)
