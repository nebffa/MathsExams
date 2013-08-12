from maths.latex import expressions
from maths.symbols import *


def test_integral():
    assert expressions.integral(0, 1, x) == r'\displaystyle\int^{1}_{0} x\ dx'
    assert expressions.integral(0, 1, x, var=y) == r'\displaystyle\int^{1}_{0} x\ dy'
    

def test_integral_intermediate():
    assert expressions.integral_intermediate(0, 1, x) == r'\left[x\right]^{1}_{0}'


def test_integral_intermediate_eval():
    assert expressions.integral_intermediate_eval(0, 1, x) == r'\left[1 - 0\right]'
    assert expressions.integral_intermediate_eval(1, 2, -x) == r'\left[-2 - (-1)\right]'
