import sympy
import random
from .. import all_functions, not_named_yet
from ..symbols import *


class PiecewiseProbDensityFunction(object):
    def __init__(self):
        self.function_type = random.choice(['sin', 'cos', 'linear', 'quadratic'])

        self.function_type = 'quadratic'

        if self.function_type == 'sin':
            self.equation = all_functions.request_sin(difficulty=1).equation
        elif self.function_type == 'cos':
            self.equation = all_functions.request_cos(difficulty=1).equation
        elif self.function_type == 'linear':
            while True:
                m = not_named_yet.randint(-2, 2, exclude=[0])
                a = random.randint(8, 12)
                c = not_named_yet.randint_no_zero(-3, 3)

                self.equation = ((m*x + c)/a).together()

                x_intercept = -c/m

                if m < 0:
                    upper = x_intercept - 1
                    trapezoid_area = (upper - z)/2 * (self.equation.subs({x: upper}) + self.equation.subs({x: z}))
                    lower = sympy.solve(trapezoid_area - 1)

                    lower = filter(lambda f: f < upper, lower)[0]
                    
                elif m > 0:
                    lower = x_intercept + 1
                    trapezoid_area = (z - lower)/2 * (self.equation.subs({x: lower}) + self.equation.subs({x: z}))
                    upper = sympy.solve(trapezoid_area - 1)

                    upper = filter(lambda f: f > lower, upper)[0]

                if sympy.ask(sympy.Q.rational(lower)) and sympy.ask(sympy.Q.rational(upper)):
                    break

            self.domain = sympy.Interval(lower, upper, False, False)
        elif self.function_type == 'quadratic':
            x1_intercept = not_named_yet.randint(-3, 1)

            x2_intercept = x1_intercept + not_named_yet.randint(4, 6)
            self.equation = z*(x - x1_intercept) * (x - x2_intercept)

            area = self.equation.integrate((x, x1_intercept, x2_intercept))

            values = sympy.solve(area - 1)

            print values


y = PiecewiseProbDensityFunction()
print y.equation
print y.domain
print y.equation.integrate((x, y.domain.left, y.domain.right))