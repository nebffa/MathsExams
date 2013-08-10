from ..latex import latex, tex_to_pdf
import os

def new_question(question_number, part):
    """ Create a new question.

    Required inputs: 
        1. Question number inside the exam
        2. A question part

    """
    return latex.QuestionTree(part_number=question_number, 
                              question_statement=part.question_statement(), 
                              solution_statement=part.solution_statement(), 
                              num_lines=part.num_lines,
                              num_marks=part.num_marks)


def add_part(question_tree, tree_location1, tree_location2=None, part=None):
    """ Add a new part to an existing question.

    Required inputs:
        1. A QuestionTree object
        2. A question part
        3. The part's location inside the QuestionTree

    """

    if part is None:
        question_tree.add_part(tree_location1)
    else:
        question_tree.add_part(tree_location1, 
                               question_statement=part.question_statement(),
                               solution_statement=part.solution_statement(),
                               num_lines=part.num_lines,
                               num_marks=part.num_marks)
        

def test_question(question_obj):
    """ Test whether a question's latex is compilable to a PDF.

    """ 

    question_tree = new_question(question_number=1, part=question_obj)
    f = open('test.tex', 'w')
    _write_question(f, question_tree)
    f.close()

    try:
        tex_to_pdf.make_pdf('test')
        os.remove('test.pdf')
    except:
        raise IOError('Could not compile .tex file')


def _write_question(f, question_tree):
    """ A helper function to test_question - writes a single question as a standalone .tex file.

    """

    latex.document_class(f)
    latex.packages(f)
    latex.new_commands(f)
    latex.begin(f)
    latex.set_tabs(f)
    question_tree.write_question(f)
    question_tree.write_solution(f)
    latex.end(f)
