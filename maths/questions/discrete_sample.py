import sympy
import random
from ..latex import solution_lines, expressions
from ..phrasing import item_position, items
import copy
import functools
import operator
import itertools
import math
from . import relationships


@relationships.root
class NoReplacement(relationships.QuestionPart):
    """There is currently only a version for NoReplacement - Replacement would need some modification as all the classes assume no replacement.

    Question description
    ====================

    Random selection of items from a box, where the items are not returned to the box.


    Real-life instances
    ===================

    2009 5: [Blank slate]
    """

    def __init__(self):
        self.num_lines, self.num_marks = 0, 0
        self._qp = {}

        self._qp['n_items'] = random.randint(4, 6)
        self._qp['n_selections'] = random.randint(2, 3)
        self._qp['items'] = list(range(1, self._qp['n_items'] + 1))

    def question_statement(self):
        item_numbers = [i + 1 for i in range(self._qp['n_items'])]
        item_text = items.list_numbers(item_numbers)

        if self._qp['n_selections'] == 2:
            additional_balls, is_or_are = 'second', 'is'
        elif self._qp['n_selections'] == 3:
            additional_balls, is_or_are = 'second and third', 'are'

        return r'''${n_items}$ identical balls are numbered {item_text} and put into a box. A ball is randomly drawn from the box, and not returned to the box.
            A {additional_balls} balls {is_or_are} then randomly drawn from the box.'''.format(
            n_items=self._qp['n_items'],
            item_text=item_text,
            additional_balls=additional_balls,
            is_or_are=is_or_are
        )


@relationships.is_child_of(NoReplacement)
class SpecificPermutation(relationships.QuestionPart):
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
        self._qp['choices'] = random.sample(self._qp['items'], self._qp['n_selections'])

        values_text = items.list_numbers(self._qp['choices'])

        return r'''Find the probability that the values of the balls are {values_text}, respectively.'''.format(values_text=values_text)

    def solution_statement(self):
        lines = solution_lines.Lines()

        probabilities = ['ball_{ball_number} = {ball_value}'.format(ball_number=index + 1, ball_value=ball_value) for
                         index, ball_value in enumerate(self._qp['choices'])]
        probabilities_union = expressions.union_of_probabilities(probabilities)

        fractions = []
        for n_already_chosen in range(self._qp['n_selections']):
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


class DiscreteSum():
    """A helper class to prevent code duplication between Sum and ConditionalSum.
    """

    @staticmethod
    def good_number_of_permutations(num_permutations):
        """State whether there is too little or too much work for the student to do on this question.
        """

        # this gives us a range between 4 and 12 - 4 is when we have 2 x 2! permutations, 12 is when we have 2 x 3! permutations
        too_few, too_many = 3, 13

        return too_few < num_permutations < too_many

    @staticmethod
    def sum_combination_probabilities(combinations):
        """Return LaTeX to represent the sum of the probabilities of selecting particular
        combinations of items.
        """

        probabilities = []
        n_selections = len(combinations[0])
        for combination in combinations:
            event = expressions.union_of_probabilities(['ball_{ball_number} = {ball_value}'.format(
                ball_number=index + 1, ball_value=item_value) for index, item_value in enumerate(combination)])

            probability = r'{n_selections}! \times Pr({event})'.format(
                n_selections=n_selections,
                event=event
            )

            probabilities.append(probability)

        return ' + '.join(probabilities)

    @staticmethod
    def sum_permutation_probabilities(permutations):
        """Return LaTeX to represent the sum of the probabilities of selecting particular
        permutations of items.
        """

        probabilities = []
        for permutation in permutations:
            event = expressions.union_of_probabilities(['ball_{ball_number} = {ball_value}'.format(
                ball_number=index + 1, ball_value=item_value) for index, item_value in enumerate(permutation)])

            probabilities.append(
                r'Pr({event})'.format(event=event)
            )

        return ' + '.join(probabilities)

    def single_combination_probability(self):
        """Return the probability of an arbitrary combination of item selections occurring.

        e.g. if n_selections = 3 and n_items = 5:
        The probability of any item being selected first is 1/5
        The probability of any item being selected second is 1/4
        The probabiltiy of any item being selected third is 1/3

        Therefore the probability of any combination occuring is 1/60
        """

        probability_of_a_single_combination = 1
        for i in range(self._qp['n_selections']):
            probability_of_a_single_combination *= sympy.Rational(1, self._qp['n_items'] - i)

        return probability_of_a_single_combination

    def appropriate_sums(self):
        """Return a sum that will make the question worth doing.

        The sum is used in the questions - e.g. "Find the probability that the sum of the numbers on the 3 balls is 10."

        If the sum is too small or too big, then there is too little or too much work for the student to do, respectively.

        Here we work out which sums will be appropriate for the question.
        """

        smallest_set = self._qp['items'][:self._qp['n_selections']]
        largest_set = self._qp['items'][-self._qp['n_selections']:]

        smallest_sum, largest_sum = sum(smallest_set), sum(largest_set)
        possible_ball_sums = range(smallest_sum, largest_sum)

        possible_ball_selection_orders = list(itertools.permutations(self._qp['items'], self._qp['n_selections']))
        appropriate_options = []
        for possible_sum in possible_ball_sums:
            valid_permutations = [i for i in possible_ball_selection_orders if sum(i) == possible_sum]
            num_valid_permutations = len(valid_permutations)

            if DiscreteSum.good_number_of_permutations(num_valid_permutations):
                appropriate_options.append(possible_sum)

        return appropriate_options


