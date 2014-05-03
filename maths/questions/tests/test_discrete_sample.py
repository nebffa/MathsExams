from ...questions import relationships, discrete_sample
from .question_tester import question_tester
from ...latex.questions import QuestionTree


def test_discrete_sample():
    question = relationships.parse_structure(discrete_sample)
    question_tester(question)
