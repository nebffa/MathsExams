from maths.parts import sketch_misc, simple_sketch
from maths.latex.questions import QuestionTree
from .question_tester import question_tester
import sympy


def test_SketchMisc():
    base_q = simple_sketch.SimpleSketch()
    base_q._qp['domain'] = sympy.Interval(-sympy.oo, sympy.oo)

    q1 = sketch_misc.SketchDoubleInverse(base_q)
    question_tester(QuestionTree(part=q1))