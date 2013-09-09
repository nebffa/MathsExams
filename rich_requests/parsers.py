import re
import sympy
import functions

discretes = (int, sympy.Rational)



def parse_absolute_value_args(**kwargs):
    spec = {
        'turning_points':           {
                                'x': None,  # could be int, sympy.Rational, or a relation
                                'y': None   # could be int, sympy.Rational, or a relation
                            },

        'gradient': None,      # could be int, sympy.Rational, or a relation
        'direction': None      # could be -1 or 1, maybe 'positive', 'negative', 'up', 'down'?
    }

    # regular expressions
    TPx = r'[(tp)(ep)][_ ]*x[_ ]*'
    TPy = r'[(tp)(ep)][_ ]*y[_ ]*'
    gradient = r'grad'
    direction = r'direction'

    for key, value in kwargs.items():
        if not isinstance(value, (discretes, sympy.Interval)):
            raise ValueError('The supplied value: {0} is not a valid specifier.'.format(value))

        key = key.lower()
        if re.search(TPx, key):
            spec['turning_points']['x'] = value
        elif re.search(TPy, key):
            spec['turning_points']['y'] = value
        elif re.search(gradient, key):
            spec['gradient'] = value
        elif re.search(direction, key):
            spec['direction'] = value
        else:
            raise KeyError('The supplied keyword argument: {0} could not be parsed.'.format(key))

    return spec


def parse_cubic_args(**kwargs):
    spec = {
        'turning_points':            {
                                'n': None,
                                'locations': None
                            },

        'inflexion_points':          {
                                'locations': None
                            },

        'x_intercepts':             {
                                'n': None,
                                'locations': None,
                            },

        'y_intercept': None,
        'direction': None,  # could be -1 or 1, maybe 'positive', 'negative', 'up', 'down'?
    }

    # regular expressions
    TURNING_POINT = r'tp'
    INFLEXION_POINT = r'inflex'
    DIRECTION = r'dir'
    Y_INT = r'y[ _]int'
    X_INTS = r'x[ _]int'
    NUM = r'num'

    for key, value in kwargs.items():
        if not isinstance(value, (discretes, sympy.Interval)):
            raise ValueError('The supplied value: {0} is not a valid specifier.'.format(value))

        key = key.lower()
        if re.search(TURNING_POINT, key) and re.search(NUM, key):
            spec['turning_points']['n'] = value
        elif re.search(TURNING_POINT, key):
            spec['turning_points']['locations'] = value
        elif re.search(INFLEXION_POINT, key):
            spec['inflexion_points']['locations'] = value
        elif re.search(X_INTS, key) and re.search(NUM, key):
            spec['x_intercepts']['n'] = value
        elif re.search(X_INTS, key):
            spec['x_intercepts']['locations'] = value
        elif re.search(Y_INT, key):
            spec['y_intercept'] = value
        elif re.search(DIRECTION, key):
            spec['direction'] = value
        else:
            raise KeyError('The supplied keyword argument: {0} could not be parsed.'.format(key))

    return spec

x = parse_cubic_args(tp_num=2, tp=sympy.Interval(-1, sympy.oo, False, True))
y = functions.cubic(x)

#print(y)
#print([i for i in sympy.solve(y) if sympy.ask(sympy.Q.real(i))])
print([i for i in sympy.solve(y.diff())])