@relationships.is_child_of(NoReplacement)
class Sum(relationships.QuestionPart, DiscreteSum):
    """Question description
    ====================

    Find the probability that the sum of the selections is a particular value.


    Real-life instances
    ===================

    2009 5b: [5 lines] [1 mark]
    """

    def __init__(self, part):
        self.num_lines, self.num_marks = 5, 1
        self._qp = copy.copy(part._qp)

        self._qp['sum'] = random.choice(self.appropriate_sums())

    def question_statement(self):
        return r'''What is the probability that the sum of the numbers on the {n_selections} balls is ${sum}$?'''.format(
            **self._qp
        )

    def solution_statement(self):
        lines = solution_lines.Lines()

        ball_combinations = itertools.combinations(self._qp['items'], self._qp['n_selections'])
        valid_total_sum_combinations = [i for i in ball_combinations if sum(i) == self._qp['sum']]

        # e.g. Pr(sum = 14) = 3! * Pr(ball1 = 3 and ball2 = 5 and ball3 = 6)
        lines += r'$Pr(\text{{sum}} = {sum}) = {sum_of_probabilities}$'.format(
            sum=self._qp['sum'],
            sum_of_probabilities=self.__class__.sum_combination_probabilities(valid_total_sum_combinations)
        )

        probability_of_a_single_combination = self.single_combination_probability()
        prob_instance = r'{n_valid_permutations} \times {probability_of_a_single_combination}'.format(
            n_valid_permutations=math.factorial(self._qp['n_selections']),
            probability_of_a_single_combination=sympy.latex(probability_of_a_single_combination)
        )

        # e.g. = 6 * (1/120) + 6 * (1/120)
        lines += r'$= {probabilities_sum}$'.format(
            probabilities_sum=' + '.join([prob_instance] * len(valid_total_sum_combinations))
        )

        answer = probability_of_a_single_combination * math.factorial(self._qp['n_selections']) * len(valid_total_sum_combinations)
        # e.g. = 1/20
        lines += r'$= {answer}$'.format(answer=sympy.latex(answer))

        return lines.write()


