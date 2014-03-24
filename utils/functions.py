import sympy
from sympy import oo
import functools
import operator
from ..symbols import *


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


def is_convex(expr, location):
    symbol_used = expr.free_symbols.pop()

    second_deriv = expr.diff().diff().subs({symbol_used: location})

    if second_deriv > 0:
        return True
    else:
        return False


def is_concave(expr, location):
    symbol_used = expr.free_symbols.pop()

    second_deriv = expr.diff().diff().subs({symbol_used: location})

    if second_deriv > 0:
        return False
    else:
        return True


def parse_type(expr):
    ''' Return which type (or types) an expression is.

    '''

    types = set()

    possible_types = [
        sympy.exp,
        sympy.log,
        sympy.sin,
        sympy.cos,
        sympy.tan,
        sympy.csc,
        sympy.sec,
        sympy.cot,
    ]


    for each in possible_types:
        if expr.find(each):
            types.add(each)

    if len(types) == 0:
        types.add(sympy.Poly)

    return types


def maximal_domain(expr, domain=sympy.Interval(-oo, oo)):
    ''' Return the maximal domain of an expression.

    >>> maximal_domain(sympy.log(x**2 - 1))
    (-oo, -1) U (1, oo)

    >>> maximal_domain(1 / (x**2 - 4))
    (-oo, -2) U (-2, 2) U (2, oo)

    >>> maximal_domain((x - 2) ** (sympy.Rational(3, 2)))
    (2, oo)
    '''

    # 4 possible scenarios:
    #       1. 1/(a) -- a != 0
    #       2. sqrt(b) -- b > 0
    #       3. log(c) -- c > 0
    #       4. tan(d) -- d != the solutions of tan

    for symbol in expr.free_symbols:
        if symbol == x:
            expr = expr.replace(x, sympy.Symbol('x', real=True))
        else:
            raise NotImplementedError('only x is currently supported - but that can be easily changed')



    powers = expr.find(sympy.Pow)
    # case 1
    for power in powers:
        if power.args[1] < 0:
            denominator = power.args[0]

            solution = sympy.solve(denominator)
            domain &= -sympy.FiniteSet(solution)

        # case 2
        if isinstance(power.args[1], sympy.Rational):
            if power.args[1].q % 2 != 0:
                continue

            sqrt_interior = power.args[0]

            solution = sympy.solve(sqrt_interior > 0)
            domain &= relation_to_interval(solution)


    # case 3
    logs = expr.find(sympy.log)
    for log in logs:
        interior = log.args[0]

        solution = sympy.solve(interior > 0)    
        domain &= relation_to_interval(solution)


    # case 4
    if expr.find(sympy.tan) or expr.find(sympy.cot) or expr.find(sympy.sec) or expr.find(sympy.csc):
        raise NotImplementedError('tan/cot/sec/csc are not supported')

    return domain
