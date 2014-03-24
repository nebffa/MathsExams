from maths.questions import antiderivative
from .question_tester import question_tester
from maths.latex.questions import QuestionTree


def test_Antiderivative():
    q1 = QuestionTree(part=antiderivative.Antiderivative())
    question_tester(q1)