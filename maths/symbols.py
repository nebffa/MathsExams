import sympy

x, y, z = sympy.symbols('x y z')
a, b, c, d, e = sympy.symbols('a b c d e')

x0 = sympy.Wild('x0')
x1 = sympy.Wild('x1')
x2 = sympy.Wild('x2')
x3 = sympy.Wild('x3')
x4 = sympy.Wild('x4')
x5 = sympy.Wild('x5')
x6 = sympy.Wild('x6')
x7 = sympy.Wild('x7')
x8 = sympy.Wild('x8')
x9 = sympy.Wild('x9')

# the exclude is used to prevent unusual matching
# without it, (x**2 - 2).match(x0*x**2 + x1*x + x2) will give {x0: 1, x1: -2/x, x2: 0}
# https://github.com/sympy/sympy/wiki/Idioms-and-Antipatterns
coeff0 = sympy.Wild('coeff0', exclude=[x])
coeff1 = sympy.Wild('coeff1', exclude=[x])
coeff2 = sympy.Wild('coeff2', exclude=[x])
coeff3 = sympy.Wild('coeff3', exclude=[x])
coeff4 = sympy.Wild('coeff4', exclude=[x])
coeff5 = sympy.Wild('coeff5', exclude=[x])

k = sympy.Symbol('k')
