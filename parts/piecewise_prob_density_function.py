import sympy
import random
from maths import domains
from maths.symbols import *
from maths.latex import expressions, latex, solution_lines
from maths.utils import sensible_values
import copy
import math


class PiecewiseProbDensityFunctionUnknown(object):
    def __init__(self):

        # 2008 Q4 [7 lines] [2 marks]
        # 2010 Q7a [12 lines] [3 marks]

        self.num_marks = 3
        self.num_lines = 12

        self._qp = {}
        self.function_type = random.choice(['sin', 'cos', 'linear', 'quadratic'])

        if self.function_type == 'sin':
            while True:
                self._qp['domain'] = domains.integer_domain(low=0, high=2, minimum_distance=1)
                m = random.choice([sympy.pi/2, sympy.pi])
                self._qp['equation'] = k * sympy.sin(m*x)

                area = self._qp['equation'].integrate((x, self._qp['domain'].left, self._qp['domain'].right))
                try:
                    self._qp['k'] = sympy.solve(area - 1)[0]
                except:
                    self._qp['k'] = None

                if self._qp['k'] is not None:
                    break

        elif self.function_type == 'cos':
            while True:
                self._qp['domain'] = domains.integer_domain(low=0, high=2, minimum_distance=1)
                m = random.choice([sympy.pi/2, sympy.pi])
                self._qp['equation'] = k * sympy.cos(m*x)

                area = self._qp['equation'].integrate((x, self._qp['domain'].left, self._qp['domain'].right))
                try:
                    self._qp['k'] = sympy.solve(area - 1)[0]
                except:
                    self._qp['k'] = None

                if self._qp['k'] is not None:
                    break

        elif self.function_type == 'linear':
            self._qp['domain'] = domains.integer_domain()
            m = random.randint(1, 2)
            a = random.randint(7, 12)
            self._qp['equation'] = ((m*x + k) / a).together()

            area = self._qp['equation'].integrate((x, self._qp['domain'].left, self._qp['domain'].right))
            self._qp['k'] = sympy.solve(area - 1)[0]

        elif self.function_type == 'quadratic':
            self._qp['domain'] = domains.integer_domain()
            self._qp['equation'] = k * (x - self._qp['domain'].left) * (x - self._qp['domain'].right)

            area = self._qp['equation'].integrate((x, self._qp['domain'].left, self._qp['domain'].right))
            self._qp['k'] = sympy.solve(area - 1)[0]


    def question_statement(self):
        piecewise = sympy.Piecewise((self._qp['equation'], sympy.And(self._qp['domain'].left < x, x < self._qp['domain'].right)), (0, True))

        lines = solution_lines.Lines()

        lines += r'The function $f(x) = {0}$'.format( expressions.piecewise(piecewise) )
        lines += r'is a probability density function for the continuous random variable $X$. Show that $k = {0}$.'.format(sympy.latex(self._qp['k']))
        
        return lines.write()

    def solution_statement(self):
        lines = solution_lines.Lines()

        lines += r'${0} = 1$'.format( expressions.integral(lb=self._qp['domain'].left, ub=self._qp['domain'].right, expr=self._qp['equation']) )
        lines += r'${0} = {1} = {2} = 1$'.format(
                                    expressions.integral_intermediate(lb=self._qp['domain'].left, ub=self._qp['domain'].right, 
                                            expr=self._qp['equation']),
                                    expressions.integral_intermediate_eval(lb=self._qp['domain'].left, ub=self._qp['domain'].right, 
                                            expr=self._qp['equation']),
                                    sympy.latex(self._qp['equation'].integrate((x, self._qp['domain'].left, self._qp['domain'].right)))
                                    )
        lines += r'$\therefore k = {0}$'.format( sympy.latex(self._qp['k']) )

        return lines.write()

    def sanity_check(self):
        true_equation = self._qp['equation'].subs({k: self._qp['k']})

        if true_equation.integrate((x, self._qp['domain'].left, self._qp['domain'].right)) != 1:
            raise RuntimeError(r'equation: {0}, domain: {1}, does not integrate to 1'.format(self._qp['equation'], self._qp['domain']))


