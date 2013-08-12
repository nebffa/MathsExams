import random
import sympy
from sympy.abc import *
from maths import not_named_yet

coefficients_bound = 5


def request_linear(difficulty):
    return Linear(difficulty)


class Linear(object):
    """ Return a linear polynomial in one variable.

    Keyword arguments:
    difficulty: influences the type of equation generated

        y = Linear(1) -- y = m*x
        y = Linear(2) -- y = x + c
        y = Linear(3) -- y = m*x + c

    Public attributes:
    equation -- the actual equation of the polynomial
    domain -- which is always the reals for a line
    range -- which is always the reals for a line

    """

    def __init__(self, difficulty):

        if difficulty == 1:
            c = 0
            m = random.randint(-coefficients_bound + 2, coefficients_bound - 4)
            if m >= 0:  # make sure m is not 0 or 1
                m += 2
        elif difficulty == 2:
            c = not_named_yet.randint_no_zero(-coefficients_bound, coefficients_bound)
            m = 1
        elif difficulty == 3:
            c = not_named_yet.randint_no_zero(-coefficients_bound, coefficients_bound)
            m = random.randint(-coefficients_bound + 2, coefficients_bound - 4)
            if m >= 0:  # make sure m is not 0 or 1
                m += 2
        else:
            raise ValueError('You have supplied an invalid difficulty level! Choose between 1, 2 or 3.')

        self.equation = m * x + c
        self.domain = sympy.Interval(-sympy.oo, sympy.oo, True, True)
        self.range = sympy.Interval(-sympy.oo, sympy.oo, True, True)


class SimultaneousLinearEquations(object):
    global coefficients_bound

    def __init__(self):
        while True:
            equations = []
            x, y, k = sympy.symbols('x, y, k')
            coefficients = [[], []]

            small_domain = [i for i in range(-coefficients_bound + 2, coefficients_bound - 1) if i != 0]
            large_domain = [i for i in range(-2 * coefficients_bound, 2 * coefficients_bound) if i != 0]
            coefficients[0].append((random.sample(small_domain, 1)[0] * k + random.sample(large_domain, 1)[0]) * x)
            coefficients[0].append((random.sample(small_domain, 1)[0] * k + random.sample(large_domain, 1)[0]) * y)
            coefficients[0].append((random.sample(small_domain, 1)[0] * k + random.sample(large_domain, 1)[0]))
            coefficients[1].append(random.sample(large_domain, 1)[0] * x)
            coefficients[1].append(random.sample(large_domain, 1)[0] * y)
            coefficients[1].append(random.sample(large_domain, 1)[0])
            choices = [0, 1, 2]

            equations_layout = {choices.pop(random.randint(0, 2)): 0, choices.pop(random.randint(0, 1)): 0, choices[0]: 1}
            equations = [[coefficients[equations_layout[i]][i] for i in equations_layout],
                        [coefficients[1 - equations_layout[i]][i] for i in equations_layout]]

            gradients = [sympy.simplify(-equations[0][0].as_coefficient(x) / equations[0][1].as_coefficient(y)),
                         sympy.simplify(-equations[1][0].as_coefficient(x) / equations[1][1].as_coefficient(y))]

            parallel = sympy.solve(gradients[0] - gradients[1], k)

            if len(parallel) == 1 and coefficients[0][0] != coefficients[1][0] and coefficients[0][0] != -coefficients[1][0]:
                break

        infinite_solutions = random.randint(0, 1)
        if infinite_solutions == 1:
            equations_fixed = [[i.subs({k: parallel[0]}) if type(i) != int else i for i in equations[0]],
                               [i.subs({k: parallel[0]}) if type(i) != int else i for i in equations[1]]]

            ratio = equations_fixed[0][0] / equations_fixed[1][0]
            equations[1][2] += (equations_fixed[0][2] - ratio * equations_fixed[1][2]) / ratio

            self.k_parallel_or_infinite = parallel
