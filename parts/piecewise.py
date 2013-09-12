import sympy
import random
from sympy.abc import *
from maths.rich_requests import requests
from maths.plot import plot


class Piecewise:
    def __init__(self):
        self.num_lines, self.num_marks = 0, 0
        
        partition_x = random.randint(-2, 2)

        functions = random.sample(['hyperbola', 'cubic', 'absolute_value'], 2)
        function_left, function_right = functions

        domain_left = sympy.Interval(-6, partition_x)
        domain_right = sympy.Interval(partition_x, 6)

        if function_left == 'hyperbola':
            function_left = requests.hyperbola(vertical_asymptote=domain_left)
        elif function_left == 'cubic':
            function_left = requests.cubic(turning_points_location=domain_left, num_turning_points=2)
        elif function_left == 'absolute_value':
            function_left = requests.absolute_value(extreme_point=domain_left)

        if function_right == 'hyperbola':
            function_right = requests.hyperbola(vertical_asymptote=domain_right)
        elif function_right == 'cubic':
            function_right = requests.cubic(turning_points_location=domain_right, num_turning_points=2)
        elif function_right == 'absolute_value':
            function_right = requests.absolute_value(extreme_point=domain_right)        

        self.equation = sympy.Piecewise((function_left, x < domain_left.right), (function_right, x >= domain_left.right))
        self.domain = domain_left + domain_right

    def question_statement(self):
        path = plot.plot(y.equation, self.domain)

        return r'''The graph of the function $f$ is shown, where {0} \\
                        \includegraphics{{{1}}}'''.format(sympy.latex(self.equation), path.strip('.eps'))
        
    def solution_statement(self):
        pass

    def sanity_check(self):
        pass

