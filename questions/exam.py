from maths.latex import latex, questions
from maths.parts import (
                            antiderivative,
                            definite_integral_equality,
                            piecewise,
                            piecewise_prob_density_function,
                            prob_table_known,
                            prob_table_unknown,
                            simple_diff,
                            simple_inverse, 
                            simple_definite_integral, 
                            worded_definite_integral
                        )


with open('exam.tex', 'w') as f:
    latex.begin_tex_document(f)

    q = simple_inverse.SimpleInverse()
    question = questions.QuestionTree(1, q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = simple_definite_integral.SimpleDefiniteIntegral()
    question = questions.QuestionTree(2, q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)

    q = definite_integral_equality.DefiniteIntegralEquality()
    question = questions.QuestionTree(3, q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = piecewise.Piecewise()
    question = questions.QuestionTree(4, q)
    q_sub1 = piecewise.DomainDerivative(q)
    q_sub2 = piecewise.AbsoluteValue(q)
    question.add_part(q_sub1, 1)
    question.add_part(q_sub2, 2)
    question.write_question(f)
    question.write_solution(f)



    latex.end_tex_document(f)
