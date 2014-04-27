from maths.questions import worded_definite_integral, relationships
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_worded_definite_integral():
    question = relationships.parse_structure(worded_definite_integral)
    question_tester(question)
