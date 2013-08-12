import random
import sympy
import copy
import operator
import itertools
import math
from maths import not_named_yet
from sympy.abc import *

coefficients_bound = 5


class Sin(object):
    def __init__(self, difficulty):
        # general: y = a * sin(h * [pi * ]x) + k
        # base: h == 1 or pi
        # difficulty +: h != 1, h is an integer or the reciprocal of one
        a = not_named_yet.randint_no_zero(-2, 2)
        c = random.choice([-5*sympy.pi/6, -3*sympy.pi/4, -2*sympy.pi/3, -sympy.pi/2, -sympy.pi/3, -sympy.pi/4, -sympy.pi/6,
                                         sympy.pi/6, sympy.pi/4, sympy.pi/3, sympy.pi/2, 2*sympy.pi/3, 3*sympy.pi/4, 5*sympy.pi/6])

        if difficulty == 1:
            self.equation = sympy.sin(a*x, evaluate=False)
        elif difficulty == 2:
            self.equation = sympy.sin(a*x + c, evaluate=False)
        else:
            raise ValueError('You have supplied an invalid difficulty level! Choose between 1 or 2')


class Cos(object):
    def __init__(self, difficulty):
        # general: y = a * cos(h * [pi * ]x) + k
        # base: h == 1 or pi
        # difficulty +: h != 1, h is an integer or the reciprocal of one
        a = not_named_yet.randint_no_zero(-2, 2)
        c = random.choice([-5*sympy.pi/6, -3*sympy.pi/4, -2*sympy.pi/3, -sympy.pi/2, -sympy.pi/3, -sympy.pi/4, -sympy.pi/6,
                                         sympy.pi/6, sympy.pi/4, sympy.pi/3, sympy.pi/2, 2*sympy.pi/3, 3*sympy.pi/4, 5*sympy.pi/6])

        if difficulty == 1:
            self.equation = sympy.cos(a*x, evaluate=False)
        elif difficulty == 2:
            self.equation = sympy.cos(a*x + c, evaluate=False)
        else:
            raise ValueError('You have supplied an invalid difficulty level! Choose between 1 or 2')


class Tan(object):
    def __init__(self, difficulty):
        # general: y = a * tan(h * [pi * ]x) + k
        # base: h == 1 or pi
        # difficulty +: h != 1, h is an integer or the reciprocal of one
        a = not_named_yet.randint_no_zero(-2, 2)
        c = random.choice([-5*sympy.pi/6, -3*sympy.pi/4, -2*sympy.pi/3, -sympy.pi/2, -sympy.pi/3, -sympy.pi/4, -sympy.pi/6,
                                         sympy.pi/6, sympy.pi/4, sympy.pi/3, sympy.pi/2, 2*sympy.pi/3, 3*sympy.pi/4, 5*sympy.pi/6])

        if difficulty == 1:
            self.equation = sympy.tan(a*x, evaluate=False)  # prevents automatic transformation to cotangent in some cases
        elif difficulty == 2:
            self.equation = sympy.tan(a*x + c, evaluate=False)  # prevents automatic transformation to cotangent in some cases
        else:
            raise ValueError('You have supplied an invalid difficulty level! Choose between 1 or 2')


