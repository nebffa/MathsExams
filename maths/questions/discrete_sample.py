import sympy
import random
from sympy.abc import *
from .. import all_functions, not_named_yet
from ..latex import solution_lines, expressions
from ..phrasing import item_position
import copy
import functools
import operator
import itertools
import math
from . import relationships


def sum_probabilities_string(qp, iterable, show_permutations=False):
    """Return LaTeX to represent a union of probabilities.
    """
    item_probs = []
    for sequence in iterable:
        item_prob = r'\, \cap \, '.join(['ball_{0} = {1}'.format(item_num + 1, item_value) for item_num, item_value in enumerate(sequence)])

        if show_permutations:
            prob = r'Pr({0})'.format(
                item_prob
            )
        else:
            prob = r'{0}! \times Pr({1})'.format(
                qp['num_selections'],
                item_prob
            )

        item_probs.append(prob)

    return ' + '.join(item_probs)


def list_numbers(items):
    """Return an English-readable listing of a set of numbers.
    """
    head = items[:-1]
    tail = items[-1]

    head_text = ', '.join([str(i) for i in head])
    return head_text + ' and ' + str(tail)


def union_of_probabilities(probabilities):
    """Return LaTeX to represent a union of probabilities.
    """
    return r'\ \cap \ '.join(probabilities)


@relationships.root
class NoReplacement:
    """There is currently only a version for NoReplacement - Replacement would need some modification as all the classes assume no replacement.

    Question description
    ====================

    Random selection of balls from a box, where the balls are not returned to the box.


    Real-life instances
    ===================

    2009 5: Blank slate
    """

    def __init__(self):
        self.num_lines, self.num_marks = 0, 0
        self._qp = {}

        self._qp['num_items'] = random.randint(4, 6)
        self._qp['num_selections'] = random.randint(2, 3)
        self._qp['items'] = list(range(1, self._qp['num_items'] + 1))


    def question_statement(self):
        self._qi = {}

        item_numbers = [i + 1 for i in range(self._qp['num_items'])]
        item_text = list_numbers(item_numbers)

        if self._qp['num_selections'] == 2:
            additional_balls, is_or_are = 'second', 'is'
        elif self._qp['num_selections'] == 3:
            additional_balls, is_or_are = 'second and third', 'are'

        return r'''${num_items}$ identical balls are numbered {item_text} and put into a box. A ball is randomly drawn from the box, and not returned to the box.
                    A {additional_balls} balls {is_or_are} then randomly drawn from the box.'''.format(
                        num_items=self._qp['num_items'],
                        item_text=item_text,
                        additional_balls=additional_balls,
                        is_or_are=is_or_are
                    )


@relationships.is_child_of(NoReplacement)
class SpecificPermutation:
    """Question description
    ====================

    Find the probability that a specific permutation of selections occurs.


    Real-life instances
    ===================

    2009 5a: [4 lines] [1 mark]
    """

    def __init__(self, part):
        self.num_lines, self.num_marks = 4, 1

        self._qp = copy.copy(part._qp)

    def question_statement(self):
        self._qp['choices'] = random.sample(self._qp['items'], self._qp['num_selections'])

        values_text = list_numbers(self._qp['choices'])

        return r'''Find the probability that the values of the balls are {values_text}, respectively.'''.format(values_text=values_text)

    def solution_statement(self):
        lines = solution_lines.Lines()

        probabilities = ['ball_{ball_number} = {ball_value}'.format(ball_number=index + 1, ball_value=ball_value) for
            index, ball_value in enumerate(self._qp['choices'])]
        probabilities_union = union_of_probabilities(probabilities)

        fractions = []
        for n_already_chosen in range(self._qp['num_selections']):
            n_items = len(self._qp['items'])
            probability = sympy.Rational(1, n_items - n_already_chosen)
            fractions.append(probability)

        probabilities_multiplied = r' \times '.join(map(sympy.latex, fractions))

        answer = functools.reduce(operator.mul, fractions)

        lines += r'$Pr({probabilities_union}) = {probabilities_multiplied} = {answer}$'.format(
            probabilities_union=probabilities_union,
            probabilities_multiplied=probabilities_multiplied,
            answer=sympy.latex(answer)
        )

        return lines.write()


