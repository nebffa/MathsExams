import sympy
from sympy.abc import *
from maths.rich_requests import requests
from maths.plot import plot
from maths.utils import transformations
import copy


class SimpleSketch:
    def __init__(self):

        self.num_lines, self.num_marks = 0, 3

        function_type = random.choice(['absolute_value', 'hyperbola'])

        self._qp = {}
        self._qp['plot_domain'] = self._qp['plot_range'] = sympy.Interval(-6, 6)


        if function_type == 'absolute_value':
            self._qp['equation'] = requests.absolute_value(extreme_point=self._qp['domain'])
        elif function_type == 'hyperbola':
            self._qp['equation'] = requests.hyperbola(vertical_asymptote=self._qp['domain'],
                                            horizontal_asymptote=self._qp['range'])

    
    def question_statement(self):
        path = plot.blank_plot(self._qp['plot_domain'], self._qp['plot_range'])

        return r'''Sketch the graph of $f: {0} \rightarrow R, f(x) = {1}$. Label the axes intercepts and endpoints with their coordinates. {2}'''.format(
                    self._qp['expr_domain'], self._qp['equation'], plot.latex(path))


    def solution_statement(self):
        path = plot.plot(self._qp['equation'], self._qp['domain'],
                            expr_domain=self._qp['expr_domain'])


        return r'''{0}'''.format(plot.latex(path))


class placeholder_name:
    def __init__(self, part):
        self.num_lines, self.num_marks = 4, 1
        self._qp = copy.copy(part._qp)

        x_point = random.choice(range(self._qp['expr_domain'].left, self._qp['expr_domain'].right + 1))
        y_point = self._qp['equation'].subs({x: x_point})
        self._qp['point'] = (x_point, y_point)
        self._qp['transformation'] = transformations.random_transformations(num_transformations=2)

    def question_statement(self):
        return r'''Find the coordinates of the image of the point ({0}, {1}), under {transformation}.'''.format(
                    *self._qp['point'], transformation=transformations.print_transformations(self._qp['transformation']))

    def solution_statement(self):
        pass
