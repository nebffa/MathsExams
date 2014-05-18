import sympy
import random
from ..symbols import x, y, k
from .. import not_named_yet
from ..latex import solutions
from . import relationships
import copy


@relationships.root
class SimultaneousLinearEquationsSetup(relationships.QuestionPart):
    def __init__(self):
        self.num_lines, self.num_marks = 0, 0
        self._qp = {}

        equation_one_coefficients = [not_named_yet.randint(-5, 5, exclude=[0]) for i in range(3)]
        multiplier = random.choice([2, sympy.Rational(1, 2)])
        if random.choice([True, False]):  # infinite solutions
            equation_two_coefficients = [i * multiplier for i in equation_one_coefficients]
            self._qp['infinite_solutions'] = True
        else:  # no solutions
            equation_two_coefficients = [i * multiplier for i in equation_one_coefficients]
            equation_two_coefficients[2] += not_named_yet.randint(-5, 5, exclude=[0])
            self._qp['infinite_solutions'] = False

        if equation_one_coefficients[0] > equation_two_coefficients[0]:
            k_value = random.randint(int(equation_two_coefficients[0]), int(equation_one_coefficients[0]))
        else:
            k_value = random.randint(int(equation_one_coefficients[0]), int(equation_two_coefficients[0]))
        self._qp['k_value'] = k_value

        equation_one_coefficients[0] = k - (k_value - equation_one_coefficients[0])
        equation_one_coefficients[2] = k - (k_value - equation_one_coefficients[2])
        equation_two_coefficients[1] = k - (k_value - equation_two_coefficients[1])

        equation_one = [equation_one_coefficients[0] * x + equation_one_coefficients[1] * y, equation_one_coefficients[2]]
        equation_two = [equation_two_coefficients[0] * x + equation_two_coefficients[1] * y, equation_two_coefficients[2]]

        if random.choice([True, False]):
            self._qp['equation_one'] = equation_one
            self._qp['equation_two'] = equation_two
        else:
            self._qp['equation_one'] = equation_two
            self._qp['equation_two'] = equation_one

    def question_statement(self):
        lines = solutions.Lines()
        lines += r'equation 1 is: ${0} = {1}$'.format(
            sympy.latex(self._qp['equation_one'][0]),
            sympy.latex(self._qp['equation_one'][1])
        )
        lines += r'equation 2 is: ${0} = {1}$'.format(
            sympy.latex(self._qp['equation_two'][0]),
            sympy.latex(self._qp['equation_two'][1])
        )

        return lines.write()


@relationships.is_child_of(SimultaneousLinearEquationsSetup)
class InfiniteOrNoSolutions(relationships.QuestionPart):
    """
    Question description
    ====================

    Find the value of the unknown such that there are infinite or no solutions.


    Real-life instances
    ===================

    2010 6b: [4 lines] [1 mark]
    """

    def __init__(self, part):
        self.num_lines, self.num_marks = 9, 3
        self._qp = copy.deepcopy(part._qp)

    def question_statement(self):
        return r'Find the values of $k$ for which there are {quantity} solutions.'.format(
            quantity='infinitely many' if self._qp['infinite_solutions'] else 'no'
        )

    def solution_statement(self):
        lines = solutions.Lines()

        lines += r'For the lines to be parallel, the ratios of coefficients between $x$ and $y$ must be the same:'

        x_equation_one = self._qp['equation_one'][0].coeff(x)
        x_equation_two = self._qp['equation_two'][0].coeff(x)
        y_equation_one = self._qp['equation_one'][0].coeff(y)
        y_equation_two = self._qp['equation_two'][0].coeff(y)

        lines += r'$\frac{{{x_equation_one}}}{{{x_equation_two}}} = \frac{{{y_equation_one}}}{{{y_equation_two}}}$'.format(
            x_equation_one=sympy.latex(x_equation_one),
            x_equation_two=sympy.latex(x_equation_two),
            y_equation_one=sympy.latex(y_equation_one),
            y_equation_two=sympy.latex(y_equation_two)
        )

        quadratic = x_equation_one * y_equation_two - x_equation_two * y_equation_one
        lines += r'${0} = 0$'.format(
            sympy.latex(quadratic.expand())
        )

        k_solutions = sympy.solve(quadratic)
        lines += r'$k = {0}$'.format(
            ', '.join(sympy.latex(i) for i in k_solutions)
        )

        return lines.write()


@relationships.is_child_of(SimultaneousLinearEquationsSetup)
class UniqueSolution(relationships.QuestionPart):
    """
    Question description
    ====================

    Find the value of the unknown such that there is a unique solution.


    Real-life instances
    ===================

    2011 6a: [9 lines] [3 marks]
    """

    def __init__(self, part):
        self.num_lines, self.num_marks = 2, 1
        self._qp = copy.deepcopy(part._qp)

    def question_statement(self):
        return r'Find the values of $k$ for which there is a unique solution.'

    def solution_statement(self):
        lines = solutions.Lines()

        x_equation_one = self._qp['equation_one'][0].coeff(x)
        x_equation_two = self._qp['equation_two'][0].coeff(x)
        y_equation_one = self._qp['equation_one'][0].coeff(y)
        y_equation_two = self._qp['equation_two'][0].coeff(y)

        quadratic = x_equation_one * y_equation_two - x_equation_two * y_equation_one
        k_solutions = sympy.solve(quadratic)

        lines += r'$k \neq {0}$'.format(
            ', '.join(sympy.latex(i) for i in k_solutions)
        )

        return lines.write()
