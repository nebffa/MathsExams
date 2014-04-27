from maths.questions import simple_diff, relationships
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_simple_diff():
    question = relationships.parse_structure(simple_diff)
    question_tester(question)
