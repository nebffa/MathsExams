from maths.latex import latex
import functions

file = open('exam.tex', 'w')

latex.document_class(file)
latex.packages(file)
latex.new_commands(file)
latex.begin(file)
latex.set_tabs(file)

q = functions.SimpleInverse()

question = latex.QuestionTree(part_number=1, question_statement=q.question_statement(), solution_statement=q.solution_statement(), num_lines=q.num_lines)
question.write_question(file)
question.write_solution(file)

latex.end(file)
