import sympy


def substitute(expr, var, value):
    latex = sympy.latex(expr)

    latex = latex.replace(str(var), sympy.latex(value))

    return latex


def integral_working(expr, var, l, h):
    left = substitute(expr, var, h)  # upper bound goes on the left
    right = substitute(expr, var, l)  # lower bound goes on the right

    return '\left(' + left + r'\right)' + ' - ' + '\left(' + right + r'\right)'
