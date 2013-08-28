import sympy
import random
from sympy.abc import *
from maths import all_functions, not_named_yet, simplify
from . import questions


class SimpleInverse(object):
    def __init__(self):

        self.function_type = random.choice(['exp', 'hyperbola', 'log', 'cubic'])

        self.function_type = 'log'

        self.domain, self.range = None, None

        if self.function_type == 'exp':
            # 2008 10a: f(x) = e^(2x) - 1 [6 lines] [2 marks]
            func = all_functions.request_exp(difficulty=3)
            self.equation = func.equation
        elif self.function_type == 'hyperbola':
            # 2009 3: f(x) = 3/x - 4 [7 lines] [3 marks]
            func = all_functions.request_hyperbola(difficulty=3)
            self.equation = func.equation
        elif self.function_type == 'log':
            # there was no exam question involving a log, but since it's hte inverse of exp which has been used, I thought to include it
            func = all_functions.request_log(difficulty=3)
            self.equation = func.equation
        elif self.function_type == 'cubic':  # no base class for cubics so I make it here
            # 2012 3: h(x) = 2x**3 + 1 [5 lines] [2 marks]
            m = not_named_yet.randint_no_zero(-3, 3)
            c = not_named_yet.randint_no_zero(-5, 5)
            self.equation = m*x**3 + c
            if random.choice([True, False]):
                self.domain = sympy.Interval(-sympy.oo, 0, True, False)
                if m > 0:
                    self.range = sympy.Interval(-sympy.oo, c, True, False)
                else:
                    self.range = sympy.Interval(c, sympy.oo, False, True)
            else:
                self.domain = sympy.Interval(0, sympy.oo, False, True)
                if m > 0:
                    self.range = sympy.Interval(c, sympy.oo, False, True)
                else:
                    self.range = sympy.Interval(-sympy.oo, c, True, False)

        self.inverse = all_functions.inverse(self.equation)

        # do some simplification for printing purposes
        if self.function_type == 'hyperbola':
            self.inverse = sympy.apart(self.inverse)
        elif self.function_type == 'exp':
            self.inverse = simplify.canonise_log(self.inverse)

        if self.domain is None and self.range is None:
            self.domain, self.range = func.domain, func.range
        self.inverse_domain, self.inverse_range = self.range, self.domain

    def question_statement(self):
        if random.choice([True, False]):
            self.num_lines, self.num_marks = 6, 2  # the question won't involve finding the domain
            question_statement = r'''Let $f:%s \rightarrow R, f(x) = %s$. Find the rule and
                                    domain of the inverse function $f^{-1}.$''' % (sympy.latex(self.domain), sympy.latex(self.equation))
        else:
            self.num_lines, self.num_marks = 7, 3
            question_statement = r'''Let $f:%s \rightarrow R$, where $f(x) = %s$. Find $f^{-1}$,
                                    the inverse function of $f$.''' % (sympy.latex(self.domain), sympy.latex(self.equation))

        return question_statement

    def solution_statement(self):
        solution = []
        if self.num_lines == 7:
            solution += [r'$d_{f^{-1}} = r_{f} = %s$' % sympy.latex(self.inverse_domain)]

        solution += [r'$f^{-1}(x) = %s$' % sympy.latex(self.inverse)]

        return questions.to_string(solution)
