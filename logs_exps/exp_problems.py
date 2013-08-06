import quadratic
import sympy


class QuadraticLookalike(object):    
    def __init__(self, difficulty):
    
        if difficulty >= 4:
            raise ValueException('The difficulty of the quadratic cannot be greater than 4. This gives complex arguments in the logarithm solutions!')
    
        while True:
            quadratic_intermediate = quadratic.Quadratic(difficulty)
            f = quadratic_intermediate.equation
            
            self.equation = f.replace(lambda expr: expr.is_Symbol, lambda expr: sympy.exp(expr))
            
            self.solutions = []
            for solution in quadratic_intermediate.solutions:
                if solution < 0:
                    continue
                self.solutions.append(sympy.log(solution))
                
            if len(self.solutions) != 0:
                break
                
g = QuadraticLookalike(5)
print g.equation
print g.solutions