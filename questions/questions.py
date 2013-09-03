from maths.latex import latex, tex_to_pdf, questions


def test_question(question_obj):
    """ Test whether a question's latex is compilable to a PDF.
        TO BE DEPRECATED SOON in favour of test_question_new
    """ 

    question_tree = questions.QuestionTree(question_number=1, part=question_obj)
    f = open('test.tex', 'w')
    _write_question(f, question_tree)
    f.close()

    tex_to_pdf.make_pdf('test')
    #try:
    #    tex_to_pdf.make_pdf('test')
    #    #os.remove('test.pdf')
    #except:
    #    raise IOError('Could not compile .tex file')


def test_question_new(question_tree):
    """ Test whether a question's latex is compilable to a PDF.

    """ 

    f = open('test.tex', 'w')
    _write_question(f, question_tree)
    f.close()

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
