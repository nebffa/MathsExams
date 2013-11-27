import sympy
import random
from sympy.abc import *
from maths import all_functions, not_named_yet
from maths.latex import solution_lines
import copy
import functools
import operator
import itertools
import math


class NoReplacement:
    def __init__(self):
        self.num_lines, self.num_marks = 0, 0
        self._qp = {}

        self._qp['num_items'] = random.randint(4, 6)
        self._qp['num_selections'] = random.randint(2, 3)
        self._qp['items'] = list(range(1, self._qp['num_items'] + 1))


    def question_statement(self):
        self._qi = {}

        
        item_numbers = ', '.join( ['${0}$'.format(i + 1) for i in range(self._qp['num_items'])[:-1]]) + ' and ' + '${0}$'.format(self._qp['num_items']) 

        if self._qp['num_selections'] == 2:
            additional_balls, is_or_are = 'second', 'is'
        elif self._qp['num_selections'] == 3:
            additional_balls, is_or_are = 'second and third', 'are'


        return r'''${num_items}$ identical balls are numbered {item_numbers} and put into a box. A ball is randomly drawn from the box, and not returned to the box. 
                    A {additional_balls} balls {is_or_are} then randomly drawn from the box.'''.format(
                        num_items=self._qp['num_items'],
                        item_numbers=item_numbers,
                        additional_balls=additional_balls,
                        is_or_are=is_or_are
                    )


    def solution_statement(self):
        lines = solution_lines.Lines()
        
        return lines.write()


class SpecificPermutation:
    def __init__(self, part):
        self.num_lines, self.num_marks = 4, 1

        self._qp = copy.copy(part._qp)

    def question_statement(self):
        self._qp['choices'] = random.sample(self._qp['items'], self._qp['num_selections'])

        
        values = ', '.join(['${0}$'.format(i) for i in self._qp['choices'][:-1]]) + ' and ' + '${0}$'.format(self._qp['choices'][-1])

        return r'''Find the probability that the values of the balls are {0}, respectively.'''.format(values)

    def solution_statement(self):
        lines = solution_lines.Lines()
        
        symbolic_pr_chain = r'\ \cap \ '.join(['ball_{0} = {1}'.format(index + 1, ball_value) for index, ball_value in enumerate(self._qp['choices'])])

        fractions = [sympy.Rational(1, len(self._qp['items']) - i) for i in range(self._qp['num_selections'])]
        pr_chain = r' \times '.join([sympy.latex(frac) for frac in fractions])

        answer = functools.reduce(operator.mul, fractions)

        lines += r'$Pr({0}) = {1} = {2}$'.format(
            symbolic_pr_chain,
            pr_chain,
            sympy.latex(answer)
        )

        return lines.write()


class Sum:
    def __init__(self, part):
        self.num_lines, self.num_marks = 5, 1 
        self._qp = copy.copy(part._qp)

        ball_average = sum(self._qp['items']) / len(self._qp['items'])

        sum_average = int(ball_average * self._qp['num_selections'])

        self._qp['sum'] = random.randint(sum_average - 1, sum_average + 1)


    def question_statement(self):
        return r'''What is the probability that the sum of the numbers on the {0} balls is ${1}$?'''.format(
                    self._qp['num_selections'],
                    self._qp['sum']
                )


    def solution_statement(self):
        lines = solution_lines.Lines()
        
        combinations = itertools.combinations(self._qp['items'], self._qp['num_selections'])
        valid_combinations = list(filter(lambda perm: sum(perm) == self._qp['sum'], combinations))

        item_probs = []
        for combination in valid_combinations:
            item_prob = '\, \cap \, '.join(['ball_{0} = {1}'.format(item_num, item_value) for item_num, item_value in enumerate(combination)])

            prob = r'{0}! \times Pr({1})'.format(
                self._qp['num_selections'],
                item_prob
            )

            item_probs.append(prob)


        lines += r'$Pr(\text{{sum}} = {0}) = {1}$'.format(
                    self._qp['sum'],
                    ' + '.join(item_probs)
                )

        individual_prob_instance = sympy.Rational(1, math.factorial(self._qp['num_items']) / (math.factorial(self._qp['num_items'] - self._qp['num_selections'])))
        prob_instance = r'{0} \times {1}'.format(math.factorial(self._qp['num_selections']), sympy.latex(individual_prob_instance))

        lines += r'$= {0}$'.format('\, + \, '.join([prob_instance] * len(valid_combinations)))

        lines += r'$= {0}$'.format(sympy.latex(individual_prob_instance * math.factorial(self._qp['num_selections']) * len(valid_combinations)))




        return lines.write()
