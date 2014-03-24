import sympy
import random
from ..symbols import *
import math
import itertools


MAX_INPUT = 5
MAX_OUTPUT = 30


def integral_domain(expr, domain):
    ''' Return a sensible domain to integrate a function over.
    '''

    return sorted(_delegate(expr, domain, num=2))


def derivative(expr, domain):
    deriv = expr.diff()

    return _delegate(deriv, domain)


def antiderivative(expr, domain):
    antideriv = expr.integrate()

    return _delegate(antideriv, domain)


def standard(expr, domain):
    return _delegate(expr, domain)


def conditional_integral(expr, domain):
    ''' Return two points within the domain (excluding the end-points) on which to perform a conditional integral from one side of the domain.
    '''

    modified_domain = sympy.Interval(domain.left, domain.right, True, True)

    return _delegate(expr, modified_domain, num=2)





def _delegate(expr, domain, num=1):
    trigs = (sympy.sin, sympy.cos, sympy.tan, sympy.cot, sympy.sec, sympy.csc)

    for trig in trigs:
        if expr.find(trig):
            return _trig(expr, domain, num)

    if expr.find(sympy.log):
        return _log(expr, domain, num)

    if expr.find(sympy.exp):
        return _exp(expr, domain, num)

    return _polynomial(expr, domain, num)        


def looks_good(value):
    if not sympy.ask(sympy.Q.real(value)):
        return False

    if isinstance(value, sympy.Rational):
        if not (-MAX_OUTPUT < value.p < MAX_OUTPUT):
            return False

        elif not (-MAX_OUTPUT < value.q < MAX_OUTPUT):
            return False

        return True

    elif isinstance(value, (sympy.Integer, int)):
        return True if -MAX_OUTPUT < value < MAX_OUTPUT else False






def _polynomial(expr, domain, num=1):
    points = set()

    for denom in range(1, MAX_INPUT + 1):
        for numerator in range(-MAX_INPUT, MAX_INPUT + 1):
            frac = sympy.Rational(numerator, denom)

            if frac not in points:
                points.add(frac)

    good_choices = []
    for point in points:

        if point not in domain:
            continue

        evaluated_expr = expr.subs({x: point})

        if looks_good(evaluated_expr):
            good_choices.append(point)


    return random.sample(good_choices, num)

    
def _trig(expr, domain, num=1):
    inner_function = [particle.func for particle in expr.atoms(sympy.Function)][0]
    function = list(expr.atoms(sympy.Function))[0].replace(inner_function(x0), x0)

    # we have a domain: lower_bound <= x <= upper_bound
    # we want the modified domain: f(lower_bound) <= x <= f(upper_bound)

    modified_lower_bound = function.subs(x, domain.left)
    modified_upper_bound = function.subs(x, domain.right)

    value = modified_lower_bound + (int(math.ceil(modified_lower_bound / (sympy.pi / 6))) - modified_lower_bound / (sympy.pi / 6)) * sympy.pi / 6
    values = []
    while True:
        if value <= modified_upper_bound:
            values.append(value)
        else:
            break
        value += sympy.pi / 6

    good_choices = [sympy.solve(function - test_value)[0] for test_value in values]
    good_choices = sorted([i for i in good_choices if i in domain])

    return random.sample(good_choices, num)


def _exp(expr, domain, num=1):
    exp_interior = expr.find(sympy.exp).pop().args[0]

    return _polynomial(exp_interior, domain, num)    


def _log(expr, domain, num=1):
    log_interior = expr.find(sympy.log).pop().args[0]

    # for now, let's trial this range of powers of "e". 
    # the main thing is - we can't just take a log and find all powers of "e" that can be found within a domain.
    # e.g. find all powers of "e" within a domain of (0, 1) for log(x). There are infinite such powers 
    # e^-1, e^-2, ..., e^-k, ...  all of which are between 0 and 1, so we must restrict this domain
    viable_solutions = [sympy.E**i for i in range(-5, 6)]

    solutions = [sympy.solve(log_interior - i) for i in viable_solutions]

    # now flatten the solutions
    solutions = list(itertools.chain(*solutions))

    return random.sample(solutions, num)
