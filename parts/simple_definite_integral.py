import sympy
import random
from sympy.abc import *
from maths import all_functions, solutions_printing, not_named_yet
from maths.latex import expressions, latex, solution_lines


class SimpleDefiniteIntegral(object):
    def __init__(self):
        # 2009 2b: Evaluate integral(sqrt(x) + 1, 1, 4) [10 lines] [3 marks]
        self.num_lines = 3
        self.num_marks = 3

        function_type = random.choice(['exp', 'trig', 'sqrt'])

        c = not_named_yet.randint_no_zero(-3, 3)
        if function_type == 'sqrt':
            self.equation = sympy.sqrt(x) + c

            possible_x_values = [i**2 for i in range(1, 6)]

        elif function_type == 'trig':
            outer_function = random.choice([sympy.cos, sympy.sin])
            self.equation = outer_function(x) + c

            possible_x_values = all_functions.sensible_trig_x_values(self.equation)

        elif function_type == 'exp':
            self.equation = sympy.exp(x) + c

            possible_x_values = list(range(1, 5))

        self.boundary = all_functions.choose_bounds(possible_x_values)
        self.answer = self.equation.integrate((x, self.boundary[0], self.boundary[1]))

    def question_statement(self):
        question_statement = r'Evaluate ${0}$.'.format(expressions.integral(lb=self.boundary[0], ub=self.boundary[1], expr=self.equation))

        return question_statement

    def solution_statement(self):
        lines = solution_lines.Lines()

        lines += r'${0} = {1}$'.format(
            expressions.integral(lb=self.boundary[0], ub=self.boundary[1], expr=self.equation),
            expressions.integral_intermediate(lb=self.boundary[0], ub=self.boundary[1], expr=self.equation)
        )

        lines += r'$= {0}$'.format(
            expressions.integral_intermediate_eval(self.boundary[0], self.boundary[1], self.equation)
        )

        lines += r'$= {0}$'.format(
            sympy.latex(self.answer)
        )

        return lines.write()
