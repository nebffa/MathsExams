import sympy
from sympy import oo


def is_monotone_increasing(equation, domain=None):
    if domain is None:
        domain = sympy.Interval(-oo, oo, True, True)
    else:
        assert isinstance(domain, sympy.Interval)  # expand these functions to deal with unions later
        # since we look at the behaviour of how the graph changes around turning points, we don't need to look at the turning points
        # on the edge of the domain, e.g. x**2 would be monotone on [0, 1] even though it has a turning point at 0
        domain = sympy.Interval(domain.left, domain.right, True, True) 

    assert len(equation.free_symbols) == 1
    var = [symbol for symbol in equation.free_symbols][0]

    deriv = equation.diff()

    stationary_points = [solution for solution in sympy.solve(deriv) if solution in domain]
    for x_value in stationary_points:
        # imagine x^4 - its second deriv is 12x^2 which is 0, but this is still a turning point - check either side of the T.P.
        if x_value - 0.01 in domain:
            if deriv.subs({var: x_value - 0.01}) < 0:
                return False
        if x_value + 0.01 in domain:
            if deriv.subs({var: x_value + 0.01}) < 0:
                return False
        

    # the graph is monotone - but is it increasing? take a point within the domain and check if the graph is increasing
    if domain.left == -oo and domain.right == oo:
        point = 0.01
    elif domain.left != -oo and domain.right == oo:
        point = domain.left + 1.01
    elif domain.left == -oo and domain.right != oo:
        point = domain.right - 1.01
    else:
        point = (domain.left + domain.right) / 2 + 0.01

    if deriv.subs({var: point}) < 0:
        return False
    else:
        return True


def is_monotone_decreasing(equation, domain=None):
    if domain is None:
        domain = sympy.Interval(-oo, oo, True, True)
    else:
        assert isinstance(domain, sympy.Interval)  # expand these functions to deal with unions later
        # since we look at the behaviour of how the graph changes around turning points, we don't need to look at the turning points
        # on the edge of the domain, e.g. x**2 would be monotone on [0, 1] even though it has a turning point at 0
        domain = sympy.Interval(domain.left, domain.right, True, True) 

    assert len(equation.free_symbols) == 1
    var = [symbol for symbol in equation.free_symbols][0]

    deriv = equation.diff()

    stationary_points = [solution for solution in sympy.solve(deriv) if solution in domain]
    for x_value in stationary_points:
        # imagine x^4 - its second deriv is 12x^2 which is 0, but this is still a turning point - check either side of the T.P.
        if x_value - 0.01 in domain:
            if deriv.subs({var: x_value - 0.01}) > 0:
                return False
        if x_value + 0.01 in domain:
            if deriv.subs({var: x_value + 0.01}) > 0:
                return False
        

    # the graph is monotone - but is it increasing? take a point within the domain and check if the graph is increasing
    if domain.left == -oo and domain.right == oo:
        point = 0.01
    elif domain.left != -oo and domain.right == oo:
        point = domain.left + 1.01
    elif domain.left == -oo and domain.right != oo:
        point = domain.right - 1.01
    else:
        point = (domain.left + domain.right) / 2 + 0.01

    if deriv.subs({var: point}) > 0:
        return False
    else:
        return True
