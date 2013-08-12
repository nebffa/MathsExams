from maths.questions import questions, simple_diff


def test_SimpleDiff():
    q1 = simple_diff.SimpleDiff()
    questions.test_question(q1)


def test_SimpleDiffEval():
    q1 = simple_diff.SimpleDiff()
    q2 = simple_diff.SimpleDiffEval(q1.function_type)

    questions.test_question(q1)
    questions.test_question(q2)