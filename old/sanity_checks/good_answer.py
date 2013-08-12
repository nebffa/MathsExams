import sympy

test = (-8*sympy.sqrt(10)/9 + 3*(-2/9 + 2*sympy.sqrt(10)/9)**3 + 2*(-2/9 + 2*sympy.sqrt(10)/9)**2 + 8/9)
print test
print dir(test)


''' (-8*sympy.sqrt(10)/9 + 3*(-2/9 + 2*sympy.sqrt(10)/9)**3 + 2*(-2/9 + 2*sympy.sqrt(10)/9)**2 + 8/9).atoms() 
            = set([1/2, 2/9, 10, 2, -8/9, 3, -1])
            
    (-13/10).atoms()
            = set([-13/10])
    
    
def sane_fraction(fraction):
    if len(fraction.atoms()) == 1: 
        return True
    else:
        return False
    
    
    
sane_fraction(test)