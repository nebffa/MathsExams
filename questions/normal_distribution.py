import sympy
import random
from sympy.abc import *
from . import all_functions, not_named_yet
from ..latex import solution_lines, expressions
from ..utils import functions
import copy


class NormalDistribution:
    def __init__(self):
        self._qp = {}
        self.num_lines, self.num_marks = 0, 0

        self._qp['mean'] = random.choice([5*i for i in range(1, 21)])
        self._qp['sd'] = random.choice(list(range(5, 11)))
        self._qp['variance'] = self._qp['sd']**2


    def question_statement(self):
        return r'''Let X be a normally distributed random variable with mean {mean} and variance {variance} and let Z be the random variable with the standard
                normal distribution'''.format(**self._qp)

    def solution_statement(self):
        return r''''''


class SimpleNormalDistribution(NormalDistribution):
    def __init__(self):
        super(SimpleNormalDistribution, self).__init__()
        self.num_lines, self.num_marks = 6, 2

        self._qp['point'] = not_named_yet.randint(self._qp['mean'] - 10, self._qp['mean'] + 10, exclude=[self._qp['mean']])
        self._qp['opposite_point'] = 2*self._qp['mean'] - self._qp['point']
        # there are 4 connected intervals:
        # where "2*mean - point" is the symmetric opposite of "point" in terms of the mean
        # (-sympy.oo, point)   pr = q
        # (2*mean - point, sympy.oo)   pr = q
        # (mean, point)   pr = q - 0.5
        # (2*mean - point, mean)   pr = q - 0.5
        if False:
        #if random.choice([True, False]):
            # we do not have infinity as one of the bounds
            if self._qp['point'] > self._qp['mean']:
                self._qp['interval'] = sympy.Interval(self._qp['mean'], self._qp['point'])
                self._qp['opposite_interval'] = sympy.Interval(-sympy.oo, self._qp['opposite_point'])
                self._qp['value'] = sympy.Symbol('a')
            else:
                self._qp['interval'] = sympy.Interval(self._qp['point'], self._qp['mean'])
                self._qp['opposite_interval'] = sympy.Interval(self._qp['opposite_point'], sympy.oo)
                self._qp['value'] = sympy.Symbol('b')
            self._qp['answer'] = sympy.Rational(1, 2) - self._qp['value'] 

        else:
            # we do have infinity as one of the bounds
            if self._qp['point'] > self._qp['mean']:
                self._qp['interval'] = sympy.Interval(-sympy.oo, self._qp['point'])
                self._qp['opposite_interval'] = sympy.Interval(self._qp['opposite_point'], self._qp['mean'])
                self._qp['value'] = sympy.Symbol('c')
            else:
                self._qp['interval'] = sympy.Interval(self._qp['point'], sympy.oo)
                self._qp['opposite_interval'] = sympy.Interval(self._qp['mean'], self._qp['opposite_point'])
                self._qp['value'] = sympy.Symbol('d')
            self._qp['answer'] = -sympy.Rational(1, 2) + self._qp['value'] 


    def question_statement(self):
        self._qi = {}

        return r'''The random variable X is normally distributed with mean {mean} and standard deviation {sd}. If $Pr({0}) = {1}$, find $Pr({2})$ in terms of ${1}$.'''.format(
                    expressions.relation(self._qp['interval'], var=X),
                    self._qp['value'],
                    expressions.relation(self._qp['opposite_interval'], var=X),
                    **self._qp
                )




    def solution_statement(self):
        lines = solution_lines.Lines()

        if self._qp['interval'].left == -sympy.oo:
            some_interval = sympy.Interval(self._qp['mean'], self._qp['point'])
            opposite_half_interval = sympy.Interval(self._qp['mean'], sympy.oo)
            last_interval = sympy.Interval(self._qp['interval'].right, sympy.oo)
            left_pr = sympy.Rational(1, 2)
            right_pr = 1 - self._qp['value']
        elif self._qp['interval'].right == sympy.oo:
            some_interval = sympy.Interval(self._qp['point'], self._qp['mean'])
            opposite_half_interval = sympy.Interval(-sympy.oo, self._qp['mean'])
            last_interval = sympy.Interval(-sympy.oo, self._qp['interval'].left)
            left_pr = sympy.Rational(1, 2)
            right_pr = 1 - self._qp['value']
        elif self._qp['point'] < self._qp['mean']:
            some_interval = sympy.Interval(-sympy.oo, self._qp['point'])
            opposite_half_interval = sympy.Interval(-sympy.oo, self._qp['mean'])
            last_interval = self._qp['interval']
            left_pr = sympy.Rational(1, 2)
            right_pr = self._qp['value']
        else:
            some_interval = sympy.Interval(self._qp['point'], sympy.oo)
            opposite_half_interval = sympy.Interval(self._qp['mean'], sympy.oo)
            last_interval = self._qp['interval']
            left_pr = sympy.Rational(1, 2)
            right_pr = self._qp['value']

        
        # e.g. Pr(56 <= X <= 60) = Pr(60 <= X <= 64) = Pr(X >= 60) - Pr(X >= 64)
        lines += r'$Pr({0}) = Pr({1}) = Pr({2}) - Pr({3})$'.format(
                    expressions.relation(self._qp['opposite_interval'], var=X),
                    expressions.relation(some_interval, var=X),
                    expressions.relation(opposite_half_interval, var=X),
                    expressions.relation(last_interval, var=X),
                )

        # e.g. = (1/2) - (-c + 1) = c - 1/2
        lines += r'$= ({0}) - ({1}) = {2}$'.format(
                    sympy.latex(left_pr),
                    sympy.latex(right_pr),
                    sympy.latex(self._qp['answer'])
                )

        return lines.write()