@relationships.is_child_of(NoReplacement)
class ConditionalSum(relationships.QuestionPart, DiscreteSum):
    """Question description
    ====================

    Find the probability that a particular item number has a particular value, given the sum of the selections.


    Real-life instances
    ===================

    2009 5c: [4 lines] [2 marks]
    """

    def __init__(self, part):
        self._qp = copy.copy(part._qp)
        self.num_lines, self.num_marks = (4, 1) if self._qp['n_selections'] == 2 else (5, 2)

        self._qp['sum'] = random.choice(self.appropriate_sums())
        self._qp['ball_index'] = random.randint(1, self._qp['n_selections'])

        # if we have a sum of 10 and the only way to achieve this sum is by (1, 4, 5) then we can't select a ball value of 2 or 3
        # so we find only the possible values (possible_values here) that we can select from
        item_permutations = itertools.permutations(self._qp['items'], self._qp['n_selections'])
        valid_item_permutations = (i for i in item_permutations if sum(i) == self._qp['sum'])
        valid_ball_values = set(itertools.chain.from_iterable(valid_item_permutations))

        self._qp['ball_value'] = random.choice(list(valid_ball_values))

    def question_statement(self):
        nth_ball = item_position.int_to_nth(self._qp['ball_index'])

        return r'Given that the sum of the numbers on the ${n_selections}$ balls is ${sum}$, what is the probability that the \
            {nth_ball} is numbered ${ball_value}$?'.format(
            nth_ball=nth_ball,
            **self._qp
        )

    def solution_statement(self):
        lines = solution_lines.Lines()

        ball_combinations = list(itertools.combinations(self._qp['items'], self._qp['n_selections']))
        valid_total_sum_combinations = [i for i in ball_combinations if sum(i) == self._qp['sum']]

        # e.g. Pr(sum = 14) = 3! * Pr(ball1 = 2 and ball2 = 5 and ball3 = 6) + 3! * Pr(ball1 = 3 and ball2 = 4 and ball3 = 6)
        lines += r'$Pr(\text{{sum}} = {0}) = {1}$'.format(
            self._qp['sum'],
            self.__class__.sum_combination_probabilities(valid_total_sum_combinations)
        )

        probability_of_a_single_combination = self.single_combination_probability()

        # e.g. = 6 * (1/120) + 6 * (1/120)
        prob_instance = r'{n_permutations} \times {probability_of_combination}'.format(
            n_permutations=math.factorial(self._qp['n_selections']),
            probability_of_combination=sympy.latex(probability_of_a_single_combination)
        )
        lines += r'$= {probabilities}$'.format(
            probabilities=' + '.join([prob_instance] * len(valid_total_sum_combinations))
        )

        given_result = probability_of_a_single_combination * math.factorial(self._qp['n_selections']) * len(valid_total_sum_combinations)
        # e.g. = 1/10
        lines += r'$= {givee_result}$'.format(givee_result=sympy.latex(given_result))

        ball_permutations = itertools.permutations(self._qp['items'], self._qp['n_selections'])
        valid_ball_permutations = [i for i in ball_permutations if sum(i) == self._qp['sum']]
        valid_givee_permutations = [i for i in valid_ball_permutations if i[self._qp['ball_index'] - 1] == self._qp['ball_value']]

        # e.g. Pr(ball3  = 6 and sum = 13) = Pr(ball1 = 2 and ball2 = 5 and ball3 = 6) + Pr(ball1 = 3 and ball2 = 4 and ball3 = 6) + ...
        lines += r'$Pr(ball_{{{ball_index}}} = {ball_value} \, \cap \, \text{{sum}} = {{{sum}}}) = {sum_of_probabilities}$'.format(
            sum_of_probabilities=self.__class__.sum_permutation_probabilities(valid_givee_permutations),
            **self._qp
        )

        # e.g. = 1/30
        givee_result = probability_of_a_single_combination * len(valid_givee_permutations)
        lines += r'$= {givee_result}$'.format(givee_result=sympy.latex(givee_result))

        givee_event = 'ball_{ball_index} = {ball_value}'.format(**self._qp)
        given_event = 'sum = {sum}'.format(**self._qp)

        conditional_probability = expressions.conditional_probability(
            givee=givee_event,
            given=given_event
        )

        # e.g. Pr(ball3 = 6 | sum = 13) = Pr(ball3 = 6 and sum = 13) / Pr(sum = 13) = (1/30) / (1/10) = 1/3
        lines += r'$Pr({givee_event} | {given_event}) = {conditional_probability} = \frac{{{givee_result}}}{{{given_result}}} = {answer}$'.format(
            givee_event=givee_event,
            given_event=given_event,
            conditional_probability=conditional_probability,
            givee_result=sympy.latex(givee_result),
            given_result=sympy.latex(given_result),
            answer=sympy.latex(givee_result / given_result)
        )

        return lines.write()
