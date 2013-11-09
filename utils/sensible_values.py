import sympy
import random
from maths.symbols import *
import math


MAX_INPUT = 5
MAX_OUTPUT = 30


def derivative(expr, domain):
    deriv = expr.diff()

    return _delegate(deriv, domain)


def antiderivative(expr, domain):
    antideriv = expr.integrate()

    return _delegate(antideriv, domain)


def standard(expr, domain):
    return _delegate(expr, domain)


def conditional_integral(expr, domain):
    '''    Return two points within the domain (excluding the end-points) on which to perform a conditional integral from one side of the domain.
    '''

    modified_domain = sympy.Interval(domain.left, domain.right, True, True)

    return _delegate(expr, modified_domain, num=2)





def _delegate(expr, domain, num=1):
    trigs = (sympy.sin, sympy.cos, sympy.tan, sympy.cot, sympy.sec, sympy.csc)

    for trig in trigs:
        if expr.find(trig):
            return _trig(expr, domain, num)

    if expr.find(sympy.log):
        pass

    if expr.find(sympy.exp):
        pass

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
    pass


def _log(expr, domain, num=1):
    pass
