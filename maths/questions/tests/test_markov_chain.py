from maths.questions import markov_chain, relationships
from maths.latex.questions import QuestionTree
from .question_tester import question_tester
import decimal
import functools
import operator


transition_matrix = {
    (0, 0): decimal.Decimal('0.7'), (1, 0): decimal.Decimal('0.4'),
    (0, 1): decimal.Decimal('0.3'), (1, 1): decimal.Decimal('0.6')
}

location_names = ['A', 'B']


def test_MarkovChain():
    question = relationships.parse_structure(markov_chain)
    question_tester(question)


def test_all_path():
    all_paths = markov_chain.MarkovChainBinomial.all_paths(start_state=0, n_trials=3)
    assert set(tuple(path) for path in all_paths) == set(((0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1)))


def test_cinema_path():
    path = [0, 1, 1, 0]
    assert markov_chain.MarkovChainBinomial.cinema_path(path, location_names) == \
        r'Pr(X_{0} = \text{A}) \times Pr(X_{1} = \text{B}) \times Pr(X_{2} = \text{B}) \times Pr(X_{3} = \text{A})'


def test_numeric_path():
    path = [0, 0, 1, 1, 0]
    transitions = [decimal.Decimal('0.7'), decimal.Decimal('0.3'), decimal.Decimal('0.6'), decimal.Decimal('0.4')]
    assert markov_chain.MarkovChainBinomial.numeric_path(path, transition_matrix) == \
        r' \times '.join(str(i) for i in transitions)


def test_path_value():
    path = [0, 0, 1, 1, 0]
    transitions = [decimal.Decimal('0.7'), decimal.Decimal('0.3'), decimal.Decimal('0.6'), decimal.Decimal('0.4')]
    assert markov_chain.MarkovChainBinomial.path_value(path, transition_matrix) == functools.reduce(operator.mul, transitions)
