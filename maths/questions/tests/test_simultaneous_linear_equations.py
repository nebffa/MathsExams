from .. import relationships, simultaneous_linear_equations
from .question_tester import question_tester


def test_simultaneous_linear_equations():
    question = relationships.parse_structure(simultaneous_linear_equations)
    question_tester(question)