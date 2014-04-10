from ... import not_named_yet
from ...relations.polynomials.linear import request_linear
from ...utils import functions
from ...symbols import *


coefficients_bound = 5


class Log(object):
    def __init__(self, difficulty):
        # y = a * ln(k * x) + c
        a = not_named_yet.randint(-3, 3, exclude=[0, 1])
        k = not_named_yet.randint(-3, 3, exclude=[0])
        c = not_named_yet.randint(-4, 4, exclude=[0])
        if difficulty == 1:
            self.equation = sympy.log(k*x) + c
        elif difficulty == 2:
            self.equation = a * sympy.log(k*x) + c
        elif difficulty == 3:
            inner_function = request_linear(difficulty=3).equation
            self.equation = a*sympy.log(inner_function) + c
        else:
            raise ValueError('You have supplied an invalid difficulty level! Choose between 1, 2 or 3')

        a1, a2, a3 = sympy.Wild('a1'), sympy.Wild('a2'), sympy.Wild('a3')
        interior = self.equation.match(a1 * sympy.log(a2) + a3)[a2]
        interior = interior.replace(x, sympy.Symbol('x', real=True))

        domain = sympy.solve(interior > 0)

        self.domain = functions.relation_to_interval(domain)
        self.range = sympy.Interval(-sympy.oo, sympy.oo, True, True)
