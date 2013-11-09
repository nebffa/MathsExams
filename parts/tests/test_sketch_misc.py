from maths.parts import sketch_misc
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_SketchMisc():
    q1 = sketch_misc.SketchMisc()
    question_tester(QuestionTree(part=q1))