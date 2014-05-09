import sympy
import random
from ..symbols import x
from .. import not_named_yet
from ..latex import solutions
from . import relationships


@relationships.root
class TrigProperties(relationships.QuestionPart):
    """
    Question description
    ====================

    For a given trigonometric function, determine the period as well as one of the range or amplitude.


    Real-life instances
    ===================

    2010 4: [4 lines] [2 marks]
    2011 3a: [5 lines] [2 marks]
    """

    def __init__(self):
        self.num_lines, self.num_marks = 4, 2
        self._qp = {}

        trig_type = random.choice([sympy.sin, sympy.cos, sympy.tan])

        self._qp['amplitude'] = not_named_yet.randint(1, 4)
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

        return r'''State the {range_or_amplitude} and period of the function $f, R \rightarrow R, f(x) = {equation}$'''.format(
            range_or_amplitude=self._qi['range_or_amplitude'],
            equation=sympy.latex(self._qp['equation'])
        )

    def solution_statement(self):
        lines = solutions.Lines()

        lines += r'The {range_or_amplitude} is ${range_or_amplitude_answer}$'.format(
            **self._qi
        )

        lines += r'The period is ${answer}$'.format(
            answer=sympy.latex(self._qp['period'])
        )

        return lines.write()