# deprecated
class Trig(object):
    global coefficients_bound

    def __init__(self, difficulty, exclude=[]):
        # general: y = a * sin^n(h * [pi * ]x) + k
        # base: h == 1 or pi
        # difficulty +: h != 1, n == 1, h is an integer or the reciprocal of one
        # difficulty ++: n != 1
        a = 0
        while a == 0:
            a = random.randint(-coefficients_bound / 2, coefficients_bound / 2)

        if difficulty in [1, 2]:
            h = random.sample([1, sympy.pi], 1)[0]
            positive_or_negative = 1
            n = 1
        if difficulty in [3, 4]:
            n = 1
            while True:
                positive_or_negative = random.sample([-1, 1], 1)[0]
                h = sympy.Rational(random.randint(1, coefficients_bound - 1),
                                   random.randint(1, coefficients_bound - 2) * positive_or_negative)
                if h not in [-1, 1]:
                    break
        if difficulty == 4:
            n = 2
        if difficulty not in [1, 2, 3, 4]:
            raise ValueError('You have supplied an invalid difficulty level! Choose between 1, 2, 3 or 4')

        x, k = sympy.symbols('x, k')
        f = sympy.Function('f')

        contains_pi = random.sample([1, sympy.pi], 1)[0]  # used for determining the length of a domain
        f = contains_pi * x

        self.restricted_solutions = []
        while not (2 <= len(self.restricted_solutions) <= 6):  # we want a reasonable number of solutions
            equations, general_solutions = [], []
            for factor in range(n):
                intermediate_solutions, general_solution = [], []
                while True:
                    pathway = random.sample(['sin', 'cos', 'tan'], 1)[0]
                    if pathway not in exclude:
                        break

                value_to_radians = \
                    {
                        'sin':
                        {
                            sympy.Rational(-1): [-sympy.pi / 2],
                            -sympy.sqrt(3) / 2: [-2 * sympy.pi / 3, - sympy.pi / 3],
                            -sympy.sqrt(2) / 2: [-3 * sympy.pi / 4, - sympy.pi / 4],
                            sympy.Rational(-1, 2): [-5 * sympy.pi / 6, -sympy.pi / 6],
                            sympy.Rational(0): [0],
                            sympy.Rational(1, 2): [5 * sympy.pi / 6, sympy.pi / 6],
                            sympy.sqrt(2) / 2: [3 * sympy.pi / 4, sympy.pi / 4],
                            sympy.sqrt(3) / 2: [2 * sympy.pi / 3, sympy.pi / 3],
                            sympy.Rational(1): [sympy.pi / 2]
                        },

                        'cos':
                        {
                            sympy.Rational(-1): [sympy.pi],
                            -sympy.sqrt(3) / 2: [-5 * sympy.pi / 6, 5 * sympy.pi / 6],
                            -sympy.sqrt(2) / 2: [-3 * sympy.pi / 4, 3 * sympy.pi / 4],
                            sympy.Rational(-1, 2): [-2 * sympy.pi / 3, 2 * sympy.pi / 3],
                            sympy.Rational(0): [sympy.pi / 2],
                            sympy.Rational(1, 2): [-sympy.pi / 3, sympy.pi / 3],
                            sympy.sqrt(2) / 2: [-sympy.pi / 4, sympy.pi / 4],
                            sympy.sqrt(3) / 2: [-sympy.pi / 6, sympy.pi / 6],
                            sympy.Rational(1): [0]
                        },

                        'tan':  # tan always has one general solution, so we only need one base solution
                        {
                            -sympy.sqrt(3): [2 * sympy.pi / 3],
                            sympy.Rational(-1): [3 * sympy.pi / 4],
                            -sympy.sqrt(3) / 3: [5 * sympy.pi / 6],
                            sympy.Rational(0): [0],
                            sympy.sqrt(3) / 3: [sympy.pi / 6],
                            sympy.Rational(1): [sympy.pi / 4],
                            sympy.sqrt(3): [sympy.pi / 3]
                        }
                    }[pathway]

                if difficulty == 1:
                    trig_value = 0
                else:
                    trig_value = random.sample(value_to_radians, 1)[0]

                equation = a * \
                    {
                        'sin': sympy.sin(f),
                        'cos': sympy.cos(f),
                        'tan': sympy.tan(f)}[pathway] + \
                    a * trig_value

                intermediate = sympy.solve(equation,
                                           {
                                               'sin': sympy.sin(f * positive_or_negative),
                                               'cos': sympy.cos(f * positive_or_negative),
                                               'tan': sympy.tan(f * positive_or_negative)}[pathway])

                for radian in value_to_radians[intermediate[0]]:
                    intermediate_solutions.append(sympy.solve(f * positive_or_negative - radian, x)[0])

                for intermediate_solution in intermediate_solutions:
                    if pathway in ['sin', 'cos']:
                        if trig_value == sympy.Rational(0):
                            general_solution.append(intermediate_solution + k * (sympy.pi if (contains_pi == 1) else 1) * positive_or_negative)
                        else:
                            general_solution.append(intermediate_solution + k * 2 * (sympy.pi if (contains_pi == 1) else 1) * positive_or_negative)
                    else:
                        general_solution.append(intermediate_solution + k * (sympy.pi if (contains_pi == 1) else 1) * positive_or_negative)

                for solution in intermediate_solutions:
                    if not equation.subs({x: solution}) == 0:
                        print equation.subs({x: solution})  # for debuggings's sake
                        raise ArithmeticError("Some random error when I'm new to writing errors..")

                equations.append(equation)
                general_solutions.append(copy.copy(general_solution))

            self.equation = sympy.expand(reduce(operator.mul, equations))
            self.general_solutions = list(set(itertools.chain.from_iterable(general_solutions)))

            solutions = []
            for j in range(-coefficients_bound / 2, coefficients_bound / 2 + 1):
                for general_solution in self.general_solutions:
                    solutions.append(general_solution.subs({k: j}))

            if contains_pi == sympy.pi:
                start_of_domain = random.randint(-1, 0)
                length_of_domain = random.randint(1, 3)
            else:
                start_of_domain = random.randint(-3, 0)
                length_of_domain = random.randint(1, 4)
            self.domain = [sympy.pi / contains_pi * start_of_domain, sympy.pi / contains_pi * (start_of_domain + length_of_domain)]

            restricted_solutions = []
            for solution in solutions:
                if self.domain[0] <= solution <= self.domain[1]:
                    restricted_solutions.append(solution)

            self.restricted_solutions = sorted(list(set(restricted_solutions)))
            if n == 1:
                if pathway in ['sin', 'cos']:
                    self.period = 2 * sympy.pi / (abs(h) * contains_pi)
                else:
                    self.period = sympy.pi / (abs(h) * contains_pi)

                self.amplitude = abs(a)


