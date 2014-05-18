from .. import relationships, hidden_quadratic
from .question_tester import question_tester


def test_hidden_quadratic():
    question = relationships.parse_structure(hidden_quadratic)
    question_tester(question)