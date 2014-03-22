from maths.latex import latex, questions
from maths.parts import (
                            normal_distribution
                        )
from maths.parts.tests import question_tester
from maths import maths_path
import subprocess
import os


FILE_NAME = os.path.join(maths_path.maths_path(), 'debug', 'exam.tex')

exam_questions = []

q = normal_distribution.SimpleNormalDistribution()
exam_questions.append(questions.QuestionTree(q))

q = normal_distribution.NormalDistribution()
q_a = normal_distribution.Half(q)
q_b = normal_distribution.ProbabilityEquality(q)
question = questions.QuestionTree(q)
question.add_part(part=q_a)
question.add_part(part=q_b)
exam_questions.append(question)


try:
    subprocess.call(['killall', 'evince'])
    question_tester.question_tester(exam_questions, view_output=True)
except Exception as e:
    raise e