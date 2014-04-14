import sympy
import random
from ..symbols import x
from ..latex import solution_lines, expressions
from ..utils import sensible_values
import copy
from . import relationships


@relationships.root
class HiddenIntegrationByParts(relationships.QuestionPart):
    """
    Question description
    ====================

    Take a simple expression and find its antiderivative.


    Real-life instances
    ===================

    2010 9: [Blank slate]
    2012 9: [Blank slate]
    """

    def __init__(self):
        self.num_lines, self.num_marks = 0, 0
        self._qp = {}

        self._qp['equation'] = random.choice([
            x * sympy.sin(x),
            x * sympy.cos(x),
            x * sympy.exp(x),
            x ** 2 * sympy.log(x)
        ])

        derivative = self._qp['equation'].diff()
        for product_rule_half in derivative.args:
            # note that these variables are for use down the track in the Integration subpart
            # the product rule will split each equation into something like x*cos(x) + sin(x), 2*x*log(x) + x
            # and we want to choose the part that requires integration by parts to solve, so we choose the subpart that has more than 1 arg
            if len(product_rule_half.args) > 1:
                # x**2 * sympy.log(x) differentiates to 2*x*log(x) + x, we want the hidden objective to be x*log(x), not 2*x*log(x)
                self._qp['hidden_objective_coefficient'], self._qp['hidden_objective'] = product_rule_half.as_two_terms()
            else:
                self._qp['other_deriv_part'] = product_rule_half

    def question_statement(self):
        return r'''Let $f(x) = {0}$.'''.format(sympy.latex(self._qp['equation']))


@relationships.is_child_of(HiddenIntegrationByParts)
class Derivative(relationships.QuestionPart):
    """
    Question description
    ====================

    Take a simple expression and find its antiderivative.


    Real-life instances
    ===================

    2010 9a: [3 lines] [1 mark]
    2012 9a: [4 lines] [1 mark]
    """

    def __init__(self, part):
        self.num_lines, self.num_marks = 3, 1
        self._qp = copy.copy(part._qp)

    def question_statement(self):
        return r'''Find $f'(x)$.'''

    def solution_statement(self):
        lines = solution_lines.Lines()

        # e.g. f'(x) = 2 * x * log(x) + x
        lines += r'''$f'(x) = {0}$'''.format(sympy.latex(self._qp['equation'].diff()))

        return lines.write()


@relationships.is_child_of(HiddenIntegrationByParts)
class Integration(relationships.QuestionPart):
    """
    Question description
    ====================

    Take a simple expression and find its antiderivative.


    Real-life instances
    ===================

    2010 9b: [10 lines] [3 mark]
    2012 9b: [15 lines] [3 mark]
    """

    def __init__(self, part):
        self.num_lines, self.num_marks = 12, 3
        self._qp = copy.copy(part._qp)

        domain = sympy.Interval(-2 * sympy.pi, 2 * sympy.pi)
        bounds = sensible_values.integral_domain(self._qp['equation'], domain)
        self._qp['domain'] = sympy.Interval(bounds[0], bounds[1])

        self._qp['answer'] = self._qp['hidden_objective'].integrate((x, self._qp['domain'].left, self._qp['domain'].right))

    def question_statement(self):
        integral = expressions.integral(lb=self._qp['domain'].left, ub=self._qp['domain'].right, expr=self._qp['hidden_objective'])

        return r'Use the result of part a. to find the value of ${0}$.'.format(integral)

    def solution_statement(self):
        lines = solution_lines.Lines()

        # so that we can easily jumble around the parts of the equation, we make symbols for f' and f
        f_ = sympy.Symbol("f'(x)")
        f = sympy.Symbol("f(x)")

        hidden_objective_equivalent = (f_ - self._qp['other_deriv_part']) / self._qp['hidden_objective_coefficient']
        # e.g. x*log(x) = f'(x)/2 - x/2
        lines += r'${hidden_objective} = {hidden_objective_equivalent}$'.format(
            hidden_objective=sympy.latex(self._qp['hidden_objective']),
            hidden_objective_equivalent=sympy.latex(hidden_objective_equivalent)
        )

        # e.g. integral(x*log(x), e^(-4), e^(3)) = integral(f'(x)/2 - x/2, e^(-4), e^(3))
        lines += r'${hidden_objective_integral} = {equivalent_integral}$'.format(
            hidden_objective_integral=expressions.integral(lb=self._qp['domain'].left, ub=self._qp['domain'].right, expr=self._qp['hidden_objective']),
            equivalent_integral=expressions.integral(lb=self._qp['domain'].left, ub=self._qp['domain'].right, expr=hidden_objective_equivalent)
        )

        hidden_objective_equivalent_antiderivative = (f - self._qp['other_deriv_part'].integrate()) / self._qp['hidden_objective_coefficient']
        # e.g. = [f(x)/2 - (x^2)/4](e^(-4), e^3)
        lines += r'$= \left[{expression}\right]^{{{upper_bound}}}_{{{lower_bound}}}$'.format(
            expression=sympy.latex(hidden_objective_equivalent_antiderivative),
            lower_bound=sympy.latex(self._qp['domain'].left),
            upper_bound=sympy.latex(self._qp['domain'].right)
        )

        hidden_objective_equivalent_derivative = hidden_objective_equivalent.subs({f_: self._qp['equation'].diff()})

        # e.g. = [x**2 * log(x)/2 - (x^2)/4](e^(-4), e^3)
        lines += r'$= {integral_intermediate}$'.format(
            integral_intermediate=expressions.integral_intermediate(lb=self._qp['domain'].left, ub=self._qp['domain'].right,
                                                                    expr=hidden_objective_equivalent_derivative)
        )

        # e.g. = 5e^6 / 4 - ((-9) / (4e^8))
        lines += r'$= {integral_result}$'.format(
            integral_result=expressions.integral_intermediate_eval(lb=self._qp['domain'].left, ub=self._qp['domain'].right,
                                                                   expr=hidden_objective_equivalent_derivative)
        )

        # e.g. = (-9) / (4e^8) + 5e^6 / 4
        lines += r'''$= {answer}$'''.format(
            answer=sympy.latex(self._qp['answer'])
        )

        return lines.write()
