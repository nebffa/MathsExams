import sympy
import random
from .. import domains
from ..symbols import x, k
from ..latex import expressions, solution_lines
from ..utils import sensible_values
from . import relationships
import copy


class PiecewiseProbDensityFunction:
    """Setup a question for a probability distribution, whether it is known (has no parameters except x) or unknown.
    """

    def __init__(self):
        self._qp = {}
        function_type = random.choice([sympy.sin, sympy.cos, 'linear', 'quadratic'])

        if function_type in [sympy.sin, sympy.cos]:
            while True:
                self._qp['domain'] = domains.integer_domain(low=0, high=2, minimum_distance=1)
                m = random.choice([sympy.pi / 2, sympy.pi])
                self._qp['equation'] = k * function_type(m * x)

                area = self._qp['equation'].integrate((x, self._qp['domain'].left, self._qp['domain'].right))

                solution = sympy.solve(area - 1)
                if len(solution) == 0:
                    continue

                self._qp['k'] = solution[0]
                break

        elif function_type == 'linear':
            self._qp['domain'] = domains.integer_domain()
            m = random.randint(1, 2)
            a = random.randint(7, 12)
            self._qp['equation'] = ((m * x + k) / a).together()

            area = self._qp['equation'].integrate((x, self._qp['domain'].left, self._qp['domain'].right))
            self._qp['k'] = sympy.solve(area - 1)[0]

        elif function_type == 'quadratic':
            self._qp['domain'] = domains.integer_domain()
            self._qp['equation'] = k * (x - self._qp['domain'].left) * (x - self._qp['domain'].right)

            area = self._qp['equation'].integrate((x, self._qp['domain'].left, self._qp['domain'].right))
            self._qp['k'] = sympy.solve(area - 1)[0]

    def question_statement(self):
        piecewise = sympy.Piecewise((self._qp['equation'], sympy.And(self._qp['domain'].left <= x, x <= self._qp['domain'].right)), (0, True))

        lines = solution_lines.Lines()

        lines += r'The function $$f(x) = {equation}$$ is a probability density function for the continuous random variable $X$.'.format(
            equation=expressions.piecewise(piecewise)
        )

        return lines.write()


@relationships.root
class UnknownDensityFunctionSetup(relationships.QuestionPart, PiecewiseProbDensityFunction):
    """Setup a question for an unknown probability distribution.

    e.g. y = k * x * (x + 3) for x ∈ [-3, 0]
    """

    def __init__(self):
        PiecewiseProbDensityFunction.__init__(self)
        self.num_marks, self.num_lines = 0, 0


@relationships.root
class KnownDensityFunctionSetup(relationships.QuestionPart, PiecewiseProbDensityFunction):
    """Setup a question for a known probability distribution.

    e.g. y = -2 * x * (x + 3) / 9 for x ∈ [-3, 0]
    """

    def __init__(self):
        PiecewiseProbDensityFunction.__init__(self)
        self.num_lines, self.num_marks = 0, 0

        self._qp['equation'] = self._qp['equation'].subs({k: self._qp['k']})


@relationships.is_child_of(UnknownDensityFunctionSetup)
class PiecewiseProbDensityFunctionUnknown(relationships.QuestionPart):
    """
    Question description
    ====================

    Calculate the value of an unknown so that an expression is a valid probability distribution (i.e. sums to 1).


    Real-life instances
    ===================

    2008 4a: [7 lines] [2 marks]
    2010 7a: [12 lines] [3 marks]

    """

    def __init__(self, part):
        self._qp = copy.deepcopy(part._qp)
        self.num_marks, self.num_lines = 3, 12

    def question_statement(self):
        piecewise = sympy.Piecewise((self._qp['equation'], sympy.And(self._qp['domain'].left < x, x < self._qp['domain'].right)), (0, True))

        return r'''Show that $k = {k}$.'''.format(
            equation=expressions.piecewise(piecewise),
            k=sympy.latex(self._qp['k'])
        )

    def solution_statement(self):
        lines = solution_lines.Lines()

        integral, integral_intermediate, integral_intermediate_eval = \
            expressions.integral_trifecta(lb=self._qp['domain'].left, ub=self._qp['domain'].right, expr=self._qp['equation'])

        lines += r'${integral} = 1$'.format(
            integral=integral
        )

        answer = self._qp['equation'].integrate((x, self._qp['domain'].left, self._qp['domain'].right))
        lines += r'${integral_intermediate} = {integral_intermediate_eval} = {answer} = 1$'.format(
            integral_intermediate=integral_intermediate,
            integral_intermediate_eval=integral_intermediate_eval,
            answer=sympy.latex(answer)
        )

        lines += r'$\therefore k = {k}$'.format(
            k=sympy.latex(self._qp['k'])
        )

        return lines.write()

    def sanity_check(self):
        true_equation = self._qp['equation'].subs({k: self._qp['k']})

        if true_equation.integrate((x, self._qp['domain'].left, self._qp['domain'].right)) != 1:
            raise RuntimeError(r'equation: {0}, domain: {1}, does not integrate to 1'.format(self._qp['equation'], self._qp['domain']))