def plausible_value(trig_function):

    if trig_function in [sympy.sin, sympy.cos]:
        return random.choice([
                             sympy.Rational(-1),
                             -sympy.sqrt(3) / 2,
                             -sympy.sqrt(2) / 2,
                             sympy.Rational(-1, 2),
                             sympy.Rational(0),
                             sympy.Rational(1, 2),
                             sympy.sqrt(2) / 2,
                             sympy.sqrt(3) / 2,
                             sympy.Rational(1)])
    elif trig_function == sympy.tan:
        return random.choice([
                             -sympy.sqrt(3),
                             sympy.Rational(-1),
                             -sympy.sqrt(3) / 3,
                             sympy.Rational(0),
                             sympy.sqrt(3) / 3,
                             sympy.Rational(1),
                             sympy.sqrt(3)])


def plausible_value_no_zero(trig_type):

    if trig_type in [sympy.sin, sympy.cos]:
        return random.choice([
                             sympy.Rational(-1),
                             -sympy.sqrt(3) / 2,
                             -sympy.sqrt(2) / 2,
                             sympy.Rational(-1, 2),
                             sympy.Rational(1, 2),
                             sympy.sqrt(2) / 2,
                             sympy.sqrt(3) / 2,
                             sympy.Rational(1)])
    elif trig_type == sympy.tan:
        return random.choice([
                             -sympy.sqrt(3),
                             sympy.Rational(-1),
                             -sympy.sqrt(3) / 3,
                             sympy.sqrt(3) / 3,
                             sympy.Rational(1),
                             sympy.sqrt(3)])


def domain(function, lower_bound, upper_bound):
    x = sympy.Symbol('x')
    a = sympy.Wild('a')

    inner_function = [particle.func for particle in function.atoms(sympy.Function)][0]
    function = list(function.atoms(sympy.Function))[0].replace(inner_function(a), a)

    # we have a domain: lower_bound <= x <= upper_bound
    # we want the modified domain: f(lower_bound) <= x <= f(upper_bound)

    modified_lower_bound = function.subs(x, lower_bound)
    modified_upper_bound = function.subs(x, upper_bound)

    value = modified_lower_bound + (int(math.ceil(modified_lower_bound / (sympy.pi / 6))) - modified_lower_bound / (sympy.pi / 6)) * sympy.pi / 6
    values = []
    while True:
        if value <= modified_upper_bound:
            values.append(value)
        else:
            break
        value += sympy.pi / 6

    return [sympy.solve(function - test_value)[0] for test_value in values]


def request_limited_domain(trig_function):
    if trig_function.has(sympy.cos):
        function_type = sympy.cos
    elif trig_function.has(sympy.sin):
        function_type = sympy.sin
    elif trig_function.has(sympy.tan):
        function_type = sympy.tan
    elif trig_function.has(sympy.cot):
        function_type = sympy.cot

    x0, x1, x2, x3 = sympy.Wild('x0'), sympy.Wild('x1'), sympy.Wild('x2'), sympy.Wild('x3')
    match = trig_function.match(x0 * function_type(x1*x + x2) + x3)

    if function_type in [sympy.cos, sympy.sin]:
        period = abs(2*sympy.pi / match[x1])
    elif function_type in [sympy.tan, sympy.cot]:
        period = abs(sympy.pi / match[x1])

    domain_middle = random.choice([sympy.pi/2 * i for i in range(-2, 3)])
    if function_type in [sympy.cos, sympy.sin]:
        domain_length = random.choice([1, 2]) * period
    elif function_type in [sympy.tan, sympy.cot]:
        domain_length = period

    domain = sympy.Interval(domain_middle - domain_length/2, domain_middle + domain_length/2, False, False)

    k = sympy.Symbol('k')
    if function_type == sympy.tan:
        match = trig_function.match(x0 * function_type(x1) + x2)
        interior = match[x1]

        base_asymptote = sympy.solve(interior - sympy.pi/2)[0]

        asymptotes = base_asymptote + k * period

        domain = domain_remove_asymptotes(domain, asymptotes)
    elif function_type == sympy.cot:
        match = trig_function.match(x0 * function_type(x1) + x2)
        interior = match[x1]

        base_asymptote = sympy.solve(interior)[0]

        asymptotes = base_asymptote + k * period

        domain = domain_remove_asymptotes(domain, asymptotes)


    return domain


