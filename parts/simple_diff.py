import sympy
import random
from maths import all_functions, not_named_yet


# always produces Q1a
class SimpleDiff(object):
    def __init__(self):
        self.num_lines = 5
        self.num_marks = 2

        # since we will never write the function type when writing the exam, we would like to not expose this. however,
        # class SimpleDiffEval needs to know what function type was used here as 1a and 1b never use the same function type
        self.function_type = random.choice(['sqrt', 'quadratic', 'product'])

        if self.function_type == 'sqrt':
            # 2011 1a: y = sqrt(4 - x)
            outer_function = all_functions.request_linear(difficulty=2).equation
            inner_function = all_functions.request_linear(difficulty=1).equation
            inner_function = inner_function.replace(lambda expr: expr.is_Symbol, lambda expr: sympy.sqrt(expr))

            x = sympy.Symbol('x')
            self.equation = outer_function.replace(x, inner_function)
            self.derivative = sympy.diff(self.equation)

        elif self.function_type == 'quadratic':
            # 2008 1a: y = (3x**2 - 5x) ** 5
            # 2012 1a: y = (x**2 - 5x) ** 4
            x = sympy.Symbol('x')
            power_two_coeff = not_named_yet.randint_no_zero(-3, 3)
            power_one_coeff = not_named_yet.randint_no_zero(-5, 5)
            inner_function = power_two_coeff * x ** 2 + power_one_coeff * x
            index = random.randint(3, 5)

            self.equation = inner_function ** index
            self.derivative = sympy.diff(self.equation)

        elif self.function_type == 'product':
            # 2009 1a: y = x * ln(x)
            # 2010 1a: y = (x ** 3) * e ** (2x)
            x = sympy.Symbol('x')
            left_function = x ** random.randint(1, 3)
            right_outer_function = random.choice([sympy.sin, sympy.cos, sympy.log, sympy.exp])
            right_inner_function = not_named_yet.randint_no_zero(-3, 3) * x

            self.equation = left_function * right_outer_function(right_inner_function)
            self.derivative = sympy.diff(self.equation)

    def question_statement(self):
        equation_text = sympy.latex(self.equation)

        question = random.choice(
            [{'statement': r'Differentiate $%s$ with respect to $x$.', 'type': 'f'},
                {'statement': r'If $y = %s$, find $\frac{dy}{dx}$.', 'type': 'y'},
                {'statement': r'Differentiate $%s$.', 'type': 'f'},
                {'statement': r'Let $y = %s$. Find $\frac{dy}{dx}$.', 'type': 'f'}])

        # write_solution needs to know if we are using y or f(x) in order to modify the solution
        self._question_type = question['type']
        return question['statement'] % equation_text
        #file.write('\\textbf{Question 1} \\\\ \n')

        #file.write('\\textbf{a.} \\tab\=' + (question['statement'] % equation_text) + " \\\\ \n")

        #file.write('\\\\\n')
        #for i in range(0, self.num_lines):
        #    file.write('\> \linefill \\\\\n')
        #file.write('\\\\\n')

    def solution_statement(self):
        total_string = ''
        if self._question_type == 'f':
            # look for chain rule candidates and show extra working for the chain rule
            if self.equation.as_base_exp()[1] != 1:
                u = sympy.Symbol('u')
                inner_function, exponent = self.equation.as_base_exp()
                total_string += "Let $f(x) = %s = %s, u = %s$ \\\\ \n" % (sympy.latex(self.equation), sympy.latex(u ** exponent), sympy.latex(inner_function))
                total_string += "$f'(x) = %s \\times u'$ \\\\ \n" % sympy.latex((u ** exponent).diff())

            total_string += "$f'(x) = %s$ \\\\ \n" % sympy.latex(self.derivative.factor())

        elif self._question_type == 'y':
        # look for chain rule candidates and show extra working for the chain rule
            if self.equation.as_base_exp()[1] != 1:
                u = sympy.Symbol('u')
                inner_function, exponent = self.equation.as_base_exp()
                total_string += "Let $y = %s = %s, u = %s$ \\\\ \n" % (sympy.latex(self.equation), sympy.latex(u ** exponent), sympy.latex(inner_function))
                total_string += "$\\frac{dy}{dx} = %s * u'$ \\\\ \n" % sympy.latex((u ** exponent).diff())

            total_string += "$\\frac{dy}{dx} = %s$ \\\\ \n" % sympy.latex(self.derivative)

        return total_string


