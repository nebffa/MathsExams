from maths.parts import simple_diff
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_SimpleDiff():
    q1 = simple_diff.SimpleDiff()
    question_tester(QuestionTree(q1))


def test_SimpleDiffEval():
    q1 = simple_diff.SimpleDiff()
    q2 = simple_diff.SimpleDiffEval(q1.function_type)

    question_tester(QuestionTree(q2))