from maths.questions import log_misc, relationships
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_log_misc():
    question = relationships.parse_structure(log_misc)
    question_tester(question)
