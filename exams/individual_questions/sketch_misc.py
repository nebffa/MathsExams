from maths.latex import latex, questions
from maths.questions import (
                            sketch_misc,
                            piecewise
                        )


# currently consigned to a dustbin as it has nothing to be paired with - it requires a parent question with a function that has an open-ended domain
'''
with open('exam.tex', 'w') as f:
    latex.begin_tex_document(f)

    
    q_a = sketch_misc.SketchDoubleInverse(q)

    question = questions.QuestionTree(questions.DummyPart())
    question.add_part(q)
    question.add_part(q_a)

    question.write_question(f)
    latex.new_page(f)
    question.write_solution(f)

    latex.end_tex_document(f)
'''