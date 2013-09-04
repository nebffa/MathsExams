import sympy
import random
from sympy.abc import *
from maths import all_functions


class Antiderivative:
    def __init__(self):

        # there is no correlation between function type and marks assigned, so we have to choose between
        # the historic 1 or 2 marks this question has been assigned
        self.num_marks = random.randint(1, 2)
        self.num_lines = 4

        self._function_type = random.choice(['linear', 'trig'])

        inner_function = all_functions.request_linear(difficulty=3).equation
        if self._function_type == 'linear':
            # 2009 2a: y = 1 / (1 - 2x) [4 lines] [2 marks]
            # 2011 2a: y = 1 / (3x - 4) [5 lines] [1 mark]
            # 2012 2: y = 1 / (2x - 1)^3 [4 lines] [2 marks]
            self.num_lines = 4

            index = random.randint(1, 3)

            self.equation = 1 / inner_function ** index

        elif self._function_type == 'trig':
            # 2010 2a: y = cos(2x + 1) [2 lines] [1 mark]
            self.num_lines = 2

            outer_function = random.choice([sympy.cos, sympy.sin])
            self.equation = outer_function(inner_function)

        self.antiderivative = self.equation.integrate()

    # in all years but 2012, question 2 has been composed of two unrelated parts - we need to signal to write_question
    # whether is a subpart or whether it is an entire question
    def question_statement(self):

        # sympy prints things like (1 + 2x)^-2 as exactly that, rather than in fraction form, so we have to manually
        # print it as a fraction
        if self._function_type == 'linear':
            inner_function, index = self.equation.as_base_exp()
            # don't print the index if it's one!!!
            if abs(index) == 1:
                equation = r"\frac{1}{%s}" % sympy.latex(inner_function)
            else:
                equation = r"\frac{1}{\left(%s\right)^{%d}}" % (sympy.latex(inner_function), abs(index))
        else:
            equation = sympy.latex(self.equation)

        return 'Find an antiderivative of $%s$ with respect to $x$.' % equation

    def solution_statement(self):
        # sympy integrates things like 1/x as log(x), not log(|x|) (the explanation given to me was that it was due to complex numbers)

        proper_antiderivative = self.antiderivative.replace(sympy.log(a), sympy.log(sympy.Abs(a)))

        total_string = r'$%s + c$' % sympy.latex(proper_antiderivative)
        total_string += r'The constant $c$ is not necessary. It can be any real number, including zero.'

        return total_string

    def sanity_check(self):
        pass
