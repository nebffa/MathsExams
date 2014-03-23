from maths.questions import linear_approximation
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_LinearApproximation():
    q1 = linear_approximation.LinearApproximation()
    question_tester(QuestionTree(part=q1))