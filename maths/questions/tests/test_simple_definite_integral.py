from maths.questions import simple_definite_integral, relationships
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_simple_definite_integral():
    question = relationships.parse_structure(simple_definite_integral)
    question_tester(question)
