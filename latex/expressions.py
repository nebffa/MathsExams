import sympy
from maths.symbols import *


def integral(lb, ub, expr, var=x):
    return r'\displaystyle\int^{{{0}}}_{{{1}}} {2}\ d{3}'.format(ub, lb, sympy.latex(expr), sympy.latex(var))


def integral_intermediate(lb, ub, expr):
    return r'\left[{0}\right]^{{{1}}}_{{{2}}}'.format(sympy.latex(expr), ub, lb)


def integral_intermediate_eval(lb, ub, expr, var=x):
    left = expr.subs({var: ub})
    right = expr.subs({var: lb})

    if right.could_extract_minus_sign():
        return r'\left[{0} - ({1})\right]'.format(sympy.latex(left), sympy.latex(right))
    else:
        return r'\left[{0} - {1}\right]'.format(sympy.latex(left), sympy.latex(right))


def discrete_expectation_x_squared(prob_table):
    # prob_table will come in the form of a dict
    return ' + '.join([r'{0}^2 \times {1}'.format(k, sympy.latex(v)) for k, v in prob_table.items()])


def discrete_expectation_x(prob_table):
    # prob_table will come in the form of a dict
    return ' + '.join([r'{0} \times {1}'.format(k, sympy.latex(v)) for k, v in prob_table.items()])

def quadratic_formula(quadratic, var=x):
    match = quadratic.match(x0*var**2 + x1*var + x2)

    a = r'({0})'.format(sympy.latex(match[x0])) if match[x0].could_extract_minus_sign() else sympy.latex(match[x0])
    b = r'({0})'.format(sympy.latex(match[x1])) if match[x1].could_extract_minus_sign() else sympy.latex(match[x1])
    c = r'({0})'.format(sympy.latex(match[x2])) if match[x2].could_extract_minus_sign() else sympy.latex(match[x2])

    return r'\dfrac{{-{1} \pm \sqrt{{{1}^2 - 4 \times {0} \times {2}}}}}{{2 \times{0}}}'.format(a, b, c)

