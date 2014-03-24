from . import latex


class DummyPart:
    def __init__(self):
        self.num_lines, self.num_marks = 0, 0

    def question_statement(self):
        return ''

    def solution_statement(self):
        return ''

    def sanity_check(self):
        pass


class Part(object):
    def __init__(self, question_statement='', solution_statement='', num_lines=0, num_marks=0):
        self.question_statement = question_statement
        self.solution_statement = solution_statement
        self.num_lines = num_lines
        self.num_marks = num_marks
        self.children = []

    def add_child(self, question_statement='', solution_statement='', num_lines=0, num_marks=0):
        self.children.append(Part(question_statement, solution_statement, num_lines, num_marks))


    # does use the enumitem package, few hbox errors
    def new_question_traversal_to_latex(self, obj, depth):
        total_string = r'\item' + '\n'

        if obj.question_statement and depth == 0:
            total_string += r'$ $\newline' + '\n' + obj.question_statement + '\n'
        elif obj.question_statement:
            total_string += obj.question_statement + '\n'
        else:
            total_string += r'$ $'

        if obj.num_lines != 0:
            total_string += r'\fillwithlines{{{0}in}}'.format(obj.num_lines / 4) + '\n'

        if obj.children:
            total_string += r'\begin{parts}' + '\n' + '\n'.join(
                        obj.new_question_traversal_to_latex(i, depth + 1) for i in obj.children) + r'\end{parts}' + '\n'

        return total_string + '\n'


    # does use the enumitem package, few hbox errors
    def new_solution_traversal_to_latex(self, obj, depth):
        total_string = ''
        if depth == 0:
            total_string += r'\addtocounter{partsi}{-1}' + '\n'
        total_string += r'\item' + '\n'

        if obj.solution_statement and depth == 0:
            total_string += r'$ $\newline' + '\n' + obj.solution_statement + '\n'
        elif obj.solution_statement:
            total_string += obj.solution_statement + '\n'
        else:
            total_string += r'$ $'

        if obj.children:
            total_string += r'\begin{parts}' + '\n' + '\n'.join(
                        obj.new_solution_traversal_to_latex(i, depth + 1) for i in obj.children) + r'\end{parts}' + '\n'

        return total_string + '\n'


    def _question_lines(self, depth, num_lines):
        total_string = (r'\tab' * (depth + 2) + r'\hrulefill' + latex.latex_newline()) * num_lines
        #total_string = latex.latex_newline().join([r'\tab' * (depth + 2) + r'\hrulefill'] * num_lines)

        return total_string + '\n'


# TODO: needs work to incorporate num_marks in the latex output
class QuestionTree(object):

    def __init__(self, part=DummyPart()):
        self.root = Part(part.question_statement(), part.solution_statement(), part.num_lines, part.num_marks)

    def add_part(self, part=DummyPart(), tree_location=None):
        if tree_location is None:
            self.root.add_child(part.question_statement(), part.solution_statement(), part.num_lines, part.num_marks)
        else:
            self.root.children[tree_location].add_child(
                                part.question_statement(), part.solution_statement(), part.num_lines, part.num_marks)

    def write_question(self, f):
        f.write(self.root.new_question_traversal_to_latex(self.root, depth=0))

    def write_solution(self, f):
        f.write(self.root.new_solution_traversal_to_latex(self.root, depth=0))

    def question_latex(self):
        return self.root.new_question_traversal_to_latex(self.root, depth=0)

    def solution_latex(self):
        return self.root.new_solution_traversal_to_latex(self.root, depth=0)
