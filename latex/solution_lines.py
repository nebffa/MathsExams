from maths.latex import latex


class Lines:
    def __init__(self):
        self.lines = []


    def __add__(self, text):
        if isinstance(text, str):
            self.lines.append(text)
        elif isinstance(text, Lines):
            self.lines.extend(text.lines)

        return self


    def write(self):
        return latex.latex_newline().join(self.lines)
