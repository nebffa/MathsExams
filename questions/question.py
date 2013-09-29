from maths.latex import latex, questions
from maths.parts import (
                            worded_definite_integral
                        )


with open('exam.tex', 'w') as f:
    latex.begin_tex_document(f)

    q = worded_definite_integral.WordedDefiniteIntegral()
    question = questions.QuestionTree(q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    latex.end_tex_document(f)
