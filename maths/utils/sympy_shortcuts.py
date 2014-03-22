import sympy


def easy_sub(func, value):
    if len(func.free_symbols) != 1:
        raise ValueError('This function: {0} must have only 1 variable'.format(func))

    symbol = func.free_symbols.pop()

    return func.subs({symbol: value})