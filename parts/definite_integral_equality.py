import sympy
import random
from maths.symbols import *
from maths import all_functions
from maths.latex import latex, expressions, solution_lines
from maths.utils import noevals


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
        self.antiderivative = self.equation.integrate().replace(sympy.log(x0), sympy.log(sympy.Abs(x0)))
        self.integral = self.equation.integrate((x, self.boundary[0], self.boundary[1]))

        if len(self.integral.find(sympy.log)) > 1:  # there is more than one log
            logs = self.integral.find(sympy.log)
            left_inside = logs.pop().args[0]
            right_inside = logs.pop().args[0]
            denominator = self.integral.args[0].args[0].q

            # the denominator of the first log
            if self.integral.args[0].could_extract_minus_sign():
                left_inside = 1 / left_inside
            # the denominator of the second log
            if self.integral.args[1].could_extract_minus_sign():
                right_inside = 1 / right_inside

            self.p = left_inside * right_inside
            self.integral = sympy.log(self.p, evaluate=False) / denominator

        else:
            self.p = self.integral.match(sympy.log(x0) / x1)[x0]

        p = sympy.Symbol('p')
        self.integral = self.integral.replace(sympy.log(x0), sympy.log(p))

    def question_statement(self):
        return r'Find p given that $\displaystyle\int^{%d}_{%d} %s\ dx = %s$' % (self.boundary[1], self.boundary[0],
                                                                                 sympy.latex(self.equation), sympy.latex(self.integral))

    def solution_statement(self):
        lines = solution_lines.Lines()

        lines += r'${0}$'.format(expressions.integral_intermediate(lb=self.boundary[0], ub=self.boundary[1], expr=self.equation))

        complex_proof = self.equation.integrate().replace(sympy.log(x0), sympy.log(sympy.Abs(x0)))

        lines += r'$= {0}$'.format(expressions.integral_intermediate_eval(lb=self.boundary[0], ub=self.boundary[1], expr=self.equation))
        lines += r'$= {0} = {1}$'.format(
                            sympy.latex( complex_proof.subs({x: self.boundary[1]}) - complex_proof.subs({x: self.boundary[0]}) ), 
                            sympy.latex( sympy.logcombine( complex_proof.subs({x: self.boundary[1]}) - complex_proof.subs({x: self.boundary[0]}) ) ))
        lines += r'$\therefore p = {0}.$'.format(sympy.latex(self.p))

        return lines.write()