class PiecewiseProbDensityFunctionKnown(PiecewiseProbDensityFunctionUnknown):
    def __init__(self):
        super(PiecewiseProbDensityFunctionKnown, self).__init__()

        self.num_lines, self.num_marks = 0, 0

        self._qp['equation'] = self._qp['equation'].subs({k: self._qp['k']})


    def question_statement(self):


        piecewise = sympy.Piecewise((self._qp['equation'], sympy.And(self._qp['domain'].left <= x, x <= self._qp['domain'].right)), (0, True))

        lines = solution_lines.Lines()

        lines += r'The function $f(x) = {0}$'.format( expressions.piecewise(piecewise) )
        lines += r'is a probability density function for the continuous random variable $X$.'
        return lines.write()



    def solution_statement(self):
        return ''


# can be used for known and unknown
class SimpleInterval:
    def __init__(self, part):
        # 2011 Q5a [5 lines] [2 marks]
        self.num_lines, self.num_marks = 5, 2

        domain = part._qp['domain']

        choices = [domain.left + sympy.Rational(i, 4) * domain.measure for i in [1, 2, 3]]


        self._qp = copy.copy(part._qp)
        self._qp['bound'] = random.choice(choices)
        self._qp['direction'] = random.choice(['left', 'right'])

        if self._qp['direction'] == 'left':
            self._qp['domain'] = sympy.Interval(self._qp['domain'].left, self._qp['bound'])
        else:
            self._qp['domain'] = sympy.Interval(self._qp['bound'], self._qp['domain'].right)



    def question_statement(self):
        return r'''Find Pr(X {0} {1}).'''.format('\le' if self._qp['direction'] == 'left' else '\ge', self._qp['bound'])


    def solution_statement(self):
        lines = solution_lines.Lines()

        answer = self._qp['equation'].integrate((x, self._qp['domain'].left, self._qp['domain'].right))

        lines += '$= {0}$'.format(expressions.integral(expr=self._qp['equation'], lb=self._qp['domain'].left, ub=self._qp['domain'].right))

        lines += '$= {0}$'.format(expressions.integral_intermediate(expr=self._qp['equation'], lb=self._qp['domain'].left, ub=self._qp['domain'].right))

        lines += '$= {0}$'.format(answer)

        return lines.write()


# can be used for known and unknown
class Conditional:
    def __init__(self, part):
        # 2008 Q4b [8 lines] [3 marks]
        # 2011 Q5b [5 lines] [2 marks]

        self.num_lines, self.num_marks = 8, 2

        self._qp = copy.copy(part._qp)

        two_values = sensible_values.conditional_integral(self._qp['equation'], self._qp['domain'])


        self._qp['major_bound'], self._qp['minor_bound'] = two_values


        self._qp['major_direction'] = r'\le' if self._qp['minor_bound'] < self._qp['major_bound'] else r'\ge'
        self._qp['minor_direction'] = random.choice([r'\le', r'\ge'])
    
        
    def question_statement(self):
        return r'Find $Pr(X {0} {1} | X {2} {3})$.'.format(self._qp['minor_direction'], sympy.latex(self._qp['minor_bound']),
                                                            self._qp['major_direction'], sympy.latex(self._qp['major_bound']))


    def solution_statement(self):
        lines = solution_lines.Lines()

        minor = r'X {0} {1}'.format(self._qp['minor_direction'], sympy.latex(self._qp['minor_bound']))
        major = r'X {0} {1}'.format(self._qp['major_direction'], sympy.latex(self._qp['major_bound']))


        lines += r'$Pr({0} | {1}) = {2}$'.format(minor, major, expressions.conditional_probability(minor, major))

        lb = min(self._qp['minor_bound'], self._qp['major_bound'])
        ub = max(self._qp['minor_bound'], self._qp['major_bound'])
        top_integral = expressions.integral(lb=lb, ub=ub, expr=self._qp['equation'])
        top_intermediate = expressions.integral_intermediate(lb=lb, ub=ub, expr=self._qp['equation'])
        top_eval = expressions.integral_intermediate_eval(lb=lb, ub=ub, expr=self._qp['equation'])
        top_value = self._qp['equation'].integrate((x, lb, ub))


        if self._qp['major_direction'] == r'\le':
            lb = self._qp['domain'].left
            ub = self._qp['major_bound']
        else:
            lb = self._qp['major_bound']
            ub = self._qp['domain'].right


        bottom_integral = expressions.integral(lb=lb, ub=ub, expr=self._qp['equation'])
        bottom_intermediate = expressions.integral_intermediate(lb=lb, ub=ub, expr=self._qp['equation'])
        bottom_eval = expressions.integral_intermediate_eval(lb=lb, ub=ub, expr=self._qp['equation'])
        bottom_value = self._qp['equation'].integrate((x, lb, ub))

        lines += r'$= \frac{{ {0} }}{{ {1} }}$'.format(top_integral, bottom_integral)

        lines += r'$= \frac{{ {0} }}{{ {1} }}$'.format(top_intermediate, bottom_intermediate)

        lines += r'$= \frac{{ {0} }}{{ {1} }}$'.format(top_eval, bottom_eval)

        lines += r'$= {0}$'.format(sympy.latex(top_value / bottom_value))

        return lines.write()


