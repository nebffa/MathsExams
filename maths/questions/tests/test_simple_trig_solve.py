from maths.questions import simple_trig_solve
from maths.latex.questions import QuestionTree
from .question_tester import question_tester
import pytest


@pytest.mark.xfail
def test_SimpleTrigSolve():
    q1 = simple_trig_solve.SimpleTrigSolve()
    question_tester(QuestionTree(q1))