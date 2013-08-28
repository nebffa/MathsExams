import sympy
import random

class Cylinder(object):
    def __init__(self):
        
        r, h = sympy.symbols('r, h')
        g = sympy.Function('g')

        R = random.randint(1, 5)
        while True:
            H = random.randint(1, 5)
            if H != R:
                break
        
        self.surface_area = 2 * sympy.pi * r * h + 2 * sympy.pi * r ** 2
        self.volume = h * sympy.pi * r ** 2
        
        self.surface_area_r = sympy.simplify(self.surface_area.subs(h, (H * R - H * r) / R))
        self.surface_area_h = sympy.simplify(self.surface_area.subs(r, (H * R - R * h) / H))
        
        self.derivative_r = sympy.simplify(self.surface_area_r.diff())
        self.derivative_h = sympy.simplify(self.surface_area_h.diff())
        
        self.max_r = sympy.solve(self.derivative_r)[0]
        self.max_h = sympy.solve(self.derivative_h)[0]
        
class TriangularPrism(object):
    def __init__(self):
        v, l, d = sympy.symbols('v, l, d')
        
        v = random.randint(1, 10) * 100
        if random.sample([False, True], 1)[0]:
            d = 4 * v / (sympy.sqrt(3) * l ** 2)
        else:
            l = sympy.sqrt(4 * v / (sympy.sqrt(3) * d))
        
        
        self.surface_area = 3 * l * d + sympy.sqrt(3) / 2 * l ** 2
        self.volume = sympy.sqrt(3) / 4 * l ** 2 * d # not needed in calculations as we know volume from the start
        
        self.surface_area_d = sympy.simplify(self.surface_area.subs(l, sympy.sqrt(4 * d * v / sympy.sqrt(3))))
        self.surface_area_l = self.surface_area.subs(d, sympy.sqrt(4 * v / (sympy.sqrt(3) * l ** 2)))
        
        self.derivative_d = sympy.simplify(self.surface_area_d.diff(), d)
        self.derivative_l = sympy.simplify(self.surface_area_l.diff(), l)
        
        self.min_d = [i for i in sympy.solve(self.derivative_d) if sympy.ask(sympy.Q.real(i)) and i > 0][0]
        self.min_l = [i for i in sympy.solve(self.derivative_l) if sympy.ask(sympy.Q.real(i)) and i > 0][0]
        
        self.min_surface_area = self.surface_area_d.subs(d, self.min_d)
        
        
y = TriangularPrism()
print(y.surface_area_l)
print(y.min_d)
print(y.min_l)
print(y.min_surface_area)
