from maths.questions import simple_trig_solve, relationships
from maths.latex.questions import QuestionTree
from .question_tester import question_tester
import pytest


@pytest.mark.xfail
def test_simple_trig_solve():
    question = relationships.parse_structure(simple_trig_solve)
    question_tester(question)
