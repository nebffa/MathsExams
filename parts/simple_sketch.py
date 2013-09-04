import sympy
from sympy.abc import *
from maths import all_functions


class SimpleSketch(object):
    def __init__(self):

        function_type = random.choice('absolute_value', 'hyperbola')

        if function_type == 'absolute_value':
            function = all_functions.request_absolute_value(difficulty=3)
        elif function_type == 'hyperbola':
            function = all_functions.request_hyperbola(difficulty=3)

        numpy_function = sympy_to_numpy(function)

