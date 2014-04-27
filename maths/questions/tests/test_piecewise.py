from maths.questions import piecewise, relationships
from maths.latex.questions import QuestionTree
from .question_tester import question_tester
import pytest


def test_piecewise():
    question = relationships.parse_structure(piecewise)
    question_tester(question)
