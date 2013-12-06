import sympy
import random
from sympy.abc import *
from maths import all_functions, not_named_yet
from maths.latex import solution_lines, expressions
from maths.utils import functions


class NormalDistribution:
    def __init__(self):
        self._qp = {}

        self._qp['mean'] = random.choice([5*i for i in range(1, 21)])
        self._qp['sd'] = random.choice(list(range(5, 11)))
        self._qp['variance'] = self._qp['sd']**2


class SimpleNormalDistribution(NormalDistribution):
    def __init__(self):
        self.num_lines, self.num_marks = 4, -1
        super(SimpleNormalDistribution, self).__init__()

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
                    expressions.relation(self._qp['interval']),
                    self._qp['value'],
                    expressions.relation(self._qp['opposite_interval']),
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

        
        lines += r'$Pr({0}) = Pr({1}) = Pr({2}) - Pr({3})$'.format(
                    expressions.relation(self._qp['opposite_interval']),
                    expressions.relation(some_interval),
                    expressions.relation(opposite_half_interval),
                    expressions.relation(last_interval),
                )

        
        lines += r'$= ({0}) - ({1}) = {2}$'.format(
                    sympy.latex(left_pr),
                    sympy.latex(right_pr),
                    sympy.latex(self._qp['answer'])
                )

        return lines.write()
