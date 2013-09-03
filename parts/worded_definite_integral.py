import sympy
import random
from sympy.abc import *
from maths import all_functions, not_named_yet, simplify
from maths.utils import functions
from maths.latex import expressions, latex


class WordedDefiniteIntegral(object):
    def __init__(self):
        # 2008 Q5 [8 lines] [3 marks]

        self._question_params = {}


        while True:
            function_type = random.choice(['log'])
            if function_type == 'log':
                equation = all_functions.request_exp(difficulty=3).equation

            bound = sympy.Rational(not_named_yet.randint(-5, 5, exclude=[0]), not_named_yet.randint(-5, 5, exclude=[0]))

            if bound < 0:
                domain = sympy.Interval(bound, 0, False, False)
            else:
                domain = sympy.Interval(0, bound, False, False)

            y_intercept = equation.subs({x: 0})
            if bound < 0 and y_intercept < 0 and functions.is_monotone_decreasing(equation, domain):
                continue
            elif bound < 0 and y_intercept > 0 and functions.is_monotone_increasing(equation, domain):
                continue
            elif bound > 0 and y_intercept < 0 and functions.is_monotone_increasing(equation, domain):
                continue
            elif bound > 0 and y_intercept > 0 and functions.is_monotone_decreasing(equation, domain):
                continue


            area = sympy.integrate(equation, (x, domain.left, domain.right))

            break

        self._question_params['equation'] = equation
        self._question_params['domain'] = domain
        self._question_params['area'] = area
        self._question_params['big_letter'] = sympy.Symbol('C')

    def question_statement(self):
        sign = 'positive' if self._question_params['domain'].left == 0 else 'negative'

        return r'''The area of the region bounded by the y-axis, the x-axis, the curve $y = {0}$ and the line x = {2}, where {2} is 
                a {3} real constant, is {1}. Find {2}.'''.format(self._question_params['equation'],
                                                                self._question_params['big_letter'],
                                                                self._question_params['area'],
                                                                sign)

    def solution_statement(self):
        integral = sympy.integrate(self._question_params['equation'])

        if self._question_params['domain'].left < 0:
            line_1 = '$' + expressions.integral(lb=self._question_params['big_letter'],
                                            ub=self._question_params['domain'].right,
                                            expr=self._question_params['equation']) + ' = {0}$'.format(self._question_params['area'])

            line_2 = '$' + expressions.integral_intermediate(lb=self._question_params['big_letter'],
                                            ub=self._question_params['domain'].right,
                                            expr=self._question_params['equation']) + ' = {0}$'.format(self._question_params['area'])


            line_3 = r'''$= {0} = {1}$'''.format(integral.subs({x: self._question_params['domain'].right}) -
                                                        integral.subs({x: self._question_params['big_letter']}), self._question_params['area'])

            line_4 = r'''${0} = {1}$.'''.format(self._question_params['big_letter'], self._question_params['domain'].left)
        else:
            line_1 = '$' + expressions.integral(lb=self._question_params['domain'].left,
                                            ub=self._question_params['big_letter'],
                                            expr=self._question_params['equation']) + ' = {0}$'.format(self._question_params['area'])

            line_2 = '$' + expressions.integral_intermediate(lb=self._question_params['domain'].left,
                                            ub=self._question_params['big_letter'],
                                            expr=self._question_params['equation']) + ' = {0}$'.format(self._question_params['area'])

            line_3 = r'''$= {0} = {1}$'''.format(integral.subs({x: self._question_params['big_letter']}) -
                                                        integral.subs({x: self._question_params['domain'].left}), self._question_params['area'])

            line_4 = r'''${0} = {1}$.'''.format(self._question_params['big_letter'], self._question_params['domain'].right)

            

        return latex.latex_newline().join([line_1, line_2, line_3, line_4])


    def sanity_check(self):
        assert sympy.integrate(self._question_params['equation'], (x, self._question_params['domain'].left, 
                self._question_params['domain'].right)) == self._question_params['area']

        # make sure we have no x-intercepts in the domain
        solutions = [solution for solution in sympy.solve(self._question_params['equation']) if sympy.ask(sympy.Q.real(solution))]
        assert all([solution not in self._question_params['domain'] for solution in solutions])
