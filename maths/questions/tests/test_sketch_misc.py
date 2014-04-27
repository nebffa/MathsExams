from maths.questions import sketch_misc, relationships
from maths.latex.questions import QuestionTree
from .question_tester import question_tester
import pytest


@pytest.mark.xfail
def test_sketch_misc():
    question = relationships.parse_structure(sketch_misc)
    question_tester(question)