def domain_remove_asymptotes(interval, asymptotes_general_equation):
    if interval.is_left_unbounded:
        raise ValueError('The interval given is left-unbounded')
    elif interval.is_right_unbounded:
        raise ValueError('The interval given is right-unbounded')

    x0, x1 = sympy.Wild('x0'), sympy.Wild('x1')
    match = asymptotes_general_equation.match(x0*k + x1)

    # solving inequalities over integer symbols is not yet implemented in SymPy. We need to use a workaround
    # we transform the interval by doing (interval - x1)/x0, then finding integer values in this range, then transforming back by
    # doing (integers * x0) + x1 to give us all the asymptotes in the interval
    intermediate_interval = sympy.Interval((interval.left - match[x1]) / match[x0], (interval.right - match[x1]) / match[x0], False, False)

    # for the left bound, if it is not an integer we must round towards the middle of the interval (i.e. up)
    # likewise, we must round the right bound towards the middle of the interval (i.e. down)
    if isinstance(intermediate_interval.left, sympy.Integer):
        left_bound = intermediate_interval.left
    elif isinstance(intermediate_interval.left, sympy.Rational):
        left_bound = int(math.floor(intermediate_interval.left)) + 1

    if isinstance(intermediate_interval.right, sympy.Integer):
        right_bound = intermediate_interval.right
    elif isinstance(intermediate_interval.right, sympy.Rational):
        right_bound = int(math.floor(intermediate_interval.right))

    untransformed_asymptotes = range(left_bound, right_bound + 1)
    asymptotes = [i * match[x0] + match[x1] for i in untransformed_asymptotes]

    # now we have the original interval, as well as all asymptotes that we need to exclude - let's make the
    # sympy.Interval/sympy.Union object
    exclude_left, exclude_right = False, False
    if interval.left_open & (interval.left == asymptotes[0]):  # the left of the domain is an asymptote, exclude it from the final domain
        exclude_left = True
        asymptotes.pop(0)
    elif interval.left_open:
        exclude_left = True
    if interval.right_open & len(asymptotes) > 0 & (interval.right == asymptotes[-1]):  # the right of the domain is an
                                                                                        # asymptote, exclude it from the final domain
        exclude_right = True
        asymptotes.pop(-1)
    elif interval.right_open:
        exclude_right = True

    # starting from the left of the interval, we make a union of all intervals separated by asymptotes
    domain = sympy.EmptySet()

    if len(asymptotes) > 0:
        domain += sympy.Interval(interval.left, asymptotes[0], exclude_left, True)
    else:
        domain += sympy.Interval(interval.left, interval.right, exclude_left, exclude_right)

    while len(asymptotes) > 1:
        domain += sympy.Interval(asymptotes[0], asymptotes[1], True, True)
        asymptotes.pop(0)

    if len(asymptotes) == 1:
        domain += sympy.Interval(asymptotes[0], interval.right, True, exclude_right)
    else:
        domain += sympy.Interval(domain.right, interval_right, True, exclude_right)

    return domain


class TestDomainRemoveAsymptotes:
    def test_one(self):
        test_interval = sympy.Interval(-sympy.pi, sympy.pi, False, True)
        test_asymptotes = k*sympy.pi + sympy.pi/2
        assert(domain_remove_asymptotes(test_interval, test_asymptotes) == sympy.Interval(-sympy.pi, -sympy.pi/2, False, True) +
               sympy.Interval(-sympy.pi/2, sympy.pi/2, True, True) + sympy.Interval(sympy.pi/2, sympy.pi, True, True))

    def test_two(self):
        test_interval = sympy.Interval(-sympy.pi, sympy.pi, True, False)
        test_asymptotes = k*sympy.pi + sympy.pi/2
        assert(domain_remove_asymptotes(test_interval, test_asymptotes) == sympy.Interval(-sympy.pi, -sympy.pi/2, True, True) +
               sympy.Interval(-sympy.pi/2, sympy.pi/2, True, True) + sympy.Interval(sympy.pi/2, sympy.pi, True, False))