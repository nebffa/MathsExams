from maths.questions import definite_integral_equality, relationships
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_definite_integral_equality():
    question = relationships.parse_structure(definite_integral_equality)
    question_tester(question)
