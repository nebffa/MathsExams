import sympy
import random
from sympy.abc import *
from maths import all_functions, sets
from maths.trig import trig


class SimpleTrigSolve(object):
    def __init__(self):
        trig_function = all_functions.request_trig(difficulty=random.randint(1, 2)).equation

        # 2008 Q3: Solve the equation cos(3x/2) = 1/2 for x in [-pi/2, pi/2] [6 lines] [2 marks]
        # 2009 Q4: Solve the equation tan(2x) = sqrt(3) for x in (-pi/4, pi/4) U (pi/4, 3pi/4) [5 lines] [3 marks]
        # 2010 Q4b: Solve the equation sqrt(3)*sin(x) = cos(x) for x in [-pi, pi] [4 lines] [2 marks]
        # 2011 Q3b: Solve the equation sin(2x + pi/3) = 1/2 for x in [0, pi] [12 lines] [2 marks]

        trig_function = sympy.tan(-x - 2*sympy.pi/3)
        print trig_function
        self.function_type = all_functions.detect_expr_type(trig_function)

        if self.function_type == sympy.cot:  # because some tans get changed to cots internally, we want to get a value for tan
            value = trig.plausible_value_no_zero(sympy.tan)
        else:
            value = trig.plausible_value_no_zero(self.function_type)

        x0, x1, x2, x3 = sympy.Wild('x0'), sympy.Wild('x1'), sympy.Wild('x2'), sympy.Wild('x3')
        match = value.match(x0 / x1)

        if random.choice([True, False]):
            self.equation = match[x0] * trig_function
            self.value = match[x1]
        else:
            self.equation = trig_function
            self.value = value

        match = self.equation.match(x0 * self.function_type(x1*x + x2) + x3)
        self._equation_interior = match[x1]*x + match[x2]  # for use in writing the solution
        self._equation_coeff = match[x0]

        self.domain = trig.request_limited_domain(self.equation)

    def write_question(self):
        question_statement = r'Solve the equation %s = %s for x \in %s.'

        return question_statement % (sympy.latex(self.equation), sympy.latex(self.value), sympy.latex(self.domain))

    def write_solution(self):
        lines = []
        # perform the transformation of self._equation_interior on the domain
        transformed_domain = sets.transform_set(x, self._equation_interior, self.domain)
        if self._equation_coeff != 1:
            equation = self.equation / self._equation_coeff
            value = self.value / self._equation_coeff
            lines.append(r'$%s = %s, x \in %s$' % equation, value, transformed_domain)
        else:
            lines.append(r'$x \in %s$' % transformed_domain)


def all_solutions(trig_function, domain):
    # TO DO: complete later. SymPy currently does not support solving inequalities over irrationals
    assert(isinstance(domain, sympy.Interval) or isinstance(domain, sympy.Union))

    if isinstance(domain, sympy.Union):
        return flatten([all_solutions(trig_function, i) for i in domain.args])

    x0, x1, x2= sympy.Wild('x0'), sympy.Wild('x1'), sympy.Wild('x2')

    trig_type = all_functions.detect_expr_type(trig_function)
    if trig_type in [sympy.sin, sympy.cos, sympy.sec, sympy.csc]:
        period = 2*sympy.pi
    elif trig_type in [sympy.sec, sympy.csc]:
        period = sympy.pi

    match = trig_function.match(x0 * trig_type(x1) + x2)

    transformed_domain = sets.transform_set(x, match[x1], domain)

    y, k = sympy.Symbol('y'), sympy.Symbol('k', integer=True)
    value_find_function = trig_function.replace(trig_type(x0), trig_type(y))
    general_solutions = [i + period*k for i in sympy.solve(value_find_function)]

    for solution in general_solutions:
        lower = sympy.solve(solution > domain.left)
        upper = sympy.solve(solution < domain.right)













y = SimpleTrigSolve()
print y.equation
print y.value
print y.domain
