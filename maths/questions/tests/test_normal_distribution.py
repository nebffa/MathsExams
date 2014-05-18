from .. import relationships, normal_distribution
from .question_tester import question_tester


def test_normal_distribution():
    question = relationships.parse_structure(normal_distribution)
    question_tester(question)