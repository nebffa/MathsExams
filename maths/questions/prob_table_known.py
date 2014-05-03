import random
import sympy
from sympy import GreaterThan, LessThan, StrictGreaterThan, StrictLessThan
from .. import not_named_yet
from ..phrasing import first_names
from ..latex import expressions, table, solutions
from ..probability.discrete import prob_table
from . import relationships
import operator
from collections import OrderedDict
import functools
import copy
import itertools


@relationships.root
class ProbTableKnown(relationships.QuestionPart):
    """
    Question description
    ====================

    Setup a probability table where all keys and values are known.


    Real-life instances
    ===================

    2008 7: [Blank Slate]
    2009 7: [Blank Slate]
    2012 4: [Blank Slate]
    """

    def __init__(self):
        self.num_lines, self.num_marks = 0, 0
        self._qp, self._qi = {}, {}

        options = list(range(random.randint(4, 5)))

        partition = random.choice([i for i in not_named_yet.partition(10) if len(i) == len(options)])
        partition = list(partition)

        random.shuffle(partition)
        partition = [sympy.Rational(i, 10) for i in partition]

        self._qp['prob_table'] = OrderedDict(list(zip(options, partition)))

        question_contexts = {
            'green traffic lights': '''When {first_name} drives to work each morning they pass a number of intersections with traffic lights. The number X of
                traffic lights that are green when {first_name} is driving to work is a random variable with probability distribution given by''',
            'telephone calls': '''Every day, the number X of telephone calls that {first_name} receives at work is a random variable with probability
                distribution given by''',
            'free marshmallows': '''Every day, {first_name} goes to {possessive_pronoun} local cafe for lunch and orders a hot chocolate. The number
            X of free marshmallows that are included with the hot chocolate is a random variable with probability distribution given by'''}
        self._qi['item'] = random.choice(list(question_contexts.keys()))
        self._qi['question_context'] = question_contexts[self._qi['item']]

        self._qi['first_name'], gender = first_names.random_first_name(gender=True)
        self._qi['possessive_pronoun'] = first_names.possessive_pronoun(gender)

    def question_statement(self):
        text = self._qi['question_context'].format(**self._qi)
        return text + r'\\' + table.probability_table(self._qp['prob_table']) + r'\\'


@relationships.is_child_of(ProbTableKnown)
class Property(relationships.QuestionPart):
    """
    Question description
    ====================

    Calculate the mean, variance or mode of a probability table.


    Real-life instances
    ===================

    2008 7a: Calculate the mode [2 lines] [1 mark]
    2009 7b: Calculate the variance [7 lines] [3 marks]
    2012 4a: Calculate the mean [4 lines] [2 marks]
    """

    def __init__(self, part):
        self._qp = copy.deepcopy(part._qp)

        self._qp['question_type'] = random.choice(['mean', 'variance', 'mode'])

        if self._qp['question_type'] == 'mean':
            self.num_lines, self.num_marks = 4, 2
            self._qp['answer'] = prob_table.expectation_x(self._qp['prob_table'])

        elif self._qp['question_type'] == 'variance':
            self.num_lines, self.num_marks = 7, 3
            self._qp['answer'] = prob_table.expectation_x(self._qp['prob_table'], power=2) - \
                prob_table.expectation_x(self._qp['prob_table']) ** 2

        elif self._qp['question_type'] == 'mode':
            self.num_lines, self.num_marks = 2, 1
            self._qp['answer'] = prob_table.mode(self._qp['prob_table'])

    def question_statement(self):
        if self._qp['question_type'] == 'mean':
            return r'Find E(X), the mean of X.'
        elif self._qp['question_type'] == 'variance':
            return r'Find Var(X), the variance of X.'
        elif self._qp['question_type'] == 'mode':
            return r'Find the mode of X.'

    def solution_statement(self):
        lines = solutions.Lines()

        if self._qp['question_type'] == 'mean':
            lines += r'$E(X) = \sum\limits_{{i=1}}^{{n}} x_{{i}} \times Pr(X = x_{{i}})$'

            lines += r'$= {expectation_of_x} = {answer}$'.format(
                expectation_of_x=expressions.discrete_expectation_x(self._qp['prob_table']),
                answer=self._qp['answer']
            )

        elif self._qp['question_type'] == 'variance':

            lines += r'$Var(X) = E(X^2) - (E(X))^2$'

            lines += r'$= [{expectation_of_x_squared}] - [{expectation_of_x}]^2$'.format(
                expectation_of_x_squared=expressions.discrete_expectation_x_squared(self._qp['prob_table']),
                expectation_of_x=expressions.discrete_expectation_x(self._qp['prob_table'])
            )

            expectation_of_x = prob_table.expectation_x(self._qp['prob_table'])
            expectation_of_x_squared = prob_table.expectation_x(self._qp['prob_table'], power=2)
            lines += r'$= {expectation_of_x_squared} - {expectation_of_x}^2 = {answer}$'.format(
                expectation_of_x_squared=sympy.latex(expectation_of_x_squared),
                expectation_of_x=sympy.latex(expectation_of_x),
                answer=sympy.latex(self._qp['answer'])
            )

        elif self._qp['question_type'] == 'mode':
            lines += r'${answer}$'.format(
                answer=prob_table.mode(self._qp['prob_table'])
            )

        return lines.write()


