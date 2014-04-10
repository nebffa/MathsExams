from ...relations.trigonometry import trig
import sympy
import random

class cdf(object):
    def __init__(self):
        
        x = sympy.Symbol('x')
        k = sympy.Symbol('k')
        while True:
            y = trig.Trig(1, exclude = ['tan'])
            if y.equation not in [sympy.sin(x), sympy.cos(x)]:
                break        

        self.lower_bound = y.general_solutions[0].subs(k, 0)
        self.upper_bound = y.general_solutions[0].subs(k, 1)
        self.equation = y.equation / y.equation.integrate((x, self.lower_bound, self.upper_bound))

        choices = trig.domain(self.equation, self.lower_bound, self.upper_bound)
        
        while True:
            self.integral_lower_bound = random.sample(choices, 1)[0]
            self.integral_middle_bound = random.sample(choices, 1)[0]
            self.integral_upper_bound = random.sample(choices, 1)[0]
            if self.integral_lower_bound < self.integral_middle_bound < self.integral_upper_bound:
                break
    
        print(self.equation)
        print(self.integral_lower_bound, self.equation.subs(x, self.integral_lower_bound))
        print(self.integral_middle_bound, self.equation.subs(x, self.integral_middle_bound))
        print(self.integral_upper_bound, self.equation.subs(x, self.integral_upper_bound))
