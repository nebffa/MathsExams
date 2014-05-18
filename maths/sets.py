import sympy


def transform_set(x, expr, sympy_set):
    """ Transform a sympy_set by an expression

    >>> x = sympy.Symbol('x')
    >>> domain = sympy.Interval(-sympy.pi / 4, -sympy.pi / 6, False, True) | sympy.Interval(sympy.pi / 6, sympy.pi / 4, True, False)
    >>> transform_set(x, -2 * x, domain)
    [-pi/2, -pi/3) U (pi/3, pi/2]
    """

    if isinstance(sympy_set, sympy.Union):
        return sympy.Union(transform_set(x, expr, arg) for arg in sympy_set.args)
    if isinstance(sympy_set, sympy.Intersection):
        return sympy.Intersection(transform_set(x, expr, arg) for arg in sympy_set.args)

    f = sympy.Lambda(x, expr)
    if isinstance(sympy_set, sympy.Interval):
        left, right = f(sympy_set.left), f(sympy_set.right)

        if left < right:
            new_left_open = sympy_set.left_open
            new_right_open = sympy_set.right_open
        else:
            new_left_open = sympy_set.right_open
            new_right_open = sympy_set.left_open

        return sympy.Interval(sympy.Min(left, right), sympy.Max(left, right),
                              new_left_open, new_right_open)

    if isinstance(sympy_set, sympy.FiniteSet):
        return sympy.FiniteSet(list(map(f, sympy_set)))
