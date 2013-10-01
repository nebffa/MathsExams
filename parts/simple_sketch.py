import sympy
from sympy.abc import *
from maths.rich_requests import requests
from maths.plot import plot
from maths.utils import transformations
import random
import copy
from maths.latex import latex


class SimpleSketch:
    def __init__(self):

        self.num_lines, self.num_marks = 0, 3

        function_type = random.choice(['absolute_value', 'hyperbola'])

        self._qp = {}
        self._qp['plot_domain'] = self._qp['plot_range'] = sympy.Interval(-6, 6)

        self._qp['expr_domain'] = sympy.Interval(random.randint(-5, -3), random.randint(3, 5))


        if function_type == 'absolute_value':
            self._qp['equation'] = requests.absolute_value(extreme_point=self._qp['expr_domain'])
        elif function_type == 'hyperbola':
            self._qp['equation'] = requests.hyperbola(vertical_asymptote=self._qp['expr_domain'],
                                            horizontal_asymptote=self._qp['plot_range'])

    
    def question_statement(self):
        path = plot.blank_plot(self._qp['plot_domain'], self._qp['plot_range'])

        return r'''Sketch the graph of $f: {0} \rightarrow R, f(x) = {1}$. Label the axes intercepts and endpoints with their coordinates. {2}'''.format(
                    sympy.latex(self._qp['expr_domain']), sympy.latex(self._qp['equation']), plot.latex(path))


    def solution_statement(self):
        path = plot.plot(self._qp['equation'], self._qp['plot_domain'], self._qp['plot_range'],
                            expr_domain=self._qp['expr_domain'])


        return r'''{0}'''.format(plot.latex(path))


class PointTransformation:
    def __init__(self, part):
        self.num_lines, self.num_marks = 4, 1
        self._qp = copy.copy(part._qp)

        y_point = sympy.oo
        while y_point in [-sympy.oo, sympy.oo]:
            x_point = random.choice(range(self._qp['expr_domain'].left, self._qp['expr_domain'].right + 1))
            y_point = self._qp['equation'].subs({x: x_point})
        self._qp['point'] = (x_point, y_point)
        self._qp['transformations'] = transformations.random_transformation(num_transformations=2)

    def question_statement(self):
        return r'''Find the coordinates of the image of the point $({0}, {1})$ {2}.'''.format(
                    sympy.latex(self._qp['point'][0]), 
                    sympy.latex(self._qp['point'][1]), 
                    transformations.print_transformations(self._qp['transformations']) 
                    )

    def solution_statement(self):
        mapping = transformations.show_mapping(self._qp['transformations'])
        mapped_point = transformations.apply_transformations(self._qp['transformations'], self._qp['point'])

        therefore = r'\therefore ({0}, {1}) \rightarrow ({2}, {3})'.format(
                        sympy.latex(self._qp['point'][0]), 
                        sympy.latex(self._qp['point'][1]),
                        sympy.latex(mapped_point[0]), 
                        sympy.latex(mapped_point[1])
                        )

        return r'''${0}$ '''.format(mapping) + latex.latex_newline() + therefore


class EquationTransformation:
    def __init__(self, part):
        self.num_lines, self.num_marks = 8, 2
        self._qp = copy.copy(part._qp)

        self._qp['transformations'] = transformations.random_transformation(num_transformations=2)

    def question_statement(self):
        return r'''Find the equation of the image of the graph of $f$ {0}.'''.format(
                        transformations.print_transformations(self._qp['transformations']) )

    def solution_statement(self):
        mapping = transformations.show_mapping(self._qp['transformations'])
        mapped_equation = transformations.apply_transformations(self._qp['transformations'], self._qp['equation'])

        return r'''${0} {1}$'''.format(mapping, sympy.latex(mapped_equation))
