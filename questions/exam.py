from maths.latex import latex
import questions
import functions
import simple_integral


with open('exam.tex', 'w') as f:
    latex.begin_tex_document(f)

    q = functions.SimpleInverse()
    question = questions.new_question(1, q)
    question.write_question(f)
    question.write_solution(f)


    q = simple_integral.SimpleDefiniteIntegral()
    question = questions.new_question(2, q)
    question.write_question(f)
    question.write_solution(f)


    q = simple_integral.DefiniteIntegralEquality()
    question = questions.new_question(3, q)
    question.write_question(f)
    question.write_solution(f)

    latex.end_tex_document(f)
