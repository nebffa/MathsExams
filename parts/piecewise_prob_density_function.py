import sympy
import random
from maths import domains
from maths.symbols import *
from maths.latex import expressions, latex, solution_lines
from maths.utils import sensible_values
import copy
from maths.parts.piecewise_prob_density_function_unknown import PiecewiseProbDensityFunctionUnknown


class PiecewiseProbDensityFunction(PiecewiseProbDensityFunctionUnknown):
    def __init__(self):
        super(PiecewiseProbDensityFunction, self).__init__()

        self.num_lines, self.num_marks = 0, 0

        self._qp['equation'] = self._qp['equation'].subs({k: self._qp['k']})


    def question_statement(self):


        piecewise = sympy.Piecewise((self._qp['equation'], sympy.And(self._qp['domain'].left <= x, x <= self._qp['domain'].right)), (0, True))

        lines = solution_lines.Lines()

        lines += r'The function $f(x) = {0}$'.format( expressions.piecewise(piecewise) )
        lines += r'is a probability density function for the continuous random variable $X$.'
        return lines.write()



    def solution_statement(self):
        return ''


class SimpleInterval:
    def __init__(self, part):
        self.num_lines, self.num_marks = -1, -1

        domain = part._qp['domain']

        choices = [domain.left + sympy.Rational(i, 4) * domain.measure for i in [1, 2, 3]]


        self._qp = copy.copy(part._qp)
        self._qp['bound'] = random.choice(choices)
        self._qp['direction'] = random.choice(['left', 'right'])

        if self._qp['direction'] == 'left':
            self._qp['domain'] = sympy.Interval(self._qp['domain'].left, self._qp['bound'])
        else:
            self._qp['domain'] = sympy.Interval(self._qp['bound'], self._qp['domain'].right)



    def question_statement(self):
        return r'''Find Pr(X {0} {1}).'''.format('\le' if self._qp['direction'] == 'left' else '\ge', self._qp['bound'])


    def solution_statement(self):
        lines = solution_lines.Lines()

        answer = self._qp['equation'].integrate((x, self._qp['domain'].left, self._qp['domain'].right))

        lines += '$= {0}$'.format(expressions.integral(expr=self._qp['equation'], lb=self._qp['domain'].left, ub=self._qp['domain'].right))

        lines += '$= {0}$'.format(expressions.integral_intermediate(expr=self._qp['equation'], lb=self._qp['domain'].left, ub=self._qp['domain'].right))

        lines += '$= {0}$'.format(answer)

        return lines.write()


class Conditional:
    def __init__(self, part):
        self.num_lines, self.num_marks = 8, 2

        self._qp = copy.copy(part._qp)

        two_values = sensible_values.conditional_integral(self._qp['equation'], self._qp['domain'])


        self._qp['major_bound'], self._qp['minor_bound'] = two_values


        self._qp['major_direction'] = r'\le' if self._qp['minor_bound'] < self._qp['major_bound'] else r'\ge'
        self._qp['minor_direction'] = random.choice([r'\le', r'\ge'])
    
        
    def question_statement(self):
        return r'Find $Pr(X {0} {1} | X {2} {3})$.'.format(self._qp['minor_direction'], sympy.latex(self._qp['minor_bound']),
                                                            self._qp['major_direction'], sympy.latex(self._qp['major_bound']))


    def solution_statement(self):
        lines = solution_lines.Lines()

        minor = r'X {0} {1}'.format(self._qp['minor_direction'], sympy.latex(self._qp['minor_bound']))
        major = r'X {0} {1}'.format(self._qp['major_direction'], sympy.latex(self._qp['major_bound']))


        lines += r'$Pr({0} | {1}) = {2}$'.format(minor, major, expressions.conditional_probability(minor, major))

        lb = min(self._qp['minor_bound'], self._qp['major_bound'])
        ub = max(self._qp['minor_bound'], self._qp['major_bound'])
        top_integral = expressions.integral(lb=lb, ub=ub, expr=self._qp['equation'])
        top_intermediate = expressions.integral_intermediate(lb=lb, ub=ub, expr=self._qp['equation'].integrate())
        top_eval = expressions.integral_intermediate_eval(lb=lb, ub=ub, expr=self._qp['equation'].integrate())
        top_value = self._qp['equation'].integrate((x, lb, ub))


        if self._qp['major_direction'] == r'\le':
            lb = self._qp['domain'].left
            ub = self._qp['major_bound']
        else:
            lb = self._qp['major_bound']
            ub = self._qp['domain'].right


        bottom_integral = expressions.integral(lb=lb, ub=ub, expr=self._qp['equation'])
        bottom_intermediate = expressions.integral_intermediate(lb=lb, ub=ub, expr=self._qp['equation'].integrate())
        bottom_eval = expressions.integral_intermediate_eval(lb=lb, ub=ub, expr=self._qp['equation'].integrate())
        bottom_value = self._qp['equation'].integrate((x, lb, ub))

        lines += r'$= \frac{{ {0} }}{{ {1} }}$'.format(top_integral, bottom_integral)

        lines += r'$= \frac{{ {0} }}{{ {1} }}$'.format(top_intermediate, bottom_intermediate)

        lines += r'$= \frac{{ {0} }}{{ {1} }}$'.format(top_eval, bottom_eval)

        print(self._qp['equation'])
        print(top_value, bottom_value)
        lines += r'$= {0}$'.format(sympy.latex(top_value / bottom_value))

        return lines.write()