@relationships.is_child_of(NoReplacement)
class DiscreteSum:

    @staticmethod
    def good_number_of_permutations(num_permutations):
        """State whether there is too little or too much work for the student to do on this question.
        """
        # this gives us a range between 4 and 12 - 4 is when we have 2 x 2! permutations, 12 is when we have 2 x 3! permutations
        too_few, too_many = 3, 13

        return too_few < num_permutations < too_many

    def appropriate_sums(self):
        """Return a sum that will make the question worth doing.

        The sum is used in the questions - e.g. "Find the probability that the sum of the numbers on the 3 balls is 10."

        If the sum is too small or too big, then there is too little or too much work for the student to do, respectively.

        Here we work out which sums will be appropriate for the question.
        """
        # the number of items selected is self._qp['num_selections']. In this comment we call it "n"
        # the smallest possible sum of n items is the smallest n items - self._qp['items'][:n]
        smallest_set = self._qp['items'][:self_qp['num_selections']]
        # the largest possible sum of n items is the largest n items - self._qp['items'][-n:]
        largest_set = self._qp['items'][-self._qp['num_selections']:]

        smallest_sum, largest_sum = sum(smallest_set), sum(largest_set)
        sum_options = range(smallest_sum, largest_sum)

        possible_ball_selection_orders = list(itertools.permutations(self._qp['items'], self._qp['num_selections']))
        final_sum_options = []
        for possible_sum in sum_options:
            num_valid_permutations = len(list(filter(lambda perm: sum(perm) == possible_sum, possible_ball_selection_orders)))

            if DiscreteSum.good_number_of_permutations(num_valid_permutations):
                final_sum_options.append(possible_sum)

        return final_sum_options


@relationships.is_child_of(NoReplacement)
class Sum(DiscreteSum):
    def __init__(self, part):
        # 2009 Q5b [5 lines] [1 mark]
        self.num_lines, self.num_marks = 5, 1 
        self._qp = copy.copy(part._qp)
        
        self._qp['sum'] = random.choice(self.appropriate_sums())


    def question_statement(self):
        return r'''What is the probability that the sum of the numbers on the {0} balls is ${1}$?'''.format(
                    self._qp['num_selections'],
                    self._qp['sum']
                )


    def solution_statement(self):
        lines = solution_lines.Lines()

        combinations = itertools.combinations(self._qp['items'], self._qp['num_selections'])
        valid_combinations = list(filter(lambda perm: sum(perm) == self._qp['sum'], combinations))

        # e.g. Pr(sum = 14) = 3! * Pr(ball1 = 3 and ball2 = 5 and ball3 = 6)
        lines += r'$Pr(\text{{sum}} = {0}) = {1}$'.format(
                    self._qp['sum'],
                    sum_probabilities_string(self._qp, valid_combinations)
                )

        individual_prob_instance = sympy.Rational(1, math.factorial(self._qp['num_items']) / (math.factorial(self._qp['num_items'] - self._qp['num_selections'])))
        prob_instance = r'{0} \times {1}'.format(math.factorial(self._qp['num_selections']), sympy.latex(individual_prob_instance))

        # e.g. = 6 * (1/120) + 6 * (1/120)
        lines += r'$= {0}$'.format(' + '.join([prob_instance] * len(valid_combinations)))

        answer = individual_prob_instance * math.factorial(self._qp['num_selections']) * len(valid_combinations)
        # e.g. = 1/20
        lines += r'$= {0}$'.format(sympy.latex(answer))

        return lines.write()


