import sympy
import random
from maths import all_functions, not_named_yet
from maths.symbols import *
from maths.utils import functions
from maths.latex import expressions, latex


class WordedDefiniteIntegral(object):
    def __init__(self):
        # 2008 Q5 [8 lines] [3 marks]

        self._question_params = {}
        self.num_lines, self.num_marks = 8, 3


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
        self._question_params['area'] = sympy.Abs(area)
        self._question_params['big_letter'] = sympy.Symbol('C')

    def question_statement(self):
        sign = 'positive' if self._question_params['domain'].left == 0 else 'negative'

        return r'''The area of the region bounded by the y-axis, the x-axis, the curve $y = {0}$ and the line x = {2}, where {2} is 
                a {3} real constant, is ${1}$. Find {2}.'''.format(sympy.latex(self._question_params['equation']),
                                                                sympy.latex(self._question_params['area']),
                                                                self._question_params['big_letter'],
                                                                sign)

    def solution_statement(self):
        below_x_axis = True if self._question_params['equation'].subs({x: 0}) < 0 else False

        if self._question_params['domain'].left < 0:
            question_domain = (self._question_params['big_letter'], 0)
        else:
            question_domain = (0, self._question_params['big_letter'])

        lines = []
        

        if below_x_axis:
            signed_equation = -1 * self._question_params['equation']


            lines.append( r'Since the curve is below the x-axis, we take the signed area.' )
            lines.append( r'$= -{0} = {1}$'.format( expressions.integral(lb=question_domain[0],
                                            ub=question_domain[1],
                                            expr=self._question_params['equation']),
                                                    expressions.integral(lb=question_domain[0],
                                            ub=question_domain[1],
                                            expr=signed_equation)
                                                ) 
                        )
            lines.append( r'$= {0}$'.format( expressions.integral_intermediate(lb=question_domain[0],
                                            ub=question_domain[1],
                                            expr=signed_equation.integrate())) )
            
        else:
            lines.append( r'${0}$'.format( expressions.integral(lb=question_domain[0],
                                            ub=question_domain[1],
                                            expr=self._question_params['equation']) ))

            lines.append( r'$= {0}$'.format(expressions.integral_intermediate(lb=question_domain[0], ub=question_domain[1],
                                                    expr=self._question_params['equation'].integrate() )) )


        lines.append( r'''$= {0} = {1}$'''.format(expressions.integral_intermediate_eval(lb=question_domain[0], 
                                        ub=question_domain[1],
                                        expr=self._question_params['equation'].integrate()), sympy.latex(self._question_params['area'])) )

        # the value of the big letter is the sum of the ends of the domains (since one of the ends of the domains is 0)
        lines.append( r'''${0} = {1}$.'''.format(self._question_params['big_letter'], 
                    sympy.latex(self._question_params['domain'].left + self._question_params['domain'].right)) )
        
        return latex.latex_newline().join(lines)


    def sanity_check(self):
        assert sympy.integrate(self._question_params['equation'], (x, self._question_params['domain'].left, 
                self._question_params['domain'].right)) == self._question_params['area']

        # make sure we have no x-intercepts in the domain
        solutions = [solution for solution in sympy.solve(self._question_params['equation']) if sympy.ask(sympy.Q.real(solution))]
        assert all([solution not in self._question_params['domain'] for solution in solutions])
