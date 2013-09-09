from maths.latex import latex


class Part(object):
    def __init__(self, part_number, question_statement='', solution_statement='', num_lines=0, num_marks=0):
        self.part_number = part_number
        self.question_statement = question_statement
        self.solution_statement = solution_statement
        self.num_lines = num_lines
        self.num_marks = num_marks
        self.children = []

    def add_child(self, part_number, question_statement='', solution_statement='', num_lines=0, num_marks=0):
        self.children.append(Part(part_number, question_statement, solution_statement, num_lines, num_marks))

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
            total_string += obj.question_statement + latex.latex_newline() + '\n'

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
            total_string += obj.solution_statement + latex.latex_newline() + '\n'
        for i in obj.children:
            total_string += obj.solution_traversal_to_latex(i, depth + 1)

        return total_string

    def _question_lines(self, depth, num_lines):
        total_string = (r'\>' * (depth + 2) + r'\linefill' + latex.latex_newline()) * num_lines

        return total_string + '\n'

    def _question_heading(self):
        return r'\textbf{{Question {0}}}'.format(self.part_number) + latex.latex_newline()

    def _question_part(self, part_symbol):
        return r'\textbf{{{0}.}} \tab\='.format(part_symbol)


# TODO: needs work to incorporate num_marks in the latex output
class QuestionTree(object):
    def __init__(self, question_number, part):
        self.root = Part(question_number, part.question_statement(), part.solution_statement(), part.num_lines, part.num_marks)

    def add_part(self, part, tree_location1, tree_location2=None):
        if tree_location2 is None:
            self.root.add_child(tree_location1, part.question_statement(), part.solution_statement(), part.num_lines, part.num_marks)
        else:
            self.root.children[tree_location1].add_child(
                                tree_location2, part.question_statement(), part.solution_statement(), part.num_lines, part.num_marks)

    def write_question(self, f):
        f.write(self.root.question_traversal_to_latex(self.root, depth=0))

    def write_solution(self, f):
        f.write(self.root.solution_traversal_to_latex(self.root, depth=0))