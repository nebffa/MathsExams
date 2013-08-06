import pprint
import constants
import random
import sympy
import itertools
from math import factorial

class SmallBinomial(object):    
    def __init__(self, difficulty):
        # p is the probability of drawing a head
        # n is the number of trials
        # x is the number of heads
        p = sympy.Symbol('p')
        self.n = random.randint(3, 4)
        
        if difficulty == 1:
            self.x = random.sample([0, self.n], 1)[0]
        elif difficulty == 2:
            self.x = random.randint(1, self.n - 1)
            
        self.solution = factorial(self.n) / (factorial(self.n - self.x) * factorial(self.x))  * p ** self.x * (1 - p) ** (self.n - self.x)
            
class LargeBinomial(object):
    def __init__(self, difficulty):
        # p is the probability of drawing a head
        # n is the number of trials
        # x is the number of heads
        p = sympy.Symbol('p')
        self.n = random.sample([40, 50, 60, 70], 1)[0]
        
        if difficulty == 1:
            self.x = random.sample([0, self.n], 1)[0]
        elif difficulty == 2:
            self.x = random.sample([1, self.n - 1], 1)[0]
            
        self.solution = factorial(self.n) / (factorial(self.n - self.x) * factorial(self.x))  * p ** self.x * (1 - p) ** (self.n - self.x)
        
class ProbabilityTable(object):
    def __init__(self):
        
        a = b = a_and_b = 1
        while a + b > 1:
            a = sympy.Rational(random.randint(1, 5), random.randint(3, 6))
            b = sympy.Rational(random.randint(1, 5), random.randint(3, 6))
            
        while a_and_b >= min(a, b):
            a_and_b = sympy.Rational(random.randint(1, 5), random.randint(3, 7))
        
        self.non_me =  \
                {
                    'a': a, 
                    'b': b, 
                    'nota': 1 - a, 
                    'notb': 1 - b, 
                    'a_and_b': a_and_b, 
                    'a_and_notb': a - a_and_b, 
                    'nota_and_b': b - a_and_b, 
                    'nota_and_notb': 1 - a - b + a_and_b, 
                    'a_or_b': a + b - a_and_b, 
                    'a_or_notb': 1 - b + a_and_b, 
                    'nota_or_b': 1 - a + a_and_b, 
                    'nota_or_notb': 1 - a_and_b
                }

        a_and_b = 0 # set for mutually exclusive
        self.me =  \
                {
                    'a': a, 
                    'b': b, 
                    'nota': 1 - a, 
                    'notb': 1 - b, 
                    'a_and_b': a_and_b, 
                    'a_and_notb': a - a_and_b, 
                    'nota_and_b': b - a_and_b, 
                    'nota_and_notb': 1 - a - b + a_and_b, 
                    'a_or_b': a + b - a_and_b, 
                    'a_or_notb': 1 - b + a_and_b, 
                    'nota_or_b': 1 - a + a_and_b, 
                    'nota_or_notb': 1 - a_and_b
                }
                
x = ProbabilityTable()
pprint.pprint( x.non_me)
