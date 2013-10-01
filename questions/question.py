from maths.latex import latex, questions
from maths.parts import (
                            simple_sketch
                        )


with open('exam.tex', 'w') as f:
    latex.begin_tex_document(f)

    q = simple_sketch.SimpleSketch()
    question = questions.QuestionTree()
    question.add_part(q, tree_location1=1)
    
    question.add_part(questions.DummyPart(), tree_location1=2)
    
    question.add_part(simple_sketch.PointTransformation(q), tree_location1=2)
    question.add_part(simple_sketch.EquationTransformation(q), tree_location1=2)
    question.write_question(f)
    question.write_solution(f)

    latex.end_tex_document(f)
