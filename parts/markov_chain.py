import sympy
import random
import decimal
import itertools
import functools
import operator
from maths.symbols import *
from maths.questionmisc import days, first_names
from maths.latex import latex


class MarkovChainBinomial:

    def __init__(self):
        self.num_lines, self.num_marks = 10, 3

        self._qp = {}

        # in range 0.10, 0.15, ..., 0.90
        amounts = random.sample([decimal.Decimal('0.05')*i for i in range(2, 19)], 2)
        prob_place1_becomes_place1 = amounts[0]
        prob_place1_becomes_place2 = 1 - prob_place1_becomes_place1


        prob_place2_becomes_place1 = amounts[1]
        prob_place2_becomes_place2 = 1 - prob_place2_becomes_place1


        self._qp['probabilities'] = {
            (0, 0): prob_place1_becomes_place1,
            (0, 1): prob_place1_becomes_place2,
            (1, 0): prob_place2_becomes_place1,
            (1, 1): prob_place2_becomes_place2
        }



        self._qp['start_state'] = random.randint(0, 1)

        # just leaving the total at 3 for now
        total = random.randint(3, 3)
        self._qp['binomial'] = {
            'cinema': random.randint(0, 1),
            'num_successes': random.choice([1, total - 1]),
            'num_trials': total
        }


    def question_statement(self):
        self._qp['cinemas'] = ['Pollos', 'Altiplano']
        
        day = days.random_day()
        first_name, gender = first_names.random_first_name(gender=True)
        start_cinema = self._qp['cinemas'][self._qp['start_state']]

        target_cinema = self._qp['cinemas'][self._qp['binomial']['cinema']]

        pronoun = 'he' if gender == 'male' else 'she'

        self._qi = {
            'day': day,
            'first_name': first_name,
            'gender': gender,
        }

        

        setup = r'''Every {0} {1} goes to see a movie. {2} always goes to one of two nearby cinemas - the {3} or the {4}.

        If {2} goes to the {3} one {0}, the probability that {2} goes to the {4} is {5}. If {2} goes to the {4} one {0}, 
        then the probability that {2} goes to the {3} the next {0} is {6}.

        On any given {0} the cinema {2} goes to depends only on the cinema {2} went to on the previous {0}.
        '''.format(day, first_name, pronoun, self._qp['cinemas'][0], self._qp['cinemas'][1], 
                    self._qp['probabilities'][(0, 1)], self._qp['probabilities'][(1, 0)])


        question = r'''If {0} goes to the {1} one {2}, what is the probability that {0} goes to the {3} on 
        exactly {4} of the next {5} {2}s?'''.format(pronoun, start_cinema, day, target_cinema, 
                self._qp['binomial']['num_successes'], self._qp['binomial']['num_trials'])


        return setup + latex.latex_newline() + question


    def solution_statement(self):

        states = [ [0], [1] ]


        

        while len(states[0]) < self._qp['binomial']['num_trials']:
            unflattened_states = [[state + [0], state + [1]] for state in states]
            states = list( itertools.chain.from_iterable(unflattened_states) )

        if self._qp['binomial']['cinema'] == 0:
            solution_paths = list(filter(lambda x: len(x) - sum(x) == self._qp['binomial']['num_successes'], states))
        else:
            solution_paths = list(filter(lambda x: sum(x) == self._qp['binomial']['num_successes'], states))


        path_strings = []
        for path in solution_paths:
            product_parts = [r'Pr(X_{{{0}}} = \text{{{1}}})'.format(k, self._qp['cinemas'][v]) for k, v in enumerate(path)]
            product = r' \times '.join(product_parts)

            path_strings.append(product)


        numeric_strings = []
        answer = 0
        for path in solution_paths:
            numerics = []
            for i in range(len(path)):
                if i == 0:
                    transition = self._qp['probabilities'][(self._qp['start_state'], path[i])]
                else:
                    transition = self._qp['probabilities'][(path[i - 1], path[i])]

                numerics.append(transition)

            answer += functools.reduce(operator.mul, numerics)
            numeric_strings.append(r' \times '.join([str(i) for i in numerics]))
        
        

        line_1 = r'''Let $X$ represent the number of times {0} goes to {1} over the ${2}$ {3}s'''.format(
                    self._qi['first_name'], self._qp['cinemas'][self._qp['binomial']['cinema']], self._qp['binomial']['num_trials'], self._qi['day'])

        line_2 = r'''$Pr(X = {0}) = {1}$'''.format(self._qp['binomial']['num_successes'], ' + '.join(path_strings))

        line_3 = r'''$= {0}$'''.format(' + '.join(numeric_strings))

        # not sure how to make decimal.Decimal stop at the endless 0s of a decimal
        line_4 = r'''$= {0}$'''.format(answer)


        return latex.latex_newline().join([line_1, line_2, line_3, line_4])
