from maths.questions import prob_table_unknown, relationships
from maths.latex.questions import QuestionTree
from .question_tester import question_tester


def test_prob_table_unknown():
    question = relationships.parse_structure(prob_table_unknown)
    question_tester(question)
