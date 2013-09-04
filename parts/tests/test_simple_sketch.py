from maths.parts import simple_sketch
from maths.latex.questions import QuestionTree
from .question_tester import question_tester
import pytest


@pytest.mark.xfail
def test_SimpleSketch():
    q1 = simple_sketch.SimpleSketch()
    question_tester(QuestionTree(1, q1))