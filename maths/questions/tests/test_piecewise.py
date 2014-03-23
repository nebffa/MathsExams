from maths.questions import piecewise
from maths.latex.questions import QuestionTree
from .question_tester import question_tester
import pytest


def test_Piecewise():
    q1 = piecewise.Piecewise()
    question_tester(QuestionTree(q1))