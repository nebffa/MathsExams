from ..relations.trigonometry import trig
import random
from ..symbols import *
from .. import all_functions, sets
from ..utils import functions
from . import relationships


@relationships.root
class SimpleTrigSolve(object):
    def __init__(self):
        self.num_lines, self.num_marks = 8, 2


        trig_function = all_functions.request_trig(difficulty=random.randint(1, 2)).equation

        # 2008 Q3: Solve the equation cos(3x/2) = 1/2 for x in [-pi/2, pi/2] [6 lines] [2 marks]
        # 2009 Q4: Solve the equation tan(2x) = sqrt(3) for x in (-pi/4, pi/4) U (pi/4, 3pi/4) [5 lines] [3 marks]
        # 2010 Q4b: Solve the equation sqrt(3)*sin(x) = cos(x) for x in [-pi, pi] [4 lines] [2 marks]
        # 2011 Q3b: Solve the equation sin(2x + pi/3) = 1/2 for x in [0, pi] [12 lines] [2 marks]

        trig_function = sympy.tan(-x - 2*sympy.pi/3)
        print(trig_function)
        self.function_type = all_functions.detect_expr_type(trig_function)

        if self.function_type == sympy.cot:  # because some tans get changed to cots internally, we want to get a value for tan
            value = trig.plausible_value_no_zero(sympy.tan)
        else:
            value = trig.plausible_value_no_zero(self.function_type)


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
        question_statement = r'Solve the equation {0} = {1} for x \in {2}.'

        return question_statement.format(sympy.latex(self.equation), sympy.latex(self.value), sympy.latex(self.domain))

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

    if isinstance(domain, sympy.Union):
        return flatten([all_solutions(trig_function, i) for i in domain.args])


    trig_type = all_functions.detect_expr_type(trig_function)

    if trig_type in [sympy.sin, sympy.cos, sympy.sec, sympy.csc]:
        base_period = 2 * sympy.pi
    else:
        base_period = sympy.pi


    trig_interior = trig_function.find(trig_type).pop().args[0]
    transformed_domain = sets.transform_set(x, trig_interior, domain)


    value_find_function = trig_function.replace(trig_type(x0), trig_type(y))
    base_solutions = sympy.solve(value_find_function)


    k = sympy.Symbol('k', integer=True)
    general_solutions = [i + base_period*k for i in base_solutions]
        

    for general_solution in general_solutions:
        print(general_solution, transformed_domain.left)
        lower_constraint = sympy.solve(general_solution > transformed_domain.left)
        upper_constraint = sympy.solve(general_solution < transformed_domain.right)

        interval_one = functions.relation_to_interval(lower_constraint)
        interval_two = functions.relation_to_interval(upper_constraint)

        solution_space = interval_one & interval_two
        solutions = [i for i in range(int(y.left), int(y.right + 1))]

        print(solutions)

