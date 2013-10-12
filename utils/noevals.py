import sympy

# calls to the printers aren't working


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


# doesn't work with negative arguments
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


# doesn't work at all
class noevalPow(sympy.Pow):
    pass
