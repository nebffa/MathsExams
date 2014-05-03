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
