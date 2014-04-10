from . import parsers, functions


def absolute_value(**kwargs):
    spec = parsers.parse_absolute_value(**kwargs)

    return functions.absolute_value(spec)


def cubic(**kwargs):
    spec = parsers.parse_cubic(**kwargs)

    return functions.cubic(spec)


def hyperbola(**kwargs):
    spec = parsers.parse_hyperbola(**kwargs)

    return functions.hyperbola(spec)
