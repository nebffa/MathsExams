import sympy
import random
from sympy.abc import *
from maths import all_functions, not_named_yet, simplify


class PiecewiseProbDensityFunction(object):
    def __init__(self):
        self.function_type = random.choice(['sin', 'cos', 'linear', 'quadratic'])

        if self.function_type == 'sin':
            self.equation = all_functions.request_sin(difficulty=1)
        elif self.function_type == 'cos':
            self.equation = all_functions.request_cos(difficulty=1)
        elif self.function_type == 'linear':
            self.equation = all_functions.request_linear(difficulty)
