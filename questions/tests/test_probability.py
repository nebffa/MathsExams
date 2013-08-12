from maths.questions import questions, probability


def test_PiecewiseProbDensityFunction():
    q1 = probability.PiecewiseProbDensityFunction()
    questions.test_question(q1)
