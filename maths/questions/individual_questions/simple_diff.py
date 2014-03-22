from maths.latex import latex, questions
from maths.parts import (
                            simple_diff
                        )


with open('exam.tex', 'w') as f:
    latex.begin_tex_document(f)

    q = simple_diff.SimpleDiff()
    q2 = simple_diff.SimpleDiffEval(q)

    question = questions.QuestionTree(q)
    question.add_part(q2)



    question.write_question(f)
    latex.new_page(f)
    question.write_solution(f)

    latex.end_tex_document(f)
