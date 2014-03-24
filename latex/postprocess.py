import re
import sympy


operators = r'[+-%/*]'

def log(latex, base=sympy.E):
    latex = re.sub('log\\{\\\\left \\(([\w+-/*% ]*)\\\\right \\)\\}', r'log{\\left\\lvert {\1} \\right\\rvert }', latex)
    latex = re.sub('log{', 'log_{{{0}}}{{'.format(sympy.latex(base)), latex)

    return latex
