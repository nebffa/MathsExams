from maths.utils import transformations
from maths.symbols import *
import sympy


def test_apply_transformation():

    transl_x_positive = [{'type': 'translation', 'axis': 'x', 'amount': 2}]
    transl_x_negative = [{'type': 'translation', 'axis': 'x', 'amount': -2}]
    transl_y_positive = [{'type': 'translation', 'axis': 'y', 'amount': 2}]
    transl_y_negative = [{'type': 'translation', 'axis': 'y', 'amount': -2}]

    assert transformations.apply_transformations(transl_x_positive, x**2) == (x - 2)**2
    assert transformations.apply_transformations(transl_x_negative, x**2) == (x + 2)**2
    assert transformations.apply_transformations(transl_y_positive, x**2) == x**2 + 2
    assert transformations.apply_transformations(transl_y_negative, x**2) == x**2 - 2

    dilation_x_away = [{'type': 'dilation', 'axis': 'x', 'amount': 2}]
    dilation_x_towards = [{'type': 'dilation', 'axis': 'x', 'amount': sympy.Rational(1, 2)}]
    dilation_y_away = [{'type': 'dilation', 'axis': 'y', 'amount': 2}]
    dilation_y_towards = [{'type': 'dilation', 'axis': 'y', 'amount': sympy.Rational(1, 2)}]

    assert transformations.apply_transformations(dilation_x_away, x**2) == x**2/4
    assert transformations.apply_transformations(dilation_x_towards, x**2) == 4*x**2
    assert transformations.apply_transformations(dilation_y_away, x**2) == 2*x**2
    assert transformations.apply_transformations(dilation_y_towards, x**2) == (x**2)/2

    reflection_x = [{'type': 'reflection', 'axis': 'x'}]
    reflection_y = [{'type': 'reflection', 'axis': 'y'}]

    assert transformations.apply_transformations(reflection_x, x**2) == -x**2
    assert transformations.apply_transformations(reflection_y, x**3) == -x**3