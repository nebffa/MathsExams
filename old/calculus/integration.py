import sympy
import random
import linear
import all_functions


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
        
class Area(object): # SO FAR HAS BEEN ONE OF 3 POSSIBILITIES!!! NOT SURE HOW TO TAKE THIS ONE FORWARD.
    def __init__(self):
        
        x = sympy.Symbol('x')
        remove = random.sample([['log'], ['exp']], 1)[0]
        while True:
            self.equation = all_functions.random_function(log_difficulty = 1, \
                    exp_difficulty = 1, exclude = ['linear', 'quadratic', 'trig'] + remove).equation
                    
            self.lower_bound = random.randint(-3, 1)
            self.upper_bound = self.lower_bound + random.randint(1, 4)
            
            if sympy.ask(sympy.Q.real(self.equation.subs({x: self.lower_bound}))) and sympy.ask(sympy.Q.real(self.equation.subs({x: self.upper_bound}))) \
                and self.equation.subs({x: self.lower_bound}) > 0 and self.equation.subs({x: self.upper_bound}) > 0:
                break
            
        self.area = self.equation.integrate((x, self.lower_bound, self.upper_bound))
        
print(Area().area)
        