from . import latex


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



# this construction can be used to make a multi-line equation with the equals signs aligned, e.g:
# y = x
#   = z
#   = x**3 + 2
# rather than:
# y = x
# = z
# = x**3 + 2
"""
\begin{flalign*}
x &= y &\\
&= z &
\end{flalign*}
"""