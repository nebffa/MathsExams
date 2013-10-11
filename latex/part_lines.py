from maths.latex import latex


class Lines:
    def __init__(self):
        self.lines = []


    def __add__(self, text):
        self.lines.append(text)
        return self


    def write(self):
        return latex.latex_newline().join(self.lines)
