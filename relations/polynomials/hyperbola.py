from maths.symbols import *
from maths import not_named_yet
from maths.relations.polynomials.linear import request_linear


class Hyperbola(object):
    def __init__(self, difficulty):

        c = not_named_yet.randint_no_zero(-4, 4)
        m = not_named_yet.randint_no_zero(-3, 3)
        inner_function = request_linear(difficulty=3).equation
        if difficulty == 1:
            denominator = x
            self.equation = 1 / x + c
        elif difficulty == 2:
            denominator = inner_function
            self.equation = 1 / inner_function + c
        elif difficulty == 3:
            denominator = inner_function
            m = not_named_yet.randint_no_zero(-2, 2)
            if m < 0:
                m -= 1
            else:
                m += 1
            self.equation = m / inner_function + c

        x_asymptote = sympy.solve(denominator)[0]

        self.domain = sympy.Interval(-sympy.oo, x_asymptote, True, True) + sympy.Interval(x_asymptote, sympy.oo, True, True)
        self.range = sympy.Interval(-sympy.oo, c, True, True) + sympy.Interval(c, sympy.oo, True, True)
