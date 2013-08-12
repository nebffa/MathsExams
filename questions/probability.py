import sympy
import random
from maths import domains
from maths.symbols import *
from maths.latex import expressions


class PiecewiseProbDensityFunction(object):
    def __init__(self):

        # 2008 Q4 [7 lines] [2 marks]
        # 2010 Q7a [12 lines] [3 marks]
        # 2012 Q8b [12 lines] [3 marks]

        self.num_marks = 3
        self.num_lines = 12


        self.function_type = random.choice(['sin', 'cos', 'linear', 'quadratic'])

        if self.function_type == 'sin':
            while True:
                self.domain = domains.integer_domain(low=0, high=2, minimum_distance=1)
                m = random.choice([sympy.pi/2, sympy.pi])
                self.equation = k * sympy.sin(m*x)

                area = self.equation.integrate((x, self.domain.left, self.domain.right))
                try:
                    self.value = sympy.solve(area - 1)[0]
                except:
                    self.value = None

                if self.value is not None:
                    self.equation = self.equation.subs({k: self.value})
                    break

        elif self.function_type == 'cos':
            while True:
                self.domain = domains.integer_domain(low=0, high=2, minimum_distance=1)
                m = random.choice([sympy.pi/2, sympy.pi])
                self.equation = k * sympy.cos(m*x)

                area = self.equation.integrate((x, self.domain.left, self.domain.right))
                try:
                    self.value = sympy.solve(area - 1)[0]
                except:
                    self.value = None

                if self.value is not None:
                    self.equation = self.equation.subs({k: self.value})
                    break

        elif self.function_type == 'linear':
            self.domain = domains.integer_domain()
            m = random.randint(1, 2)
            a = random.randint(7, 12)
            self.equation = (m*x + z) / a

            area = self.equation.integrate((x, self.domain.left, self.domain.right))
            self.value = sympy.solve(area - 1)
            self.equation = self.equation.subs({z: self.value[0]})

        elif self.function_type == 'quadratic':
            self.domain = domains.integer_domain()
            self.equation = z * (x - self.domain.left) * (x - self.domain.right)


            area = self.equation.integrate((x, self.domain.left, self.domain.right))
            self.value = sympy.solve(area - 1)[0]
            self.equation = self.equation.subs({z: self.value})

    def question_statement(self):
        piecewise = sympy.Piecewise((self.equation, self.domain.left < x < self.domain.right), (0, True))
        line_1 = r'The function $f(x) = %s$ is a probability density function for the continuous random variable $X$.' % sympy.latex(piecewise)
        line_2 = r'Show that $k = %s$.' % self.value
        return line_1 + line_2

    def solution_statement(self):
        line_1 = r'$k %s = 1$' % expressions.integral(lb=self.domain.left, ub=self.domain.right, expr=self.equation)
        line_2 = r'$k %s = k %s = k %s = 1$' % (expressions.integral_intermediate(lb=self.domain.left, ub=self.domain.right, expr=self.equation),
                                    expressions.integral_intermediate_eval(lb=self.domain.left, ub=self.domain.right, expr=self.equation),
                                    sympy.latex(self.equation.subs({x: self.domain.right}) - self.equation.subs({x: self.domain.left}))
                                    )
        line_3 = r'$\therefore k = %s$' % self.value
        return line_1 + line_2 + line_3
