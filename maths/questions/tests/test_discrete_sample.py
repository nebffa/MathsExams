from ...questions import relationships, discrete_sample
from .question_tester import question_tester
from ...latex.questions import QuestionTree


def test_discrete_sample():
    question = relationships.parse_structure(discrete_sample)
    question_tester(question)


def test_sum_combination_probabilities():
    assert discrete_sample.DiscreteSum.sum_combination_probabilities([[2, 5, 6], [3, 4, 6]]) == \
        r'3! \times Pr(ball_1 = 2 \cap ball_2 = 5 \cap ball_3 = 6) + 3! \times Pr(ball_1 = 3 \cap ball_2 = 4 \cap ball_3 = 6)'


def test_sum_permutation_probabilities():
    assert discrete_sample.DiscreteSum.sum_permutation_probabilities([[2, 5, 6], [5, 2, 6]]) == \
        r'Pr(ball_1 = 2 \cap ball_2 = 5 \cap ball_3 = 6) + Pr(ball_1 = 5 \cap ball_2 = 2 \cap ball_3 = 6)'
    