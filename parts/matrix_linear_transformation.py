import sympy
import random
from maths import all_functions, not_named_yet
from maths.symbols import *
from maths.latex import solution_lines
from maths.utils import transformations, noevals
import collections


class MatrixLinearTransformation:
    def __init__(self):
        # 2010 Q6 [11 lines] [3 marks]
        self.num_lines, self.num_marks = 11, 3
        self._qp = {}

        self._qp['transformation'] = transformations.random_transformation(num_transformations=2)

        self._qp['overall_transformation'] = transformations.overall_transformation(self._qp['transformation'])

        self._qp['x_dilation_and_translation'] = self._qp['overall_transformation'][0].coeff(x)
        self._qp['y_dilation_and_translation'] = self._qp['overall_transformation'][1].coeff(y)

        self._qp['x_translation'] = self._qp['overall_transformation'][0].as_coeff_Add()[0]
        self._qp['y_translation'] = self._qp['overall_transformation'][1].as_coeff_Add()[0]

        self._qp['equation'] = all_functions.random_function(exclude=['linear']).equation

        
        # wanted to use wilds, but sympy auto-rearranges any symbols to precede a wild.
        # e.g. y = a*sin(b*x + c) + d    when printed becomes    y = a*sin(x*b + c) + d which is not how the convention goes
        # so we use symbols here for writing the equation, and we will use wilds in the solution for finding the answer
        a, b, c, d = sympy.symbols('a b c d')


        sympy_types = [sympy.cos, sympy.sin, sympy.tan, sympy.cot, sympy.sec, sympy.csc, sympy.log, sympy.exp]

        wildcards = dict((sympy_type, a*sympy_type(b*x + c) + d) for sympy_type in sympy_types)
        wildcards[2] = a*x**2 + b*x + c

        expr_type = all_functions.detect_expr_type(self._qp['equation'])

        self._qp['wildcard_equation'] = wildcards[expr_type]


    def question_statement(self):
        self._qi = {}

        symbols_matrix = sympy.Matrix([x, y])
        dilation_matrix = sympy.Matrix([[self._qp['x_dilation_and_translation'], 0], [0, self._qp['y_dilation_and_translation']]])
        translation_matrix = sympy.Matrix([self._qp['x_translation'], self._qp['y_translation']])
        formula = r'''T({0}) = {1}{0} + {2}'''.format(
                    sympy.latex(symbols_matrix),
                    sympy.latex(dilation_matrix),
                    sympy.latex(translation_matrix)
                )



        # the symbols can get pulled out of order when looking at expr.free_symbols. As of 10/12/2013 we can use
        # the builtin sorted to sort them in alphabetical order
        wilds = sorted([i for i in self._qp['wildcard_equation'].free_symbols if i != x])

        return r'''The transformation $T: R^{{2}} \rightarrow R^{{2}}$ is defined by \[{0}\]
                The image of the curve $y = {1}$ under the transformation $T$ has equation y = ${2}$. Find the values of ${3}$.'''.format(
                        formula,
                        sympy.latex(self._qp['equation']),
                        sympy.latex(self._qp['wildcard_equation']),
                        ', '.join([sympy.latex(i) for i in wilds])
                    )




    def solution_statement(self):
        lines = solution_lines.Lines()

        # e.g. T([x; y]) = [x - 2; y]        
        lines += r'''$T({0}) = {1}$'''.format(
                    sympy.latex(sympy.Matrix([x, y])),
                    sympy.latex(sympy.Matrix(self._qp['overall_transformation']))
                )

        noevaled = noevals.noevalify(self._qp['equation'])
        noevaled = noevaled.subs({x: self._qp['overall_transformation'][0]})


        # e.g. \therefore y = tan(-x + 3*pi/4) transforms to y = -tan(x/2 - 2 + pi/4)
        lines += r'''$\therefore y = {0}$ transforms to ${1} = {2}$'''.format(
                    sympy.latex(self._qp['equation']),
                    sympy.latex(self._qp['overall_transformation'][1]),
                    sympy.latex(noevaled)
                )

        transformed_equation = transformations.apply_transformations(self._qp['transformation'], self._qp['equation'])

        test = noevals.noevalify(self._qp['equation'])
        test = transformations.apply_transformations(self._qp['transformation'], test)
        # whilst we can't rely on noevals printing
        if test.is_polynomial():
            test = test.expand()
        # e.g. = -tan(2x + pi/4 + 4)
        lines += r'''$y = {0}$'''.format(
                    sympy.latex(test)
                )

        a, b, c, d = sympy.symbols('a b c d')
        wildcard = self._qp['wildcard_equation'].subs({a: x0, b: x1, c: x2, d: x3})
        match = transformed_equation.match(wildcard)
        match = collections.OrderedDict(sorted(match.items()))

        symbols = collections.OrderedDict([
            (x0, a),
            (x1, b),
            (x2, c),
            (x3, d)
        ])

        # e.g. \therefore a = -1, b = 2, c = pi/4 + 4, d = 0
        answer = ', '.join(['{0} = {1}'.format(symbols[k], sympy.latex(v)) for k, v in match.items()])

        lines += r'$\therefore {0}$'.format(answer)






        return lines.write()
