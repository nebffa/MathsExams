import sympy
import random
from sympy.abc import *
from maths.rich_requests import requests
from maths.plot import plot
from maths.utils import functions
from maths.symbols import *


class Piecewise:
    def __init__(self):
        self.num_lines, self.num_marks = 0, 0
        
        self._question_params = {}

        partition_x = random.randint(-2, 2)

        function_left, function_right = random.sample(['hyperbola', 'cubic', 'absolute_value'], 2)

        if random.randint(0, 1):  # decide which part of the Piecewise gets ownership of the shared x-coordinate
            domain_left = sympy.Interval(-sympy.oo, partition_x, False, True)
            domain_right = sympy.Interval(partition_x, sympy.oo, False, False)
        else:
            domain_left = sympy.Interval(-sympy.oo, partition_x, False, False)
            domain_right = sympy.Interval(partition_x, sympy.oo, True, False)

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
        self._question_params['plot_domain'] = sympy.Interval(-6, 6)

    def question_statement(self):
        path = plot.plot(self.equation, self._question_params['plot_domain'])

        return r'''The graph of the function $f$ is shown, where ${0}$ \\
                        {1}'''.format(sympy.latex(self.equation), plot.latex(path))
        
    def solution_statement(self):
        return ''

    def sanity_check(self):
        # check that the middle point does not have the same y-value and same derivative. otherwise that would be an oopsie!!
        middle = self.equation.args[0].args[1].rhs
        func_left, func_right = self.equation.args[0].args[0], self.equation.args[1].args[0]

        if (func_left.subs({x: middle}) == func_right.subs({x: middle}) and 
            func_left.diff().subs({x: middle}) == func_right.diff().subs({x: middle}) ):
            raise ValueError('The piecewise function is differentiable at its split point!')
        

class DomainDerivative:
    def __init__(self, part):
        self.num_lines, self.num_marks = 3, 1

        self.equation = part.equation
        self.domain = sympy.Interval(-sympy.oo, sympy.oo)
        for piecewise_part in self.equation.args:
            expr = piecewise_part[0]

            self.domain &= functions.maximal_domain(expr, self.domain)

            if expr.find(sympy.Abs):
                match = expr.match(x0 * sympy.Abs(x1 * x - x2) + x3)
                self.domain -= sympy.FiniteSet(match[x2] / match[x1])

        middle = self.equation.args[0].args[1].rhs
        self.domain -= sympy.FiniteSet(middle)

        
    def question_statement(self):
        return r"""The stationary points of the function are labelled with their coordinates. Write down the domain of the derivative function $f'$."""

    def solution_statement(self):
        return r'''${0}$'''.format(sympy.latex(self.domain))

    def sanity_check(self):
        pass


class AbsoluteValue:
    def __init__(self, part):
        self.num_lines, self.num_marks = 0, 2
        self._question_params = {}
        self._question_params['plot_domain'] = part._question_params['plot_domain']


        # find the half of the piecewise that is not already an absolute value
        func_left, func_right = part.equation.args
        if func_left[0].has(sympy.Abs):
            self.function = func_right
            self._question_params['equation'] = sympy.Abs(func_right[0])
            self._question_params['domain'] = functions.relation_to_interval(func_right[1]) & self._question_params['plot_domain']
        else:
            self._question_params['equation'] = sympy.Abs(func_left[0])
            self._question_params['domain'] = functions.relation_to_interval(func_left[1]) & self._question_params['plot_domain']

        self._question_params['is_cubic'] = self._question_params['equation'].has(x**3)


    def question_statement(self):
        path = plot.blank_plot(self._question_params['plot_domain'])

        if self._question_params['is_cubic']:
            cubic_statement = r'''Label stationary points with their coordinates (do not attempt to find x-axis intercepts).'''
        else: 
            cubic_statement = r''

        return r'''By referring to the graph of $f$, sketch the graph of the function with rule 
            $y = {0}$, for ${1}$. {2} {3}'''.format(sympy.latex(self._question_params['equation']), 
                                                    sympy.latex(self._question_params['domain']), 
                                                    cubic_statement, 
                                                    plot.latex(path))


    def solution_statement(self):
        path = plot.plot(self._question_params['equation'], self._question_params['plot_domain'], expr_domain=self._question_params['domain'])

        return r'''{0}'''.format(plot.latex(path))

    def sanity_check(self):
        pass
