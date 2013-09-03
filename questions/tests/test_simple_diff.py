from maths.questions import questions, simple_diff
from maths.latex.questions import QuestionTree


def test_SimpleDiff():
    q1 = simple_diff.SimpleDiff()
    questions.test_question(QuestionTree(1, q1))


def test_SimpleDiffEval():
    q1 = simple_diff.SimpleDiff()
    q2 = simple_diff.SimpleDiffEval(q1.function_type)

    questions.test_question(QuestionTree(1, q1))
    questions.test_question(QuestionTree(1, q2))