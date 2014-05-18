from .. import relationships, tangent
from .question_tester import question_tester
import pytest


@pytest.mark.xfail
def test_tangent():
    question = relationships.parse_structure(tangent)
    question_tester(question)