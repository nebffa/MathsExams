from maths.parts import piecewise_prob_density_function
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_PiecewiseProbDensityFunction():
    q1 = piecewise_prob_density_function.PiecewiseProbDensityFunction()
    question_tester(QuestionTree(question_number=1, part=q1))
