import sympy
import random
from ..symbols import x
from .. import not_named_yet
from ..latex import solution_lines, expressions
from ..utils import noevals, functions
import copy
import decimal
from . import relationships


@relationships.is_child_of(relationships.DummyPart)
class LinearApproximation:
    """
    Question description
    ====================

    Given an original point, use linear approximation to approximate the y-coordinate at a nearby point on the curve.


    Real-life instances
    ===================

    2009 10a: Find an approximate value for cube_root(8.06) [7 lines] [4 marks]
    """

    def __init__(self):
        self.num_lines, self.num_marks = 7, 4

        self._qp = {}
        self._qi = {}

        self._qp['equation'] = random.choice([x ** sympy.Rational(1, random.randint(2, 3)), x ** random.randint(2, 3)])
        self._qi['noeval_equation'] = self._qp['equation'].replace(sympy.Pow, noevals.noevalPow)

        if isinstance(self._qp['equation'], sympy.Pow):
            _, exponent = self._qp['equation'].as_base_exp()

            if exponent > 1:
                self._qp['location'] = random.randint(2, 4)
            else:
                self._qp['location'] = 2 ** exponent.q

        self._qp['delta'] = not_named_yet.randint_no_zero(-1, 1) * random.randint(5, 9) * decimal.Decimal('0.01')
        self._qp['new_location'] = self._qp['location'] + self._qp['delta']

    def question_statement(self):
        f_of_new_location = self._qi['noeval_equation'].subs({x: self._qp['new_location']})
        return r'''Use the relationship $f(x + h) \approx f(x) + h f'(x)$ for a small positive value of h,
            to find an approximate value for ${f_of_new_location}$.'''.format(f_of_new_location=sympy.latex(f_of_new_location))

    def solution_statement(self):
        lines = solution_lines.Lines()

        derivative = self._qp['equation'].diff()
        lines += r'''$y = {equation}, y' = {derivative}$'''.format(
            equation=sympy.latex(self._qp['equation']),
            derivative=sympy.latex(derivative)
        )

        original_y_coordinate = self._qp['equation'].subs({x: self._qp['location']})
        lines += r'$y({original_x_coordinate}) = {original_y_coordinate}$'.format(
            original_x_coordinate=self._qp['location'],
            original_y_coordinate=original_y_coordinate
        )

        derivative_at_original_location = derivative.subs({x: self._qp['location']})
        lines += r'''$y'({original_x_coordinate}) = {derivative_at_original_location}$'''.format(
            original_x_coordinate=self._qp['location'],
            derivative_at_original_location=sympy.latex(derivative_at_original_location)
        )

        unevaluated_approximation_of_answer = noevals.noevalAdd(original_y_coordinate, noevals.noevalMul(self._qp['delta'], derivative_at_original_location))
        answer = original_y_coordinate + self._qp['delta'] * derivative_at_original_location
        lines += r'$\therefore y({new_x_coordinate}) \approx {unevaluated_approximation_of_answer} = {answer}$'.format(
            new_x_coordinate=self._qp['new_location'],
            unevaluated_approximation_of_answer=noevals.latex(unevaluated_approximation_of_answer),
            answer=sympy.latex(answer)
        )

        return lines.write()


@relationships.is_child_of(relationships.DummyPart)
class LinearApproximationExplain:
    """
    Question description
    ====================

    In words, explain why this approximation is greater than or less than the exact value.


    Real-life instances
    ===================

    2009 10b: Explain why this approximate value is greater than the exact value for cube_root(8.06) [4 lines] [1 mark]
    """

    def __init__(self, part):
        self.num_lines, self.num_marks = 4, 1

        self._qp = copy.copy(part._qp)
        self._qi = copy.copy(part._qi)

        self._qp['concave_or_convex'] = functions.concave_or_convex(self._qp['equation'], self._qp['location'])

    def question_statement(self):
        direction = 'less than' if self._qp['concave_or_convex'] else 'greater than'

        return r'''Explain why this approximate value is {inequality} than the exact value for ${unevaluated_f_of_new_location}$.'''.format(
            inequality=direction,
            unevaluated_f_of_new_location=sympy.latex(self._qi['noeval_equation'].subs({x: self._qp['new_location']}))
        )

    def solution_statement(self):
        lines = solution_lines.Lines()

        second_derivative = self._qp['equation'].diff().diff()
        second_derivative_leibniz_form = r'{derivative}({location})'.format(
            derivative=expressions.derivative(upper_variable="x", lower_variable="y", degree=2),
            location=self._qp['location']
        )
        second_derivative_at_original_location = second_derivative.subs({x: self._qp['location']})
        lines += r'''The function is {concave_or_convex} at $x = {location}$ since the second derivative
            ${second_derivative_leibniz_form} = {second_derivative_at_original_location}$ is {greater_than_or_less_than} than $0$.'''.format(
            concave_or_convex=self._qp['concave_or_convex'],
            location=self._qp['location'],
            second_derivative_leibniz_form=second_derivative_leibniz_form,
            second_derivative_at_original_location=sympy.latex(second_derivative_at_original_location),
            greater_than_or_less_than='greater than' if second_derivative_at_original_location > 0 else 'less than'
        )

        lines += r'''Therefore, the gradient of ${equation}$ {increases_or_decreases} as $x$ moves from ${location}$ to ${new_location}$
            and as a result, linear approximation {under_or_over}estimates the true value of ${unevaluated_f_of_new_location}$'''.format(
            equation=sympy.latex(self._qp['equation']),
            increases_or_decreases='increases' if second_derivative_at_original_location > 0 else 'decreases',
            location=self._qp['location'],
            new_location=self._qp['new_location'],
            under_or_over='under' if self._qp['concave_or_convex'] else 'over',
            unevaluated_f_of_new_location=sympy.latex(self._qi['noeval_equation'].subs({x: self._qp['new_location']}))
        )

        return lines.write()
