from .. import latex


def test_latex_newline():
    assert latex.latex_newline() == r' \\ ' + '\n'


def test_Part_question_lines():
    test_part = latex.Part(part_number=1)

    assert test_part._question_lines(depth=1, num_lines=2) == r'\>\>\>\linefill' + latex.latex_newline() + r'\>\>\>\linefill' + latex.latex_newline() + '\n'
    assert test_part._question_lines(depth=2, num_lines=1) == r'\>\>\>\>\linefill' + latex.latex_newline() + '\n'
    assert test_part._question_lines(depth=2, num_lines=2) == r'\>\>\>\>\linefill' + latex.latex_newline() + r'\>\>\>\>\linefill' + latex.latex_newline() + '\n'
