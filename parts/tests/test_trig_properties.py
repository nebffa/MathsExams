from maths.parts import trig_properties
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_TrigProperties():
    q1 = trig_properties.TrigProperties()
    question_tester(QuestionTree(part=q1))