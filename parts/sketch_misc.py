import sympy
import random
from sympy.abc import *
from maths.plot import plot
from maths import all_functions, not_named_yet
from maths.utils import functions
import copy


class SketchDoubleInverse:
    def __init__(self, part):
        # 2008 Q10b [0 lines] [1 mark] [Blank plot]
        self.num_lines, self.num_marks = 0, 1

        self._qp = copy.copy(part._qp)

        if self._qp['domain'].left != -sympy.oo and self._qp['domain'].right != sympy.oo:
            raise ValueError('This questions needs an open ended domain.')

        self._qp['MAX_PLOT_RANGE'] = 10


    def question_statement(self):
        limits = sympy.Interval(-self._qp['MAX_PLOT_RANGE'], self._qp['MAX_PLOT_RANGE'])
        path = plot.blank_plot(limits, limits)

        return r'''On the axes provided, sketch the graph of $y = f(f'(x))$ for its maximal domain. {0}'''.format(plot.latex(path))


    def solution_statement(self):

        inverse = all_functions.inverse(self._qp['equation'])

        maximal_domain_original = functions.maximal_domain(self._qp['equation'])
        maximal_domain_inverse = functions.maximal_domain(inverse)

        maximal_domain = maximal_domain_original & maximal_domain_inverse

        expr_domain = maximal_domain & sympy.Interval(-self._qp['MAX_PLOT_RANGE'], self._qp['MAX_PLOT_RANGE'])

        # an inverse of an inverse is always just "y = x"
        path = plot.plot(x, 
            plot_domain=sympy.Interval(-self._qp['MAX_PLOT_RANGE'], self._qp['MAX_PLOT_RANGE']), 
            plot_range=sympy.Interval(-self._qp['MAX_PLOT_RANGE'], self._qp['MAX_PLOT_RANGE']), 
            expr_domain=expr_domain
        )
        
        return r'''{0}'''.format(plot.latex(path))

