import sympy
import random
import itertools
import operator


def expectation_x(prob_table, power=1):
    ''' Return the expectation of X to a certain power.

    By default, the mean of X is returned, but higher order expectations can be specified using power.'''

    return sum([k**power*v for k, v in prob_table.iteritems()])


def mode(prob_table):
    ''' Return the mode of the probability table'''
    mode_key = max(prob_table.iterkeys(), key=lambda key: prob_table[key])

    if len([v for v in prob_table.itervalues() if v == prob_table[mode_key]]) > 1:
        # ensure there is only one mode
        make_one_mode(prob_table)

    return mode_key


def make_one_mode(prob_table):
    mode = max(prob_table.itervalues())

    max_keys = [k for k, v in prob_table.iteritems() if v == mode]

    designated_mode_key = random.choice(max_keys)

    for key in max_keys:
        if key != designated_mode_key:
            prob_table[key] -= 0.05
            prob_table[designated_mode_key] += 0.05


def prob_sum(prob_table, total, n_trials):
    ''' Return Pr(X1 + X2 + ... X(n_trials) == total). '''

    valid_perms = valid_permutations(prob_table, total, n_trials)
    probability = 0
    for perm in valid_perms:
        probability += reduce(operator.mul, [prob_table[i] for i in perm])

    return probability


def valid_permutations(prob_table, total, n_trials):
    permutations = itertools.product(prob_table, repeat=n_trials)

    valid_perms = []
    for perm in permutations:
        if sum(perm) == total:
            valid_perms.append(perm)

    return valid_perms
