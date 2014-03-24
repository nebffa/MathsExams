from ..questions import antiderivative
from ..latex import latex, questions



def question():
    """
    The first attempt at an API, so that our flask app can request questions.

    """

    q = questions.QuestionTree(antiderivative.Antiderivative())

    return q.question_latex()
