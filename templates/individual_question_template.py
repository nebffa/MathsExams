from maths.latex import questions
from maths.parts import (
                            
                        )
from maths.parts.tests import question_tester
import subprocess


exam_questions = []


q = 
question = questions.QuestionTree(q)


exam_questions.append(question)


try:
    subprocess.call(['killall', 'evince'])
    question_tester.question_tester(exam_questions, view_output=True)
except Exception as e:
    raise e