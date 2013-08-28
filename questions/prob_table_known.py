import random
import sympy
from sympy import GreaterThan, LessThan, StrictGreaterThan, StrictLessThan
from sympy.abc import *
from maths import not_named_yet
from maths.names import first_names
from maths.latex import latex, expressions
from maths.latex.table import probability_table
from maths.probability.discrete import prob_table
import operator
from collections import OrderedDict
from functools import reduce


class ProbTableKnown(object):
    def __init__(self):
        self.num_lines = 0
        self.num_marks = 0

        options = list(range(random.randint(4, 5)))

        partition = random.choice([i for i in not_named_yet.partition(10) if len(i) == len(options)])
        partition = list(partition)

        random.shuffle(partition)
        partition = [sympy.Rational(i, 10) for i in partition]

        self.prob_table = OrderedDict(list(zip(options, partition)))
        self.first_name = random.choice(first_names.names)

    def question_statement(self):        

        question_contexts = {
                'green traffic lights': '''When {0} drives to work each morning they pass a number of intersections with traffic lights. The number X of 
                            traffic lights that are green when {0} is driving to work is a random variable with probability distribution given by''',
                'telephone calls': '''Every day, the number X of telephone calls that {0} receives at work is a random variable with probability 
                            distribution given by''',
                'free marshmallows': '''Every day, {0} goes to her local cafe for lunch and orders a hot chocolate. The number X of free marshmallows 
                            that are included with the hot chocolate is a random variable with probability distribution given by'''}

        self.question_context = random.choice(list(question_contexts.keys()))
        text = question_contexts[self.question_context].format(self.first_name)
        table = probability_table(self.prob_table)

        return text + table

    def solution_statement(self):
        return ''


class Property(object):
    def __init__(self, part):
        assert isinstance(part, ProbTableKnown)
        
        self._question_type = random.choice(['mean', 'variance', 'mode'])
        self._prob_table = part.prob_table
        self._working = {}

        if self._question_type == 'mean':
            self.num_lines, self.num_marks = 4, 2

            self._working['E_x'] = prob_table.expectation_x(self._prob_table)
            self.answer = self._working['E_x']
        elif self._question_type == 'variance':
            self.num_lines, self.num_marks = 7, 3

            self._working['E_x'] = prob_table.expectation_x(self._prob_table)
            self._working['E_x_sq'] = prob_table.expectation_x(self._prob_table, power=2)

            self.answer = self._working['E_x_sq'] - self._working['E_x']**2
        elif self._question_type == 'mode':
            self.num_lines, self.num_marks = 2, 1

            self.answer = prob_table.mode(self._prob_table)

    def question_statement(self):
        if self._question_type == 'mean':
            return r'Find E(X), the mean of X.'
        elif self._question_type == 'variance':
            return r'Find Var(X), the variance of X.'
        elif self._question_type == 'mode':
            return r'Find the mode of X.'

    def solution_statement(self):
        
        if self._question_type == 'mean':
            line_1 = r'$E(X) = \sum\limits_{{i=1}}^{{n}} x_{{i}} \times Pr(X = x_{{i}}) = {0} = {1}$'.format(
                            expressions.discrete_expectation_x(self._prob_table), self.answer)

            line_2 = r'$= ' + expressions.discrete_expectation_x(self._prob_table) + r' = %s$' % self.answer
            lines = [line_1, line_2]

        elif self._question_type == 'variance':
            line_1 = r'$Var(X) = E(X^2) - (E(X))^2$'
            line_2 = r'$= [{0}] - [{1}]$'.format(expressions.discrete_expectation_x_squared(self._prob_table), 
                                                 expressions.discrete_expectation_x(self._prob_table))

            line_3 = r'$= {0} - {1} = {2}$'.format(sympy.latex(self._working['E_x_sq']), 
                                                    sympy.latex(self._working['E_x']**2), 
                                                    sympy.latex(self._working['E_x_sq'] - self._working['E_x']**2))

            lines = [line_1, line_2, line_3]

        elif self._question_type == 'mode':
            lines = [r'${0}$'.format(prob_table.mode(self._prob_table))]
            
        return latex.latex_newline().join(lines)


class Multinomial(object):
    def __init__(self, part):
        assert isinstance(part, ProbTableKnown)

        self.question_type = random.choice(['one_x', 'any_x'])
        self._prob_table = part.prob_table
        self._question_context = part.question_context
        self._first_name = part.first_name

        self._question_params = {}

        if self.question_type == 'one_x':
            self.num_lines, self.num_marks = 4, 1

            self._question_params['x_value'] = random.choice(list(self._prob_table.keys()))
            self._question_params['n_days'] = 3

        elif self.question_type == 'any_x':
            self.num_lines, self.num_marks = 5, 2

            self._question_params['n_days'] = random.randint(2, 3)

    def question_statement(self):
        if self.question_type == 'one_x':
            return r'''What is the probability that the number of {0} {1} gets on each of 
                        {2} consecutive days is {3}?'''.format(self._question_context, self._first_name, 
                                                                self._question_params['n_days'], self._question_params['x_value'])

        elif self.question_type == 'any_x':
            return r'''What is the probability that the number of {0} {1} gets is the same on each 
                                    of {2} consecutive days?'''.format(self._question_context, self._first_name, self._question_params['n_days'])

    def solution_statement(self):
        if self.question_type == 'one_x':
            return r'''$Pr(X = {0}$, {1} days in a row$) = {2}^{1} = {3}.$'''.format(self._question_params['x_value'],
                                                                self._question_params['n_days'],
                                                                self._prob_table[self._question_params['x_value']],
                                                                self._prob_table[self._question_params['x_value']] ** self._question_params['n_days'])

        elif self.question_type == 'any_x':
            sum_of_probs = ' + '.join([r'''Pr(X = {0})^{1}'''.format(k, self._question_params['n_days']) for k in self._prob_table])
            line_1 = r'''$Pr(X$ is the same number {0} days in a row$) = {1}$'''.format(self._question_params['n_days'], sum_of_probs)

            sum_of_probs = ' + '.join(['({0})^{1}'.format(sympy.latex(v), self._question_params['n_days']) for v in self._prob_table.values()])
            answer = sum(v**self._question_params['n_days'] for v in self._prob_table.values())
            line_2 = r'''$= {0} = {1}$'''.format(sum_of_probs, sympy.latex(answer))

            return latex.latex_newline().join([line_1, line_2])