# always produces Q1b
class SimpleDiffEval(object):
    # function_type_in_simple_diff is the function type used in the class SimpleDiff. we need to know it so we don't use the same function type
    # since questions 1a and 1b never use the same function type
    def __init__(self, function_type_in_simple_diff):
        self.num_lines = 5
        self.num_marks = 2

        function_types = ['product', 'quotient', 'composite']
        try:
            # it might not be in function_types, in which case it will error
            function_types.remove(function_type_in_simple_diff)
        except:
            pass
        self.__function_type = random.choice(function_types)

        if self.__function_type == 'product':
            # 2008 1b: y = x * e**(3x), a = 0
            # 2011 1b: y = x**2 * sin(2x), a = pi / 6
            x = sympy.Symbol('x')
            index = random.randint(1, 3)
            left_function = x ** index

            right_outer_function = random.choice([sympy.sin, sympy.cos, sympy.log, sympy.exp])
            right_inner_function = not_named_yet.randint_no_zero(-3, 3) * x

            self.equation = left_function * right_outer_function(right_inner_function)
            self.derivative = sympy.diff(self.equation)

            if right_outer_function in [sympy.sin, sympy.cos]:
                # using multiples of pi/6 can lead to large coefficients like pi**3/54
                if index == 1:
                    self.x_value = random.choice([sympy.pi/6 * i for i in range(-5, 7)])
                elif index in [2, 3]:
                    self.x_value = random.choice([sympy.pi/2 * i for i in range(-1, 3)])

            elif right_outer_function == sympy.log:
                self.x_value = sympy.Rational(1, right_inner_function.coeff(x)) * sympy.E ** random.randint(1, 3)
            elif right_outer_function == sympy.exp:
                # with something like x**3 * e^x using x = 3, we'd get large answers. we restrict x values based on the index of x
                self.x_value = random.randint(-3 // index, 3 // index)

        elif self.__function_type == 'quotient':
            # 2009 1b: y = cos(x) / (2x + 2), a = pi
            # 2012 1b: y = x / sin(x), a = pi / 2
            x = sympy.Symbol('x')
            special_function = random.choice([sympy.cos(x), sympy.sin(x), sympy.exp(x)])
            linear_function = all_functions.request_linear(difficulty=3).equation

            if random.randint(0, 1):
                self.equation = special_function / linear_function
                bottom_function = linear_function
            else:
                self.equation = linear_function / special_function
                bottom_function = special_function

            while True:
                if special_function in [sympy.sin(x), sympy.cos(x)]:
                    # with the trig function we can easily get overly complicated answers like 2*sqrt(3)*(3 + 2*pi)/3
                    # so we will restrict x
                    if special_function == sympy.cos(x):
                        self.x_value = random.choice([0, sympy.pi, -sympy.pi])
                    elif special_function == sympy.sin(x):
                        self.x_value = random.choice([-1, 1]) * sympy.pi / 2

                elif special_function == sympy.exp(x):
                    self.x_value = random.randint(-2, 2)

                if (bottom_function ** 2).subs({x: self.x_value}) != 0:
                    break

        elif self.__function_type == 'composite':
            # 2010 1b: y = ln(x**2 + 1), a = 2
            x = sympy.Symbol('x')

            # i thought of including sin and cos, but i can't remember ever seeing a question where a quadratic was nested inside
            # of a trig function
            outer_function = random.choice([sympy.exp, sympy.log])

            inner_function = all_functions.request_quadratic(difficulty=random.randint(1, 3)).equation

            if outer_function == sympy.exp:
                # with bad x values we can get things like: dy/dx = (4*x + 4)*exp(2*x**2 + 4*x + 20), at x = 1, dy/dx = exp(26)
                count = 0
                while True:
                    self.x_value = random.randint(-3, 3)
                    if -5 < inner_function.subs({x: self.x_value}) < 5 and -5 < inner_function.diff().subs({x: self.x_value}):
                        break
                    else:
                        count += 1

                    if count > 5:
                        inner_function = all_functions.request_quadratic(difficulty=random.randint(1, 3)).equation
            elif outer_function == sympy.log:
                # the inner quadratic may never yield a positive number in this domain, so we will try
                # a couple of times to find an x value that works, then we will request a new quadratic
                count = 0
                while True:
                    self.x_value = random.randint(-3, 3)
                    if 0 < inner_function.subs({x: self.x_value}) < 5:
                        break
                    else:
                        count += 1

                    if count > 5:
                        inner_function = all_functions.request_quadratic(difficulty=random.randint(1, 3)).equation
            self.equation = outer_function(inner_function)

        if self.__function_type == 'quotient':
            # quotients are always written as one big fraction, but sympy always separates them into multiple fractions, so we have to factorise
            self.derivative = sympy.diff(self.equation).together()
        else:
            self.derivative = sympy.diff(self.equation)

        self.answer = self.derivative.subs({x: self.x_value})

    def question_statement(self):
        equation_text = sympy.latex(self.equation)
        x_value_text = sympy.latex(self.x_value)

        question = random.choice(
            [{'statement': "Let $f(x) = %s$. Evaluate $f'(%s)$.", 'type': 'f'},
                {'statement': "For $f(x) = %s$, find $f'(%s)$.", 'type': 'f'},
                {'statement': "If $g(x) = %s$, find $g'(%s)$.", 'type': 'g'},
                {'statement': "If $f(x) = %s$, find $f'(%s)$.", 'type': 'f'}])

        self._question_type = question['type']
        return question['statement'] % (equation_text, x_value_text)
        #file.write('\\textbf{b.} \\tab\=' + question['statement'] % (equation_text, x_value_text) + " \\\\ \n")

        #file.write('\\\\\n')
        #for i in range(0, self.num_lines):
        #    file.write('\> \linefill \\\\\n')
        #file.write('\\\\\n')
        #file.write('\n')

    def solution_statement(self):
        # needs more work at the moment - likely an inbetween step to evaluate every subexpression in f'(x) but not f'(x) itself
        total_string = "$%s'(x) = %s$ \\\\ \n" % (self._question_type, sympy.latex(self.derivative))
        x = sympy.Symbol('x')

        # print extra steps when dealing with trig functions
        if self.equation.find(sympy.sin) or self.equation.find(sympy.cos):
            a = sympy.Wild('a')
            no_eval = sympy.latex(self.derivative.replace(sympy.sin(a),
                                  sympy.sin(a.subs({x: self.x_value}), evaluate=False)).replace(sympy.cos(a),
                                  sympy.cos(a.subs({x: self.x_value}), evaluate=False)))
            total_string += "$%s'(%s) = %s$ \\\\ \n" % (self._question_type, sympy.latex(self.x_value), no_eval)
            total_string += ', '.join(["$%s = %s$" % (sympy.latex(i.
                       replace(sympy.sin(a), lambda a: sympy.sin(a.subs({x: self.x_value}), evaluate=False)).
                       replace(sympy.cos(a), lambda a: sympy.cos(a.subs({x: self.x_value}), evaluate=False))
                       ), sympy.latex(i.subs({x: self.x_value}))) for i in self.derivative.find(lambda expr: expr.is_Function)]) + " \\\\ \n"

        total_string += "$%s'(%s) = %s$ \\\\ \n" % (self._question_type, sympy.latex(self.x_value), sympy.latex(self.answer))

        return total_string
