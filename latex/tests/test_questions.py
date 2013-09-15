from .. import questions
from maths.latex import latex


def test_Part_question_lines():
    test_part = questions.Part(part_number=1)

    assert test_part._question_lines(depth=1, num_lines=2) == (
            r'\tab\tab\tab\hrulefill' + latex.latex_newline() + r'\tab\tab\tab\hrulefill' + latex.latex_newline() + '\n')
    assert test_part._question_lines(depth=2, num_lines=1) == (
            r'\tab\tab\tab\tab\hrulefill' + latex.latex_newline() + '\n')
    assert test_part._question_lines(depth=2, num_lines=2) == (
            r'\tab\tab\tab\tab\hrulefill' + latex.latex_newline() + r'\tab\tab\tab\tab\hrulefill' + latex.latex_newline() + '\n')
