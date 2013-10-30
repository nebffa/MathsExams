import sympy
import random
from maths import domains
from maths.symbols import *
from maths.latex import expressions, latex, solution_lines


class PiecewiseProbDensityFunctionUnknown(object):
    def __init__(self):

        # 2008 Q4 [7 lines] [2 marks]
        # 2010 Q7a [12 lines] [3 marks]
        # 2012 Q8b [12 lines] [3 marks]

        self.num_marks = 3
        self.num_lines = 12

        self._qp = {}
        self.function_type = random.choice(['sin', 'cos', 'linear', 'quadratic'])

        if self.function_type == 'sin':
            while True:
                self._qp['domain'] = domains.integer_domain(low=0, high=2, minimum_distance=1)
                m = random.choice([sympy.pi/2, sympy.pi])
                self._qp['equation'] = k * sympy.sin(m*x)

                area = self._qp['equation'].integrate((x, self._qp['domain'].left, self._qp['domain'].right))
                try:
                    self._qp['k'] = sympy.solve(area - 1)[0]
                except:
                    self._qp['k'] = None

                if self._qp['k'] is not None:
                    break

        elif self.function_type == 'cos':
            while True:
                self._qp['domain'] = domains.integer_domain(low=0, high=2, minimum_distance=1)
                m = random.choice([sympy.pi/2, sympy.pi])
                self._qp['equation'] = k * sympy.cos(m*x)

                area = self._qp['equation'].integrate((x, self._qp['domain'].left, self._qp['domain'].right))
                try:
                    self._qp['k'] = sympy.solve(area - 1)[0]
                except:
                    self._qp['k'] = None

                if self._qp['k'] is not None:
                    break

        elif self.function_type == 'linear':
            self._qp['domain'] = domains.integer_domain()
            m = random.randint(1, 2)
            a = random.randint(7, 12)
            self._qp['equation'] = ((m*x + k) / a).together()

            area = self._qp['equation'].integrate((x, self._qp['domain'].left, self._qp['domain'].right))
            self._qp['k'] = sympy.solve(area - 1)[0]

        elif self.function_type == 'quadratic':
            self._qp['domain'] = domains.integer_domain()
            self._qp['equation'] = k * (x - self._qp['domain'].left) * (x - self._qp['domain'].right)

            area = self._qp['equation'].integrate((x, self._qp['domain'].left, self._qp['domain'].right))
            self._qp['k'] = sympy.solve(area - 1)[0]


    def question_statement(self):
        piecewise = sympy.Piecewise((self._qp['equation'], sympy.And(self._qp['domain'].left < x, x < self._qp['domain'].right)), (0, True))

        lines = solution_lines.Lines()

        lines += r'The function $f(x) = {0}$'.format( expressions.piecewise(piecewise) )
        lines += r'is a probability density function for the continuous random variable $X$. Show that $k = {0}$.'.format(sympy.latex(self._qp['k']))
        
        return lines.write()

    def solution_statement(self):
        lines = solution_lines.Lines()

        lines += r'${0} = 1$'.format( expressions.integral(lb=self._qp['domain'].left, ub=self._qp['domain'].right, expr=self._qp['equation']) )
        lines += r'${0} = {1} = {2} = 1$'.format(
                                    expressions.integral_intermediate(lb=self._qp['domain'].left, ub=self._qp['domain'].right, 
                                            expr=self._qp['equation']),
                                    expressions.integral_intermediate_eval(lb=self._qp['domain'].left, ub=self._qp['domain'].right, 
                                            expr=self._qp['equation']),
                                    sympy.latex(self._qp['equation'].integrate((x, self._qp['domain'].left, self._qp['domain'].right)))
                                    )
        lines += r'$\therefore k = {0}$'.format( sympy.latex(self._qp['k']) )

        return lines.write()

    def sanity_check(self):
        true_equation = self._qp['equation'].subs({k: self._qp['k']})

        if true_equation.integrate((x, self._qp['domain'].left, self._qp['domain'].right)) != 1:
            raise RuntimeError(r'equation: {0}, domain: {1}, does not integrate to 1'.format(self._qp['equation'], self._qp['domain']))
