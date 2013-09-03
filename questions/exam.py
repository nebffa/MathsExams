from maths.latex import latex, questions
from maths.questions import functions
from maths.questions import simple_integral


with open('exam.tex', 'w') as f:
    latex.begin_tex_document(f)

    q = functions.SimpleInverse()
    question = questions.QuestionTree(1, q)
    question.write_question(f)
    question.write_solution(f)


    q = simple_integral.SimpleDefiniteIntegral()
    question = questions.QuestionTree(2, q)
    question.write_question(f)
    question.write_solution(f)


    q = simple_integral.DefiniteIntegralEquality()
    question = questions.QuestionTree(3, q)
    question.write_question(f)
    question.write_solution(f)

    latex.end_tex_document(f)
