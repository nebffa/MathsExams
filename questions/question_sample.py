from . import prob_table_unknown
from maths.latex import latex
from . import questions


with open('question_sample.tex', 'w') as f:
    latex.begin_tex_document(f)

    q = prob_table_unknown.ProbTableUnknown()
    q.sanity_check()
    question = questions.new_question(1, q)

    question.write_question(f)
    question.write_solution(f)
    latex.end_tex_document(f)