@relationships.is_child_of(ProbTableKnown)
class Multinomial(relationships.QuestionPart):
    """
    Question description
    ====================

    Calculate the probability of the outcome being the same on each day.


    Real-life instances
    ===================

    2008 7b: [5 lines] [2 marks]
    2012 4b: [4 lines] [1 mark]
    """

    def __init__(self, part):
        self._qp = copy.deepcopy(part._qp)
        self._qi = copy.deepcopy(part._qi)

        self._qp['question_type'] = random.choice(['one_x', 'any_x'])

        if self._qp['question_type'] == 'one_x':
            self.num_lines, self.num_marks = 4, 1
            self._qp['x_value'] = random.choice(list(self._qp['prob_table'].keys()))
            self._qp['n_days'] = 3

        elif self._qp['question_type'] == 'any_x':
            self.num_lines, self.num_marks = 5, 2
            self._qp['n_days'] = random.randint(2, 3)

    def question_statement(self):
        combined_dict = dict(itertools.chain(self._qp.items(), self._qi.items()))

        if self._qp['question_type'] == 'one_x':
            return r'''What is the probability that the number of {item} {first_name} gets on each of
                {n_days} consecutive days is {x_value}?'''.format(
                **combined_dict
            )

        elif self._qp['question_type'] == 'any_x':
            return r'''What is the probability that the number of {item} {first_name} gets is the same on each
                of {n_days} consecutive days?'''.format(
                **combined_dict
            )

    def solution_statement(self):
        lines = solutions.Lines()

        if self._qp['question_type'] == 'one_x':
            answer = self._qp['prob_table'][self._qp['x_value']] ** self._qp['n_days']
            lines += r'$Pr(X = {x_value}$, {n_days} days in a row$) = {probability_of_x}^{n_days} = {answer}.$'.format(
                x_value=self._qp['x_value'],
                n_days=self._qp['n_days'],
                probability_of_x=sympy.latex(self._qp['prob_table'][self._qp['x_value']]),
                answer=sympy.latex(answer)
            )

        elif self._qp['question_type'] == 'any_x':
            sum_of_probabilities = ' + '.join([r'''Pr(X = {0})^{1}'''.format(k, self._qp['n_days']) for k in self._qp['prob_table']])
            lines += r'''$Pr(X$ is the same number {n_days} days in a row$) = {sum_of_probabilities}$'''.format(
                n_days=self._qp['n_days'],
                sum_of_probabilities=sum_of_probabilities
            )

            sum_of_probabilities = ' + '.join(['({0})^{1}'.format(sympy.latex(v), self._qp['n_days']) for v in self._qp['prob_table'].values()])
            answer = sum(v ** self._qp['n_days'] for v in self._qp['prob_table'].values())
            lines += r'''$= {sum_of_probabilities} = {answer}$'''.format(
                sum_of_probabilities=sum_of_probabilities,
                answer=sympy.latex(answer)
            )

        return lines.write()


