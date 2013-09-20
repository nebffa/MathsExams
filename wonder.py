from symbols import *
from sympy import *


y = -3*exp(-3*x + 4) - 4
print(y.integrate())