class Half:
    def __init__(self, part):
        self.num_lines, self.num_marks = 2, 1
        self._qp = copy.copy(part._qp)

        self._qp['interval'] = random.choice([
                sympy.Interval(-sympy.oo, self._qp['mean']),
                sympy.Interval(self._qp['mean'], sympy.oo)
            ])

    def question_statement(self):
        self._qi = {}

        return r'''Find $Pr({0})$.'''.format(
                    expressions.relation(self._qp['interval'], var="X")
                )

    def solution_statement(self):
        lines = solution_lines.Lines()
        
        lines += r'${0}$'.format(sympy.latex(sympy.Rational(1, 2)))

        return lines.write()


def N_to_Z_interval(interval, mean, sd):
    Z_left = (interval.left - mean) / sd
    Z_right = (interval.right - mean) / sd

    return sympy.Interval(Z_left, Z_right)


def Z_to_N_interval(interval, mean, sd):
    N_left = mean + sd * interval.left
    N_right = mean + sd * interval.right

    return sympy.Interval(N_left, N_right)


def opposite_interval(interval, mean):
    new_left = 2*mean - interval.right
    new_right = 2*mean - interval.left

    return sympy.Interval(new_left, new_right)


class ProbabilityEquality:
    def __init__(self, part):
        self.num_lines, self.num_marks = 4, 2
        self._qp = copy.copy(part._qp)

        self._qp['num_standard_deviations'] = sympy.Rational(not_named_yet.randint(-3, 3, exclude=[0]), random.choice([1, self._qp['sd']]))

        self._qp['location'] = self._qp['mean'] + self._qp['num_standard_deviations'] * self._qp['sd']
        self._qp['interval'] = random.choice([
                sympy.Interval(-sympy.oo, self._qp['location']),
                sympy.Interval(self._qp['location'], sympy.oo)
            ])

        self._qp['Z_interval'] = N_to_Z_interval(self._qp['interval'], mean=self._qp['mean'], sd=self._qp['sd'])
        self._qp['flipped'] = random.choice([True, False])

        if self._qp['flipped']:
            self._qp['Z_interval'] = opposite_interval(self._qp['Z_interval'], mean=0)

        self._qp['unknown_location'] = random.choice(['original', 'Z'])

        c = sympy.Symbol('c', real=True)
        if self._qp['unknown_location'] == 'original':
            self._qp['question_original_interval'] = sympy.Interval(-sympy.oo, c) if self._qp['interval'].left == -sympy.oo else sympy.Interval(c, sympy.oo)
            self._qp['question_Z_interval'] = self._qp['Z_interval']
        else:
            self._qp['question_original_interval'] = self._qp['interval']
            self._qp['question_Z_interval'] = sympy.Interval(-sympy.oo, c) if self._qp['Z_interval'].left == -sympy.oo else sympy.Interval(c, sympy.oo)


    def question_statement(self):
        self._qi = {}

        return r'''Find c such that $Pr({0}) = Pr({1})$.'''.format(
                    expressions.relation(self._qp['question_original_interval'], var="X"),
                    expressions.relation(self._qp['question_Z_interval'], var="Z")
                )




    def solution_statement(self):
        lines = solution_lines.Lines()
        
        if self._qp['unknown_location'] == 'Z':
            interval = N_to_Z_interval(self._qp['question_original_interval'], mean=self._qp['mean'], sd=self._qp['sd'])
            value = interval.left if interval.left != -sympy.oo else interval.right
            z_score = r'\frac{{{location} - {mean}}}{{{sd}}}'.format(**self._qp)

            # e.g. Pr(X >= 13) = Pr(Z >= (13 - 15)/9) = Pr(Z >= -2/9)
            lines += r'''$Pr({0}) = Pr({1}) = Pr({2})$'''.format(
                        expressions.relation(self._qp['question_original_interval'], var="X"),
                        expressions.relation(interval, var="Z").replace(sympy.latex(value), z_score),
                        expressions.relation(interval, var="Z")
                    )
        else:
            interval = Z_to_N_interval(self._qp['question_Z_interval'], mean=self._qp['mean'], sd=self._qp['sd'])
            value = interval.left if interval.left != -sympy.oo else interval.right
            num_sds = self._qp['num_standard_deviations'] * (-1 if self._qp['flipped'] else 1)
            n_score = r'{0} \times {sd} + {mean}'.format(sympy.latex(num_sds), **self._qp)

            # e.g. Pr(Z >= -3) = Pr(X >= -3 * 7 + 40) = Pr(X >= 19)
            lines += r'''$Pr({0}) = Pr({1}) = Pr({2})$'''.format(
                        expressions.relation(self._qp['question_Z_interval'], var="Z"),
                        expressions.relation(interval, var="X").replace(sympy.latex(value), n_score),
                        expressions.relation(interval, var="X")
                    )


        if self._qp['flipped']:
            # e.g. = Pr(Z <= 2/9)
            lines += r'''$= Pr({0})$'''.format(
                        expressions.relation(opposite_interval(interval, mean=0), var="Z")
                    )

        answer = -value if self._qp['flipped'] else value

        # e.g. \therefore c = 79
        lines += r'''$\therefore c = {0}$'''.format(sympy.latex(answer))

        return lines.write()
