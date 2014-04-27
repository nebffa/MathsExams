from maths.questions import linear_approximation, relationships
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_linear_approximation():
    question = relationships.parse_structure(linear_approximation)
    question_tester(question)
