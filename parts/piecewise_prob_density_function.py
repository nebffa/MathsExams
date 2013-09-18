import sympy
import random
from maths import domains
from maths.symbols import *
from maths.latex import expressions, latex


class PiecewiseProbDensityFunction(object):
    def __init__(self):

        # 2008 Q4 [7 lines] [2 marks]
        # 2010 Q7a [12 lines] [3 marks]
        # 2012 Q8b [12 lines] [3 marks]

        self.num_marks = 3
        self.num_lines = 12

        self._question_params = {}
        self.function_type = random.choice(['sin', 'cos', 'linear', 'quadratic'])

        if self.function_type == 'sin':
            while True:
                self.domain = domains.integer_domain(low=0, high=2, minimum_distance=1)
                m = random.choice([sympy.pi/2, sympy.pi])
                self._question_params['equation'] = k * sympy.sin(m*x)

                area = self._question_params['equation'].integrate((x, self.domain.left, self.domain.right))
                try:
                    self._question_params['k'] = sympy.solve(area - 1)[0]
                except:
                    self._question_params['k'] = None

                if self._question_params['k'] is not None:
                    self._question_params['equation'] = self._question_params['equation'].subs({k: self._question_params['k']})
                    break

        elif self.function_type == 'cos':
            while True:
                self.domain = domains.integer_domain(low=0, high=2, minimum_distance=1)
                m = random.choice([sympy.pi/2, sympy.pi])
                self._question_params['equation'] = k * sympy.cos(m*x)

                area = self._question_params['equation'].integrate((x, self.domain.left, self.domain.right))
                try:
                    self._question_params['k'] = sympy.solve(area - 1)[0]
                except:
                    self._question_params['k'] = None

                if self._question_params['k'] is not None:
                    self._question_params['equation'] = self._question_params['equation'].subs({k: self._question_params['k']})
                    break

        elif self.function_type == 'linear':
            self.domain = domains.integer_domain()
            m = random.randint(1, 2)
            a = random.randint(7, 12)
            self._question_params['equation'] = (m*x + z) / a

            area = self._question_params['equation'].integrate((x, self.domain.left, self.domain.right))
            self._question_params['k'] = sympy.solve(area - 1)[0]
            self._question_params['equation'] = self._question_params['equation'].subs({z: self._question_params['k']})

        elif self.function_type == 'quadratic':
            self.domain = domains.integer_domain()
            self._question_params['equation'] = z * (x - self.domain.left) * (x - self.domain.right)

            area = self._question_params['equation'].integrate((x, self.domain.left, self.domain.right))
            self._question_params['k'] = sympy.solve(area - 1)[0]
            self._question_params['equation'] = self._question_params['equation'].subs({z: self._question_params['k']})

        self._question_params['question_equation'] = self._question_params['equation'] * k / self._question_params['k']

    def question_statement(self):
        piecewise = sympy.Piecewise((self._question_params['question_equation'], sympy.And(self.domain.left < x, x < self.domain.right)), (0, True))

        line_1 = r'The function $f(x) = {0}$'.format( expressions.piecewise(piecewise) )
        line_2 = r'is a probability density function for the continuous random variable $X$. Show that $k = {0}$.'.format(sympy.latex(self._question_params['k']))
        return latex.latex_newline().join([line_1, line_2])

    def solution_statement(self):
        line_1 = r'$%s = 1$' % expressions.integral(lb=self.domain.left, ub=self.domain.right, expr=self._question_params['question_equation'])
        line_2 = r'$%s = %s = %s = 1$' % (
                                    expressions.integral_intermediate(lb=self.domain.left, ub=self.domain.right, expr=self._question_params['question_equation']),
                                    expressions.integral_intermediate_eval(lb=self.domain.left, ub=self.domain.right, expr=self._question_params['question_equation']),
                                    sympy.latex(self._question_params['question_equation'].subs({x: self.domain.right}) - 
                                            self._question_params['equation'].subs({x: self.domain.left}))
                                    )
        line_3 = r'$\therefore k = %s$' % self._question_params['k']
        return latex.latex_newline().join([line_1, line_2, line_3])
