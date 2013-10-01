import sympy
import random
from sympy.abc import *
from maths import not_named_yet
import textwrap
from maths.latex import latex


def translation(lb=-5, ub=5, axis=None):
    amount = not_named_yet.randint(lb, ub, exclude=[0])
    
    if axis is None:
        axis = random.choice(['x', 'y'])

    return [{'type': 'translation', 'axis': axis, 'amount': amount}]


def dilation(lb=-3, ub=3, axis=None):
    amount = not_named_yet.randint(lb, ub, exclude=[-1, 0, 1])

    if random.choice([True, False]):
        amount = sympy.Rational(1, amount)

    if axis is None:
        axis = random.choice(['x', 'y'])

    if amount < 0:
        transfs = [{'type': 'dilation', 'axis': axis, 'amount': abs(amount)}, {'type': 'reflection', 'axis': axis}]
        random.shuffle(transfs)
        return transfs
    else:
        return [{'type': 'dilation', 'axis': axis, 'amount': amount}]
    


def reflection(axis=None):
    axis = random.choice(['x', 'y'])
    return [{'type': 'reflection', 'axis': axis}]



def overall_transformation(transformations):
    ''' Condense a list of transformations into one combined transformation.
    '''
    coords = (x, y)

    for transf in transformations:
        coords = _reduce_transformation(transf, coords)

    return coords


def _reduce_transformation(transformation, coords):
    coords = list(coords)
    if transformation['axis'] == 'x':
        tuple_index = 0
    else:
        tuple_index = 1

    if transformation['type'] == 'translation':
        coords[tuple_index] += transformation['amount']
    elif transformation['type'] == 'dilation':
        coords[tuple_index] *= transformation['amount']
    elif transformation['type'] == 'reflection':
        coords[tuple_index] *= -1
    else:
        raise KeyError('this transformation is not supported: {0}'.format(transformation['type']))

    return tuple(coords)


def apply_transformations(transformations, thing):
    ''' Transform a point or an expression according to a list of transformations.
    '''

    transf = overall_transformation(transformations)

    if isinstance(thing, tuple):  # it's a set of coordinates
        return ( transf[0].subs({x: thing[0]}), transf[1].subs({y: thing[1]}) )
    else:  # it's an expression
        reversed_transf = _reverse_mapping(transf)

        solve_friendly_expr = -y + thing
        transformed = solve_friendly_expr.subs({x: reversed_transf[0], y: reversed_transf[1]})
        return sympy.solve(transformed, y)[0]


def _print_transformation(transformation):
    if transformation['type'] == 'reflection':
        if transformation['axis'] == 'x':
            axis = 'y'
        else:
            axis = 'x'

        return r'reflection in the {0}-axis'.format(axis)

    elif transformation['type'] == 'dilation':
        if transformation['axis'] == 'x':
            axis = 'y'
        else:
            axis = 'x'

        return r'dilation of factor ${0}$ from the {1}-axis'.format(sympy.latex(transformation['amount']), axis)            

    elif transformation['type'] == 'translation':
        direction = 'positive' if (transformation['amount'] > 0) else 'negative'

        return r'translation of ${0}$ in the {1} direction of the {2}-axis'.format(
                    sympy.latex(abs(transformation['amount'])), direction, transformation['axis'])



def print_transformations(transformations):
    strings = map(_print_transformation, transformations)
    return r''' under a ''' + ', followed by a '.join(strings)


def show_mapping(transformations):
    mapping = '(x, y)'

    coords = (x, y)
    for transf in transformations:
        mapped_coords = _reduce_transformation(transf, coords)
        coords = mapped_coords

        mapping += r' \rightarrow ({0}, {1})'.format(sympy.latex(mapped_coords[0]), sympy.latex(mapped_coords[1]))
        

    return mapping


def _reverse_mapping(mapping):

    maps = []
    temp = sympy.Symbol('temp')
    for each in mapping:
        symbol_used = each.free_symbols.pop()

        the_map = sympy.solve(each - temp, symbol_used)[0]
        maps.append(the_map.replace(temp, symbol_used))

    return tuple(maps)



def random_transformation(num_transformations):
    if num_transformations == 2:
        return random.choice([
            translation() + dilation(),
            dilation() + translation()
        ])    
    else:
        raise KeyError(r'Generation of this many (number = {0}) transformations is not supported'.format(num_transformations))