# can be used for known and unknown
@relationships.is_child_of(KnownDensityFunctionSetup, UnknownDensityFunctionSetup)
class SimpleInterval(relationships.QuestionPart):
    """
    Question description
    ====================

    Calculate the probability of a one-sided interval.


    Real-life instances
    ===================

    2011 5a: [5 lines] [2 marks]
    """

    def __init__(self, part):
        # 2011 Q5a [5 lines] [2 marks]
        self.num_lines, self.num_marks = 5, 2

        self._qp = copy.deepcopy(part._qp)

        choices = [self._qp['domain'].left + sympy.Rational(i, 4) * self._qp['domain'].measure for i in [1, 2, 3]]
        self._qp['bound'] = random.choice(choices)

        self._qp['direction'] = random.choice(['left', 'right'])

        if self._qp['direction'] == 'left':
            self._qp['domain'] = sympy.Interval(self._qp['domain'].left, self._qp['bound'])
        else:
            self._qp['domain'] = sympy.Interval(self._qp['bound'], self._qp['domain'].right)

    def question_statement(self):
        return r'''Find $Pr(X {direction} {bound})$.'''.format(
            direction=r'\le' if self._qp['direction'] == 'left' else r'\ge',
            bound=sympy.latex(self._qp['bound'])
        )

    def solution_statement(self):
        lines = solution_lines.Lines()

        lines += '$= {integral}$'.format(
            integral=expressions.integral(expr=self._qp['equation'], lb=self._qp['domain'].left, ub=self._qp['domain'].right)
        )

        lines += '$= {integral_intermediate}$'.format(
            integral_intermediate=expressions.integral_intermediate(expr=self._qp['equation'], lb=self._qp['domain'].left, ub=self._qp['domain'].right)
        )

        answer = self._qp['equation'].integrate((x, self._qp['domain'].left, self._qp['domain'].right))
        lines += '$= {answer}$'.format(
            answer=sympy.latex(answer)
        )

        return lines.write()


# TODO: does not work for now (see parts_in_construction.txt)
# can be used for known and unknown
@relationships.is_child_of(KnownDensityFunctionSetup, UnknownDensityFunctionSetup)
class Conditional:
    """
    Question description
    ====================

    Calculate the probability of a one-sided interval, given another event.


    Real-life instances
    ===================

    2008 4b: [8 lines] [3 marks]
    2011 5b: [5 lines] [2 marks]
    """

    def __init__(self, part):
        # 2008 Q4b [8 lines] [3 marks]
        # 2011 Q5b [5 lines] [2 marks]

        self.num_lines, self.num_marks = 8, 2

        self._qp = copy.deepcopy(part._qp)

        self._qp['major_bound'], self._qp['minor_bound'] = sensible_values.conditional_integral(self._qp['equation'], self._qp['domain'])

        self._qp['major_direction'] = r'\le' if self._qp['minor_bound'] < self._qp['major_bound'] else r'\ge'
        self._qp['minor_direction'] = random.choice([r'\le', r'\ge'])

    def question_statement(self):
        return r'Find $Pr(X {minor_direction} {minor_bound} | X {major_direction} {major_bound})$.'.format(
            minor_direction=self._qp['minor_direction'],
            minor_bound=sympy.latex(self._qp['minor_bound']),
            major_direction=self._qp['major_direction'],
            major_bound=sympy.latex(self._qp['major_bound'])
        )

    def solution_statement(self):
        lines = solution_lines.Lines()

        minor_event = r'X {minor_direction} {minor_bound}'.format(**self._qp)
        major_event = r'X {major_direction} {major_bound}'.format(**self._qp)
        lines += r'$Pr({minor_event} | {major_event}) = {probability}$'.format(
            minor_event=minor_event,
            major_event=major_event,
            probability=expressions.conditional_probability(minor_event, major_event)
        )

        top_lb = min(self._qp['minor_bound'], self._qp['major_bound'])
        top_ub = max(self._qp['minor_bound'], self._qp['major_bound'])
        top_integral, top_intermediate, top_eval = expressions.integral_trifecta(lb=top_lb, ub=top_ub, expr=self._qp['equation'])
        top_value = self._qp['equation'].integrate((x, top_lb, top_ub))

        if self._qp['major_direction'] == r'\le':
            bottom_lb = self._qp['domain'].left
            bottom_ub = self._qp['major_bound']
        else:
            bottom_lb = self._qp['major_bound']
            bottom_ub = self._qp['domain'].right
        bottom_integral, bottom_intermediate, bottom_eval = expressions.integral_trifecta(lb=bottom_lb, ub=bottom_ub, expr=self._qp['equation'])
        bottom_value = self._qp['equation'].integrate((x, bottom_lb, bottom_ub))

        lines += r'$= \frac{{ {0} }}{{ {1} }}$'.format(top_integral, bottom_integral)

        lines += r'$= \frac{{ {0} }}{{ {1} }}$'.format(top_intermediate, bottom_intermediate)

        lines += r'$= \frac{{ {0} }}{{ {1} }}$'.format(top_eval, bottom_eval)

        lines += r'$= {answer}$'.format(
            answer=sympy.latex(top_value / bottom_value)
        )

        return lines.write()


