import sympy


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
