

def latex_newline():
    return r' \\ ' + '\n'


def document_class(f):
    f.write(r'\documentclass[a4paper, 12pt]{article}' + '\n\n')


def packages(f):
    f.write('\usepackage{amsmath}\n')  # used for \left and \right which are for absolute values
    f.write('\usepackage{mathptmx}\n')
    f.write('\usepackage[margin=1cm]{geometry}\n\n')


def new_commands(f):
    f.write(r'\newcommand{\tab}{\hspace*{1em}}' + '\n')
    f.write('\makeatletter\n')
    f.write('\def\linefill{%\n')
    f.write('\leavevmode\n')
    f.write('\leaders\hrule\hskip\dimexpr\\textwidth -\@tempdima\mbox{}}\n\n')


def begin(f):
    f.write(r'\begin{document}' + '\n')
    f.write(r'\begin{tabbing}' + '\n\n')


def end(f):
    f.write('\end{tabbing}\n')
    f.write('\end{document}\n\n')
    f.close()


def set_tabs(f):
    f.write(r'\= \tab \tab \= \tab \tab \= \\' + '\n')


class Part(object):
    def __init__(self, part_number, question_statement='', solution_statement='', num_lines=0):
        self.part_number = part_number
        self.question_statement = question_statement
        self.solution_statement = solution_statement
        self.num_lines = num_lines
        self.children = []

    def add_child(self, part_number, question_statement='', solution_statement='', num_lines=0):
        self.children.append(Part(part_number, question_statement, solution_statement, num_lines))

    def question_traversal_to_latex(self, obj, depth):
        total_string = ''

        # 1. if there's a question statement - print it
        # 2. if there are question lines - print them
        # 3. recurse

        if depth == 0:
            total_string = obj._question_heading()
        elif depth == 1:
            part_symbol = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i'}[obj.part_number]
            total_string = obj._question_part(part_symbol)
        elif depth == 2:
            part_symbol = {1: 'i', 2: 'ii', 3: 'iii', 4: 'iv', 5: 'v', 6: 'vi', 7: 'vii', 8: 'viii', 9: 'ix'}[obj.part_number]
            total_string = obj._question_part(part_symbol)

        if obj.question_statement != '':
            total_string += obj.question_statement + latex_newline()

        if obj.num_lines > 0:
            total_string += obj._question_lines(depth, obj.num_lines)

        for i in obj.children:
            total_string += obj.question_traversal_to_latex(i, depth + 1)

        return total_string

    def solution_traversal_to_latex(self, obj, depth):
        total_string = ''

        # 1. if there's a solution_statement - print it
        # 2. recurse

        if depth == 0:
            total_string = obj._question_heading()
        elif depth == 1:
            part_symbol = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i'}[obj.part_number]
            total_string = obj._question_part(part_symbol)
        elif depth == 2:
            part_symbol = {1: 'i', 2: 'ii', 3: 'iii', 4: 'iv', 5: 'v', 6: 'vi', 7: 'vii', 8: 'viii', 9: 'ix'}[obj.part_number]
            total_string = obj._question_part(part_symbol)

        if obj.solution_statement != '':
            total_string += obj.solution_statement + latex_newline()
        for i in obj.children:
            total_string += obj.solution_traversal_to_latex(i, depth + 1)

        return total_string

    def _question_lines(self, depth, num_lines):
        total_string = ('\>' * depth + r'\linefill' + latex_newline()) * num_lines

        return total_string + '\n'

    def _question_heading(self):
        return r'\textbf{Question %d}' % self.part_number + latex_newline()

    def _question_part(self, part_symbol):
        return r'\textbf{%s.} \tab\=' % part_symbol


class QuestionTree(object):
    def __init__(self, part_number, question_statement='', solution_statement='', num_lines=0):
        #self.data = {'part_number': part_no, 'statement': stmt, 'num_lines': num_lines}
        self.root = Part(part_number, question_statement, solution_statement, num_lines)

    def add_part(self, tree_location1, question_statement='', solution_statement='', num_lines=0, tree_location2=None):
        if tree_location2 is None:
            self.root.add_child(tree_location1, question_statement, solution_statement, num_lines)
        else:
            self.root.children[tree_location1].add_child(tree_location2, question_statement, solution_statement, num_lines)

    def write_question(self, f):
        f.write(self.root.question_traversal_to_latex(self.root, depth=0))

    def write_solution(self, f):
        f.write(self.root.solution_traversal_to_latex(self.root, depth=0))




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
