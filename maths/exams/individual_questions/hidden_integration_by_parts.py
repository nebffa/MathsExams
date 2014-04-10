from maths.latex import questions
from maths.questions import (
                            hidden_integration_by_parts
                        )
from maths.questions.tests import question_tester
import subprocess


exam_questions = []


q = hidden_integration_by_parts.HiddenIntegrationByParts()
q_a = hidden_integration_by_parts.Derivative(q)
q_b = hidden_integration_by_parts.Integration(q)

question = questions.QuestionTree(q)
question.add_part(q_a)
question.add_part(q_b)



exam_questions.append(question)


try:
    subprocess.call(['killall', 'evince'])
    question_tester.question_tester(exam_questions, view_output=True)
except Exception as e:
    raise e