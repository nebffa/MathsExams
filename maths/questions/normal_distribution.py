import sympy
import random
from .. import not_named_yet
from ..latex import solutions, expressions
from ..symbols import a
from . import relationships
import copy


X = sympy.Symbol('X')
Z = sympy.Symbol('Z')


@relationships.root
class NormalDistribution(relationships.QuestionPart):
    """
    Question description
    ====================

    Setup the parameters for subsequent questions on the normal distribution.


    Real-life instances
    ===================

    2010 5: [Blank slate]
    """

    def __init__(self):
        self._qp = {}
        self.num_lines, self.num_marks = 0, 0

        self._qp['mean'] = random.choice([5 * i for i in range(1, 21)])
        self._qp['standard_deviation'] = random.choice(list(range(5, 11)))
        self._qp['variance'] = self._qp['standard_deviation'] ** 2

    def question_statement(self):
        return r'''Let X be a normally distributed random variable with mean {mean} and variance {variance} and let Z be the random variable with the standard
                normal distribution.'''.format(**self._qp)


@relationships.is_child_of(NormalDistribution)
class SimpleNormalDistribution(relationships.QuestionPart):
    """
    Question description
    ====================

    Find the probability of an event, given the probability of a separate but mathematically-related event.


    Real-life instances
    ===================

    2012 8a: [6 lines] [2 marks]
    """

    @staticmethod
    def construct_interval(boundary1, boundary2):
        """Construct a sympy interval from two boundaries, when we don't know which boundary is bigger.

        >>> SimpleNormalDistribution.construct_interval(0, 1)
        [0, 1]

        >>> SimpleNormalDistribution.construct_interval(sympy.oo, 1)
        [1, oo)
        """

        if boundary1 < boundary2:
            return sympy.Interval(boundary1, boundary2)
        else:
            return sympy.Interval(boundary2, boundary1)

    def __init__(self, part):
        self.num_lines, self.num_marks = 6, 2
        self._qp = copy.deepcopy(part._qp)

        self._qi = {}
        self._qi['unknown_variable'] = a

        self._qp['point'] = not_named_yet.randint(self._qp['mean'] - 10, self._qp['mean'] + 10, exclude=[self._qp['mean']])
        self._qp['symmetrically_opposite_point'] = 2 * self._qp['mean'] - self._qp['point']

        # there are 4 connected intervals:
        # where "2*mean - point" is the symmetric opposite of "point" in terms of the mean
        # (-sympy.oo, point)   pr = q
        # (2*mean - point, sympy.oo)   pr = q
        # (mean, point)   pr = 0.5 - q
        # (2*mean - point, mean)   pr = 0.5 - q

        if random.choice([True, False]):  # we do not have infinity as one of the bounds
            self._qp['event_provided_to_student'] = SimpleNormalDistribution.construct_interval(self._qp['mean'], self._qp['point'])
            if self._qp['point'] > self._qp['mean']:
                self._qp['desired_event'] = sympy.Interval(-sympy.oo, self._qp['symmetrically_opposite_point'])
            else:
                self._qp['desired_event'] = sympy.Interval(self._qp['symmetrically_opposite_point'], sympy.oo)
            self._qp['answer'] = sympy.Rational(1, 2) - self._qi['unknown_variable']

        else:  # we do have infinity as one of the bounds
            self._qp['desired_event'] = SimpleNormalDistribution.construct_interval(self._qp['symmetrically_opposite_point'], self._qp['mean'])
            if self._qp['point'] > self._qp['mean']:
                self._qp['event_provided_to_student'] = sympy.Interval(-sympy.oo, self._qp['point'])
            else:
                self._qp['event_provided_to_student'] = sympy.Interval(self._qp['point'], sympy.oo)
            self._qp['answer'] = -sympy.Rational(1, 2) + self._qi['unknown_variable']

    def question_statement(self):
        return r'''If $Pr({event_provided_to_student}) = {unknown_variable}$, find $Pr({desired_event})$ in terms of
            ${unknown_variable}$.'''.format(
            event_provided_to_student=expressions.relation(self._qp['event_provided_to_student'], var=X),
            desired_event=expressions.relation(self._qp['desired_event'], var=X),
            mean=self._qp['mean'],
            standard_deviation=self._qp['standard_deviation'],
            unknown_variable=self._qi['unknown_variable']
        )

    def solution_statement(self):
        lines = solutions.Lines()

        left_pr = sympy.Rational(1, 2)
        if self._qp['event_provided_to_student'].left == -sympy.oo:
            symmetrically_opposite_event = sympy.Interval(self._qp['mean'], self._qp['point'])
            opposite_half_of_normal_distribution = sympy.Interval(self._qp['mean'], sympy.oo)
            event_provided_to_student = sympy.Interval(self._qp['event_provided_to_student'].right, sympy.oo)
            right_pr = self._qi['unknown_variable']
        elif self._qp['event_provided_to_student'].right == sympy.oo:
            symmetrically_opposite_event = sympy.Interval(self._qp['point'], self._qp['mean'])
            opposite_half_of_normal_distribution = sympy.Interval(-sympy.oo, self._qp['mean'])
            event_provided_to_student = sympy.Interval(-sympy.oo, self._qp['event_provided_to_student'].left)
            right_pr = 1 - self._qi['unknown_variable']
        elif self._qp['point'] < self._qp['mean']:
            symmetrically_opposite_event = sympy.Interval(-sympy.oo, self._qp['point'])
            opposite_half_of_normal_distribution = sympy.Interval(-sympy.oo, self._qp['mean'])
            event_provided_to_student = self._qp['event_provided_to_student']
            right_pr = self._qi['unknown_variable']
        else:
            symmetrically_opposite_event = sympy.Interval(self._qp['point'], sympy.oo)
            opposite_half_of_normal_distribution = sympy.Interval(self._qp['mean'], sympy.oo)
            event_provided_to_student = self._qp['event_provided_to_student']
            right_pr = 1 - self._qi['unknown_variable']

        # e.g. Pr(56 <= X <= 60) = Pr(60 <= X <= 64) = Pr(X >= 60) - Pr(X >= 64)
        lines += r'''$Pr({desired_event}) = Pr({symmetrically_opposite_event}) =
            Pr({opposite_half_of_normal_distribution}) - Pr({event_provided_to_student})$'''.format(
            desired_event=expressions.relation(self._qp['desired_event'], var=X),
            symmetrically_opposite_event=expressions.relation(symmetrically_opposite_event, var=X),
            opposite_half_of_normal_distribution=expressions.relation(opposite_half_of_normal_distribution, var=X),
            event_provided_to_student=expressions.relation(event_provided_to_student, var=X),
        )

        # e.g. = (1/2) - (-c + 1) = c - 1/2
        lines += r'$= ({half_interval_probability}) - ({probability_derived_from_question}) = {answer}$'.format(
            half_interval_probability=sympy.latex(left_pr),
            probability_derived_from_question=sympy.latex(right_pr),
            answer=sympy.latex(self._qp['answer'])
        )

        return lines.write()


