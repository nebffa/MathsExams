from maths.parts import piecewise_prob_density_function_unknown
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_PiecewiseProbDensityFunction():
    q1 = piecewise_prob_density_function_unknown.PiecewiseProbDensityFunctionUnknown()
    question_tester(QuestionTree(part=q1))
