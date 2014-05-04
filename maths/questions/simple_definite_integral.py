import sympy
import random
from ..symbols import x
from .. import all_functions, not_named_yet
from ..latex import expressions, solutions
from . import relationships


@relationships.root
class SimpleDefiniteIntegral(relationships.QuestionPart):
    """
    Question description
    ====================

    Calculate the value of a definite integral.


    Real-life instances
    ===================

    2009 2b: [10 lines] [3 marks]
    """

    def __init__(self):
        # 2009 2b: Evaluate integral(sqrt(x) + 1, 1, 4) [10 lines] [3 marks]
        self.num_lines, self.num_marks = 10, 3
        self._qp = {}

        function_type = random.choice(['exp', 'trig', 'sqrt'])

        c = not_named_yet.randint_no_zero(-3, 3)
        if function_type == 'sqrt':
            self._qp['equation'] = sympy.sqrt(x) + c

            possible_x_values = [i ** 2 for i in range(1, 6)]

        elif function_type == 'trig':
            outer_function = random.choice([sympy.cos, sympy.sin])
            self._qp['equation'] = outer_function(x) + c

            possible_x_values = all_functions.sensible_trig_x_values(self._qp['equation'].integrate(x))

        elif function_type == 'exp':
            self._qp['equation'] = sympy.exp(x) + c

            possible_x_values = list(range(1, 5))

        self._qp['boundary'] = all_functions.choose_bounds(possible_x_values)
        self._qp['answer'] = self._qp['equation'].integrate((x, self._qp['boundary'][0], self._qp['boundary'][1]))

    def question_statement(self):
        return r'Evaluate ${definite_integral}$.'.format(
            definite_integral=expressions.integral(lb=self._qp['boundary'][0], ub=self._qp['boundary'][1], expr=self._qp['equation'])
        )

    def solution_statement(self):
        lines = solutions.Lines()

        integral, integral_intermediate, integral_intermediate_eval = expressions.integral_trifecta(
            lb=self._qp['boundary'][0], ub=self._qp['boundary'][1], expr=self._qp['equation']
        )

        lines += r'${integral} = {integral_intermediate}$'.format(
            integral=integral,
            integral_intermediate=integral_intermediate
        )

        lines += r'$= {integral_intermediate_eval}$'.format(
            integral_intermediate_eval=integral_intermediate_eval
        )

        lines += r'$= {answer}$'.format(
            answer=sympy.latex(self._qp['answer'])
        )

        return lines.write()
