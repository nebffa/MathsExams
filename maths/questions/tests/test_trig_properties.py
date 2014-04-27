from maths.questions import trig_properties, relationships
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_trig_properties():
    question = relationships.parse_structure(trig_properties)
    question_tester(question)
