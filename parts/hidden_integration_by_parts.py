import sympy
import random
from maths.symbols import *
from maths.latex import solution_lines, expressions
from maths.utils import sensible_values
import copy


class HiddenIntegrationByParts:
    def __init__(self):
        self.num_lines, self.num_marks = 0, 0
        self._qp = {}

        self._qp['equation'] = random.choice([
                    x*sympy.sin(x),
                    x*sympy.cos(x),
                    x*sympy.exp(x),
                    x**2 * sympy.log(x)
                ])

        deriv = self._qp['equation'].diff()
        for deriv_subpart in deriv.args:
            # note that these variables are for use down the track in the Integration subpart
            # the product rule will split each equation into something like x*cos(x) + sin(x), 2*x*log(x) + x, so we choose the subpart that has more than 1 arg
            if len(deriv_subpart.args) > 1:
                # x**2 * sympy.log(x) differentiates to 2*x*log(x) + x, we want the hidden objective to be x*log(x), not 2*x*log(x)
                self._qp['hidden_objective_coefficient'] = deriv_subpart.as_coeff_Mul()[0]
                self._qp['hidden_objective'] = deriv_subpart / self._qp['hidden_objective_coefficient']
            else:
                self._qp['other_deriv_part'] = deriv_subpart



    def question_statement(self):
        self._qi = {}

        return r'''Let $f(x) = {0}$.'''.format(sympy.latex(self._qp['equation']))


    def solution_statement(self):
        lines = solution_lines.Lines()
        return lines.write()


class Derivative:
    def __init__(self, part):
        self.num_lines, self.num_marks = 3, 1
        self._qp = copy.copy(part._qp)



    def question_statement(self):
        self._qi = {}
        return r'''Find $f'(x)$.'''




    def solution_statement(self):
        lines = solution_lines.Lines()
        
        lines += r'''$f'(x) = {0}$'''.format(sympy.latex(self._qp['equation'].diff()))

        return lines.write()


class Integration:
    def __init__(self, part):
        self.num_lines, self.num_marks = 12, 3
        self._qp = copy.copy(part._qp)

        domain = sympy.Interval(-2*sympy.pi, 2*sympy.pi, False, False)
        bounds = sensible_values.integral_domain(self._qp['equation'], domain)
        self._qp['domain'] = sympy.Interval(bounds[0], bounds[1])

        self._qp['answer'] = self._qp['hidden_objective'].integrate((x, self._qp['domain'].left, self._qp['domain'].right))



    def question_statement(self):
        self._qi = {}

        integral = expressions.integral(lb=self._qp['domain'].left, ub=self._qp['domain'].right, expr=self._qp['hidden_objective'])

        return r'''Use the result of part a. to find the value of ${0}$.'''.format(integral)




    def solution_statement(self):
        lines = solution_lines.Lines()

        f_ = sympy.Symbol("f'(x)")
        hidden_objective_equals = (f_ - self._qp['other_deriv_part']) / self._qp['hidden_objective_coefficient']
        lines += r'''${0} = {1}$'''.format(
                    sympy.latex(self._qp['hidden_objective']),
                    sympy.latex(hidden_objective_equals)
                )

        lines += r'''${0} = {1}$'''.format(
                    expressions.integral(lb=self._qp['domain'].left, ub=self._qp['domain'].right, expr=self._qp['hidden_objective']),
                    expressions.integral(lb=self._qp['domain'].left, ub=self._qp['domain'].right, expr=hidden_objective_equals)
                )


        f = sympy.Symbol("f(x)")
        hidden_objective_equals_antideriv = (f - self._qp['other_deriv_part'].integrate()) / self._qp['hidden_objective_coefficient']
        lines += r'''$= \left[{0}\right]^{{{1}}}_{{{2}}}$'''.format(
                    sympy.latex(hidden_objective_equals_antideriv), 
                    sympy.latex(self._qp['domain'].right), 
                    sympy.latex(self._qp['domain'].left)
                )

        
        hidden_objective_equals = hidden_objective_equals.subs({f_: self._qp['equation'].diff()})
        lines += r'''$= {0}$'''.format(
                    expressions.integral_intermediate(lb=self._qp['domain'].left, ub=self._qp['domain'].right, expr=hidden_objective_equals)
                )

        lines += r'''$= {0}$'''.format(
                    expressions.integral_intermediate_eval(lb=self._qp['domain'].left, ub=self._qp['domain'].right, expr=hidden_objective_equals)
                )

        lines += r'''$= {0}$'''.format(
                    sympy.latex(self._qp['answer'])
                )
        
        return lines.write()

