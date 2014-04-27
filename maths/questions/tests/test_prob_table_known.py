from maths.questions import prob_table_known, relationships
from .question_tester import question_tester
from maths.latex.questions import QuestionTree


def test_prob_table_known():
    question = relationships.parse_structure(prob_table_known)
    question_tester(question)
