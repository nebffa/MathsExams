from ...latex import questions
from ...questions import (
                            definite_integral_equality
                        )
from ...questions.tests import question_tester
import subprocess


exam_questions = []


q = definite_integral_equality.DefiniteIntegralEquality()
question = questions.QuestionTree(q)


exam_questions.append(question)


try:
    subprocess.call(['killall', 'evince'])
    question_tester.question_tester(exam_questions, view_output=True)
except Exception as e:
    raise e