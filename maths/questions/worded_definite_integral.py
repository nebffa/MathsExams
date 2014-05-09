import sympy
import random
from .. import all_functions, not_named_yet
from ..symbols import x
from ..utils import functions
from ..latex import expressions, solutions
from . import relationships


@relationships.root
class WordedDefiniteIntegral(relationships.QuestionPart):
    """
    Question description
    ====================

    Find the value of a pronumeral, given some information about a definite integral.


    Real-life instances
    ===================

    2008 5: [8 lines] [3 marks]
    """

    def __init__(self):
        self._qp = {}
        self.num_lines, self.num_marks = 8, 3

        while True:
            function_type = random.choice(['log'])
            if function_type == 'log':
                equation = all_functions.request_exp(difficulty=3).equation

            bound = sympy.Rational(not_named_yet.randint(-5, 5, exclude=[0]), not_named_yet.randint(-5, 5, exclude=[0]))

            if bound < 0:
                domain = sympy.Interval(bound, 0, False, False)
            else:
                domain = sympy.Interval(0, bound, False, False)

            y_intercept = equation.subs({x: 0})
            if bound < 0 and y_intercept < 0 and functions.is_monotone_decreasing(equation, domain):
                continue
            elif bound < 0 and y_intercept > 0 and functions.is_monotone_increasing(equation, domain):
                continue
            elif bound > 0 and y_intercept < 0 and functions.is_monotone_increasing(equation, domain):
                continue
            elif bound > 0 and y_intercept > 0 and functions.is_monotone_decreasing(equation, domain):
                continue

            area = sympy.integrate(equation, (x, domain.left, domain.right))
            break

        self._qp['equation'] = equation
        self._qp['domain'] = domain
        self._qp['area'] = sympy.Abs(area)
        self._qp['big_letter'] = sympy.Symbol('C')

    def question_statement(self):
        positive_or_negative = 'positive' if self._qp['domain'].left == 0 else 'negative'

        return r'''The area of the region bounded by the y-axis, the x-axis, the curve $y = {equation}$ and the line x = {big_letter},
            where {big_letter} is a {positive_or_negative} real constant, is ${area}$. Find {big_letter}.'''.format(
            equation=sympy.latex(self._qp['equation']),
            area=sympy.latex(self._qp['area']),
            big_letter=self._qp['big_letter'],
            positive_or_negative=positive_or_negative
        )

    def solution_statement(self):
        lines = solutions.Lines()

        below_x_axis = True if self._qp['equation'].subs({x: 0}) < 0 else False

        if self._qp['domain'].left < 0:  # can't use a symbol in an interval
            question_domain = (self._qp['big_letter'], 0)
        else:
            question_domain = (0, self._qp['big_letter'])

        if below_x_axis:
            signed_equation = -self._qp['equation']

            lines += r'Since the curve is below the x-axis, we take the signed area.'

            lines += r'$A = -{original_integral} = {signed_integral}$'.format(
                original_integral=expressions.integral(lb=question_domain[0], ub=question_domain[1], expr=self._qp['equation']),
                signed_integral=expressions.integral(lb=question_domain[0], ub=question_domain[1], expr=signed_equation)
            )

            equation_to_use = signed_equation
        else:
            lines += r'A = ${0}$'.format(
                expressions.integral(lb=question_domain[0], ub=question_domain[1], expr=self._qp['equation'])
            )

            equation_to_use = self._qp['equation']

        lines += r'$= {0}$'.format(
            expressions.integral_intermediate(lb=question_domain[0], ub=question_domain[1], expr=equation_to_use)
        )

        lines += r'''$= {0} = {1}$'''.format(
            expressions.integral_intermediate_eval(lb=question_domain[0], ub=question_domain[1], expr=equation_to_use),
            sympy.latex(self._qp['area'])
        )

        # the value of the big letter is the sum of the ends of the domains (since one of the ends of the domains is 0)
        lines += r'''${big_letter} = {big_letter_value}$'''.format(
            big_letter=sympy.latex(self._qp['big_letter']),
            big_letter_value=sympy.latex(self._qp['domain'].left + self._qp['domain'].right)
        )

        return lines.write()

    def sanity_check(self):
        assert sympy.integrate(self._qp['equation'], (x, self._qp['domain'].left, self._qp['domain'].right)) == self._qp['area']

        # make sure we have no x-intercepts in the domain
        solutions = [solution for solution in sympy.solve(self._qp['equation']) if sympy.ask(sympy.Q.real(solution))]
        assert all([solution not in self._qp['domain'] for solution in solutions])
