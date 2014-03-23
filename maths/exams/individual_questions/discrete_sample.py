from maths.latex import latex, questions
from maths.questions import (
                            discrete_sample
                        )
from maths.questions.tests import question_tester
from maths import maths_path
import subprocess
import os


FILE_NAME = os.path.join(maths_path.maths_path(), 'debug', 'exam.tex')

with open(FILE_NAME, 'w') as f:
    q = discrete_sample.NoReplacement()
    q_a = discrete_sample.SpecificPermutation(q)
    q_b = discrete_sample.Sum(q)
    q_c = discrete_sample.ConditionalSum(q)


    question = questions.QuestionTree(q)
    question.add_part(q_a)
    question.add_part(q_b)
    question.add_part(q_c)


try:
    subprocess.call(['killall', 'evince'])
    question_tester.question_tester(question, view_output=True)
except Exception as e:
    raise e