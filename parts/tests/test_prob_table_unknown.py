from maths.parts import prob_table_unknown
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_ProbTableUnknown():
    q1 = prob_table_unknown.ProbTableUnknown()
    question_tester(QuestionTree(q1))