# can be used for known
class Cumulative:
    def __init__(self, part):
        self.num_lines, self.num_marks = 12, 3

        self._qp = copy.copy(part._qp)

        stripped_endpoints = sympy.Interval(self._qp['domain'].left, self._qp['domain'].right, True, True)
        self._qp['location'] = sensible_values.antiderivative(self._qp['equation'], stripped_endpoints)
        self._qp['direction'] = random.choice(['left', 'right'])


    def question_statement(self):
        self._qi = {}
        # make the symbols real because SymPy can't deal with complex sympy.Intervals
        self._qi['char'] = random.choice([sympy.Symbol('a', real=True), sympy.Symbol('b', real=True), sympy.Symbol('c', real=True)])
        self._qi['inequality'] = r'\le' if self._qp['direction'] == 'left' else r'\ge'



        if self._qp['direction'] == 'left':
            self._qi['value'] = self._qp['equation'].integrate((x, self._qp['domain'].left, self._qp['location']))
            self._qi['domain'] = sympy.Interval(self._qp['domain'].left, self._qi['char'], False, True)
        else:
            self._qi['value'] = self._qp['equation'].integrate((x, self._qp['location'], self._qp['domain'].right))
            self._qi['domain'] = sympy.Interval(self._qi['char'], self._qp['domain'].right, True, False)

        return r'Find the value of {0} such that $Pr(X {1} {0}) = {2}$.'.format(
            sympy.latex(self._qi['char']),
            self._qi['inequality'],
            sympy.latex(self._qi['value'])
        )


    def solution_statement(self):
        lines = solution_lines.Lines()

        integral, integral_intermediate, integral_intermediate_eval = \
            expressions.integral_trifecta(expr=self._qp['equation'], lb=self._qi['domain'].left, ub=self._qi['domain'].right)

        lines += r'$Pr(X {0} {1}) = {2}$'.format(
            self._qi['inequality'],
            self._qi['char'],
            integral
        )

        lines += r'$= {0}$'.format(integral_intermediate)
        lines += r'$= {0} = {1}$'.format(integral_intermediate_eval, sympy.latex(self._qi['value']))

        if self._qp['direction'] == 'left':
            left_side = self._qp['equation'].integrate().subs({x: self._qi['char']})
            right_side = self._qi['value'] + self._qp['equation'].integrate().subs({x: self._qp['domain'].left})
        else:
            left_side = -1 * self._qp['equation'].integrate().subs({x: self._qi['char']})
            right_side = self._qi['value'] - self._qp['equation'].integrate().subs({x: self._qp['domain'].right})

        lines += r'${0} = {1}$'.format(sympy.latex(left_side), sympy.latex(right_side))


        lines += expressions.shrink_solution_set(left_side, self._qp['domain'], expr_equal_to=right_side, var=self._qi['char'])

        return lines.write()


# can be used for known and unknown
class DefiniteIntegral:
    def __init__(self, part):
        self._qp = copy.copy(part._qp)

        left = int(math.ceil(self._qp['domain'].left))
        

        choices = [left + sympy.Rational(1, 2)]
        while True:
            cur = choices[-1] + sympy.Rational(1, 2)

            if cur < self._qp['domain'].right:
                choices.append(cur)
            else:
                break

        self._qp['location'] = random.choice(choices)
        self._qp['direction'] = random.choice(['left', 'right'])


    def question_statement(self):
        pass


    def solution_statement(self):
        return 
