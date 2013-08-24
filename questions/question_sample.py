import prob_table_known
from maths.latex import latex
import questions
import ipdb


with open('question_sample.tex', 'w') as f:
    latex.begin_tex_document(f)

    q = prob_table_known.ProbTableKnown()
    question = questions.new_question(1, q)

    q_a = prob_table_known.Property(part=q)
    q_b = prob_table_known.Multinomial(part=q)
    q_c = prob_table_known.Conditional(part=q)
    q_d = prob_table_known.Cumulative(part=q)

    questions.add_part(question, 1, part=q_a)
    questions.add_part(question, 2, part=q_b)
    questions.add_part(question, 3, part=q_c)
    questions.add_part(question, 4, part=q_d)


    question.write_question(f)
    question.write_solution(f)
    latex.end_tex_document(f)
