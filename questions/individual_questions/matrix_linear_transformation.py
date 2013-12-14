from maths.latex import questions
from maths.parts import (
                            matrix_linear_transformation
                        )
from maths.parts.tests import question_tester
import subprocess



exam_questions = []
q = matrix_linear_transformation.MatrixLinearTransformation()
exam_questions.append(questions.QuestionTree(q))


try:
    subprocess.call(['killall', 'evince'])
    question_tester.question_tester(exam_questions, view_output=True)
except Exception as e:
    raise e