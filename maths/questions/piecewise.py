import sympy
import random
from ..rich_requests import requests
from ..plot import plot
from ..utils import functions
from ..symbols import x, coeff0, coeff1, coeff2, coeff3
from . import relationships
import copy


@relationships.root
class Piecewise(relationships.QuestionPart):
    """
    Question description
    ====================

    Setup a piecewise function.


    Real-life instances
    ===================

    2008 6: [Blank slate]
    """

    def __init__(self):
        self.num_lines, self.num_marks = 0, 0
        self._qp = {}

        function_left, function_right = random.sample(['hyperbola', 'cubic', 'absolute_value'], 2)

        partition_x = random.randint(-2, 2)
        domain_left = sympy.Interval(-sympy.oo, partition_x, False, True)
        domain_right = sympy.Interval(partition_x, sympy.oo, False, False)

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

        if random.randint(0, 1):  # decide which part of the piecewise function gets ownership of the shared x-coordinate
            self._qp['equation'] = sympy.Piecewise((function_left, x < domain_left.right), (function_right, x >= domain_left.right))
        else:
            self._qp['equation'] = sympy.Piecewise((function_left, x <= domain_left.right), (function_right, x > domain_left.right))

        self._qp['plot_domain'] = self._qp['plot_range'] = sympy.Interval(-6, 6)

    def question_statement(self):
        path = plot.plot(self._qp['equation'], self._qp['plot_domain'], self._qp['plot_range'])

        return r'''The graph of the function $f$ is shown, where $f = {equation}$ {plot}'''.format(
            equation=sympy.latex(self._qp['equation']),
            plot=plot.latex(path)
        )

    def sanity_check(self):
        # check that the middle point does not have the same y-value and same derivative. otherwise that would be an oopsie!!
        middle = self._qp['equation'].args[0].args[1].rhs
        func_left, func_right = self._qp['equation'].args[0].args[0], self._qp['equation'].args[1].args[0]

        func_left_value_at_middle = func_left.subs({x: middle})
        func_right_value_at_middle = func_right.subs({x: middle})

        left_slope_at_middle = func_left.diff().subs({x: middle})
        right_slope_at_middle = func_right.diff().subs({x: middle})

        same_y_coordinate_at_middle = True if func_left_value_at_middle == func_right_value_at_middle else False
        same_derivative_at_middle = True if left_slope_at_middle == right_slope_at_middle else False

        if same_y_coordinate_at_middle and same_derivative_at_middle:
            raise ValueError('The piecewise function is differentiable at its split point!')


@relationships.is_child_of(Piecewise)
class DomainDerivative(relationships.QuestionPart):
    """
    Question description
    ====================

    Calculate the domain of the derivative of a piecewise function.


    Real-life instances
    ===================

    2008 6a: [3 lines] [1 mark]
    """

    def __init__(self, part):
        self.num_lines, self.num_marks = 3, 1
        self._qp = copy.copy(part._qp)

        self._qp['domain'] = sympy.Interval(-sympy.oo, sympy.oo)
        for piecewise_part in self._qp['equation'].args:
            expr = piecewise_part[0]

            self._qp['domain'] &= functions.maximal_domain(expr, self._qp['domain'])

            if expr.find(sympy.Abs):  # an absolute value is not differentiable at its vertex
                match = expr.match(coeff0 * sympy.Abs(coeff1 * x - coeff2) + coeff3)
                self._qp['domain'] -= sympy.FiniteSet(match[coeff2] / match[coeff1])

        # a piecewise function is not differentiable at the meeting points of the subparts (unless the same y-coordinate
        # and the same derivative is approached from both sides, which it is guaranteed not to)
        middle = self._qp['equation'].args[0].args[1].rhs
        self._qp['domain'] -= sympy.FiniteSet(middle)

    def question_statement(self):
        return r"""The stationary points of the function are labelled with their coordinates.
            Write down the domain of the derivative function $f'$."""

    def solution_statement(self):
        return r'${answer}$'.format(
            answer=sympy.latex(self._qp['domain'])
        )


@relationships.is_child_of(Piecewise)
class AbsoluteValue(relationships.QuestionPart):
    """
    Question description
    ====================

    Sketch the absolute value of one side of a piecewise function.


    Real-life instances
    ===================

    2008 6b: [0 lines] [2 marks]
    """

    def __init__(self, part):
        self.num_lines, self.num_marks = 0, 2
        self._qp = copy.copy(part._qp)

        # find the half of the piecewise that is not already an absolute value
        func_left, func_right = self._qp['equation'].args
        if func_left.has(sympy.Abs):
            self.function = func_right
            self._qp['equation'] = sympy.Abs(func_right[0])
            self._qp['domain'] = functions.relation_to_interval(func_right[1]) & self._qp['plot_domain']
        else:
            self._qp['equation'] = sympy.Abs(func_left[0])
            self._qp['domain'] = functions.relation_to_interval(func_left[1]) & self._qp['plot_domain']

        self._qp['is_cubic'] = self._qp['equation'].has(x ** 3)

    def question_statement(self):
        path = plot.blank_plot(self._qp['plot_domain'], self._qp['plot_range'])

        if self._qp['is_cubic']:
            cubic_statement = r'Label stationary points with their coordinates (do not attempt to find x-axis intercepts).'
        else:
            cubic_statement = r''

        return r'''By referring to the graph of $f$, sketch the graph of the function with rule
            $y = {equation}$, for ${domain}$. {cubic_statement} {plot}'''.format(
            equation=sympy.latex(self._qp['equation']),
            domain=sympy.latex(self._qp['domain']),
            cubic_statement=cubic_statement,
            plot=plot.latex(path)
        )

    def solution_statement(self):
        path = plot.plot(
            self._qp['equation'],
            self._qp['plot_domain'],
            self._qp['plot_range'],
            expr_domain=self._qp['domain']
        )

        return r'''{plot}'''.format(
            plot=plot.latex(path)
        )
