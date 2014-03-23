from .latex import latex, questions
from .questions import (
                            antiderivative,
                            definite_integral_equality,
                            discrete_sample,
                            hidden_integration_by_parts,
                            linear_approximation,
                            log_misc,
                            markov_chain,
                            matrix_linear_transformation,
                            normal_distribution,


                            piecewise,
                            piecewise_prob_density_function,
                            prob_table_known,
                            prob_table_unknown,
                            related_rates,
                            simple_diff,
                            simple_inverse,
                            simple_sketch, 
                            simple_definite_integral, 
                            sketch_misc,
                            trig_properties,
                            worded_definite_integral
                        )


with open('maths/exams/exam.tex', 'w') as f:
    latex.begin_tex_document(f)

    q = antiderivative.Antiderivative()
    question = questions.QuestionTree(q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = definite_integral_equality.DefiniteIntegralEquality()
    question = questions.QuestionTree(q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = discrete_sample.NoReplacement()
    q_sub1 = discrete_sample.SpecificPermutation(q)
    q_sub2 = discrete_sample.Sum(q)
    q_sub3 = discrete_sample.ConditionalSum(q)
    question = questions.QuestionTree(q)
    question.add_part(q_sub1)
    question.add_part(q_sub2)
    question.add_part(q_sub3)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = hidden_integration_by_parts.HiddenIntegrationByParts()
    q_sub1 = hidden_integration_by_parts.Derivative(q)
    q_sub2 = hidden_integration_by_parts.Integration(q)
    question = questions.QuestionTree(q)
    question.add_part(q_sub1)
    question.add_part(q_sub2)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = linear_approximation.LinearApproximation()
    q_sub1 = linear_approximation.LinearApproximationExplain(q)
    question = questions.QuestionTree(q)
    question.add_part(q_sub1)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = log_misc.SolveLogEquation()
    question = questions.QuestionTree(q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = markov_chain.MarkovChainBinomial()
    question = questions.QuestionTree(q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = matrix_linear_transformation.MatrixLinearTransformation()
    question = questions.QuestionTree(q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = normal_distribution.NormalDistribution()
    question = questions.QuestionTree(q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = normal_distribution.SimpleNormalDistribution()
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


    q = piecewise_prob_density_function.PiecewiseProbDensityFunctionKnown()
    question = questions.QuestionTree(q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = prob_table_known.ProbTableKnown()
    q_sub1 = prob_table_known.Property(q)
    q_sub2 = prob_table_known.Multinomial(q)
    q_sub3 = prob_table_known.Conditional(q)
    q_sub4 = prob_table_known.Cumulative(q)
    question = questions.QuestionTree(q)
    question.add_part(q_sub1)
    question.add_part(q_sub2)
    question.add_part(q_sub3)
    question.add_part(q_sub4)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = prob_table_unknown.ProbTableUnknown()
    question = questions.QuestionTree(q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = related_rates.RelatedRates()
    question = questions.QuestionTree(q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = simple_definite_integral.SimpleDefiniteIntegral()
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


    q = simple_inverse.SimpleInverse()
    question = questions.QuestionTree(q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)

    
    q = simple_sketch.SimpleSketch()
    q_sub1 = simple_sketch.PointTransformation(q)
    q_sub2 = simple_sketch.EquationTransformation(q)
    question = questions.QuestionTree(q)
    question.add_part(q_sub1)
    question.add_part(q_sub2)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = trig_properties.TrigProperties()
    question = questions.QuestionTree(q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    q = worded_definite_integral.WordedDefiniteIntegral()
    question = questions.QuestionTree(q)
    question.write_question(f)
    question.write_solution(f)
    latex.new_page(f)


    latex.end_tex_document(f)
