from .latex import latex, questions
from .questions import (
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


with open('maths/exams/exam.tex', 'w') as f:
    latex.begin_tex_document(f)

    q = simple_inverse.SimpleInverse()
    question = questions.QuestionTree(q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)

    
    q = simple_definite_integral.SimpleDefiniteIntegral()
    question = questions.QuestionTree(q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = definite_integral_equality.DefiniteIntegralEquality()
    question = questions.QuestionTree(q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = piecewise.Piecewise()
    question = questions.QuestionTree(q)
    q_sub1 = piecewise.DomainDerivative(q)
    q_sub2 = piecewise.AbsoluteValue(q)
    question.add_part(q_sub1)
    question.add_part(q_sub2)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = antiderivative.Antiderivative()
    question = questions.QuestionTree(q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = piecewise_prob_density_function.PiecewiseProbDensityFunctionKnown()
    question = questions.QuestionTree(q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    question = questions.QuestionTree()
    q_sub1 = simple_diff.SimpleDiff()
    q_sub2 = simple_diff.SimpleDiffEval(q)
    question.add_part(q_sub1)
    question.add_part(q_sub2)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = worded_definite_integral.WordedDefiniteIntegral()
    question = questions.QuestionTree(q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    latex.end_tex_document(f)
