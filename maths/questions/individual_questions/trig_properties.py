from maths.latex import latex, questions
from maths.parts import (
                            trig_properties
                        )


with open('exam.tex', 'w') as f:
    latex.begin_tex_document(f)

    q = trig_properties.TrigProperties()
    question = questions.QuestionTree(q)

    question.write_question(f)
    latex.new_page(f)
    question.write_solution(f)

    latex.end_tex_document(f)
