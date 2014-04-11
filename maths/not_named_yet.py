import random
import sympy
from sympy.abc import *


def randint_no_zero(low, high):
    return randint(low, high, exclude=[0])


def randint(low, high, exclude=[]):
    """ Return a number in the range (low, high), except for the numbers in exclude.
    """

    nums = list(range(low, high + 1))

    for num in exclude:
        nums.remove(num)

    return random.choice(nums)


def add_log_abs(function):
    return function.replace(sympy.log(a), sympy.log(sympy.Abs(a)))


def remove_log_abs(function):
    return function.replace(sympy.Abs(a), a)


def partition(number, include_zero=False):
    if include_zero:
        base = 0
    else:
        base = 1

    answer = set()
    answer.add((number, ))
    for x in range(base, number):
        for y in partition(number - x):
            answer.add(tuple(sorted((x, ) + y)))
    return answer


def soft_logcombine(expr):
    """Implemented a 'softer' version of sympy.logcombine.

    The difference:
        y = log(4)/2 - log(2)/2
        sympy.logcombine(y) will give log(sqrt(2))
        soft_logcombine(y) will give log(2)/2

    i.e. it will preserve the denominator

    >>> soft_logcombine(sympy.log(4)/2 - sympy.log(2)/2)
    log(2)/2
    """

    if len(expr.find(sympy.log)) > 2:
        raise NotImplementedError('soft_logcombine only works on an expression with 2 logs or less')

    elif len(expr.find(sympy.log)) == 2:  # there is more than one log
        logs = expr.find(sympy.log)

        left_log = logs.pop()
        left_inside = left_log.args[0]

        right_log = logs.pop()
        right_inside = right_log.args[0]

        denominator = expr.args[0].args[0].q

        # the denominator of the first log
        if expr.coeff(left_log).could_extract_minus_sign():
            left_inside = 1 / left_inside
        # the denominator of the second log
        if expr.coeff(right_log).could_extract_minus_sign():
            right_inside = 1 / right_inside

        expr = sympy.log(left_inside * right_inside, evaluate=False) / denominator

    return expr
