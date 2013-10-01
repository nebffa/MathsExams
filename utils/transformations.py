import sympy
import random
from sympy.abc import *
from maths import not_named_yet
import textwrap


def translation(lb=-5, ub=5, axis=None):
    amount = not_named_yet.randint(lb, ub, exclude=[0])
    
    if axis is None:
        axis = random.choice(['x', 'y'])

    return {'type': 'translation', 'axis': axis, 'amount': amount}


def dilation(lb=-3, ub=3, axis=None):
    amount = not_named_yet.randint(lb, ub, exclude=[0])

    if axis is None:
        axis = random.choice(['x', 'y'])


    return {'type': 'dilation', 'axis': axis, 'amount': amount}


def reflection(axis=None):
    axis = random.choice(['x', 'y'])
    return {'type': 'reflection', 'axis': axis}



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
        coords[tuple_index] -= transformation['amount']
    elif transformation['type'] == 'dilation':
        coords[tuple_index] /= transformation['amount']
    elif transformation['type'] == 'reflection':
        coords[tuple_index] *= -1
    else:
        raise KeyError('this transformation is not supported: {0}'.format(transformation['type']))

    return tuple(coords)


def apply_transformations(transformations, thing):
    ''' Transform a point or an expression according to a list of transformations.
    '''

    transf = overall_transformation(transformation)

    if isinstance(thing, tuple):  # it's a set of coordinates
        return transf.subs({x: thing[0], y: thing[1]})
    else:  # it's an expression
        solve_friendly_expr = -y + thing
        transformed = solve_friendly_expr.subs({x: thing[0], y: thing[1]})
        return sympy.solve(transformed, y)[0]


def _print_transformation(transformation):
    if transformation['type'] == 'reflection':
        if transformation['axis'] == 'x':
            axis = 'y'
        else:
            axis = 'x'

        return r'a reflection in the {0}-axis'.format(axis)

    elif transformation['type'] == 'dilation':
        if transformation['axis'] == 'x':
            axis = 'y'
        else:
            axis = 'x'

        temp2 = r'a dilation of factor {0} from the {1}-axis'.format(transformation['amount'], axis)            
        if transformation['amount'] < 0:
            temp = r'a reflection in the {0}-axis'.format(axis)

            return ' and '.join(random.shuffle([temp, temp2]))
        else:
            return temp2

    elif transformation['type'] == 'translation':
        direction = 'positive' if (transformation['amount'] > 0) else 'negative'

        return r'a translation of {0} in the {1} direction of the {2}-axis'.format(abs(transformation['amount']), direction, transformation['axis'])



def print_transformations(transformations):
    strings = map(_print_transformation, transformations)
    return r''' under a ''' + ', followed by a'.join(strings)


def show_mapping(transformations):
    mapping = ''

    coords = (x, y)
    for transf in transformations:
        mapped_coords = _reduce_transformation(transf, coords)

        mapping += r'\item {0} \rightarrow {1}'.format(coords, mapped_coords) + '\n'
        coords = mapped_coords

    return text.wrap.dedent(r'''
    \begin{{description}}
        {0}
    \end{{description}}
    '''.format(mapping))


def random_transformation(num_transformations):
    if num_transformations == 2:
        return random.choice(
            [translation(), dilation()],
            [dilation(), translation()]
        )    
    else:
        raise KeyError(r'Generation of this many ({0}) transformations is not supported'.format(num_transformations))