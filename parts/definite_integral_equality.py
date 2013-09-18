import sympy
import random
from sympy.abc import *
from maths import all_functions
from maths.latex import latex, expressions, postprocess


class DefiniteIntegralEquality(object):
    def __init__(self):
        # 2010 2b. Find p given that int(2, 3, 1/(1-x)) = ln(p) [7 lines] [3 marks]
        self.num_lines = 7
        self.num_marks = 3
        function = all_functions.request_linear(difficulty=3).equation

        self.equation = 1 / function

        # we can't integrate over a range of a hyperbola that has the vertical asymptote in the middle, that would just be weird
        # we will only integrate on one side of the hyperbola
        vertical_asymptote = sympy.solve(function)[0]

        if random.randint(0, 1):  # go left
            bound = int(vertical_asymptote)
            possible_x_values = list(range(bound - 5, bound if (bound != vertical_asymptote) else bound - 1))
        else:
            bound = int(vertical_asymptote) + 1
            possible_x_values = list(range(bound if (bound != vertical_asymptote) else bound + 1, bound + 5))

        self.boundary = all_functions.choose_bounds(possible_x_values)

        # due to some (in this case) annoying rules of simplify, this step of integration can simplify directly to, for example,
        # -log(2)/2 + log(6)/2, rather than log(3)/2
        # it turns out that both logs produced always have the same denominator, so to create a single log we only need to know the
        # signs and the arguments
        a, b, c, d = sympy.Wild('a'), sympy.Wild('b'), sympy.Wild('c'), sympy.Wild('d')
        self.antiderivative = self.equation.integrate().replace(sympy.log(a), sympy.log(sympy.Abs(a)))
        self.integral = self.equation.integrate((x, self.boundary[0], self.boundary[1]))

        if len(self.integral.find(sympy.log)) > 1:  # there is more than one log
            match = self.integral.match(sympy.log(a) / b + sympy.log(c) / d)
            left_inside = match[a]
            right_inside = match[c]

            #def test_same_denominators(left_log, right_log):
            #    assert left_log.args[0] == right_log.args[0]

            denominator = abs(match[b])
            if match[b].could_extract_minus_sign():
                left_inside = 1 / left_inside
            if match[d].could_extract_minus_sign():
                right_inside = 1 / right_inside

            self.p = left_inside * right_inside
            self.integral = sympy.log(self.p, evaluate=False) / denominator

        else:
            self.p = self.integral.match(sympy.log(a) / b)[a]

        p = sympy.Symbol('p')
        self.integral = self.integral.replace(sympy.log(a), sympy.log(p))

    def question_statement(self):
        return r'Find p given that $\displaystyle\int^{%d}_{%d} %s\ dx = %s$' % (self.boundary[1], self.boundary[0],
                                                                                 sympy.latex(self.equation), sympy.latex(self.integral))

    def solution_statement(self):
        line1 = r'${0}$'.format(expressions.integral_intermediate(lb=self.boundary[0], ub=self.boundary[1], expr=self.equation.integrate()))

        inner_function = self.antiderivative.replace(a * sympy.log(b), b)

        inner_upper = inner_function.subs({x: self.boundary[1]})
        inner_lower = inner_function.subs({x: self.boundary[0]})

        upper_bound = self.antiderivative.replace(sympy.log(a), sympy.log(inner_upper, evaluate=False))
        lower_bound = self.antiderivative.replace(sympy.log(a), sympy.log(inner_lower, evaluate=False))

        line2 = r'$= {0}$'.format(expressions.integral_intermediate_eval(self.boundary[0], self.boundary[1], self.equation.integrate()))

        line3 = r'$= {0}, \, \therefore p = {1}$'.format(sympy.latex(self.equation.integrate((x, self.boundary[0], self.boundary[1]))), sympy.latex(self.p))

        return postprocess.log( latex.latex_newline().join([line1, line2, line3]) )
