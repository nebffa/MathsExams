from .. import relationships, hidden_integration_by_parts
from .question_tester import question_tester


def test_hidden_integration_by_parts():
    question = relationships.parse_structure(hidden_integration_by_parts)
    question_tester(question)