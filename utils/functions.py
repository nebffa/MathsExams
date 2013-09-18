import sympy
from sympy import oo
import functools
import operator
from maths.symbols import *


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


def maximal_domain(expr, domain=sympy.Interval(-oo, oo)):
    # detect square roots, logs, tans and reciprocals
    # i won't implement csc, sec and cot for now

    x_real = sympy.Symbol('x_real', real=True)
    expr = expr.replace(x, x_real)
    domains = [domain]

    #tests = [sympy.log, sympy.Pow, sympy.tan] #, sympy.csc, sympy.sec, sympy.cot]
    find = expr.find(sympy.log)
    domains += [relation_to_interval( sympy.solve( log.args[0] > 0 ) ) for log in find]

    find = expr.find(sympy.Pow)
    # check if the index of power is less than 0 - "If Pow.args[1] < 0"
    # if it is, solve the denominator - "Pow.args[0]" - equal to 0 and take its complement to get the maximal domain
    domains += [sympy.FiniteSet(sympy.solve( Pow.args[0] )).complement for Pow in find if Pow.args[1] < 0]


    #find = expr.find(sympy.tan)
    #domains = [sympy.FiniteSet(sympy.solve( tan.args[0] - k*pi, x )).complement for tan in find]
    if expr.find(sympy.tan):
        raise NotImplementedError("Can't find maximum domains of tans.")
    if expr.find(sympy.cot):
        raise NotImplementedError("Can't find maximum domain of cot.")
    if expr.find(sympy.csc):
        raise NotImplementedError("Can't find maximum domain of csc.")
    if expr.find(sympy.sec):
        raise NotImplementedError("Can't find maximum domain of sec.")

    return functools.reduce(operator.and_, domains)


def relation_to_interval(relation):

    if isinstance(relation, sympy.Or):
        return functools.reduce(operator.or_, [relation_to_interval(i) for i in relation.args] )

    elif isinstance(relation, sympy.And):
        return functools.reduce(operator.and_, [relation_to_interval(i) for i in relation.args] )


    if relation.rel_op == '>':
        if isinstance(relation.lhs, sympy.Symbol):
            return sympy.Interval(relation.rhs, sympy.oo, True, True)
        else:
            return sympy.Interval(-sympy.oo, relation.lhs, True, True)
    elif relation.rel_op == '>=':
        if isinstance(relation.lhs, sympy.Symbol):
            return sympy.Interval(relation.rhs, sympy.oo)
        else:
            return sympy.Interval(-sympy.oo, relation.lhs)
    elif relation.rel_op == '<':
        if isinstance(relation.lhs, sympy.Symbol):
            return sympy.Interval(-sympy.oo, relation.rhs, True, True)
        else:
            return sympy.Interval(relation.lhs, sympy.oo, True, True)
    elif relation.rel_op == '<=':
        if isinstance(relation.lhs, sympy.Symbol):
            return sympy.Interval(-sympy.oo, relation.rhs)
        else:
            return sympy.Interval(relation.lhs, sympy.oo)
