import sympy
import random
import decimal
import itertools
import functools
import operator
from ..phrasing import days, first_names
from ..latex import latex, solution_lines
from . import relationships


@relationships.root
class MarkovChainBinomial(relationships.QuestionPart):
    """
    Question description
    ====================

    Calculate the probability of getting "x" successes out of "n" trials using Markov chains.


    Real-life instances
    ===================

    2008 8: [10 lines] [3 marks]
    """

    @staticmethod
    def all_paths(start_state, n_trials):
        """Return all paths the Markov chain can take in a number of trials.
        """
        paths = [[start_state]]
        length = 1

        while length < n_trials:
            unflattened_paths = ([state + [0], state + [1]] for state in paths)
            paths = itertools.chain.from_iterable(unflattened_paths)
            length += 1

        return list(paths)

    @staticmethod
    def cinema_path(path, location_names):
        """Return LaTeX that shows the set of cinemas a path visits.
        """

        individual_trials = [r'Pr(X_{{{week_number}}} = \text{{{cinema_name}}})'.format(
            week_number=key,
            cinema_name=location_names[value])
            for key, value in enumerate(path)
        ]

        return r' \times '.join(individual_trials)

    @staticmethod
    def numeric_path(path, transition_matrix):
        """Return LaTeX that shows the probabilities of taking a particular path.
        """

        numerics = []
        for i in range(1, len(path)):
            transition = transition_matrix[(path[i - 1], path[i])]
            numerics.append(transition)

        return r' \times '.join([str(i) for i in numerics])

    @staticmethod
    def path_value(path, transition_matrix):
        """Return the probability of a path happening.
        """

        transitions = []
        for i in range(1, len(path)):
            transitions.append(transition_matrix[(path[i - 1], path[i])])

        return functools.reduce(operator.mul, transitions)

    def __init__(self):
        self.num_lines, self.num_marks = 10, 3
        self._qp = {}

        # in range 0.10, 0.15, ..., 0.90
        amounts = random.sample([decimal.Decimal('0.05') * i for i in range(2, 19)], 2)
        prob_place1_becomes_place1 = amounts[0]
        prob_place1_becomes_place2 = 1 - prob_place1_becomes_place1

        prob_place2_becomes_place1 = amounts[1]
        prob_place2_becomes_place2 = 1 - prob_place2_becomes_place1

        self._qp['transition_matrix'] = {
            (0, 0): prob_place1_becomes_place1,
            (0, 1): prob_place1_becomes_place2,
            (1, 0): prob_place2_becomes_place1,
            (1, 1): prob_place2_becomes_place2
        }

        self._qp['start_state'] = random.randint(0, 1)

        # just leaving the n_trials at 4 for now
        n_trials = 3
        self._qp['binomial'] = {
            'cinema': self._qp['start_state'],
            'n_successes': 2,
            'n_trials': n_trials
        }

    def question_statement(self):
        self._qp['cinemas'] = ['Pollos', 'Altiplano']

        day_of_the_week = days.random_day()
        first_name, gender = first_names.random_first_name(gender=True)

        start_cinema = self._qp['cinemas'][self._qp['start_state']]
        target_cinema = self._qp['cinemas'][self._qp['binomial']['cinema']]

        pronoun_for_person = 'he' if gender == 'male' else 'she'

        self._qi = {
            'day_of_the_week': day_of_the_week,
            'first_name': first_name,
        }

        setup = r'''Every {day_of_the_week} {first_name} goes to see a movie. {pronoun_for_person} always goes to one of two nearby cinemas - the
        {first_cinema_name} or the {second_cinema_name}.

        If {pronoun_for_person} goes to the {first_cinema_name} one {day_of_the_week}, the probability that {pronoun_for_person} goes to the
        {second_cinema_name} the next week is {first_to_second_transition_probability}. If {pronoun_for_person} goes to the {second_cinema_name}
        one {day_of_the_week}, then the probability that {pronoun_for_person} goes to the {first_cinema_name} the next {day_of_the_week} is
        {second_to_first_transition_probability}.

        On any given {day_of_the_week} the cinema {pronoun_for_person} goes to depends only on the cinema {pronoun_for_person} went to on the
        previous {day_of_the_week}.'''.format(
            day_of_the_week=day_of_the_week,
            first_name=first_name,
            pronoun_for_person=pronoun_for_person,
            first_cinema_name=self._qp['cinemas'][0],
            second_cinema_name=self._qp['cinemas'][1],
            first_to_second_transition_probability=self._qp['transition_matrix'][(0, 1)],
            second_to_first_transition_probability=self._qp['transition_matrix'][(1, 0)]
        )

        question = r'''If {pronoun_for_person} goes to the {start_cinema_name} one {day_of_the_week},
        what is the probability that {pronoun_for_person} goes to the {target_cinema_name} on
        exactly {number_of_cinema_trips} of the next {number_of_weeks} {day_of_the_week}s?'''.format(
            pronoun_for_person=pronoun_for_person,
            start_cinema_name=start_cinema,
            day_of_the_week=day_of_the_week,
            target_cinema_name=target_cinema,
            number_of_cinema_trips=self._qp['binomial']['n_successes'],
            number_of_weeks=self._qp['binomial']['n_trials']
        )

        return setup + latex.latex_newline() + question

    def solution_statement(self):
        lines = solution_lines.Lines()

        paths = MarkovChainBinomial.all_paths(self._qp['start_state'], self._qp['binomial']['n_trials'])
        if self._qp['binomial']['cinema'] == 0:
            solution_paths = [i for i in paths if len(i) - sum(i) == self._qp['binomial']['n_successes']]
        else:
            solution_paths = [i for i in paths if sum(i) == self._qp['binomial']['n_successes']]

        lines += r'''Let $X$ represent the number of times {first_name} goes to {target_cinema_name} over the ${number_of_weeks}$ {day_of_the_week}s'''.format(
            first_name=self._qi['first_name'],
            target_cinema_name=self._qp['cinemas'][self._qp['binomial']['cinema']],
            number_of_weeks=self._qp['binomial']['n_trials'],
            day_of_the_week=self._qi['day_of_the_week']
        )

        path_strings = [MarkovChainBinomial.cinema_path(path, self._qp['cinemas']) for path in solution_paths]
        lines += r'''$Pr(X = {number_of_cinema_trips}) = {possible_paths}$'''.format(
            number_of_cinema_trips=self._qp['binomial']['n_successes'],
            possible_paths=' + '.join(path_strings)
        )

        numeric_strings = [MarkovChainBinomial.numeric_path(path, self._qp['transition_matrix']) for path in solution_paths]
        lines += r'''$= {intermediate_paths}$'''.format(
            intermediate_paths=' + '.join(numeric_strings)
        )

        answer = sum(MarkovChainBinomial.path_value(path, self._qp['transition_matrix']) for path in solution_paths)
        # not sure how to make decimal.Decimal stop at the endless 0s of a decimal
        lines += r'''$= {answer}$'''.format(
            answer=answer
        )

        return lines.write()
