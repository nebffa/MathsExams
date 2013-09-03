from maths.latex import latex, tex_to_pdf

'''
def test_question(question_obj):
    """ Test whether a question's latex is compilable to a PDF.
        TO BE DEPRECATED SOON in favour of test_question_new
    """ 

    question_tree = questions.QuestionTree(question_number=1, part=question_obj)
    with open('test.text', 'w') as f:
        _write_question(f, question_tree)

    tex_to_pdf.make_pdf('test')'''


def test_question(question_tree):
    """ Test whether a question's latex is compilable to a PDF.

    """ 

    with open('test.tex', 'w') as f:
        _write_question(f, question_tree)

    tex_to_pdf.make_pdf('test')



def _write_question(f, question_tree):
    """ A helper function to test_question - writes a single question as a standalone .tex file.

    """

    latex.document_class(f)
    latex.packages(f)
    latex.new_commands(f)
    latex.begin_tex_document(f)
    latex.set_tabs(f)
    question_tree.write_question(f)
    question_tree.write_solution(f)
    latex.end_tex_document(f)


def to_string(lines):
    for i in range(len(lines)):
        if i != len(lines) - 1:
            lines[i] += latex.latex_newline()

    return ''.join(lines)
