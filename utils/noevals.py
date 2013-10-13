import sympy
from sympy import cache
from sympy.core.sympify import _sympify
from sympy.printing.latex import LatexPrinter



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


class noeval:
    pass


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


class noevalAdd(sympy.Add, noeval):
    @classmethod
    def flatten(cls, seq):
        return seq, [], None




class noevalMul(sympy.Mul, noeval):
    @classmethod
    def flatten(cls, seq):
        return seq, [], None



import re
import sympy
#import ipdb


class NoEvalLatexPrinter(LatexPrinter):
    


    def _print_Mul(self, expr):
        coeff, _ = expr.as_coeff_Mul()
        

        if not coeff.is_negative:
            tex = ""
        else:
            for i in range(len(expr.args)):
                # another change from the original - ensure noevalMul is preseved (the normal expr = -expr forces evaluation)
                if expr.args[i].is_negative:
                    
                    changed_args = list(expr.args)
                    changed_args[i] *= -1
                    expr = noevalMul(*changed_args)

            tex = "- "

        from sympy.simplify import fraction
        numer, denom = fraction(expr, exact=True)
        separator = self._settings['mul_symbol_latex']

        # another change from the original
        numbersep = r" \times "
        #numbersep = self._settings['mul_symbol_latex_numbers']

        def convert(expr):
            if not expr.is_Mul or not isinstance(expr, noevalMul):
                return str(self._print(expr))

            else:
                _tex = last_term_tex = ""

                if self.order not in ('old', 'none'):
                    args = expr.as_ordered_factors()
                else:
                    args = expr.args


                for i, term in enumerate(args):
                    term_tex = self._print(term)

                    if self._needs_mul_brackets(term, last=(i == len(args) - 1)):
                        term_tex = r"\left(%s\right)" % term_tex

                    if re.search("[0-9][} ]*$", last_term_tex) and \
                            re.match("[{ ]*[-+0-9]", term_tex):
                        # between two numbers
                        _tex += numbersep
                    elif _tex:
                        _tex += separator

                    _tex += term_tex
                    last_term_tex = term_tex
                return _tex

        if denom is sympy.S.One:
            # the change from the original _print_Mul - instead of passing numer, we pass the original expression
            tex += convert(expr)
        else:
            snumer = convert(numer)
            sdenom = convert(denom)
            ldenom = len(sdenom.split())
            ratio = self._settings['long_frac_ratio']
            if self._settings['fold_short_frac'] \
                    and ldenom <= 2 and not "^" in sdenom:
                # handle short fractions
                if self._needs_mul_brackets(numer, last=False):
                    tex += r"\left(%s\right) / %s" % (snumer, sdenom)
                else:
                    tex += r"%s / %s" % (snumer, sdenom)
            elif len(snumer.split()) > ratio*ldenom:
                # handle long fractions
                if self._needs_mul_brackets(numer, last=True):
                    tex += r"\frac{1}{%s}%s\left(%s\right)" \
                        % (sdenom, separator, snumer)
                elif numer.is_Mul:
                    # split a long numerator
                    a = sympy.S.One
                    b = sympy.S.One
                    for x in numer.args:
                        if self._needs_mul_brackets(x, last=False) or \
                                len(convert(a*x).split()) > ratio*ldenom or \
                                (b.is_commutative is x.is_commutative is False):
                            b *= x
                        else:
                            a *= x
                    if self._needs_mul_brackets(b, last=True):
                        tex += r"\frac{%s}{%s}%s\left(%s\right)" \
                            % (convert(a), sdenom, separator, convert(b))
                    else:
                        tex += r"\frac{%s}{%s}%s%s" \
                            % (convert(a), sdenom, separator, convert(b))
                else:
                    tex += r"\frac{1}{%s}%s%s" % (sdenom, separator, snumer)
            else:
                tex += r"\frac{%s}{%s}" % (snumer, sdenom)

        return tex






def latex(expr, **settings):
    #ipdb.set_trace()
    return NoEvalLatexPrinter(settings).doprint(expr)


# doesn't work at all
class noevalPow(sympy.Pow):
    @cache.cacheit
    def __new__(cls, b, e, evaluate=True):
        b = _sympify(b)
        e = _sympify(e)

        obj = sympy.Expr.__new__(cls, b, e)
        obj.is_commutative = (b.is_commutative and e.is_commutative)
        return obj

