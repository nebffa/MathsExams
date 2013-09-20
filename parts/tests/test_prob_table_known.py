from maths.parts import prob_table_known
from .question_tester import question_tester
from maths.latex.questions import QuestionTree


def test_ProbTableKnown():

    q = prob_table_known.ProbTableKnown()
    question = QuestionTree(part=q)

    q_a = prob_table_known.Property(part=q)
    q_b = prob_table_known.Multinomial(part=q)
    q_c = prob_table_known.Conditional(part=q)
    q_d = prob_table_known.Cumulative(part=q)

    question.add_part(tree_location1=1, part=q_a)
    question.add_part(tree_location1=2, part=q_b)
    question.add_part(tree_location1=3, part=q_c)
    question.add_part(tree_location1=4, part=q_d)

    question_tester(question)