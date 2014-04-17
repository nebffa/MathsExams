import sympy
import random
from ..symbols import x, x0, x1
from .. import all_functions
from ..utils import sensible_values
from ..latex import solution_lines
import functools
import operator
from . import relationships


@relationships.root
class SolveLogEquation(relationships.QuestionPart):
    """
    Question description
    ====================

    Solve an equation composed of logarithms.

    Real-life instances
    ===================

    2009 9: 2*log(x) - log(x + 3) = log(1/2)        [7 lines] [4 marks]
    2012 7: 2*log(x + 2) - log(x) = log(2*x + 1)    [8 lines] [3 marks]
    """

    @staticmethod
    def log_orders():
        """Return coefficients that determine the order of the logs.

        e.g. 2 * log(x) where 2 is an order
        """

        orders = [1, 2]
        random.shuffle(orders)
        return orders

    @staticmethod
    def log_coefficients():
        """Return coefficients that determine whether the logs are positive or negative.
        """

        coefficients = [-1, 1]
        random.shuffle(coefficients)
        return coefficients

    @staticmethod
    def log_interiors():
        """Return linear expressions that will be used as the interiors of the logs.
        """

        while True:
            left_log_interiors = [all_functions.request_linear(difficulty=3).equation for solution in range(2)]
            if left_log_interiors[0] != left_log_interiors[1]:
                return left_log_interiors

    @staticmethod
    def build_logs(orders, coefficients, interiors):
        """Return a set of logs that have been built from:
            - an order (positive integer)
            - a coefficient (-1 or +1)
            - an interior of the logarithm

        >>> SolveLogEquation.build_logs([2, 3], [-1, 1], [2 * x + 1, -3 * x])
        [-2*log(2*x + 1), 3*log(-3*x)]
        """

        num_logs = len(orders)

        logs = []
        for log_number in range(num_logs):
            log = orders[log_number] * coefficients[log_number] * sympy.log(interiors[log_number])
            logs.append(log)

        return logs

    @staticmethod
    def log_solver(expr, check_validity=False):
        """Return valid solutions (i.e. solutions that don't evaluate any log that's part of the expression as complex)
        for an expression that is the addition/subtraction of logs.

        >>> SolveLogEquation.log_solver(sympy.log(x - 1))
        [2]

        >>> SolveLogEquation.log_solver(sympy.log(3 * x - 2) - 2 * sympy.log(x))
        [1, 2]
        """

        single_log = sympy.logcombine(expr, force=True)
        interior = single_log.match(x0 * sympy.log(x1))[x1]

        numerator, denominator = interior.as_numer_denom()

        solutions = sympy.solve(numerator - denominator)

        if check_validity:
            return [solution for solution in solutions if SolveLogEquation.is_valid_solution(expr, solution)]
        else:
            return solutions

    @staticmethod
    def is_valid_solution(expr, solution):
        """State whether an expression of logs evaluates as real at a given solution.

        >>> SolveLogEquation.is_valid_solution(sympy.log(x), 2)
        True

        >>> SolveLogEquation.is_valid_solution(2 * sympy.log(x) - sympy.log(x + 1), -1)
        False
        """

        symbol_used = expr.free_symbols.pop()

        for log in expr.find(sympy.log):
            evaluated = log.subs({symbol_used: solution})
            if not sympy.ask(sympy.Q.real(evaluated)):
                return False

        return True

    @staticmethod
    def logcombine_include_negative_power(expr, force=False):
        """Perform a more powerful logcombine than SymPy's logcombine.

        In SymPy:
        logcombine(-log(x)) = -log(x), rather than log(1/x).

        This behaviour is implemented here.

        >>> SolveLogEquation.logcombine_include_negative_power(-sympy.log(2 * x + 1))
        log(1/(2*x + 1))
        """

        expr = sympy.logcombine(expr, force)

        if expr.could_extract_minus_sign():
            interior = expr.match(x0 * sympy.log(x1))[x1]
            expr *= -1
            expr = sympy.log(1 / interior)

        return expr

    def __init__(self):
        self.num_lines, self.num_marks = 8, 3
        self._qp = {}

        while True:
            left_orders = SolveLogEquation.log_orders()
            left_coefficients = SolveLogEquation.log_coefficients()
            left_log_interiors = SolveLogEquation.log_interiors()

            left_logs = SolveLogEquation.build_logs(left_orders, left_coefficients, left_log_interiors)

            # we have built the logs for one side of the equation, now do the same for the other side
            for log in left_logs:
                if isinstance(log, sympy.Mul):
                    coeff = log.args[0]
                    if coeff == -2:
                        right_log_coeff = -1
                    elif coeff == 2:
                        right_log_coeff = 1

            right_interior = all_functions.request_linear(difficulty=3).equation

            self._qp['left_side'] = functools.reduce(operator.add, left_logs)
            self._qp['right_side'] = right_log_coeff * sympy.log(right_interior)

            # randomly switch the sides so we don't always have 2 logs on the left and only 1 on the right
            if random.randint(0, 1):
                self._qp['left_side'], self._qp['right_side'] = self._qp['right_side'], self._qp['left_side']

            self._qp['maybe_invalid_solutions'] = SolveLogEquation.log_solver(self._qp['left_side'] - self._qp['right_side'])
            self._qp['valid_solutions'] = SolveLogEquation.log_solver(self._qp['left_side'] - self._qp['right_side'], check_validity=True)

            if len(self._qp['maybe_invalid_solutions']) < 2:  # we need enough solutions so the students have some work to do
                continue
            elif len(self._qp['valid_solutions']) == 0:
                continue

            are_all_solutions_sensible = all([sensible_values.looks_good(solution) for solution in self._qp['maybe_invalid_solutions']])
            if not are_all_solutions_sensible:
                continue

            break

    def question_statement(self):
        return r'''Solve the equation ${left_side} = {right_side}$ for $x$.'''.format(
            left_side=sympy.latex(self._qp['left_side']),
            right_side=sympy.latex(self._qp['right_side'])
        )

    def solution_statement(self):
        lines = solution_lines.Lines()

        left_combined = SolveLogEquation.logcombine_include_negative_power(self._qp['left_side'], force=True)
        right_combined = SolveLogEquation.logcombine_include_negative_power(self._qp['right_side'], force=True)
        lines += r'${left_combined} = {right_combined}$'.format(
            left_combined=sympy.latex(left_combined),
            right_combined=sympy.latex(right_combined)
        )

        lines += r'$\therefore {left_interior} = {right_interior}$'.format(
            left_interior=sympy.latex(left_combined.args[0]),
            right_interior=sympy.latex(right_combined.args[0])
        )

        left_numer, left_denom = left_combined.args[0].as_numer_denom()
        right_numer, right_denom = right_combined.args[0].as_numer_denom()
        lines += r'${left_intermediate} = {right_intermediate}$'.format(
            left_intermediate=sympy.latex((left_numer * right_denom).expand()),
            right_intermediate=sympy.latex((right_numer * left_denom).expand())
        )

        collected_like_terms = (left_numer * right_denom - right_numer * left_denom).expand()
        lines += r'${collected_like_terms} = 0$'.format(
            collected_like_terms=sympy.latex(collected_like_terms)
        )

        solutions = sympy.solve(collected_like_terms)
        lines += r'$x = {solutions}$'.format(
            solutions=', '.join([sympy.latex(solution) for solution in solutions])
        )

        invalid_solutions = set(self._qp['maybe_invalid_solutions']) - set(self._qp['valid_solutions'])
        if len(invalid_solutions) > 0:
            invalid_solution = invalid_solutions.pop()
            lines += r'but $x = {invalid_solution}$ is an invalid solution since a log can only accept positive values'.format(
                invalid_solution=sympy.latex(invalid_solution)
            )

            lines += r'$\therefore x = {valid_solution}$'.format(
                valid_solution=', '.join([sympy.latex(i) for i in self._qp['valid_solutions']])
            )

        return lines.write()
