import sympy
import random
from .. import all_functions, not_named_yet
from ..latex import latex, solutions
from ..utils import noevals
from ..symbols import *
from . import relationships


@relationships.is_child_of(relationships.DummyPart)
class SimpleDiff(relationships.QuestionPart):
    """
    Question description
    ====================

    Find the derivative of an equation.


    Real-life instances
    ===================

    There are several, all with about 4-5 lines and 2 marks.
    """

    def __init__(self):
        self.num_lines, self.num_marks = 5, 2
        self._qp = {}

        function_type = random.choice(['sqrt', 'quadratic', 'product'])

        if function_type == 'sqrt':
            outer_function = all_functions.request_linear(difficulty=2).equation
            inner_function = all_functions.request_linear(difficulty=1).equation
            inner_function = inner_function.replace(lambda expr: expr.is_Symbol, lambda expr: sympy.sqrt(expr))

            self._qp['equation'] = outer_function.replace(x, inner_function)
            self._qp['derivative'] = sympy.diff(self._qp['equation'])

        elif function_type == 'quadratic':
            power_two_coeff = not_named_yet.randint_no_zero(-3, 3)
            power_one_coeff = not_named_yet.randint_no_zero(-5, 5)
            inner_function = power_two_coeff * x ** 2 + power_one_coeff * x
            index = random.randint(3, 5)

            self._qp['equation'] = inner_function ** index
            self._qp['derivative'] = sympy.diff(self._qp['equation'])

        elif function_type == 'product':
            left_function = x ** random.randint(1, 3)
            right_outer_function = random.choice([sympy.sin, sympy.cos, sympy.log, sympy.exp])
            right_inner_function = not_named_yet.randint_no_zero(-3, 3) * x

            self._qp['equation'] = left_function * right_outer_function(right_inner_function)
            self._qp['derivative'] = sympy.diff(self._qp['equation'])

    def question_statement(self):
        return r"Let $f(x) = {equation}$. Find $f'(x)$.".format(
            equation=sympy.latex(self._qp['equation'])
        )

    def solution_statement(self):
        lines = solutions.Lines()

        # look for chain rule candidates and show extra working for the chain rule
        if self._qp['equation'].as_base_exp()[1] != 1:
            u = sympy.Symbol('u')
            inner_function, exponent = self._qp['equation'].as_base_exp()
            lines += r"Let $f(x) = {0} = {1}, u = {2}$".format(sympy.latex(self._qp['equation']), sympy.latex(u ** exponent), sympy.latex(inner_function))
            lines += r"$f'(x) = \frac{{dy}}{{du}} \times \frac{{du}}{{dx}} = %s \times u'$" % sympy.latex((u ** exponent).diff())

        lines += r"$f'(x) = {0}$".format(
            sympy.latex(self._qp['derivative'].factor())
        )

        return lines.write()


