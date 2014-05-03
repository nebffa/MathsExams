import sympy
import random
from sympy.abc import *
from .. import all_functions, not_named_yet
from ..latex import solutions
from . import relationships


@relationships.root
class TrigProperties(relationships.QuestionPart):
    def __init__(self):
        # 2010 Q4a [4 lines] [2 marks]
        # 2011 Q3a [5 lines] [2 marks]
        self.num_lines, self.num_marks = 4, 2
        self._qp = {}


        self._qp['amplitude'] = not_named_yet.randint(1, 4)
        trig_type = random.choice([sympy.sin, sympy.cos, sympy.tan])

        self._qp['period'] = random.choice([1, sympy.pi]) * sympy.Rational(random.randint(1, 3), random.randint(1, 4))
        if trig_type == sympy.tan:
            self._qp['period'] *= sympy.Rational(1, 2)

        interior = ((x + random.randint(-3, 3)) * sympy.pi / self._qp['period']).together()
        self._qp['c'] = not_named_yet.randint_no_zero(-3, 3)

        self._qp['equation'] = self._qp['amplitude'] * trig_type(interior, evaluate=False) + self._qp['c']
        self._qp['range'] = sympy.Interval(-self._qp['amplitude'] + self._qp['c'], self._qp['amplitude'] + self._qp['c'])


    def question_statement(self):
        self._qi = {}
        self._qi['range_or_amplitude'] = random.choice(['range', 'amplitude'])
        self._qi['range_or_amplitude_answer'] = self._qp[self._qi['range_or_amplitude']]

        return r'''State the {0} and period of the function $f, R \rightarrow R, f(x) = {1}$'''.format(
                self._qi['range_or_amplitude'],
                sympy.latex(self._qp['equation'])
            )


    def solution_statement(self):
        lines = solutions.Lines()


        lines += r'The {0} is ${1}$'.format(
                self._qi['range_or_amplitude'],
                self._qi['range_or_amplitude_answer']
            )

        lines += r'The period is ${0}$'.format(sympy.latex(self._qp['period']))

        return lines.write()
