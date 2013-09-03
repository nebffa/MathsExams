from maths.questions import questions, simple_integral
from maths.latex.questions import QuestionTree


def test_SimpleDefiniteIntegral():
    q1 = simple_integral.SimpleDefiniteIntegral()
    questions.test_question(QuestionTree(1, q1))


def test_DefiniteIntegralEquality():
    q1 = simple_integral.DefiniteIntegralEquality()
    questions.test_question(QuestionTree(1, q1))
