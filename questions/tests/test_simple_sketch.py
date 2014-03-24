from maths.questions import simple_sketch
from maths.latex.questions import QuestionTree
from .question_tester import question_tester



def test_SimpleSketch():
    q1 = simple_sketch.SimpleSketch()
    question_tester(QuestionTree(q1))