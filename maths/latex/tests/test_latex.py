from .. import latex


def test_latex_newline():
    assert latex.latex_newline() == r' \\ ' + '\n'
