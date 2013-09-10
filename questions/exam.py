from maths.latex import latex, questions
from maths.parts import simple_inverse
from maths.parts import simple_definite_integral, definite_integral_equality


with open('exam.tex', 'w') as f:
    latex.begin_tex_document(f)

    q = simple_inverse.SimpleInverse()
    question = questions.QuestionTree(1, q)
    question.write_question(f)
    question.write_solution(f)


    q = simple_definite_integral.SimpleDefiniteIntegral()
    question = questions.QuestionTree(2, q)
    question.write_question(f)
    question.write_solution(f)


    q = definite_integral_equality.DefiniteIntegralEquality()
    question = questions.QuestionTree(3, q)
    question.write_question(f)
    question.write_solution(f)

    latex.end_tex_document(f)
