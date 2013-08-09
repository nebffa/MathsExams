from ..latex import latex


def new_question(question_number, part):
    return latex.QuestionTree(part_number=question_number, 
                              question_statement=part.question_statement(), 
                              solution_statement=part.solution_statement(), 
                              num_lines=part.num_lines,
                              num_marks=part.num_marks)


def add_part(question_tree, tree_location1, tree_location2=None, part=None):
    if part is None:
        question_tree.add_part(tree_location1)
    else:
        question_tree.add_part(tree_location1, 
                               question_statement=part.question_statement(),
                               solution_statement=part.solution_statement(),
                               num_lines=part.num_lines,
                               num_marks=part.num_marks)
        

def question_test(f, question):
    latex.document_class(f)
    latex.packages(f)
    latex.new_commands(f)
    latex.set_tabs(f)
    latex.begin(f)
    question.write_question(f)
    question.write_solution(f)
    latex.end(f)