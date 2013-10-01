import random
from sympy.abc import *
import sympy
import functools
import operator


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







