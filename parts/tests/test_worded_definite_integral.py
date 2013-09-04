from maths.parts import worded_definite_integral
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_WordedDefiniteIntegral():
    q1 = worded_definite_integral.WordedDefiniteIntegral()
    question_tester(QuestionTree(1, q1))