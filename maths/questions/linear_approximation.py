import sympy
import random
from sympy.abc import *
from .. import not_named_yet
from ..latex import solution_lines
from ..utils import noevals, functions
import copy
import decimal
from . import relationships


@relationships.is_child_of(relationships.DummyPart)
class LinearApproximation:
    def __init__(self):
        self.num_lines, self.num_marks = 7, 4

        self._qp = {}
        self._qi = {}

        self._qp['equation'] = random.choice([x**sympy.Rational(1, random.randint(2, 3)), x**random.randint(2, 3)])
        self._qi['noeval_equation'] = self._qp['equation'].replace(sympy.Pow, noevals.noevalPow)

        
        if isinstance(self._qp['equation'], sympy.Pow):
            base, exponent = self._qp['equation'].as_base_exp()

            if exponent > 1:
                self._qp['location'] = random.randint(2, 4)
            else:
                self._qp['location'] = 2 ** exponent.q

        self._qp['delta'] = not_named_yet.randint(-1, 1, exclude=[0]) * random.randint(5, 9) * decimal.Decimal('0.01')
        self._qp['new_location'] = self._qp['location'] + self._qp['delta']


    def question_statement(self):

        return r'''Use the relationship $f(x + h) \approx f(x) + h f'(x)$ for a small positive value of h, 
                    to find an approximate value for ${0}$.'''.format( 
                        sympy.latex(self._qi['noeval_equation'].subs( {x: self._qp['new_location']}) ))




    def solution_statement(self):
        lines = solution_lines.Lines()

        deriv = self._qp['equation'].diff()

        y0 = self._qp['equation'].subs({x: self._qp['location']})
        y0_deriv = deriv.subs({x: self._qp['location']})

        intermediate = noevals.noevalAdd(y0, noevals.noevalMul(self._qp['delta'], y0_deriv))
        answer = y0 + self._qp['delta'] * y0_deriv


        lines += r'''$y = {0}, y' = {1}$'''.format(sympy.latex(self._qp['equation']), sympy.latex(deriv))
        lines += r'''$y({0}) = {1}$'''.format(self._qp['location'], y0)
        lines += r'''$y'({0}) = {1}$'''.format(self._qp['location'], sympy.latex(y0_deriv))
        lines += r'''$\therefore y({0}) \approx {1} = {2}$'''.format(self._qp['new_location'], noevals.latex(intermediate), sympy.latex(answer))

        return lines.write()


@relationships.is_child_of(relationships.DummyPart)
class LinearApproximationExplain:
    def __init__(self, part):
        self.num_lines, self.num_marks = 4, 1

        self._qp = copy.copy(part._qp)
        self._qi = copy.copy(part._qi)

        self._qp['is_convex'] = functions.is_convex(self._qp['equation'], self._qp['location'])



    def question_statement(self):
        direction = 'less than' if self._qp['is_convex'] else 'greater than'



        return r'''Explain why this approximate value is {0} than the exact value for ${1}$.'''.format(direction,
                        sympy.latex(self._qi['noeval_equation'].subs( {x: self._qp['new_location']})))




    def solution_statement(self):
        lines = solution_lines.Lines()

        second_deriv = self._qp['equation'].diff().diff()
        second_deriv_latex = r'\frac{{d^{{2}}y}}{{dx^{{2}}}}({0})'.format(self._qp['location'])
        second_deriv_eval = second_deriv.subs({x: self._qp['location']})

        lines += r'''The function is {0} at $x = {1}$ since the second derivative ${2} = {3}$ is {4} than $0$.'''.format(
                        'convex' if self._qp['is_convex'] else 'concave', self._qp['location'],
                        second_deriv_latex, sympy.latex(second_deriv_eval), 'greater than' if second_deriv_eval > 0 else 'less than'
                        )

        lines += r'''Therefore, the gradient of ${0}$ {1} as $x$ moves from ${2}$ to ${3}$ and as a result, linear approximation 
                        {4}estimates the true value of ${5}$'''.format(
                        sympy.latex(self._qp['equation']), 'increases' if second_deriv_eval > 0 else 'decreases',
                        self._qp['location'], self._qp['new_location'], 'under' if self._qp['is_convex'] else 'over', 
                        sympy.latex(self._qi['noeval_equation'].subs({x: self._qp['new_location']}))
            )



        return lines.write()
