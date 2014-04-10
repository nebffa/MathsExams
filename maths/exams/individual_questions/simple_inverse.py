from maths.latex import latex, questions
from maths.questions import (
                            simple_inverse
                        )


with open('exam.tex', 'w') as f:
    latex.begin_tex_document(f)

    q = simple_inverse.SimpleInverse()
    question = questions.QuestionTree(q)



    question.write_question(f)
    latex.new_page(f)
    question.write_solution(f)

    latex.end_tex_document(f)
