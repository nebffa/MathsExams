import sympy
import random
from sympy.abc import *
from maths import not_named_yet
from maths.latex import part_lines
from maths.utils import noevals
import copy
import decimal


class LinearApproximation:
    def __init__(self):
        self.num_lines, self.num_marks = 7, 4

        self.equation = random.choice([x**sympy.Rational(1, random.randint(2, 3)), x**random.randint(2, 3)])

        self._qp = {}

        
        if isinstance(self.equation, sympy.Pow):
            base, exponent = self.equation.as_base_exp()

            if exponent > 1:
                self._qp['location'] = random.randint(2, 3, 4)
            else:
                self._qp['location'] = random.randint(2, 3, 4) ** exponent.q

        self._qp['delta'] = not_named_yet.randint(-1, 1, exclude=[0]) * random.randint(5, 9) * decimal.Decimal('0.01')


    def question_statement(self):
        noeval_equation = self.equation.replace(sympy.Pow, noevals.noevalPow)

        return r'''Use the relationship $f(x + h) \approx f(x) + h f'(x)$ for a small positive value of h, 
                    to find an approximate value for {0}.'''.format( 
                        noeval_equation.subs( {x: self._qp['location'] + self._qp['delta']}) )




    def solution_statement(self):
        lines = part_lines.Lines()

        deriv = self.equation.diff()

        y0 = self.equation.subs({x: self._qp['location']})
        y0_deriv = deriv.subs({x: self._qp['location']})

        answer = y0 + self._qp['delta'] * y0_deriv


        lines += r'''${0}, {1}$'''.format(self.equation, deriv)
        lines += r'''$y({0}) = {1}$'''.format(self._qp['location'], y0)
        lines += r'''$y'({0}) = {1}$'''.format(self._qp['location'], y0_deriv)
        lines += r'''$\therefore y({0}) \approx {1}$'''.format(self._qp['location'] + self._qp['delta'], answer)

        return lines.write()



class LinearApproximationExplain:
    def __init__(self):
        self.num_lines, self.num_marks = -1, -1

        self._qp = copy.copy(part._qp)



    def question_statement(self):
        pass




    def solution_statement(self):
        pass
