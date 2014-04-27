from maths.questions import simple_inverse, relationships
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_simple_inverse():
    question = relationships.parse_structure(simple_inverse)
    question_tester(question)
