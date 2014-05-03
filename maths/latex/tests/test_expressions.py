from .. import expressions
from ...symbols import *


def test_integral():
    assert expressions.integral(0, 1, x) == r'\displaystyle\int^{1}_{0} x\ dx'
    assert expressions.integral(0, 1, x, var=y) == r'\displaystyle\int^{1}_{0} x\ dy'


def test_integral_intermediate():
    assert expressions.integral_intermediate(0, 1, x) == r'\left[\frac{x^{2}}{2}\right]^{1}_{0}'


def test_integral_intermediate_eval():
    assert expressions.integral_intermediate_eval(0, 1, x) == r'\frac{1}{2} - 0'
    assert expressions.integral_intermediate_eval(1, 2, -x ** 2) == r'- \frac{8}{3} - (- \frac{1}{3})'


def test_sum_combination_probabilities():
    assert expressions.sum_combination_probabilities([[2, 5, 6], [3, 4, 6]]) == \
        r'3! \times Pr(ball_1 = 2 \cap ball_2 = 5 \cap ball_3 = 6) + 3! \times Pr(ball_1 = 3 \cap ball_2 = 4 \cap ball_3 = 6)'


def test_sum_permutation_probabilities():
    assert expressions.sum_permutation_probabilities([[2, 5, 6], [5, 2, 6]]) == \
        r'Pr(ball_1 = 2 \cap ball_2 = 5 \cap ball_3 = 6) + Pr(ball_1 = 5 \cap ball_2 = 2 \cap ball_3 = 6)'
