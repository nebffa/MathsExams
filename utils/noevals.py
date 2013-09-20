import sympy

'''
I know this is looking back a month or two, but I have just started to use your idea about subclassing.

However, it is having unintended side effects.

Including the code:

class exp(sympy.exp):
    @classmethod
    def eval(cls, arg):
        return

in a module like noevals.py, and then subsequently importing noevals has disabled eval in the regular sympy.exp. 
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
