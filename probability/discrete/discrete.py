import random
import sympy


def expectation_x(prob_table):
    return sum([k*v for k, v in prob_table.iteritems()])


def expectation_x_squared(prob_table):
    return sum([k**2*v for k, v in prob_table.iteritems()])


def mode(prob_table):
    return max(prob_table.iterkeys(), key=lambda key: prob_table[key])
