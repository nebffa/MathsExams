from .. import relationships, related_rates
from .question_tester import question_tester


def test_related_rates():
    question = relationships.parse_structure(related_rates)
    question_tester(question)