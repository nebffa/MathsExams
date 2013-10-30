import sympy
from maths.symbols import *
from maths.latex import latex
from maths.utils import functions


def integral(lb, ub, expr, var=x):
    if expr.has(sympy.log):
        expr = expr.replace(sympy.log(x0), sympy.log(x0, evaluate=False))


    return r'\displaystyle\int^{{{0}}}_{{{1}}} {2}\ d{3}'.format(sympy.latex(ub), sympy.latex(lb), sympy.latex(expr), sympy.latex(var))


def integral_intermediate(lb, ub, expr, var=x):
    antideriv = expr.integrate(var)

    if antideriv.has(sympy.log):
        antideriv = antideriv.replace(sympy.log(x0), sympy.log(x0, evaluate=False))

    return r'\left[{0}\right]^{{{1}}}_{{{2}}}'.format(sympy.latex(antideriv), sympy.latex(ub), sympy.latex(lb))


def integral_intermediate_eval(lb, ub, expr, var=x):
    antideriv = expr.integrate(var)

    if antideriv.has(sympy.log):
        antideriv = antideriv.replace(sympy.log(x0), sympy.log(x0, evaluate=False))
    
    left = antideriv.subs({var: ub})
    right = antideriv.subs({var: lb})

    if right.could_extract_minus_sign():
        return r'{0} - ({1})'.format(sympy.latex(left), sympy.latex(right))
    else:
        return r'{0} - {1}'.format(sympy.latex(left), sympy.latex(right))


def piecewise(func):
    ''' 
    Return LaTeX for a piecewise expression. In this case, SymPy's ability to produce good-looking LaTeX is lackluster.
    '''

    
    line_begin = '\n' + r'\begin{cases}' + '\n'
    line_end = r'\end{cases}' + '\n'

    lines = []
    for expr in func.args:
        if isinstance(expr[1], (sympy.StrictLessThan, sympy.LessThan, sympy.StrictGreaterThan, sympy.GreaterThan, sympy.And, sympy.Or)):
            interval = sympy.latex( functions.relation_to_interval(expr[1]) )
            lines.append('\t' + r'{0} & \text{{for}}\: {1} \in {2}'.format(sympy.latex(expr[0]), func.free_symbols.pop(), interval) + '\n')
        else:
            lines.append('\t' + r'{0} & \: \text{{otherwise}}'.format(sympy.latex(expr[0])) + '\n')

        
        lines.append(latex.latex_newline())

    return line_begin + ''.join(lines) + line_end


    # $\begin{cases}
    #        - \frac{x^{3}}{4} - \frac{15 x^{2}}{4} - 18 x - 29 & \text{for}\: x < 0 
    # \\
    #       -2 - \frac{2}{x - 3} & \text{for}\: x \geq 0 
    # \end{cases}$


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


def conditional_probability(givee, given):
    return r'\frac{{ Pr({0} \cap {1}) }}{{ Pr({1}) }}'.format(givee, given)
