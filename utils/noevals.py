import sympy

'''
I know this is looking back a month or two, but I have just started to use your idea about subclassing.

However, it is having unintended side effects.

Including the code:

class exp((sympy.exp):
    @classmethod
    def eval(cls, arg):
        return

in a module like noevals.py, and then subsequently importing noevals has disabled eval in the regular (sympy.exp. 
I am super new to subclassing in general, but I know it's this code because when I delete these 4 lines the problem goes away. 
How do I retain this subclass without altering the parent's behaviour?


---------------------------------------------------------------------------------------------------------------------


I can only guess at what's happening, but does it work if you don't 
name the class "exp"? There is (unfortunately) a global class registry 
in SymPy that uses the name of the class, so a subclass called "exp" 
might inadvertently override exp for other parts of SymPy. 

If this is the issue, you can always call the class something like 
UnevaluatedExp, and then put "exp = UnevaluatedExp" at the end of the 
definition for convenience (or always import it as "from module import 
UnevaluatedExp as exp"). The important thing is the __name__ of the 
class. 

Of course, we really should get rid of the class registry. But it 
hasn't been done yet. 

@ https://groups.google.com/forum/#!topic/sympy/zilEXwN26so
'''


def noevalsub(expr, mapping):
    a = sympy.Wild('a')
    noeval_map = (
        (sympy.Abs, noevalAbs),
        (sympy.sin, noevalsin),
        (sympy.cos, noevalcos),
        (sympy.tan, noevaltan),
        (sympy.exp, noevalexp),
        (sympy.log, noevallog),
        (sympy.Add, noevalAdd),
        (sympy.Mul, noevalMul),
        (sympy.Pow, noevalPow)
    )

    for yeseval, noeval in noeval_map:
        # yes_eval, no_eval = item
        print(yeseval(a), noeval(a))
        expr = expr.subs(yeseval(a), noeval(a))
    print(expr)
    return expr.subs(mapping)


class noevalAbs(sympy.Abs):
    @classmethod
    def eval(cls, arg):
        return


class noevalsin(sympy.sin):
    @classmethod
    def eval(cls, arg):
        return


class noevalcos(sympy.cos):
    @classmethod
    def eval(cls, arg):
        return


class noevaltan(sympy.tan):
    @classmethod
    def eval(cls, arg):
        return


class noevalexp(sympy.exp):
    @classmethod
    def eval(cls, arg):
        return


class noevallog(sympy.log):
    @classmethod
    def eval(cls, arg):
        return


class noevalAdd(sympy.Add):
    @classmethod
    def flatten(cls, seq):
        return seq, [], None


class noevalMul(sympy.Mul):
    @classmethod
    def flatten(cls, seq):
        return seq, [], None


    '''def as_coeff_Mul(self):
        return -1, self

    def _keep_coeff(coeff, factors, clear=True, sign=False):
        print('asd')
        return 21312


y = noevalMul(-2, 3)
print(dir(y))
print(y)'''


class noevalPow(sympy.Pow):
    pass
