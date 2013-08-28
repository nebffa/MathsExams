import random
from sympy.abc import *
import sympy


def randint_no_zero(low, high):
    return randint(low, high, exclude=[0])


def randint(low, high, exclude=[]):
    nums = list(range(low, high + 1))

    for num in exclude:
        nums.remove(num)

    return random.choice(nums)


def add_log_abs(function):
    return function.replace(sympy.log(a), sympy.log(sympy.Abs(a)))


def remove_log_abs(function):
    return function.replace(sympy.Abs(a), a)


def relation_to_interval(relation):
    if relation.rel_op == '>':
        return sympy.Interval(relation.rhs, sympy.oo, True, True)
    elif relation.rel_op == '>=':
        return sympy.Interval(relation.rhs, sympy.oo, False, True)
    elif relation.rel_op == '<':
        return sympy.Interval(-sympy.oo, relation.rhs, True, True)
    elif relation.rel_op == '<=':
        return sympy.Interval(-sympy.oo, relation.rhs, True, False)


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







