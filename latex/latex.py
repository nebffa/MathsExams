def latex_newline():
    return r' \\ ' + '\n'


def latex_endline():
    return r' \\ ' + '\n'


def new_page(f):
    f.write(r'\newpage' + '\n')


def document_class(f):
    f.write(r'\documentclass[a4paper, 12pt]{article}' + '' + '\n')


def packages(f):
    f.write(r'\usepackage{amsmath}' + '\n')  # used for \left and \right which are for absolute values
    f.write(r'\usepackage{amssymb}' + '\n')
    f.write(r'\usepackage{mathptmx}' + '\n')
    f.write(r'\usepackage{tabularx}' + '\n')
    f.write(r'\usepackage{graphicx}' + '\n')
    f.write(r'\usepackage[margin=2cm]{geometry}' + '\n')


def settings(f):
    f.write(r'\graphicspath{ {figures/} }')
    f.write(r'\setlength{\parindent}{0pt}')


def new_commands(f):
    f.write(r'\newcommand{\tab}{\hspace*{1em}}' + '' + '\n')



def begin(f):
    f.write(r'\begin{document}' + '\n')


def begin_tex_document(f):
    document_class(f)
    f.write('\n')
    packages(f)
    f.write('\n')
    new_commands(f)
    settings(f)
    f.write('\n')
    begin(f)
    


def end_tex_document(f):
    f.write('\end{document}' + '\n')
