import sympy
from .. import all_functions
from sympy.abc import *


y = sympy.exp(2*x) - 2

print all_functions.inverse(y)
