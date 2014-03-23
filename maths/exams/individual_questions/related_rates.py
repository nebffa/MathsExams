from maths.latex import latex, questions
from maths.questions import (
                            related_rates
                        )
from maths.questions.tests import question_tester
from maths import maths_path
import subprocess
import os


FILE_NAME = os.path.join(maths_path.maths_path(), 'debug', 'exam.tex')

with open(FILE_NAME, 'w') as f:
    q = related_rates.RelatedRates()
    question = questions.QuestionTree(q)


    
try:
    subprocess.call(['killall', 'evince'])
    question_tester.question_tester(question, view_output=True)
except Exception as e:
    raise e