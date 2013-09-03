from maths.questions import probability, questions
from maths.latex.questions import QuestionTree


def test_PiecewiseProbDensityFunction():
    q1 = probability.PiecewiseProbDensityFunction()
    questions.test_question(QuestionTree(question_number=1, part=q1))
