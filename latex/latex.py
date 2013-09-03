def latex_newline():
    return r' \\ ' + '\n'


def latex_endline():
    return r' \\ '


def document_class(f):
    f.write(r'\documentclass[a4paper, 12pt]{article}' + '' + '\n\n')


def packages(f):
    f.write(r'\usepackage{amsmath}' + '\n')  # used for \left and \right which are for absolute values
    f.write(r'\usepackage{amssymb}' + '\n')
    f.write(r'\usepackage{mathptmx}' + '\n')
    f.write(r'\usepackage{tabularx}' + '\n')
    f.write(r'\usepackage[margin=1cm]{geometry}' + '\n')


def new_commands(f):
    f.write(r'\newcommand{\tab}{\hspace*{1em}}' + '' + '\n')
    f.write(r'\makeatletter\n')
    f.write(r'\def\linefill{%\n')
    f.write(r'\leavevmode\n')
    f.write(r'\leaders\hrule\hskip\dimexpr\\textwidth -\@tempdima\mbox{}}' + '\n')


def set_tabs(f):
    f.write(r'\= \tab \tab \= \tab \tab \= \\' + '\n')


def begin(f):
    f.write(r'\begin{document}' + '\n')
    f.write(r'\begin{tabbing}' + '\n\n')


def begin_tex_document(f):
    document_class(f)
    packages(f)
    new_commands(f)
    begin(f)
    set_tabs(f)


def end_tex_document(f):
    f.write('\end{tabbing}' + '\n')
    f.write('\end{document}' + '\n')


# a class to feed in question data, and ultimately have it print the question as latex
# note that each line indicates a new line of the printed latex
# note that any text in round parentheses denotes my comments
# question template is:
# line1: Question {question_number}
# line2: {question_statement}
# line3: {letter}. {subpart_question_statement}  (a new sub-part)
# line4: {roman_numeral}. {subsubpart_question_statement} (a new sub-sub-part)
# line5: questionum_lines (to 0, 1 or 2 levels of indentation depending on if we have parts and subparts)
# (repeat lines 3-5 until the question is finished)
