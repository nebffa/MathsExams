from maths.questions import log_misc
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_LogMisc():
    q1 = log_misc.SolveLogEquation()
    question_tester(QuestionTree(part=q1))