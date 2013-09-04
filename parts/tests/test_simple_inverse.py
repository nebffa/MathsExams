from maths.parts import simple_inverse
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_SimpleInverse():
    q1 = simple_inverse.SimpleInverse()
    question_tester(QuestionTree(1, q1))