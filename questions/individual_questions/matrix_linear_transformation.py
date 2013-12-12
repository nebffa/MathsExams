from maths.latex import latex, questions
from maths.parts import (
                            matrix_linear_transformation
                        )
from maths.parts.tests import question_tester
from maths import maths_path
import subprocess
import os


FILE_NAME = os.path.join(maths_path.maths_path(), 'debug', 'exam.tex')

exam_questions = []

q = matrix_linear_transformation.MatrixLinearTransformation()
exam_questions.append(questions.QuestionTree(q))


try:
    subprocess.call(['killall', 'evince'])
    question_tester.question_tester(exam_questions, view_output=True)
except Exception as e:
    raise e