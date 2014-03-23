from maths.questions import definite_integral_equality
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_DefiniteIntegralEquality():
    q1 = definite_integral_equality.DefiniteIntegralEquality()
    question_tester(QuestionTree(q1))
