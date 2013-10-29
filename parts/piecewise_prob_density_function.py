import sympy
import random
from maths import domains
from maths.symbols import *
from maths.latex import expressions, latex, solution_lines
import copy
from piecewise_prob_density_function_unknown import PiecewiseProbDensityFunctionUnknown


class PiecewiseProbDensityFunction(PiecewiseProbDensityFunctionUnknown):
    def __init__(self):
        super(PiecewiseProbDensityFunction, self).__init__()

        self._qp['equation'] = self._qp['equation'].subs({k: self._qp['k']})


    def question_statement(self):


        piecewise = sympy.Piecewise((self._qp['equation'], sympy.And(self.domain.left < x, x < self.domain.right)), (0, True))

        lines = solution_lines.Lines()

        lines += r'The function $f(x) = {0}$'.format( expressions.piecewise(piecewise) )
        lines += r'is a probability density function for the continuous random variable $X$.'
        return lines.write()



    def solution_statement(self):
        return ''


class SimpleInterval:
    def __init__(self, part):
        domain = part._qp['domain']

        choices = [domain.left + sympy.Rational(i, 4) * domain.measure for i in [1, 2, 3]]

        print(domain)
        print(choices)

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
        self._qp = copy.copy(part._qp)

        
    
        



parent = PiecewiseProbDensityFunction()
child = SimpleInterval(parent)

print(child.solution_statement())   