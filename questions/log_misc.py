import sympy
import random
from sympy.abc import *
from . import all_functions, not_named_yet
from ..utils import sensible_values
from ..latex import solution_lines
import functools
import operator


class SolveLogEquation:
    def __init__(self):
        # 2008 Q9 [7 lines] [4 marks]
        # 2012 Q7 [8 lines] [3 marks]

        self.num_lines, self.num_marks = 8, 3

        self._qp = {}


        while True:
            good = True
            left_orders = [1, 2]
            random.shuffle(left_orders)
            left_coefficients = [-1, 1]
            random.shuffle(left_coefficients)

            while True:
                left_log_interiors = [all_functions.request_linear(difficulty=3).equation for i in range(2)]
                if left_log_interiors[0] != left_log_interiors[1]:
                    break
            left_logs = [left_coefficients.pop() * left_orders.pop() * sympy.log(left_log_interiors.pop()) for i in range(2)]
                
            for log in left_logs:
                if isinstance(log, sympy.Mul):
                    coeff = log.args[0]

                    if coeff == -2:
                        right_log_coeff = -1
                    elif coeff == 2:
                        right_log_coeff = 1

            right_log = right_log_coeff * sympy.log(all_functions.request_linear(difficulty=3).equation)
                    
            if random.randint(0, 1):
                self._qp['left_side'] = functools.reduce(operator.add, left_logs)
                self._qp['right_side'] = right_log
            else:
                self._qp['left_side'] = right_log
                self._qp['right_side'] = functools.reduce(operator.add, left_logs)


            combined_log = sympy.logcombine(self._qp['left_side'] - self._qp['right_side'], force=True)
            interior = combined_log.args[0]

            numerator, denominator = interior.as_numer_denom()


            self._qp['solutions'] = sympy.solve(numerator - denominator)

            if len(self._qp['solutions']) < 2:
                continue


            for solution in self._qp['solutions']:
                if not sensible_values.looks_good(solution):
                    good = False

            all_logs = (self._qp['left_side'] - self._qp['right_side']).find(sympy.log)
            all_interiors = [log.args[0] for log in all_logs]

            valid_solution_found = False
            self._qp['good_solutions'] = []
            self._qp['bad_solutions'] = []
            for solution in self._qp['solutions']:
                if all([interior.subs({x: solution}) > 0 for interior in all_interiors]):
                    valid_solution_found = True
                    self._qp['good_solutions'].append(solution)
                else:
                    self._qp['bad_solutions'].append(solution)

            if good and valid_solution_found:
                break

    def question_statement(self):
        return r'''Solve the equation ${0} = {1}$ for $x$.'''.format(
            sympy.latex(self._qp['left_side']), 
            sympy.latex(self._qp['right_side'])
        )


    def solution_statement(self):
        lines = solution_lines.Lines()

        left_combined = sympy.logcombine(self._qp['left_side'], force=True)
        right_combined = sympy.logcombine(self._qp['right_side'], force=True)

        

        if left_combined.could_extract_minus_sign():
            left_combined *= -1
            interior = left_combined.args[0]
            left_combined = sympy.log(1 / interior)

        if right_combined.could_extract_minus_sign():
            right_combined *= -1
            interior = right_combined.args[0]
            right_combined = sympy.log(1 / interior)
                
        


        lines += r'${0} = {1}$'.format(sympy.latex(left_combined), sympy.latex(right_combined))
        
        lines += r'$\therefore {0} = {1}$'.format(
            sympy.latex(left_combined.args[0]),
            sympy.latex(right_combined.args[0])
        )


        left_numer, left_denom = left_combined.args[0].as_numer_denom()
        right_numer, right_denom = right_combined.args[0].as_numer_denom()

        lines += r'${0} = {1}$'.format(
            sympy.latex((left_numer * right_denom).expand()),
            sympy.latex((right_numer * left_denom).expand())
        )

        quadratic = (left_numer * right_denom - right_numer * left_denom).expand()
        if quadratic.coeff(x**2).could_extract_minus_sign():
            quadratic *= -1

        lines += r'${0} = 0$'.format(
            sympy.latex(quadratic)
        )

        solutions = sympy.solve(quadratic)
        lines += r'$x = {0}$'.format(
            ', '.join([sympy.latex(i) for i in solutions])
        )

        if len(self._qp['bad_solutions']) > 0:
            lines += r'but $x = {0}$ is an invalid solution since a log can only accept positive values'.format(sympy.latex(self._qp['bad_solutions'][0]))
            lines += r'$\therefore x = {0}$'.format(sympy.latex(self._qp['good_solutions'][0]))


        return lines.write()
