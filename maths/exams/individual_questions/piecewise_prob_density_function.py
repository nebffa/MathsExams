from ...latex import questions
from ...questions import piecewise_prob_density_function
from ...questions.tests import question_tester
import subprocess


exam_questions = []


q = piecewise_prob_density_function.PiecewiseProbDensityFunctionKnown()
question = questions.QuestionTree(q)
question.add_part(piecewise_prob_density_function.Conditional(q))
question.add_part(piecewise_prob_density_function.Cumulative(q))
exam_questions.append(question)

q = piecewise_prob_density_function.PiecewiseProbDensityFunctionUnknown()
question = questions.QuestionTree(q)
exam_questions.append(question)


try:
    subprocess.call(['killall', 'evince'])
    question_tester.question_tester(exam_questions, view_output=True)
except Exception as e:
    raise e