# can be used for known
@relationships.is_child_of(KnownDensityFunctionSetup)
class Cumulative(relationships.QuestionPart):
    """
    Question description
    ====================

    Find the value of a parameter given the value of a probability involving that parameter.


    Real-life instances
    ===================

    2012 8b: [12 lines] [3 marks]
    """

    def __init__(self, part):
        self.num_lines, self.num_marks = 12, 3

        self._qp = copy.deepcopy(part._qp)

        stripped_endpoints = sympy.Interval(self._qp['domain'].left, self._qp['domain'].right, True, True)
        self._qp['location'] = sensible_values.antiderivative(self._qp['equation'], stripped_endpoints)
        self._qp['direction'] = random.choice(['left', 'right'])

    def question_statement(self):
        self._qi = {}
        # make the symbols real because SymPy can't deal with complex sympy.Intervals
        self._qi['unknown'] = sympy.Symbol('a', real=True)
        self._qi['inequality'] = r'\le' if self._qp['direction'] == 'left' else r'\ge'

        if self._qp['direction'] == 'left':
            self._qi['value'] = self._qp['equation'].integrate((x, self._qp['domain'].left, self._qp['location']))
            self._qi['domain'] = sympy.Interval(self._qp['domain'].left, self._qi['unknown'], False, True)
        else:
            self._qi['value'] = self._qp['equation'].integrate((x, self._qp['location'], self._qp['domain'].right))
            self._qi['domain'] = sympy.Interval(self._qi['unknown'], self._qp['domain'].right, True, False)

        return r'Find the value of {unknown} such that $Pr(X {direction} {unknown}) = {value}$.'.format(
            unknown=sympy.latex(self._qi['unknown']),
            direction=self._qi['inequality'],
            value=sympy.latex(self._qi['value'])
        )

    def solution_statement(self):
        lines = solution_lines.Lines()

        integral, integral_intermediate, integral_intermediate_eval = \
            expressions.integral_trifecta(expr=self._qp['equation'], lb=self._qi['domain'].left, ub=self._qi['domain'].right)

        lines += r'$Pr(X {direction} {unknown}) = {integral}$'.format(
            direction=self._qi['inequality'],
            unknown=self._qi['unknown'],
            integral=integral
        )

        lines += r'$= {0}$'.format(integral_intermediate)

        lines += r'$= {integral_intermediate_eval} = {value}$'.format(
            integral_intermediate_eval=integral_intermediate_eval,
            value=sympy.latex(self._qi['value'])
        )

        if self._qp['direction'] == 'left':
            left_side = self._qp['equation'].integrate().subs({x: self._qi['unknown']})
            right_side = self._qi['value'] + self._qp['equation'].integrate().subs({x: self._qp['domain'].left})
        else:
            left_side = -1 * self._qp['equation'].integrate().subs({x: self._qi['unknown']})
            right_side = self._qi['value'] - self._qp['equation'].integrate().subs({x: self._qp['domain'].right})

        lines += r'${0} = {1}$'.format(sympy.latex(left_side), sympy.latex(right_side))

        lines += expressions.shrink_solution_set(left_side, self._qp['domain'], expr_equal_to=right_side, var=self._qi['unknown'])

        return lines.write()