@relationships.is_child_of(ProbTableKnown)
class Conditional(relationships.QuestionPart):
    """
    Question description
    ====================

    Find the probability of one event given another event.

    e.g. Pr(X > 1 | X < 3)


    Real-life instances
    ===================

    2009 7a: [4 lines] [2 marks]
    """

    def __init__(self, part):
        self._qp = copy.deepcopy(part._qp)

        self.num_lines, self.num_marks = 4, 2

        # if we have a conditional probability:
        #       Pr(X > 1 | X <= 3)
        # I then refer to 3 as the conditional major, i.e. the section of the universe we are limited to
        # and 1 as the conditional minor, i.e. the section of the now-limited universe we are calculating a probability for
        self._qp['conditional_major_relational_operator'] = random.choice([GreaterThan, LessThan])
        self._qp['conditional_minor_relational_operator'] = random.choice([GreaterThan, LessThan, StrictGreaterThan, StrictLessThan])
        if self._qp['conditional_major_relational_operator'] == GreaterThan:
            self._qp['major_bound'] = min(self._qp['prob_table']) + 1
            self._qp['minor_bound'] = random.randint(min(self._qp['prob_table']) + 2, max(self._qp['prob_table']) - 1)
        else:
            self._qp['major_bound'] = max(self._qp['prob_table']) - 1
            self._qp['minor_bound'] = random.randint(min(self._qp['prob_table']) + 1, max(self._qp['prob_table']) - 2)

        major_domain = [k for k in self._qp['prob_table'] if self._qp['conditional_major_relational_operator'](k, self._qp['major_bound'])]
        minor_domain = [k for k in major_domain if self._qp['conditional_minor_relational_operator'](k, self._qp['minor_bound'])]

        self._qp['pr_major'] = sum(self._qp['prob_table'][k] for k in major_domain)
        self._qp['pr_minor'] = sum(self._qp['prob_table'][k] for k in minor_domain)

    def question_statement(self):
        return r'''Find $Pr(X {minor_relational_operator} {minor_bound} \,|\, X {major_relational_operator} {major_bound})$.'''.format(
            minor_relational_operator=self._qp['conditional_minor_relational_operator'].rel_op,
            minor_bound=self._qp['minor_bound'],
            major_relational_operator=self._qp['conditional_major_relational_operator'].rel_op,
            major_bound=self._qp['major_bound']
        )

    def solution_statement(self):
        lines = solutions.Lines()

        lines += r'''$Pr(X {minor_relational_operator} {minor_bound} \,|\, X {major_relational_operator} {major_bound}) =
            \frac{{Pr(X {minor_relational_operator} {minor_bound} \,\cap\, X {major_relational_operator} {major_bound})}}
            {{Pr(X {major_relational_operator} {major_bound})}}$'''.format(
            minor_relational_operator=self._qp['conditional_minor_relational_operator'].rel_op,
            minor_bound=self._qp['minor_bound'],
            major_relational_operator=self._qp['conditional_major_relational_operator'].rel_op,
            major_bound=self._qp['major_bound']
        )

        lines += r'''$= \frac{{{minor_probability}}}{{{major_probability}}} = {answer}$'''.format(
            minor_probability=sympy.latex(self._qp['pr_minor']),
            major_probability=sympy.latex(self._qp['pr_major']),
            answer=sympy.latex(self._qp['pr_minor'] / self._qp['pr_major'])
        )

        return lines.write()


@relationships.is_child_of(ProbTableKnown)
class Cumulative(relationships.QuestionPart):
    """
    Question description
    ====================

    Calculate the probability of consecutive events summing to a particular value.


    Real-life instances
    ===================

    2012 4c: [5 lines] [3 marks]
    """

    def __init__(self, part):
        self._qp = copy.deepcopy(part._qp)
        self._qi = copy.deepcopy(part._qi)

        self.num_lines, self.num_marks = 5, 3

        self._qp['n_days'] = 2
        # take the target cumulative target to be near E(X)*n_days.
        self._qp['total'] = random.randint(-1, 1) + int(prob_table.expectation_x(self._qp['prob_table']) * self._qp['n_days'])

        self._qp['answer'] = prob_table.prob_sum(self._qp['prob_table'], total=self._qp['total'], n_trials=self._qp['n_days'])

        self._qp['valid_permutations'] = prob_table.valid_permutations(
            self._qp['prob_table'],
            total=self._qp['total'],
            n_trials=self._qp['n_days']
        )

    def question_statement(self):
        return r'''{first_name} receives {item} on {n_days} consecutive days. What is the probability that {first_name} receives a total of
            {total} {item} over these {n_days} days?'''.format(
            **self.combined_question_dict()
        )

    def solution_statement(self):
        lines = solutions.Lines()

        sum_large_xs = ' + '.join(['X_{0}'.format(d + 1) for d in range(self._qp['n_days'])])
        sum_permutations_symbolic = expressions.sum_permutation_probabilities(self._qp['valid_permutations'])

        lines += r'''$Pr({0} = {1}) = {2}$'''.format(
            sum_large_xs,
            self._qp['total'],
            sum_permutations_symbolic
        )

        probabilities_of_permutations = []
        for permutation in self._qp['valid_permutations']:
            probabilities_of_indivudual_permutation_events = (self._qp['prob_table'][individual_event] for individual_event in permutation)
            probability_of_permutation = functools.reduce(operator.mul, probabilities_of_indivudual_permutation_events)
            probabilities_of_permutations.append(probability_of_permutation)

        sum_permutations_numeric = ' + '.join(sympy.latex(i) for i in probabilities_of_permutations)
        lines += r'''$= {0}$'''.format(sum_permutations_numeric)

        lines += r'''$= {0}$'''.format(sympy.latex(self._qp['answer']))

        return lines.write()
