import re
import sympy

discretes = (int, sympy.Rational)


def parse_absolute_value(**kwargs):
    spec = {
        'turning_point':           {
                                'location': None,
                            },
        'x_intercepts':             {
                                'location': None,
                            },

        'gradient': None,      # could be int, sympy.Rational, or a relation
        'direction': None      # could be -1 or 1, maybe 'positive', 'negative', 'up', 'down'?
    }

    # regular expressions
    TURNING_POINT = r'[(tp)(turn)(ep)(extr)]'
    X_INTS = r'x[ _]int'
    GRADIENT = r'grad'
    DIRECTION = r'direction'

    for key, value in kwargs.items():
        if not isinstance(value, (discretes, sympy.Interval)):
            raise ValueError('The supplied value: {0} is not a valid specifier.'.format(value))

        key = key.lower()
        if re.search(TURNING_POINT, key):
            spec['turning_point']['location'] = value
        elif re.search(X_INTS, key):
            spec['x_intercepts']['location'] = value
        elif re.search(GRADIENT, key):
            spec['gradient'] = value
        elif re.search(DIRECTION, key):
            spec['direction'] = value
        else:
            raise KeyError('The supplied keyword argument: {0} could not be parsed.'.format(key))

    return spec


def parse_hyperbola(**kwargs):
    spec = {
        'h_asymptote': None,
        'v_asymptote': None,

        'x_intercepts':             {
                                'location': None,
                            },

        'direction': None
    }

    # regular expressions
    ASYMPTOTE = r'asymp'
    HORIZONTAL = r'horiz'
    VERTICAL = r'vert'
    DIRECTION = r'direction'

    for key, value in kwargs.items():
        if not isinstance(value, (discretes, sympy.Interval)):
            raise ValueError('The supplied value: {0} is not a valid specifier.'.format(value))

        key = key.lower()
        if re.search(ASYMPTOTE, key) and re.search(HORIZONTAL, key):
            spec['h_asymptote'] = value
        elif re.search(ASYMPTOTE, key) and re.search(VERTICAL, key):
            spec['v_asymptote'] = value
        elif re.search(DIRECTION, key):
            spec['direction'] = value
        else:
            raise KeyError('The supplied keyword argument: {0} could not be parsed.'.format(key))

    return spec


def parse_cubic(**kwargs):
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
    TURNING_POINT = r'[(tp)(turn)]'
    INFLEXION_POINT = r'inflex'
    DIRECTION = r'dir'
    LOCATION = r'loc'
    Y_INT = r'y[ _]int'
    X_INTS = r'x[ _]int'
    NUM = r'num'

    for key, value in kwargs.items():
        if not isinstance(value, (discretes, sympy.Interval)):
            raise ValueError('The supplied value: {0} is not a valid specifier.'.format(value))

        key = key.lower()
        if re.search(TURNING_POINT, key) and re.search(NUM, key):
            spec['turning_points']['n'] = value
        elif re.search(TURNING_POINT, key) and re.search(LOCATION, key):
            spec['turning_points']['locations'] = value
        elif re.search(INFLEXION_POINT, key) and re.search(LOCATION, key):
            spec['inflexion_points']['locations'] = value
        elif re.search(X_INTS, key) and re.search(NUM, key):
            spec['x_intercepts']['n'] = value
        elif re.search(X_INTS, key) and re.search(LOCATION, key):
            spec['x_intercepts']['locations'] = value
        elif re.search(Y_INT, key):
            spec['y_intercept'] = value
        elif re.search(DIRECTION, key):
            spec['direction'] = value
        else:
            raise KeyError('The supplied keyword argument: {0} could not be parsed.'.format(key))

    return spec
