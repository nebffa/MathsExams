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
        return r'''Find the coordinates of the image of the point ${0}$ {1}.'''.format(
                    sympy.latex(self._qp['point']), 
                    transformations.print_transformations(self._qp['transformations']) 
                    )

    def solution_statement(self):
        mapping = transformations.show_mapping(self._qp['transformations'])
        mapped_point = transformations.apply_transformations(self._qp['transformations'], self._qp['point'])

        therefore = r'$\therefore {0} \rightarrow {1}$'.format(
                        sympy.latex(self._qp['point']), 
                        sympy.latex(mapped_point), 
                        )

        return r'''${0}$'''.format(mapping) + latex.latex_newline() + therefore


class EquationTransformation:
    def __init__(self, part):
        self.num_lines, self.num_marks = 8, 2
        self._qp = copy.copy(part._qp)

        self._qp['transformations'] = transformations.random_transformation(num_transformations=2)

    def question_statement(self):
        return r'''Find the equation of the image of the graph of $f$ {0}.'''.format(
                        transformations.print_transformations(self._qp['transformations']) )

    def solution_statement(self):
        mapping_chain = transformations.show_mapping(self._qp['transformations'])
        mapped_equation = transformations.apply_transformations(self._qp['transformations'], self._qp['equation'])
        mapping = transformations.overall_transformation(self._qp['transformations'])
        reversed_mapping = transformations.reverse_mapping(mapping)

        
        line_1 = r'${0}$'.format(mapping_chain)

        x_, y_ = sympy.symbols("x' y'")
        new_coords = (x_, y_)
        line_2 = r"Let our new ${0}$ coordinates be ${1}$.".format(sympy.latex((x, y)), sympy.latex((x_, y_)))
        line_3 = r'Hence, ${0} \rightarrow {1}$'.format(sympy.latex(mapping), sympy.latex(new_coords))


        reversed_mapping = tuple(i.subs({x: x_, y: y_}) for i in reversed_mapping)        
        line_4 = r'and ${0} \rightarrow {1}$'.format(sympy.latex((x, y)), sympy.latex(reversed_mapping))

        line_5 = 'Now we apply the mapping to the equation:'
        line_6 = r'${0} = {1}$'.format(sympy.latex(reversed_mapping[1]), sympy.latex(self._qp['equation'].subs({x: reversed_mapping[0]})) )

        line_7 = r'$y = {0}$'.format(sympy.latex(mapped_equation.apart()))

        lines = line_1, line_2, line_3, line_4, line_5, line_6, line_7
        return latex.latex_newline().join(lines)
