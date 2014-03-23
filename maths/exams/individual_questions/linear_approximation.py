from maths.latex import latex, questions
from maths.questions import (
                            linear_approximation
                        )


with open('exam.tex', 'w') as f:
    latex.begin_tex_document(f)

    q = linear_approximation.LinearApproximation()
    question = questions.QuestionTree(questions.DummyPart())

    question.add_part(q)

    q_sub1 = linear_approximation.LinearApproximationExplain(q)
    question.add_part(q_sub1)


    question.write_question(f)
    latex.new_page(f)
    question.write_solution(f)

    latex.end_tex_document(f)
