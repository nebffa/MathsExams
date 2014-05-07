import sympy
from . import latex


class Lines:
    """A class to help with storing and writing solution lines.
    """

    def __init__(self):
        self.lines = []

    def __add__(self, text):
        if isinstance(text, str):
            self.lines.append(text)
        elif isinstance(text, Lines):
            self.lines.extend(text.lines)

        return self

    def write(self):
        """Write the lines in a LaTeX-friendly format.
        """
        return latex.latex_newline().join(self.lines)


def latexify_question_information(information):
    """Return the dictionary of question parameters or question information with values replaced by their latex'd version.

    The rationale:

    def question_statement(self):
        return r'Let $f:{domain} \rightarrow R$, where $f(x) = {equation}$. Find the inverse of $f$.'.format(
            equation=sympy.latex(self._qp['equation']),
            domain=sympy.latex(self._qp['domain'])
        )

    could be converted to

    def question_statement(self):
        return r'Let $f:{domain} \rightarrow R$, where $f(x) = {equation}$. Find the inverse of $f$.'.format(
            **latexify_question_information(self._qp)
        )
    """

    return {key: sympy.latex(value) for key, value in information.items()}
