from maths.utils import transformations
from maths.symbols import *
import sympy

NUM_RANDOM_TESTS = 10

def test_translation():
    assert transformations.translation().shape == (2, 1)

    for i in range(NUM_RANDOM_TESTS):
        transf = transformations.translation(direction_of_change='x')
        assert transf[0] != 0
        assert transf[1] == 0

        transf = transformations.translation(direction_of_change='y')
        assert transf[0] == 0
        assert transf[1] != 0


def test_dilation():
    assert transformations.dilation().shape == (2, 2)

    for i in range(NUM_RANDOM_TESTS):
        dilation = transformations.dilation(direction_of_change='x')
        assert dilation[0] not in [0, 1]
        assert dilation[3] == 1

        dilation = transformations.dilation(direction_of_change='y')
        assert dilation[0] == 1
        assert dilation[3] not in [0, 1]



def test_reflection():
    assert transformations.reflection().shape == (2, 2)

    dilation = transformations.reflection(direction_of_change='x')
    assert dilation[0] == -1
    assert dilation[3] == 1

    dilation = transformations.reflection(direction_of_change='y')
    assert dilation[0] == 1
    assert dilation[3] == -1


def test_overall_transformation():
    transf = sympy.Matrix([[1, 2], [3, 4]])
    transf_2 = sympy.Matrix([[2, 3], [4, 5]])
    translation = transformations.translation()
    coords = sympy.Matrix([[x], [y]])

    assert transformations.overall_transformation([transf, transf_2]) == transf_2 * transf * coords
    assert transformations.overall_transformation([transf, transf_2, translation]) == transf_2 * transf * coords + translation


def test_apply_transformation():
    transl_x_positive = [sympy.Matrix([[2], [0]])]
    transl_x_negative = [sympy.Matrix([[-2], [0]])]
    transl_y_positive = [sympy.Matrix([[0], [2]])]
    transl_y_negative = [sympy.Matrix([[0], [-2]])]

    assert transformations.apply_transformations(transl_x_positive, x**2) == (x - 2)**2
    assert transformations.apply_transformations(transl_x_negative, x**2) == (x + 2)**2
    assert transformations.apply_transformations(transl_y_positive, x**2) == x**2 + 2
    assert transformations.apply_transformations(transl_y_negative, x**2) == x**2 - 2

    dilation_x_away = [sympy.Matrix([[2, 0], [0, 1]])]
    dilation_x_towards = [sympy.Matrix([[sympy.Rational(1, 2), 0], [0, 1]])]
    dilation_y_away = [sympy.Matrix([[1, 0], [0, 2]])]
    dilation_y_towards = [sympy.Matrix([[1, 0], [0, sympy.Rational(1, 2)]])]

    assert transformations.apply_transformations(dilation_x_away, x**2) == x**2/4
    assert transformations.apply_transformations(dilation_x_towards, x**2) == 4*x**2
    assert transformations.apply_transformations(dilation_y_away, x**2) == 2*x**2
    assert transformations.apply_transformations(dilation_y_towards, x**2) == (x**2)/2

    reflection_x = [sympy.Matrix([[-1, 0], [0, 1]])]
    reflection_y = [sympy.Matrix([[1, 0], [0, -1]])]

    assert transformations.apply_transformations(reflection_x, x**2) == x**2
    assert transformations.apply_transformations(reflection_y, x**3) == -x**3


def test_reverse_mapping():
    transl_only_mapping = sympy.Matrix([[x - 1], [y - 1]])
    dil_only_mapping = sympy.Matrix([[x/2], [y/2]])
    both_mapping = sympy.Matrix([[(x - 1)/2], [(y -1)/2]])

    assert transformations.reverse_mapping(transl_only_mapping) == sympy.Matrix([[x + 1], [y + 1]])
    assert transformations.reverse_mapping(dil_only_mapping) == sympy.Matrix([[2*x], [2*y]])
    assert transformations.reverse_mapping(both_mapping) == sympy.Matrix([[2*x + 1], [2*y + 1]])
