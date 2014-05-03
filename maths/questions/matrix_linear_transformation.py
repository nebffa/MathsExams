import sympy
import random
from .. import all_functions
from ..symbols import x, y, x0, x1, x2, x3, a, b, c, d, coeff0, coeff1, coeff2, coeff3
from ..latex import solutions
from ..utils import transformations, noevals
import collections
from . import relationships
import itertools


# issues with match:
# sin(pi/2 - x) matching won't work since it automatically converts to cos(x)
# x**2 - 4 will match like so: x0=1, x1=4/x, x2=0


@relationships.root
class MatrixLinearTransformation(relationships.QuestionPart):
    """
    Question description
    ====================

    Find the image of a curve after it has undergone a linear transformation.


    Real-life instances
    ===================

    2010 6: [11 lines] [3 marks]
    """

    @staticmethod
    def match(expr):
        """Match the expression in a noeval-friendly way.

        There are a host of reasons for doing it this way. For instance, if we have

        NOTE: everything here is 'noevaled' via noevals.noevalify
        y = log(-x - 1)
        y.match(x0*log(x1*x + x2) + x3) will match properly

        but y = log(-x - 1) + 1
        y.match(x0*log(x1*x + x2) + x3) does not match,
        because for SOME reason, having the added 1 forces y.match to coerce
        log(-x - 1) into log(-(x + 1)), which does not get matched by log(x1*x + x2)

        This is one of several issues with trying to do a simple match, so we have to implement
        a more indepth matching process here.
        """

        expr_type = all_functions.detect_expr_type(expr)
        if not isinstance(expr_type, sympy.Poly):
            matcher = noevals.noevalify(coeff0 * expr_type(x0) + coeff3)

            # we need to make sure that the expression is actually noevalified,
            # removing this causes issues with certain cases, like the one in this function's docstring
            noevalified_transformed_equation = noevals.noevalify(expr)
            match = noevalified_transformed_equation.match(matcher)

            noevaled_interior = noevals.noevalify(match[x0])
            interior_matcher = noevals.noevalify(coeff1 * x + coeff2)
            interior_match = noevaled_interior.match(interior_matcher)

            overall_match = dict(itertools.chain(match.items(), interior_match.items()))
            overall_match.pop(x0)  # we don't want the "interior" wildcard to be included in the output to students
        else:
            matcher = coeff0 * x ** 2 + coeff1 * x + coeff2
            overall_match = expr.match(matcher)

        return MatrixLinearTransformation.order_match(overall_match)

    @staticmethod
    def order_match(match):
        """Return a match in the order {a: ..., b: ..., etc.} rather than {c: ..., a: ..., etc.}
        """

        key_value_pairs = []
        for wild, unknown in [(coeff0, a), (coeff1, b), (coeff2, c), (coeff3, d)]:
            if wild in match:
                key_value_pairs.append((unknown, match[wild]))

        return collections.OrderedDict(key_value_pairs)

    def __init__(self):
        self.num_lines, self.num_marks = 11, 3
        self._qp = {}

        self._qp['transformation'] = transformations.random_transformation(num_transformations=2)
        self._qp['pre_to_post_transformation'] = transformations.overall_transformation(self._qp['transformation'])

        self._qp['x_dilation_and_reflection'] = self._qp['pre_to_post_transformation'][0].coeff(x)
        self._qp['y_dilation_and_reflection'] = self._qp['pre_to_post_transformation'][1].coeff(y)

        self._qp['x_translation'] = self._qp['pre_to_post_transformation'][0].as_coeff_Add()[0]
        self._qp['y_translation'] = self._qp['pre_to_post_transformation'][1].as_coeff_Add()[0]

        self._qp['equation'] = all_functions.random_function(exclude=['linear']).equation

        # wanted to use wilds, but sympy auto-rearranges any symbols to precede a wild.
        # e.g. y = a*sin(b*x + c) + d    when printed becomes    y = a*sin(x*b + c) + d which is unconventional
        # so we use symbols here for writing the equation, and we will use wilds in the solution for finding the answer
        sympy_types = [sympy.cos, sympy.sin, sympy.tan, sympy.cot, sympy.sec, sympy.csc, sympy.log, sympy.exp]

        wildcards = dict((sympy_type, a * sympy_type(b * x + c) + d) for sympy_type in sympy_types)
        wildcards[sympy.Poly(x ** 2)] = a * x ** 2 + b * x + c  # we use a special case for quadratics because they have a different form from the rest

        expr_type = all_functions.detect_expr_type(self._qp['equation'])
        self._qp['wildcard_equation'] = wildcards[expr_type]

    def question_statement(self):
        symbols_matrix = sympy.Matrix([x, y])
        dilation_and_reflection_matrix = sympy.Matrix([[self._qp['x_dilation_and_reflection'], 0],
                                                       [0, self._qp['y_dilation_and_reflection']]])
        translation_matrix = sympy.Matrix([self._qp['x_translation'], self._qp['y_translation']])
        mapping = r'''T({symbols_matrix}) = {dilation_and_reflection_matrix}{symbols_matrix} + {translation_matrix}'''.format(
            symbols_matrix=sympy.latex(symbols_matrix),
            dilation_and_reflection_matrix=sympy.latex(dilation_and_reflection_matrix),
            translation_matrix=sympy.latex(translation_matrix)
        )

        # the symbols can get pulled out of order when looking at expr.free_symbols. As of 10/12/2013 we can use
        # the builtin sorted to sort them in alphabetical order
        wilds = sorted([i for i in self._qp['wildcard_equation'].free_symbols if i != x])
        return r'''The transformation $T: R^{{2}} \rightarrow R^{{2}}$ is defined by \[{mapping}\]
            The image of the curve $y = {equation}$ under the transformation $T$ has equation y = ${wildcard_equation}$.
            Find the values of ${wilds}$.'''.format(
            mapping=mapping,
            equation=sympy.latex(self._qp['equation']),
            wildcard_equation=sympy.latex(self._qp['wildcard_equation']),
            wilds=', '.join([sympy.latex(i) for i in wilds])
        )

    def solution_statement(self):
        lines = solutions.Lines()

        # e.g. T([x; y]) = [x - 2; y] = [x'; y']
        x_, y_ = sympy.symbols("x' y'")
        lines += r'''$T({pre_transformation_symbols_matrix}) = {overall_transformation} = {post_transformation_symbols_matrix}$'''.format(
            pre_transformation_symbols_matrix=sympy.latex(sympy.Matrix([x, y])),
            overall_transformation=sympy.latex(sympy.Matrix(self._qp['pre_to_post_transformation'])),
            post_transformation_symbols_matrix=sympy.latex(sympy.Matrix([x_, y_]))
        )

        pre_to_post_transformation = transformations.overall_transformation(self._qp['transformation'])
        post_to_pre_transformation = transformations.reverse_mapping(pre_to_post_transformation)
        lines += r'${pre_transformation_symbols_matrix} = {post_to_pre_transformation}$'.format(
            pre_transformation_symbols_matrix=sympy.latex(sympy.Matrix([x, y])),
            post_to_pre_transformation=sympy.latex(post_to_pre_transformation.subs({x: x_, y: y_}))
        )

        noevaled = noevals.noevalify(self._qp['equation'])
        noevaled = noevaled.subs({x: post_to_pre_transformation[0]})
        # e.g. \therefore y = tan(-x + 3*pi/4) transforms to y = -tan(x/2 - 2 + pi/4)
        lines += r'$\therefore y = {equation}$ transforms to ${post_transformation_y} = {post_transformation_equation}$'.format(
            equation=sympy.latex(self._qp['equation']),
            post_transformation_y=sympy.latex(post_to_pre_transformation[1].subs({y: y_})),
            post_transformation_equation=sympy.latex(noevaled.subs({x: x_}))
        )

        noevalified_equation = noevals.noevalify(self._qp['equation'])
        noevalified_transformed_equation = transformations.apply_transformations(self._qp['transformation'], noevalified_equation)
        # whilst we can't rely on noevals printing
        if noevalified_transformed_equation.is_polynomial():
            noevalified_transformed_equation = noevalified_transformed_equation.expand()
        # e.g. = -tan(2x + pi/4 + 4)
        lines += r'The transformed equation is $y = {noevalified_transformed_equation}$'.format(
            noevalified_transformed_equation=sympy.latex(noevalified_transformed_equation)
        )

        # e.g. \therefore a = -1, b = 2, c = pi/4 + 4, d = 0
        match = MatrixLinearTransformation.match(noevalified_transformed_equation)
        answer = ', '.join(['{wildcard} = {wildcard_value}'.format(
            wildcard=k,
            wildcard_value=sympy.latex(v))
            for k, v in match.items()]
        )

        lines += r'$\therefore {answer}$'.format(
            answer=answer
        )

        return lines.write()
