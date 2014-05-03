import sympy
import random
from .. import all_functions, not_named_yet
from ..latex import latex, solutions
from ..symbols import x0
from . import relationships


@relationships.root
class Antiderivative(relationships.QuestionPart):
    """
    Question description
    ====================

    Take a simple expression and find its antiderivative.


    Real-life instances
    ===================

    2009 2a: y = 1 / (1 - 2x) [4 lines] [2 marks]
    2010 2a: y = cos(2x + 1) [2 lines] [1 mark]
    2011 2a: y = 1 / (3x - 4) [5 lines] [1 mark]
    2012 2: y = 1 / (2x - 1)^3 [4 lines] [2 marks]

    there is no correlation between function type and marks assigned, so we have to choose between
    the historic 1 or 2 marks this question has been assigned
    """

    def __init__(self):
        self.num_marks = random.randint(1, 2)
        self._qp = {}

        self._qp['function_type'] = random.choice(['linear', 'trig'])

        inner_function = all_functions.request_linear(difficulty=3).equation
        if self._qp['function_type'] == 'linear':

            self.num_lines = 4

            index = random.randint(1, 3)

            self._qp['equation'] = 1 / inner_function ** index

        elif self._qp['function_type'] == 'trig':

            self.num_lines = 2

            outer_function = random.choice([sympy.cos, sympy.sin])
            self._qp['equation'] = outer_function(inner_function)

        self._qp['antiderivative'] = self._qp['equation'].integrate()

    def question_statement(self):
        return 'Find an antiderivative of ${equation}$ with respect to $x$.'.format(
            equation=sympy.latex(self._qp['equation'])
        )

    def solution_statement(self):
        # sympy integrates things like 1/x as log(x), not log(|x|) (since the symbol x is treated as a complex number, not a real number)
        proper_antiderivative = self._qp['antiderivative'].replace(sympy.log(x0), sympy.log(sympy.Abs(x0)))

        constant_of_integration = not_named_yet.randint_no_zero(-3, 3)

        lines = solutions.Lines()

        # without using .factor() here, we could have (x + 1)**(-3) integrate to -1/(2*x**2 + 4*x + 2) which is expanded
        antiderivative = proper_antiderivative.factor() + constant_of_integration
        lines += r'${antiderivative}$'.format(antiderivative=sympy.latex(antiderivative))
        lines += r'We arbitrarily choose our constant of integration to be ${constant_of_integration}$. It can be any real number, including zero.'.format(
            constant_of_integration=constant_of_integration
        )

        return lines.write()
