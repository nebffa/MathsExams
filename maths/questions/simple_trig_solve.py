import sympy
from ..relations.trigonometry import trig
import random
from ..symbols import x, coeff0, coeff1
from .. import all_functions, sets
from ..latex import solutions
from . import relationships
import itertools


@relationships.root
class SimpleTrigSolve(relationships.QuestionPart):
    """
    Question description
    ====================

    Solve a trigonometric equation for a given domain.


    Real-life instances
    ===================

    2008 3: [6 lines] [2 marks]
    2009 4: [5 lines] [3 marks]
    2010 4b: [4 lines] [2 marks]
    2011 3b: [12 lines] [2 marks]
    """

    def __init__(self):

        self.num_lines, self.num_marks = 8, 2

        self._qp = {}

        trig_function = all_functions.request_trig(difficulty=random.randint(1, 2)).equation

        # 2008 Q3: Solve the equation cos(3x/2) = 1/2 for x in [-pi/2, pi/2] [6 lines] [2 marks]
        # 2009 Q4: Solve the equation tan(2x) = sqrt(3) for x in (-pi/4, pi/4) U (pi/4, 3pi/4) [5 lines] [3 marks]
        # 2010 Q4b: Solve the equation sqrt(3)*sin(x) = cos(x) for x in [-pi, pi] [4 lines] [2 marks]
        # 2011 Q3b: Solve the equation sin(2x + pi/3) = 1/2 for x in [0, pi] [12 lines] [2 marks]

        self._qp['function_type'] = all_functions.detect_expr_type(trig_function)

        if self._qp['function_type'] == sympy.cot:  # because some tans get changed to cots internally, we want to get a value for tan
            value = trig.plausible_value_no_zero(sympy.tan)
        else:
            value = trig.plausible_value_no_zero(self._qp['function_type'])

        if random.choice([True, False]):
            numerator, denominator = value.as_numer_denom()
            self._qp['equation'] = denominator * trig_function
            self._qp['value'] = numerator
        else:
            self._qp['equation'] = trig_function
            self._qp['value'] = value

        just_the_trig_function = self._qp['equation'].find(self._qp['function_type']).pop()
        self._qp['equation_interior'] = just_the_trig_function.args[0]  # for use in writing the solution
        self._qp['equation_coeff'] = self._qp['equation'].coeff(just_the_trig_function)
        self._qp['true_value'] = self._qp['value'] / self._qp['equation_coeff']

        self._qp['domain'] = trig.request_limited_domain(self._qp['equation'])

    def question_statement(self):
        return r'Solve the equation ${equation} = {value}$ for $x \in {domain}$.'.format(
            equation=sympy.latex(self._qp['equation']),
            value=sympy.latex(self._qp['value']),
            domain=sympy.latex(self._qp['domain'])
        )

    def solution_statement(self):
        lines = solutions.Lines()

        true_equation = self._qp['equation'] / self._qp['equation_coeff']
        if self._qp['equation_coeff'] != 1:
            lines += r'${0} = {1}$'.format(
                sympy.latex(true_equation),
                sympy.latex(self._qp['true_value'])
            )

        # perform the transformation of self._qp['equation_interior'] on the domain
        dilated_domain = sets.transform_set(x, self._qp['equation_interior'].coeff(x) * x, self._qp['domain'])
        if self._qp['equation_interior'].coeff(x) != 1:
            lines += r'${dilated_x} \in {dilated_domain}$'.format(
                dilated_x=sympy.latex(self._qp['equation_interior'].coeff(x) * x),
                dilated_domain=sympy.latex(dilated_domain)
            )

        dilated_and_translated_domain = sets.transform_set(x, self._qp['equation_interior'], self._qp['domain'])
        # trying to extract the constant coefficient by calling .coeff(x, 0) is bugged
        # also, doing .as_poly().all_coeffs() does not work because SymPy thinks (-x + pi) is a two-variable (x and pi)
        # relationship. It must have something to do with how pi is defined. Anyway, we use the workaround that I can think of
        # if it's a sympy.Add object, there will be a constant coefficient
        if isinstance(self._qp['equation_interior'], sympy.Add):
            lines += r'${dilated_and_translated_x} \in {dilated_and_translated_domain}$'.format(
                dilated_and_translated_x=sympy.latex(self._qp['equation_interior']),
                dilated_and_translated_domain=sympy.latex(dilated_and_translated_domain)
            )

        trig_type = all_functions.detect_expr_type(self._qp['equation'])
        base_solutions = sympy.solve(trig_type(x) - self._qp['true_value'])
        lines += r'The {base_solutions_maybe_pluralise} for ${basic_expr} = {true_value}$ {is_or_are} ${solutions}$'.format(
            base_solutions_maybe_pluralise='base solution' if len(base_solutions) == 1 else 'base solutions',
            basic_expr=sympy.latex(trig_type(x)),
            true_value=sympy.latex(self._qp['true_value']),
            is_or_are='is' if len(base_solutions) == 1 else 'are',
            solutions=', '.join(sympy.latex(i) for i in base_solutions)
        )

        dilated_and_translated_solutions = solutions_for_transformed_domain(true_equation, self._qp['true_value'], dilated_and_translated_domain)
        period = trig.expr_period(trig_type(x))
        revolutions_away = []
        for i in dilated_and_translated_solutions:
            if (i - base_solutions[0]) % period == 0:
                base = base_solutions[0]
            else:
                base = base_solutions[1]

            n_revolutions = (i - base) / period
            string = sympy.latex(base)
            if n_revolutions > 0:
                string += r' + ({0} \times 2\pi)'.format(n_revolutions)
            elif n_revolutions < 0:
                string += r' - ({0} \times 2\pi)'.format(abs(n_revolutions))

            revolutions_away.append(string)

        lines += r'$\therefore {interior} = {solutions}$'.format(
            interior=sympy.latex(self._qp['equation_interior']),
            solutions=', '.join(i for i in revolutions_away)
        )

        dilated_and_translated_solutions = solutions_for_transformed_domain(true_equation, self._qp['true_value'], dilated_and_translated_domain)
        lines += r'$= {solutions}$'.format(
            interior=sympy.latex(self._qp['equation_interior']),
            solutions=', '.join(sympy.latex(i) for i in dilated_and_translated_solutions)
        )

        if self._qp['equation_interior'].coeff(x, 0) != 0:
            offset = self._qp['equation_interior'].coeff(x, 0)
            dilated_solutions = [i - offset for i in dilated_and_translated_solutions]
            lines += r'${interior} = {solutions}$'.format(
                interior=sympy.latex(self._qp['equation_interior'].coeff(x) * x),
                solutions=', '.join(sympy.latex(i) for i in dilated_solutions)
            )

        if self._qp['equation_interior'].coeff(x) != 1:
            coeff_x = self._qp['equation_interior'].coeff(x)
            final_solutions = sorted([i / coeff_x for i in dilated_solutions])
            lines += r'$x = {solutions}$'.format(
                solutions=', '.join(sympy.latex(i) for i in final_solutions)
            )

        return lines.write()


