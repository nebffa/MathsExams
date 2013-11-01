from maths.latex import latex, questions
from maths.parts import (
                            piecewise_prob_density_function
                        )


with open('exam.tex', 'w') as f:
    latex.begin_tex_document(f)

    q = piecewise_prob_density_function.PiecewiseProbDensityFunction()
    question = questions.QuestionTree(q)

    question.add_part(piecewise_prob_density_function.Conditional(q))


    question.write_question(f)
    latex.new_page(f)
    question.write_solution(f)

    latex.end_tex_document(f)