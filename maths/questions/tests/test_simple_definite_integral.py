from maths.questions import simple_definite_integral
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_SimpleDefiniteIntegral():
    q1 = simple_definite_integral.SimpleDefiniteIntegral()
    question_tester(QuestionTree(q1))