@relationships.is_child_of(relationships.DummyPart)
class SimpleDiffEval(relationships.QuestionPart):
    """
    Question description
    ====================

    Find the derivative of an equation and then evaluate it at a particular location.


    Real-life instances
    ===================

    There are several, all with about 4-5 lines and 2 marks.
    """

    def create_product_differentiation(self):
        """Create a product to differentiate.
        """

        index = random.randint(1, 3)
        left_function = x ** index

        right_outer_function = random.choice([sympy.sin, sympy.cos, sympy.log, sympy.exp])
        right_inner_function = not_named_yet.randint_no_zero(-3, 3) * x

        self._qp['equation'] = left_function * right_outer_function(right_inner_function)
        self._qp['derivative'] = sympy.diff(self._qp['equation'])

        if right_outer_function in [sympy.sin, sympy.cos]:
            # using multiples of pi/6 can lead to large coefficients like pi**3/54
            if index == 1:
                self._qp['x_value'] = random.choice([sympy.pi / 6 * i for i in range(-5, 7)])
            elif index in [2, 3]:
                self._qp['x_value'] = random.choice([sympy.pi / 2 * i for i in range(-1, 3)])

        elif right_outer_function == sympy.log:
            self._qp['x_value'] = sympy.Rational(1, right_inner_function.coeff(x)) * sympy.E ** random.randint(1, 3)
        elif right_outer_function == sympy.exp:
            # with something like x**3 * e^x using x = 3, we'd get large answers. we restrict x values based on the index of x
            self._qp['x_value'] = random.randint(-3 // index, 3 // index)

    def create_quotient_differentiation(self):
        """Create a quotient to differentiate.
        """

        non_linear_function = random.choice([sympy.cos(x), sympy.sin(x), sympy.exp(x)])
        linear_function = all_functions.request_linear(difficulty=3).equation

        self._qp['equation'] = non_linear_function / linear_function
        if random.choice([True, False]):
            self._qp['equation'] = 1 / self._qp['equation']
        denominator = linear_function.as_numer_denom()[1]

        while True:
            if non_linear_function == sympy.exp(x):
                self._qp['x_value'] = random.randint(-2, 2)
            else:
                possible_x_values = [-sympy.pi, 0, sympy.pi]
                self._qp['x_value'] = random.choice(possible_x_values)

            if denominator.subs({x: self._qp['x_value']}) != 0:
                break

    def create_composite_differentiation(self):
        """Create a composite function to differentiate.
        """

        outer_function = random.choice([sympy.exp, sympy.log])

        if outer_function == sympy.exp:
            # with bad x values we can get things like: dy/dx = (4*x + 4)*exp(2*x**2 + 4*x + 20), at x = 1, dy/dx = exp(26)
            self._qp['x_value'] = random.randint(-3, 3)
            inner_function = all_functions.request_quadratic(difficulty=random.randint(1, 3)).equation

        elif outer_function == sympy.log:
            # the inner quadratic may never yield a positive number in this domain, so we will try
            # a couple of times to find an x value that works, then we will request a new quadratic
            while True:
                self._qp['x_value'] = random.randint(-3, 3)
                inner_function = all_functions.request_quadratic(difficulty=random.randint(1, 3)).equation
                if inner_function.subs({x: self._qp['x_value']}) > 0:
                    break

        self._qp['equation'] = outer_function(inner_function)

    def __init__(self):
        self.num_lines, self.num_marks = 5, 2
        self._qp = {}

        function_types = ['product', 'quotient', 'composite']
        function_type = random.choice(function_types)

        if function_type == 'product':
            # 2008 1b: y = x * e**(3x), a = 0
            # 2011 1b: y = x**2 * sin(2x), a = pi / 6
            self.create_product_differentiation()

        elif function_type == 'quotient':
            # 2009 1b: y = cos(x) / (2x + 2), a = pi
            # 2012 1b: y = x / sin(x), a = pi / 2
            self.create_quotient_differentiation()

        elif function_type == 'composite':
            # I thought of including sin and cos, but I can't remember ever seeing a question where a quadratic was nested inside
            # of a trig function
            self.create_composite_differentiation()

        if function_type == 'quotient':
            # quotients are always written as one big fraction, but sympy always separates them into multiple fractions, so we have to factorise
            self._qp['derivative'] = sympy.diff(self._qp['equation']).together()
        else:
            self._qp['derivative'] = sympy.diff(self._qp['equation'])

        self._qp['answer'] = self._qp['derivative'].subs({x: self._qp['x_value']})

    def question_statement(self):
        return r"If $f(x) = {equation}$, find $f'({x_value})$.".format(
            equation=sympy.latex(self._qp['equation']),
            x_value=sympy.latex(self._qp['x_value'])
        )

    def solution_statement(self):
        # needs more work at the moment - likely an inbetween step to evaluate every subexpression in f'(x) but not f'(x) itself

        lines = solutions.Lines()
        lines += r"$f'(x) = {derivative}$".format(
            derivative=sympy.latex(self._qp['derivative'])
        )

        # print extra steps when dealing with trig functions
        if self._qp['equation'].find(sympy.sin) or self._qp['equation'].find(sympy.cos):
            noeval_derivative = noevals.noevalify(self._qp['derivative'], include=[sympy.sin, sympy.cos])

            lines += r"$f'({x_value}) = {derivative}$".format(
                x_value=sympy.latex(self._qp['x_value']),
                derivative=sympy.latex(noeval_derivative)
            )

            subpart_values = []
            for subpart in self._qp['derivative'].find(sympy.Function):
                noeval_subpart = noevals.noevalify(subpart)

                subpart_value = subpart.subs({x: self._qp['x_value']})
                unevaluated_subpart = noeval_subpart.subs({x: self._qp['x_value']})
                subpart_text = r'${unevaluated_subpart} = {subpart_value}$'.format(
                    unevaluated_subpart=sympy.latex(unevaluated_subpart),
                    subpart_value=sympy.latex(subpart_value)
                )

                subpart_values.append(subpart_text)

            lines += ', '.join(subpart_values)

        lines += r"$f'({x_value}) = {answer}$".format(
            x_value=sympy.latex(self._qp['x_value']),
            answer=sympy.latex(self._qp['answer'])
        )

        return lines.write()
