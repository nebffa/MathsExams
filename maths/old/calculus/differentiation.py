import sympy
import random
from maths.polynomials import linear
from maths import all_functions



class ChainRule(object): 

    def __init__(self): # we will do f of g. So f must be a function type (e.g. square root, or exponential), 
                                # while g must be a complete function in and of itself (e.g. g = x**2 - 2*x + 1)
        
        f = random.sample([lambda x: x ** 3, lambda x: x ** 4, sympy.sqrt], 1)[0]
        g = all_functions.random_function(linear_difficulty = 3, \
                quadratic_difficulty = random.randint(1, 3), trig_difficulty = random.randint(1, 2), exclude = ['log', 'exp', 'trig'])
        
        self.equation = f(g.equation)
        self.derivative = sympy.simplify(self.equation.diff())
        
class ProductQuotientRule(object):
    

    def __init__(self):
        
        x = sympy.Symbol('x')
        f = random.sample([sympy.exp, sympy.sin, sympy.cos], 1)[0]
        
        if f in [sympy.sin, sympy.cos]:
            g = random.sample([x, 2 * x], 1)[0]
        else:
            g = linear.Linear(1).equation
        
        h = x ** random.randint(1, 3)
        
        product_or_quotient = random.sample(['product', 'quotient'], 1)[0]
        
        if product_or_quotient == 'product':        
            self.equation = h * f(g)
        else:
            self.equation = random.sample([h / f(g), f(g) / h], 1)[0]
        self.derivative = sympy.simplify(self.equation.diff())
        
        sin_cos_angles = [-sympy.pi / 2, 0, sympy.pi / 2, sympy.pi] # no need to use all angles. Only the ones that historically appear in VCE papers

                
                
        while True:
            if f in [sympy.sin, sympy.cos]:
                self.x_value = sympy.solve(g - random.sample(sin_cos_angles, 1)[0])[0]
            else:
                self.x_value = random.randint(-2, 2)
            self.y_value = self.equation.subs({x: self.x_value})
            self.gradient = self.derivative.subs({x: self.x_value})

            if sympy.ask(sympy.Q.real(self.y_value)) and sympy.ask(sympy.Q.real(self.gradient)):
                break
            
class IndefiniteIntegral(object):
    
    def __init__(self):
        
        reciprocal = random.sample([True, False], 1)[0]
        
        x = sympy.Symbol('x')
        g = linear.Linear(3).equation
        if reciprocal:
            f = random.sample([lambda x: x, lambda x: x ** 2, lambda x: x ** 3], 1)[0]
            self.equation = 1 / f(g)
        else:
            f = random.sample([sympy.sqrt, sympy.sin, sympy.cos], 1)[0]
            if f == sympy.sqrt:
                f = linear.Linear(3).equation
                self.equation = f.replace(lambda expr: expr.is_Symbol, lambda expr: sympy.sqrt(expr))
            else:
                self.equation = f(g)
                sin_cos_angles = [-sympy.pi / 2, 0, sympy.pi / 2, sympy.pi] # no need to use all angles. Only the ones that historically appear in VCE papers
        
        self.antiderivative = self.equation.integrate(x)
                       
class DefiniteIntegral(object):
    
    def __init__(self):
        
        x = sympy.Symbol('x')
        while True:
            while True:
                self.equation = IndefiniteIntegral().equation
                if not (self.equation.count(sympy.sin) > 0 or self.equation.count(sympy.cos) > 0):
                    break        
        
            self.lower_bound = random.randint(-1, 1)
            self.upper_bound = self.lower_bound + random.randint(1, 3)
            self.answer = self.equation.integrate((x, self.lower_bound, self.upper_bound))
            
            if sympy.ask(sympy.Q.real(self.answer)) and -30 < sympy.Rational(self.answer).p < 30 and sympy.Rational(self.answer).q < 10:
                break
                
class IntegrationByParts(object):
    def __init__(self):
        
        x = sympy.Symbol('x')
        f = random.sample([x, x ** 2], 1)[0]
        
        g = random.sample([sympy.log(x), sympy.cos(x), sympy.sin(x)], 1)[0]
        
        self.equation = f * g
        self.derivative = self.equation.diff(x)
        
        if g == sympy.log(x):
            self.lower_bound = random.randint(1, 2)
            self.upper_bound = self.lower_bound + random.randint(1, 3)
        else:
            self.lower_bound = random.sample([-sympy.pi, -sympy.pi / 2, 0], 1)[0]
            self.upper_bound = random.sample([sympy.pi / 6, sympy.sqrt(2) * sympy.pi / 2, sympy.pi / 3, sympy.pi / 2, sympy.pi], 1)[0] 
            # not all possible angles are included, we want to ensure we have some 'nice' angles in there
            
        # somehow print that:
        # self.derivative.as_ordered_terms()[0] = d/dx(self.equation) - self.derivative.as_ordered.terms()[1]
        # as it's part of the working marks!!!
        self.answer = sympy.simplify(self.derivative.as_ordered_terms()[0].integrate((x, self.lower_bound, self.upper_bound))) 
        
class Tangent(object):
    def __init__(self):
        x, a, c, d, k, m = sympy.symbols('x, a, c, d, k, m')
        
        
        f = random.sample([sympy.exp, sympy.sqrt], 1)[0]
        while True:
            if f == sympy.exp:
                while True:
                    b = random.randint(-3, 3)
                    if b != 0:
                        break
                c = random.randint(-3, 3)
                self.equation = random.sample([f(x * m) + b * x, f(x) + k], 1)[0]
            else:
                self.equation = f(x) + d
            
            if f == sympy.exp:
                if b * x in self.equation.as_ordered_terms():
                    while True:
                        self.x_value = random.randint(-6, 6)
                        if self.x_value != 0:
                            break
                    self.derivative = self.equation.diff(x)
                    self.tangent = self.derivative.subs({x: self.x_value}) * x
                    self.y_value = self.equation.subs({x: self.x_value})
                    self.m_value = sympy.solve(self.y_value - self.tangent.subs({x: self.x_value}))[0]
                            
                    if sympy.Rational(self.m_value).q < 20:
                        break
                elif k in self.equation.as_ordered_terms():
                    self.x_value = a
                    self.derivative = self.equation.diff(x)
                    self.tangent = self.derivative.subs({x: self.x_value}) * x
                    self.y_value = self.equation.subs({x: self.x_value})
                    self.k_value = sympy.solve(self.y_value - self.tangent.subs({x: self.x_value}), k)[0]
                        
            else:
                self.tangent = a * x + random.randint(-3, 3)
                self.derivative = self.equation.diff(x)
                self.x_value = random.sample([4, 9, 16, 25], 1)[0]
                self.a_value = self.derivative.subs({x: self.x_value}) # start solving
                self.tangent = self.tangent.subs({a: self.a_value})
                self.c_value = sympy.solve(self.tangent.subs({x: self.x_value}) - c)[0]
                self.d_value = sympy.solve(self.equation.subs({x: self.x_value}) - self.c_value)[0]
            
                if sympy.Rational(self.a_value).q < 20:
                    break
        

        if m in self.equation.atoms():
            self.stationary_x_value = sympy.solve(self.equation.diff(x), x)[0]
