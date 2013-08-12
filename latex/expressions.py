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
