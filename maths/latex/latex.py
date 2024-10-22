import os
from .. import maths_path


def latex_newline():
    return r' \\ ' + '\n'


def latex_endline():
    return r' \\ ' + '\n'


def decrement_question_counter(f):
    """Decrement the question counter, which determines the number that the next question will be.

    In some cases, we may want to display the solution of a question immediately after a question. Therefore,
    we don't want to have 'Question 4' followed by a solution labeled 'Question 5'. Decrementing the counter
    allows us to follow with a solution labeled 'Question 4'.
    """

    f.write(r'\addtocounter{partsi}{-1}' + '\n')



def new_page(f):
    f.write(r'\newpage' + '\n')


def document_class(f):
    f.write(r'\documentclass[a4paper, 12pt]{article}' + '' + '\n')


def enumerator(f):
    f.write(r'\newlist{parts}{enumerate}{3}' + '\n')
    # there has to be something more sensible than just choosing 0.87 inches
    f.write(r'\setlist[parts]{label=\textbf{Question \arabic*}, itemindent={0.82in}, leftmargin={0in}, nosep}' + '\n')
    f.write(r'\setlist[parts, 2]{label=\textbf{\alph*.}, itemindent={0.2in}, itemsep=20pt}' + '\n')
    f.write(r'\setlist[parts, 3]{label=\textbf{\roman*.}, itemindent={0in}, itemsep=20pt, leftmargin={0.4in}}' + '\n')


def packages(f):
    fillwithlines_path = os.path.join(maths_path.maths_path(), 'exams', 'fillwithlines')
    latex_friendly_path = fillwithlines_path.replace('\\', '/')


    f.write(r'\usepackage{amsmath}' + '\n')  # used for \left and \right which are for absolute values
    f.write(r'\usepackage{amssymb}' + '\n')
    f.write(r'\usepackage{mathptmx}' + '\n')
    f.write(r'\usepackage{tabularx}' + '\n')
    f.write(r'\usepackage{graphicx}' + '\n')
    f.write(r'\usepackage{enumitem}' + '\n')
    f.write(r'\usepackage{mathtools}' + '\n')
    f.write(r'\usepackage{{{0}}}'.format(latex_friendly_path) + '\n')
    f.write(r'\usepackage[margin=2cm]{geometry}' + '\n')


def settings(f):
    f.write(r'\graphicspath{ {figures/} }' + '\n')
    f.write(r'\setlength{\parindent}{0pt}' + '\n')
    # force individual question parts to not be spread across two pages
    f.write(r'\interlinepenalty=10000' + '\n')


def new_commands(f):
    f.write(r'\newcommand{\tab}{\hspace*{1em}}' + '' + '\n')



def begin(f):
    f.write(r'\begin{document}' + '\n')
    f.write(r'\begin{parts}' + '\n')


def begin_tex_document(f):
    f.write(r'\batchmode' + '\n')
    document_class(f)
    f.write('\n')
    packages(f)
    f.write('\n')
    new_commands(f)
    f.write('\n')
    enumerator(f)
    f.write('\n')
    settings(f)
    f.write('\n')
    f.write(r'\scrollmode' + '\n')
    begin(f)



def end_tex_document(f):
    f.write('\end{parts}' + '\n')
    f.write('\end{document}' + '\n')
    f.write(r'\batchmode' + '\n')
