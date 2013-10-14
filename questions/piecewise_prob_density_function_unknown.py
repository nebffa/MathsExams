from maths.latex import latex, questions
from maths.parts import (
                            piecewise_prob_density_function_unknown
                        )


with open('exam.tex', 'w') as f:
    latex.begin_tex_document(f)

    q = piecewise_prob_density_function_unknown.PiecewiseProbDensityFunctionUnknown()
    question = questions.QuestionTree(q)


    question.write_question(f)
    latex.new_page(f)
    question.write_solution(f)

    latex.end_tex_document(f)
