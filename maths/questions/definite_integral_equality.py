import sympy
import random
from ..symbols import x0, x1, x
from .. import all_functions, not_named_yet
from ..latex import latex, expressions, solutions
from ..utils import noevals
from . import relationships


@relationships.root
class DefiniteIntegralEquality(relationships.QuestionPart):
    """
    Question description
    ====================

    Given two sides of an equation - a definite integral on one side and an expression
    in one variable on the other, find the value of that variable.


    Real-life instances
    ===================

    2010 2b: Find p given that int(2, 3, 1/(1-x)) = ln(p) [7 lines] [3 marks]
    """

    def __init__(self):
        self.num_lines = 7
        self.num_marks = 3

        self._qp = {}

        function = all_functions.request_linear(difficulty=3).equation

        self._qp['equation'] = 1 / function

        # we can't integrate over a range of a hyperbola that has the vertical asymptote in the middle
        # we will only integrate on one side of the hyperbola
        vertical_asymptote = sympy.solve(function)[0]

        if random.randint(0, 1):  # use the side to the left of the asymptote
            bound = vertical_asymptote.p // vertical_asymptote.q

            possible_x_values = list(range(bound - 5, bound))
        else:
            bound = vertical_asymptote.p // vertical_asymptote.q + 1

            possible_x_values = list(range(bound, bound + 5))

        boundary = all_functions.choose_bounds(possible_x_values)
        self._qp['boundary'] = sympy.Interval(*boundary)

        integral_result = not_named_yet.soft_logcombine(self._qp['equation'].integrate((x, self._qp['boundary'].left, self._qp['boundary'].right)))

        self._qp['answer'] = integral_result.match(sympy.log(x0) / x1)[x0]

        p = sympy.Symbol('p')
        self._qp['variable_expression'] = integral_result.replace(sympy.log(x0), sympy.log(p))

    def question_statement(self):
        integral = expressions.integral(lb=self._qp['boundary'].left, ub=self._qp['boundary'].right, expr=self._qp['equation'])
        return r'Find p given that ${integral} = {result}$'.format(
            integral=integral,
            result=sympy.latex(self._qp['variable_expression'])
        )

    def solution_statement(self):
        lines = solutions.Lines()

        intermediate = expressions.integral_intermediate(lb=self._qp['boundary'].left, ub=self._qp['boundary'].right, expr=self._qp['equation'])
        lines += r'${integral_intermediate}$'.format(
            integral_intermediate=intermediate
        )

        working = expressions.integral_intermediate_eval(lb=self._qp['boundary'].left, ub=self._qp['boundary'].right, expr=self._qp['equation'])
        lines += r'$= {integral_working}$'.format(
            integral_working=working
        )

        force_real_numbers = self._qp['equation'].integrate().replace(sympy.log(x0), sympy.log(sympy.Abs(x0)))
        integral_value = force_real_numbers.subs({x: self._qp['boundary'].right}) - force_real_numbers.subs({x: self._qp['boundary'].left})
        lines += r'$= {result}$'.format(
            result=sympy.latex(not_named_yet.soft_logcombine(integral_value))
        )

        lines += r'$\therefore p = {p_value}.$'.format(
            p_value=sympy.latex(self._qp['answer'])
        )

        return lines.write()
