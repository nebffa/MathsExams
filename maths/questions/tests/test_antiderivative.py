from maths.questions import antiderivative, relationships
from .question_tester import question_tester
from maths.latex.questions import QuestionTree


def test_antiderivative():
    question = relationships.parse_structure(antiderivative)
    question_tester(question)
