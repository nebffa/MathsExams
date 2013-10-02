from maths.latex import latex, questions
from maths.parts import (
                            simple_sketch
                        )


with open('exam.tex', 'w') as f:
    latex.begin_tex_document(f)

    q = simple_sketch.SimpleSketch()
    question = questions.QuestionTree()
    question.add_part(q)
    
    question.add_part()
    
    question.add_part(simple_sketch.PointTransformation(q), tree_location=1)
    question.add_part(simple_sketch.EquationTransformation(q), tree_location=1)
    question.write_question(f)
    latex.new_page(f)
    question.write_solution(f)

    latex.end_tex_document(f)
