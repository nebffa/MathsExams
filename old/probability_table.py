import sympy
import random


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
                
