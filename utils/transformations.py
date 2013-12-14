import sympy
import random
from sympy.abc import *
from maths import not_named_yet
import textwrap
from maths.latex import latex


def translation(lb=-5, ub=5, direction_of_change=None):
    amount = not_named_yet.randint(lb, ub, exclude=[0])
    
    if direction_of_change is None:
        direction_of_change = random.choice(['x', 'y'])

    matrix = sympy.zeros(2, 1)
    if direction_of_change == 'x':
        matrix[0] = amount
    else:
        matrix[1] = amount

    return matrix


def dilation(ub=3, direction_of_change=None):
    amount = not_named_yet.randint(2, ub)

    if random.choice([True, False]):
        amount = sympy.Rational(1, amount)

    if direction_of_change is None:
        direction_of_change = random.choice(['x', 'y'])

    matrix = sympy.eye(2)
    if direction_of_change == 'x':
        matrix[0] = amount
    else:
        matrix[3] = amount

    return matrix


def reflection(direction_of_change=None):
    direction_of_change = random.choice(['x', 'y'])

    matrix = sympy.eye(2)
    if direction_of_change == 'x':
        matrix[0] = -1
    else:
        matrix[3] = -1

    return matrix



def overall_transformation(transformations):
    ''' Condense a list of transformations into one combined transformation.
    '''

    def apply(transf, coords):
        if transf.shape == (2, 2):
            coords = transf * coords
        else:
            coords += transf
        return coords

    if isinstance(transformations, sympy.Matrix):
        return transformations
    else:
        coords = sympy.Matrix([[x], [y]])
        for transf in transformations:
            coords = apply(transf, coords)

    return coords


def _reduce_transformation(transformation, coords):
    coords = sympy.Matrix(coords)

    if transformation.shape == (2, 2):
        coords = transformation * coords
    else:
        coords += transformation

    return tuple(coords)


def apply_transformations(transformations, thing):
    ''' Transform a point or an expression according to a list of transformations.
    '''

    transf = overall_transformation(transformations)

    if isinstance(thing, tuple):  # it's a set of coordinates
        return ( transf[0].subs({x: thing[0]}), transf[1].subs({y: thing[1]}) )
    else:  # it's an expression
        solve_friendly_expr = -y + thing
        transformed = solve_friendly_expr.subs({x: transf[0], y: transf[1]})
        return sympy.solve(transformed, y)[0]


def _print_transformation(transformation):
    if transformation.shape == (2, 2):
        # reflection
        if transformation[0] == -1 or transformation[1] == -1:
            if transformation[0] == -1:  # reflection in the y-axis
                reflected_in_which_axis = 'y'
            else:  # reflection in the x-axis
                reflected_in_which_axis = 'x'

            return r'reflection in the {0}-axis'.format(reflected_in_which_axis)

        # dilation
        else:
            if transformation[0] != 0:  # dilation from the y-axis
                dilated_from_which_axis = 'y'
                amount = transformation[0]
            else:  # dilation from the x-axis
                dilated_from_which_axis = 'x'
                amount = transformation[3]


            return r'dilation of factor ${0}$ from the {1}-axis'.format(sympy.latex(amount), dilated_from_which_axis)            

    # translation
    elif transformation.shape == (2, 1):
        if transformation[0] != 0:  # translated along the x-axis
            axis = 'x'
        else:  # translated along the y-axis
            axis = 'y'
        amount = sum(transformation)
        direction = 'positive' if amount > 0 else 'negative'

        return r'translation of ${amount}$ in the {direction} direction of the {axis}-axis'.format(
                    direction=direction,
                    axis=axis,
                    amount=sympy.latex(abs(amount))
                )



def print_transformations(transformations):
    strings = map(_print_transformation, transformations)
    return r' under a ' + ', followed by a '.join(strings)


def show_mapping(transformations):
    coords = (x, y)
    mapping = sympy.latex(coords)
    
    for transf in transformations:
        mapped_coords = _reduce_transformation(transf, coords)
        coords = mapped_coords

        mapping += r' \rightarrow {0}'.format(sympy.latex(mapped_coords))
        

    return mapping


def reverse_mapping(mapping):
    maps = []
    temp = sympy.Symbol('temp')
    for each in mapping:
        symbol_used = each.free_symbols.pop()

        the_map = sympy.solve(each - temp, symbol_used)[0]
        maps.append(the_map.replace(temp, symbol_used))


    return sympy.Matrix(maps)



def random_transformation(num_transformations):
    if num_transformations == 2:
        return random.choice([
            [translation(), dilation()],
            [dilation(), translation()]
        ])
    else:
        raise KeyError(r'Generation of this many (number = {0}) transformations is not supported'.format(num_transformations))