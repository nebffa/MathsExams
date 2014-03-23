from maths.relations.polynomials import linear
import sympy
import random

coefficients_bound = 5

class Hyperbola(object):
    def __init__(self, difficulty): # difficulty in line with that of a Linear(object)
        a = random.randint(-coefficients_bound, coefficients_bound)
        while True:
            b = random.randint(-coefficients_bound, coefficients_bound)
            if b != 0:
                break
                
        g = linear.Linear(difficulty).equation
                
        self.equation = a + b / g
        self.horizontal_asymptote = a
        self.vertical_asymptote = sympy.solve(g)[0] 
        
class Truncus(object):
    def __init__(self, difficulty): # difficulty in line with that of a Linear(object)
        a = random.randint(-coefficients_bound, coefficients_bound)
        while True:
            b = random.randint(-coefficients_bound, coefficients_bound)
            if b != 0:
                break
                
        g = linear.Linear(difficulty).equation
                
        self.equation = a + b / g ** 2
        self.horizontal_asymptote = a
        self.vertical_asymptote = sympy.solve(g)[0]
    
        