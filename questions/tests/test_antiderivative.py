from maths.questions import questions, antiderivative
from maths.latex.questions import QuestionTree


def test_Antiderivative():
    q1 = QuestionTree(part=antiderivative.Antiderivative(), question_number=1)
    questions.test_question(q1)