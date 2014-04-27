from maths.questions import piecewise_prob_density_function, relationships
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_piecewise_prob_density_function():
    question = relationships.parse_structure(piecewise_prob_density_function)
    question_tester(question)