@relationships.is_child_of(NoReplacement)
class ConditionalSum(DiscreteSum):
    def __init__(self, part):
        # 2009 Q5c [4 lines] [2 marks]
        self._qp = copy.copy(part._qp)
        self.num_lines, self.num_marks = (4, 1) if self._qp['num_selections'] == 2 else (5, 2)

        self._qp['sum'] = random.choice(self.appropriate_sums())
        self._qp['ball_index'] = random.randint(1, self._qp['num_selections'])

        # if we have a sum of 10 and the only way to achieve this sum is by (1, 4, 5) then we can't select a ball value of 2 or 3
        # so we find only the possible values (possible_values here) that we can select from
        permutations = list(itertools.permutations(self._qp['items'], self._qp['num_selections']))        
        valid_permutations = list(filter(lambda perm: sum(perm) == self._qp['sum'], permutations))
        possible_values = list(itertools.chain.from_iterable(valid_permutations))

        self._qp['ball_value'] = random.choice(possible_values)


    def question_statement(self):
        self._qi = {}

        nth_ball = item_position.int_to_nth(self._qp['ball_index'])

        return r'''Given that the sum of the numbers on the ${num_selections}$ balls is ${sum}$, what is the probability that the {nth_ball} is numbered ${ball_value}$?'''.format(
                        nth_ball=nth_ball,
                        **self._qp
                    )


    def solution_statement(self):
        lines = solution_lines.Lines()


        combinations = list(itertools.combinations(self._qp['items'], self._qp['num_selections']))
        valid_givee_combinations = list(filter(lambda permutation: sum(permutation) == self._qp['sum'] and permutation[self._qp['ball_index'] - 1] == self._qp['ball_value'], combinations))
        valid_given_combinations = list(filter(lambda permutation: sum(permutation) == self._qp['sum'], combinations))

        # e.g. Pr(sum = 14) = 3! * Pr(ball1 = 2 and ball2 = 5 and ball3 = 6) + 3! * Pr(ball1 = 3 and ball2 = 4 and ball3 = 6)
        lines += r'$Pr(\text{{sum}} = {0}) = {1}$'.format(
                    self._qp['sum'],
                    sum_probabilities_string(self._qp, valid_given_combinations)
                )

        individual_prob_instance = sympy.Rational(1, math.factorial(self._qp['num_items']) / (math.factorial(self._qp['num_items'] - self._qp['num_selections'])))
        prob_instance = r'{0} \times {1}'.format(math.factorial(self._qp['num_selections']), sympy.latex(individual_prob_instance))
        # e.g. = 6 * (1/120) + 6 * (1/120)
        lines += r'$= {0}$'.format(' + '.join([prob_instance] * len(valid_given_combinations)))

        given_answer = individual_prob_instance * math.factorial(self._qp['num_selections']) * len(valid_given_combinations)
        # e.g. = 1/10
        lines += r'$= {0}$'.format(sympy.latex(given_answer))

        permutations = list(itertools.permutations(self._qp['items'], self._qp['num_selections']))
        valid_givee_permutations = list(filter(lambda permutation: sum(permutation) == self._qp['sum'] and permutation[self._qp['ball_index'] - 1] == self._qp['ball_value'], permutations))
        # e.g. Pr(ball3  = 6 and sum = 13) = Pr(ball1 = 2 and ball2 = 5 and ball3 = 6) + Pr(ball1 = 3 and ball2 = 4 and ball3 = 6) + ...
        lines += r'$Pr(ball_{{{ball_index}}} = {ball_value} \, \cap \, \text{{sum}} = {{{sum}}}) = {0}$'.format(
                    sum_probabilities_string(self._qp, valid_givee_permutations, show_permutations=True),
                    **self._qp
                )

        givee_answer = individual_prob_instance * len(valid_givee_permutations)
        # e.g. = 1/30
        lines += r'$= {0}$'.format(sympy.latex(givee_answer))



        givee = 'ball_{0} = {1}'.format(self._qp['ball_index'], self._qp['ball_value'])
        given = 'sum = {0}'.format(self._qp['sum'])

        conditional_probability = expressions.conditional_probability(
                givee=givee, 
                given=given
            )

        # e.g. Pr(ball3 = 6 | sum = 13) = Pr(ball3 = 6 and sum = 13) / Pr(sum = 13) = (1/30) / (1/10) = 1/3
        lines += r'$Pr({0} | {1}) = {2} = \frac{{{3}}}{{{4}}} = {5}$'.format(
            givee,
            given,
            conditional_probability,
            sympy.latex(givee_answer),
            sympy.latex(given_answer),
            sympy.latex(givee_answer / given_answer)
        )


        return lines.write()
