from maths.latex import questions
from maths.parts import (
                            simple_sketch
                        )
import subprocess
from maths.parts.tests import question_tester


exam_questions = []



q = simple_sketch.SimpleSketch()
question = questions.QuestionTree()
question.add_part(q)

question.add_part()

question.add_part(simple_sketch.PointTransformation(q))
question.add_part(simple_sketch.EquationTransformation(q))

exam_questions.append(question)



try:
    subprocess.call(['killall', 'evince'])
    question_tester.question_tester(exam_questions, view_output=True)
except Exception as e:
    raise e