def solutions_for_transformed_domain(expr, value, transformed_domain):
    """Solve a trig expression not for x, but for the trig interior.

    >>> solutions_for_transformed_domain(sympy.sin(2*x), 0, sympy.Interval(0, sympy.pi))
    [0, pi]

    >>> domain = sympy.Interval(-5 * sympy.pi / 3, sympy.pi /3)
    >>> solutions_for_transformed_domain(sympy.cos(2*x + sympy.pi/3), -sympy.sqrt(3)/2, domain)
    [-7*pi/6, -5*pi/6]
    """

    if isinstance(transformed_domain, sympy.Union):
        all_solutions = [solutions_for_transformed_domain(expr, value, i) for i in transformed_domain.args]

        return sorted(list(itertools.chain(*all_solutions)))

    trig_type = all_functions.detect_expr_type(expr)

    base_solutions = sympy.solve(trig_type(x) - value)
    period = trig.expr_period(trig_type(x))

    all_solutions = []
    for i in base_solutions:
        i_down = i
        while True:  # go down
            if i_down in transformed_domain:
                all_solutions.append(i_down)

            if i_down < transformed_domain.left:
                break
            i_down -= period

        i_up = i
        while True:  # go up
            i_up += period
            if i_up in transformed_domain:
                all_solutions.append(i_up)

            if i_up > transformed_domain.right:
                break

    unique = set(all_solutions)
    return sorted([i for i in unique])
