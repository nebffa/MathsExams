import sympy
from maths.symbols import *

def integral(lb, ub, expr, var=x):
    return r'\displaystyle\int^{%s}_{%s} %s\ d%s' % (ub, lb, sympy.latex(expr), sympy.latex(var))


def integral_intermediate(lb, ub, expr):
    return r'\left[%s\right]^{%s}_{%s}' % (sympy.latex(expr), ub, lb)


def integral_intermediate_eval(lb, ub, expr, var=x):
    left = expr.subs({var: ub})
    right = expr.subs({var: lb})

    if right.could_extract_minus_sign():
        return r'\left[%s - (%s)\right]' % (sympy.latex(left), sympy.latex(right))
    else:
        return r'\left[%s - %s\right]' % (sympy.latex(left), sympy.latex(right))


def discrete_expectation_x_squared(prob_table):
    # prob_table will come in the form of a dict
    return ' + '.join(['%s^2 * %s' % (k, v) for k, v in prob_table.iteritems()])


def discrete_expectation_x(prob_table):
    # prob_table will come in the form of a dict
    return ' + '.join(['%s * %s' % (k, v) for k, v in prob_table.iteritems()])
