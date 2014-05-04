import sympy
import random
from ..latex import solutions, expressions
from ..utils import sympy_shortcuts
from . import relationships


@relationships.root
class RelatedRates(relationships.QuestionPart):
    """
    Question description
    ====================

    Calculate a rate of change given information about two other related rates of change.


    Real-life instances
    ===================

    2009 6: [7 lines] [3 marks]
    """

    def __init__(self):
        self.num_lines, self.num_marks = 7, 3
        self._qp = {}

        self._qp['shape'] = random.choice(['triangle', 'circle', 'sphere'])
        self._qp['shape'] = 'triangle'

        VALUE_CHOICES = [5, 6, 7, 8, 9, 10, 20, 30, 40, 50]
        ANGLE_CHOICES = [sympy.pi / 6, sympy.pi / 4, sympy.pi / 3]
        if self._qp['shape'] == 'triangle':
            self._qp['dependent_variable_value'] = random.choice(ANGLE_CHOICES)
        else:
            self._qp['dependent_variable_value'] = random.choice(VALUE_CHOICES)

        RATE_OF_CHANGE_CHOICES = [10 * i for i in range(1, 11)]
        self._qp['constant_rate_of_change'] = random.choice(RATE_OF_CHANGE_CHOICES)

        TRIANGLE_CHOICES = [100 * i for i in range(1, 11)]
        self._qp['triangle_distance'] = random.choice(TRIANGLE_CHOICES)

        V, A, r, theta, h, t = sympy.symbols(r'V A r \theta h t')
        shape_information = {
            'sphere':
            {
                'variable_change_variable': r,
                'constant_change_variable': V,
                'time_variable': t,
                'implicit_shape_relationship': 4 * sympy.pi * r ** 3 / 3
            },

            'circle':
            {
                'variable_change_variable': r,
                'constant_change_variable': A,
                'time_variable': t,
                'implicit_shape_relationship': sympy.pi * r ** 2
            },

            'triangle':
            {
                'variable_change_variable': theta,
                'constant_change_variable': h,
                'time_variable': t,
                'implicit_shape_relationship': self._qp['triangle_distance'] * sympy.tan(theta)
            }
        }[self._qp['shape']]

        self._qp.update(**shape_information)

    def question_statement(self):
        self._qi = {
            'sphere':
            {
                'constant_change_variable_units': r'\text{Mkm}^{3}',
                'variable_change_variable_units': r'\text{Mkm}',
                'time_unit': 'year',
                'variable_change_variable_name': 'radius',
                'what': 'star',
            },

            'circle':
            {
                'constant_change_variable_units': r'\text{mm}^{2}',
                'variable_change_variable_units': r'\text{mm}',
                'time_unit': 'minute',
                'variable_change_variable_name': 'radius',
                'what': 'puddle',
            },

            'triangle':
            {
                'constant_change_variable_units': r'\text{km}',
                'variable_change_variable_units': r'\text{radians}',
                'time_unit': 'minute',
                'variable_change_variable_name': 'angle',
                'what': "observer's view between the launch position and the rocket's current location",
                'already_latexed_value': sympy.latex(self._qp['dependent_variable_value'])
            }
        }[self._qp['shape']]

        question_setup = {
            'sphere': r'''A spherical star is enlarging in size at a constant rate. The gasses are swelling in size at the rate of
                        ${constant_rate_of_change} {constant_change_variable_units}$ per {time_unit} causing the star to expand evenly.
                        ''',

            'circle': r'''Oil is leaking at a constant rate to form a circular puddle on the floor. The oil is being added to
                        the puddle such that puddle is increasing evenly in size at the rate of ${constant_rate_of_change} {constant_change_variable_units}$
                        per {time_unit}.
                        ''',

            'triangle': r'''A rocket is flying vertically towards outer-space at a constant rate, forming a right-angled with an observer standing
                        ${triangle_distance} {constant_change_variable_units}$ away from the position where the rocket launched. The rocket's altitude
                        is is increasing at a rate of ${constant_rate_of_change} {constant_change_variable_units}$ per {time_unit}.
                        ''',
        }[self._qp['shape']]

        question_ask = r'''Find the rate of change of the {variable_change_variable_name} of the {what} when the {variable_change_variable_name} is
        ${already_latexed_value}$ {variable_change_variable_units}. Give an exact answer, with units of {variable_change_variable_units} per
        {time_unit}.
        '''

        question = question_setup + question_ask

        return question.format(**self.combined_question_dict())

    def solution_statement(self):
        lines = solutions.Lines()

        # e.g. dV/dt = 10 mm^3
        lines += r'${leibniz_derivative} = {value}$'.format(
            leibniz_derivative=expressions.derivative(self._qp['constant_change_variable'], self._qp['time_variable']),
            value=self._qp['constant_rate_of_change']
        )

        # e.g. dV/dr = 4 * pi * r
        lines += r'${leibniz_derivative} = {value}$'.format(
            leibniz_derivative=expressions.derivative(self._qp['constant_change_variable'], self._qp['variable_change_variable']),
            value=sympy.latex(self._qp['implicit_shape_relationship'].diff())
        )

        # e.g. dr/dV = 1 / (dV/dr) = 1 / (4 * pi * r)
        lines += r'${leibniz_derivative} = \frac{{1}}{{{inverted_leibniz_derivative}}} = \frac{{1}}{{{value}}}$'.format(
            leibniz_derivative=expressions.derivative(self._qp['variable_change_variable'], self._qp['constant_change_variable']),
            inverted_leibniz_derivative=expressions.derivative(self._qp['constant_change_variable'], self._qp['variable_change_variable']),
            value=sympy.latex(self._qp['implicit_shape_relationship'].diff())
        )

        # e.g. dr/dt = dr/dV * dV/dt
        lines += r'${leibniz_derivative} = {first_related_leibniz} \times {second_related_leibniz}$'.format(
            leibniz_derivative=expressions.derivative(self._qp['variable_change_variable'], self._qp['time_variable']),
            first_related_leibniz=expressions.derivative(self._qp['variable_change_variable'], self._qp['constant_change_variable']),
            second_related_leibniz=expressions.derivative(self._qp['constant_change_variable'], self._qp['time_variable'])
        )

        final_rate_of_change = self._qp['constant_rate_of_change'] / self._qp['implicit_shape_relationship'].diff()
        # e.g. \therefore dr/dt = 5 / (2 * pi * r)
        lines += r'$\therefore {leibniz_derivative} = {value}$'.format(
            leibniz_derivative=expressions.derivative(self._qp['variable_change_variable'], self._qp['time_variable']),
            value=sympy.latex(final_rate_of_change)
        )

        # e.g. dr/dt(30) = 1 / (12 * pi)
        lines += r'${leibniz_derivative}({dependent_variable_value}) = {answer} \text{{{units}}}$'.format(
            leibniz_derivative=expressions.derivative(self._qp['variable_change_variable'], self._qp['time_variable']),
            dependent_variable_value=sympy.latex(self._qp['dependent_variable_value']),
            answer=sympy.latex(sympy_shortcuts.easy_sub(final_rate_of_change, self._qp['dependent_variable_value'])),
            units=r'{0}/{1}'.format(self._qi['variable_change_variable_units'], self._qi['time_unit'])
        )

        return lines.write()