@relationships.is_child_of(NormalDistribution)
class OneSidedHalf(relationships.QuestionPart):
    """
    Question description
    ====================

    Find the probability of one half of the normal distribution.


    Real-life instances
    ===================

    2010 5a: [2 lines] [1 mark]
    """

    def __init__(self, part):
        self.num_lines, self.num_marks = 2, 1
        self._qp = copy.deepcopy(part._qp)

        self._qp['interval'] = random.choice([
            sympy.Interval(-sympy.oo, self._qp['mean']),
            sympy.Interval(self._qp['mean'], sympy.oo)
        ])

    def question_statement(self):
        return r'''Find $Pr({event})$.'''.format(
            event=expressions.relation(self._qp['interval'], var="X")
        )

    def solution_statement(self):
        lines = solutions.Lines()
        lines += r'${answer}$'.format(
            answer=sympy.latex(sympy.Rational(1, 2))
        )

        return lines.write()


@relationships.is_child_of(NormalDistribution)
class ProbabilityEquality(relationships.QuestionPart):
    """
    Question description
    ====================

    Find the value of a variable given a relationship between a standard normal event,
    and an event in a particular normal distribution.


    Real-life instances
    ===================

    2010 5b: [4 lines] [2 marks]
    """

    @staticmethod
    def N_to_Z_interval(interval, mean, standard_deviation):
        """Return the corresponding standard normal distribution interval, given an interval
        on some normal distribution.

        >>> ProbabilityEquality.N_to_Z_interval(sympy.Interval(-5, 10), 5, 5)
        [-2, 1]
        """

        Z_left = (interval.left - mean) / standard_deviation
        Z_right = (interval.right - mean) / standard_deviation

        return sympy.Interval(Z_left, Z_right)

    @staticmethod
    def Z_to_N_interval(interval, mean, standard_deviation):
        """Return the corresponding interval for a normal distribution, given an interval
        on the standard normal distribution.

        >>> ProbabilityEquality.Z_to_N_interval(sympy.Interval(-1, 1), 10, 2)
        [8, 12]
        """

        N_left = mean + standard_deviation * interval.left
        N_right = mean + standard_deviation * interval.right

        return sympy.Interval(N_left, N_right)

    @staticmethod
    def symmetrically_opposite_interval(interval, mean):
        """Return the interval that is symmetrically opposite the mean.

        >>> ProbabilityEquality.symmetrically_opposite_interval(sympy.Interval(5, 10), 4)
        [-2, 3]
        """

        new_left = 2 * mean - interval.right
        new_right = 2 * mean - interval.left

        return sympy.Interval(new_left, new_right)

    def __init__(self, part):
        self.num_lines, self.num_marks = 4, 2
        self._qp = copy.deepcopy(part._qp)

        self._qp['num_standard_deviations'] = sympy.Rational(
            not_named_yet.randint(-3, 3, exclude=[0]),
            random.choice([1, self._qp['standard_deviation']])
        )

        self._qp['location'] = self._qp['mean'] + self._qp['num_standard_deviations'] * self._qp['standard_deviation']
        self._qp['interval'] = random.choice([
            sympy.Interval(-sympy.oo, self._qp['location']),
            sympy.Interval(self._qp['location'], sympy.oo)
        ])

        self._qp['Z_interval'] = ProbabilityEquality.N_to_Z_interval(
            self._qp['interval'],
            mean=self._qp['mean'],
            standard_deviation=self._qp['standard_deviation']
        )
        self._qp['flipped'] = random.choice([True, False])

        if self._qp['flipped']:
            self._qp['Z_interval'] = ProbabilityEquality.opposite_interval(self._qp['Z_interval'], mean=0)

        self._qp['unknown_location'] = random.choice(['original', 'Z'])

        c = sympy.Symbol('c', real=True)
        if self._qp['unknown_location'] == 'original':
            self._qp['question_original_interval'] = sympy.Interval(-sympy.oo, c) if self._qp['interval'].left == -sympy.oo else sympy.Interval(c, sympy.oo)
            self._qp['question_Z_interval'] = self._qp['Z_interval']
        else:
            self._qp['question_original_interval'] = self._qp['interval']
            self._qp['question_Z_interval'] = sympy.Interval(-sympy.oo, c) if self._qp['Z_interval'].left == -sympy.oo else sympy.Interval(c, sympy.oo)

    def question_statement(self):
        return r'''Find c such that $Pr({question_original_interval}) = Pr({question_Z_interval})$.'''.format(
            question_original_interval=expressions.relation(self._qp['question_original_interval'], var=X),
            question_Z_interval=expressions.relation(self._qp['question_Z_interval'], var=Z)
        )

    def solution_statement(self):
        lines = solutions.Lines()

        if self._qp['unknown_location'] == 'Z':
            interval = ProbabilityEquality.N_to_Z_interval(
                self._qp['question_original_interval'],
                mean=self._qp['mean'],
                standard_deviation=self._qp['standard_deviation']
            )
            value = interval.left if interval.left != -sympy.oo else interval.right
            z_score = r'\frac{{{location} - {mean}}}{{{standard_deviation}}}'.format(**self._qp)

            # e.g. Pr(X >= 13) = Pr(Z >= (13 - 15)/9) = Pr(Z >= -2/9)
            lines += r'''$Pr({0}) = Pr({1}) = Pr({2})$'''.format(
                expressions.relation(self._qp['question_original_interval'], var="X"),
                expressions.relation(interval, var="Z").replace(sympy.latex(value), z_score),
                expressions.relation(interval, var="Z")
            )
        else:
            interval = ProbabilityEquality.Z_to_N_interval(
                self._qp['question_Z_interval'],
                mean=self._qp['mean'],
                standard_deviation=self._qp['standard_deviation']
            )
            value = interval.left if interval.left != -sympy.oo else interval.right
            num_sds = self._qp['num_standard_deviations'] * (-1 if self._qp['flipped'] else 1)
            n_score = r'{0} \times {standard_deviation} + {mean}'.format(sympy.latex(num_sds), **self._qp)

            # e.g. Pr(Z >= -3) = Pr(X >= -3 * 7 + 40) = Pr(X >= 19)
            lines += r'''$Pr({0}) = Pr({1}) = Pr({2})$'''.format(
                expressions.relation(self._qp['question_Z_interval'], var="Z"),
                expressions.relation(interval, var="X").replace(sympy.latex(value), n_score),
                expressions.relation(interval, var="X")
            )

        if self._qp['flipped']:
            # e.g. = Pr(Z <= 2/9)
            lines += r'''$= Pr({0})$'''.format(
                expressions.relation(ProbabilityEquality.opposite_interval(interval, mean=0), var="Z")
            )

        answer = -value if self._qp['flipped'] else value

        # e.g. \therefore c = 79
        lines += r'''$\therefore c = {answer}$'''.format(
            answer=sympy.latex(answer)
        )

        return lines.write()
