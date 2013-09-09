from . import parsers
from . import functions


def absolute_value(**kwargs):
    spec = parsers.parse_absolute_value_args(kwargs)

    return functions.absolute_value(spec)