class Conditional(object):
    def __init__(self, part):
        assert isinstance(part, ProbTableKnown)

        self.num_lines, self.num_marks = 4, 2

        self._prob_table = part.prob_table

        self._question_params = {}

        # if we have a conditional probability: 
        #       Pr(X > 1 | X <= 3)
        # I then refer to 3 as the conditional major, i.e. the section of the universe we are limited to
        # and 1 as the conditional minor, i.e. the section of the now-limited universe we are calculating a probability for
        self._question_params['conditional_major_rel_op'] = random.choice([GreaterThan, LessThan])
        self._question_params['conditional_minor_rel_op'] = random.choice([GreaterThan, LessThan, StrictGreaterThan, StrictLessThan])
        if self._question_params['conditional_major_rel_op'] == GreaterThan:
            self._question_params['conditional_major'] = min(self._prob_table) + 1
            self._question_params['conditional_minor'] = random.randint(min(self._prob_table) + 2, max(self._prob_table) - 1)
        else:
            self._question_params['conditional_major'] = max(self._prob_table) - 1
            self._question_params['conditional_minor'] = random.randint(min(self._prob_table) + 1, max(self._prob_table) - 2)

        major_domain = [k for k in self._prob_table if self._question_params['conditional_major_rel_op'](k, self._question_params['conditional_major'])]
        minor_domain = [k for k in major_domain if self._question_params['conditional_minor_rel_op'](k, self._question_params['conditional_minor'])]

        self._question_params['pr_major'] = sum(self._prob_table[k] for k in major_domain)
        self._question_params['pr_minor'] = sum(self._prob_table[k] for k in minor_domain)

    def question_statement(self):
        return r'''Find $Pr(X {0} {1} \,|\, X {2} {3})$.'''.format(self._question_params['conditional_minor_rel_op'].rel_op,
                                                                self._question_params['conditional_minor'],
                                                                self._question_params['conditional_major_rel_op'].rel_op,
                                                                self._question_params['conditional_major'])

    def solution_statement(self):
        #ipdb.set_trace()
        line_1 = r'''$Pr(X {0} {1} \,|\, X {2} {3}) = \frac{{Pr(X {0} {1} \,\cap\, X {2} {3})}}{{Pr(X {2} {3})}}$'''.format(
                                                                self._question_params['conditional_minor_rel_op'].rel_op,
                                                                self._question_params['conditional_minor'],
                                                                self._question_params['conditional_major_rel_op'].rel_op,
                                                                self._question_params['conditional_major'])

        line_2 = r'''$= \frac{{{0}}}{{{1}}} = {2}$'''.format(sympy.latex(self._question_params['pr_minor']), 
                                                                sympy.latex(self._question_params['pr_major']), 
                                                                sympy.latex(self._question_params['pr_minor'] / self._question_params['pr_major']))

        return latex.latex_newline().join([line_1, line_2])


class Cumulative(object):
    def __init__(self, part):
        assert isinstance(part, ProbTableKnown)

        self.num_lines, self.num_marks = 5, 3

        self._prob_table = part.prob_table
        self._question_type = part.question_context
        self._first_name = part.first_name

        self._question_params = {}

        self._question_params['n_days'] = 2
        # take the target cumulative target to be near E(X)*n_days. 
        self._question_params['total'] = random.randint(-1, 1) + int(prob_table.expectation_x(self._prob_table) * self._question_params['n_days'])
        self._answer = prob_table.prob_sum(self._prob_table, total=self._question_params['total'], 
                                                                        n_trials=self._question_params['n_days'])
        self._valid_permutations = prob_table.valid_permutations(self._prob_table, total=self._question_params['total'], 
                                                                        n_trials=self._question_params['n_days'])

    def question_statement(self):
        return r'''{0} receives {1} on {2} consecutive days. What is the probability that {0} receives a total of {3} {1} over these 
                {2} days?'''.format(self._first_name, self._question_type, self._question_params['n_days'], self._question_params['total'])

    def solution_statement(self):
        sum_large_xs = ' + '.join(['X_{0}'.format(d + 1) for d in range(self._question_params['n_days'])])
        sum_permutations_symbolic = ' + '.join([r' \times '.join(['Pr(X = {0})'.format(value) for value in perm]) for perm in self._valid_permutations])
        line_1 = r'''$Pr({0} = {1}) = {2}$'''.format(sum_large_xs, self._question_params['total'], sum_permutations_symbolic)

        sum_permutations_numeric = ' + '.join([sympy.latex(reduce(operator.mul, [self._prob_table[i] for i in perm])) for perm in self._valid_permutations])
        line_2 = r'''$= {0}$'''.format(sum_permutations_numeric)
        line_3 = r'''$= {0}$'''.format(sympy.latex(self._answer))

        return latex.latex_newline().join([line_1, line_2, line_3])
