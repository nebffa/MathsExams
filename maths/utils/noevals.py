import sympy
from sympy.core.sympify import _sympify
from sympy.printing.latex import LatexPrinter
from ..symbols import x
import re
import collections


def noevalify(expr, include=None):
    """Replace instances of sympy classes with their corresponding noeval subclass.
    """

    mapping = noevalmapping()

    while True:
        old_expr = expr
        for eval_function, noeval_function in mapping.items():
            if include is not None and eval_function not in include:
                continue

            expr = expr.replace(eval_function, noeval_function)

        if old_expr == expr:
            break

    if not is_eval_free(expr):
        raise RuntimeError("Noevalify hasn't worked.")

    return expr


def is_eval_free(expr):
    """Check whether an expression has only noeval subclasses or not.

    >>> is_eval_free(x + 2)
    False

    >>> is_eval_free(noevalAdd(x, 2))
    True
    """

    for eval_function, noeval_function in noevalmapping().items():
        instances = expr.find(eval_function)
        for instance in instances:
            if is_eval_instance(instance, noeval_function):
                return False

    return True


def is_eval_instance(obj, noevaltype):
    """Check whether an object is of its eval or noeval type.

    >>> is_eval_instance(sympy.sin(x), noevalsin)
    True

    >>> is_eval_instance(noevalcos(x), noevalcos)
    False

    >>> is_eval_instance(sympy.exp(x), noevaltan)
    Traceback (most recent call last):
     ...
    ValueError: The object: exp(x) is not of type or noevaltype of: tan
    """

    if noevaltype not in noevalmapping().values():
        raise ValueError('The supplied type must be a noeval type, not: {invalid_type}'.format(invalid_type=noevaltype))

    if len(noevaltype.__bases__) > 1:
        raise NotImplementedError('Only works for noevals with only 1 superclass')

    noevaltype_superclass = noevaltype.__bases__[0]
    if isinstance(obj, noevaltype):
        return False
    elif isinstance(obj, noevaltype_superclass):
        return True
    else:
        raise ValueError('The object: {obj} is not of type or noevaltype of: {noevaltype}'.format(
            obj=obj,
            noevaltype=noevaltype)
        )


class noevalAbs(sympy.Abs):
    @classmethod
    def eval(cls, arg):
        return


class noevalsin(sympy.sin):
    @classmethod
    def eval(cls, arg):
        return
noevalsin.__name__ = sympy.sin.__name__


class noevalcos(sympy.cos):
    @classmethod
    def eval(cls, arg):
        return
noevalcos.__name__ = sympy.cos.__name__


class noevaltan(sympy.tan):
    @classmethod
    def eval(cls, arg):
        return
noevaltan.__name__ = sympy.tan.__name__


class noevalexp(sympy.exp):
    @classmethod
    def eval(cls, arg):
        return


class noevallog(sympy.log):
    @classmethod
    def eval(cls, arg):
        return
noevallog.__name__ = sympy.log.__name__


class noevalAdd(sympy.Add):
    @classmethod
    def flatten(cls, seq):
        for o in seq:
            if isinstance(o, noevalAdd):
                seq.remove(o)
                seq.extend(o.args)

        return seq, [], None


class noevalMul(sympy.Mul):
    @classmethod
    def flatten(cls, seq):
        for o in seq:
            if isinstance(o, noevalMul):
                seq.remove(o)
                seq.extend(o.args)

        return seq, [], None


class noevalPow(sympy.Pow):
    @sympy.cache.cacheit
    def __new__(cls, b, e, evaluate=True):
        b = _sympify(b)
        e = _sympify(e)

        obj = sympy.Expr.__new__(cls, b, e)
        obj.is_commutative = (b.is_commutative and e.is_commutative)
        return obj


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
        # numbersep = self._settings['mul_symbol_latex_numbers']

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
                    and ldenom <= 2 and "^" not in sdenom:
                # handle short fractions
                if self._needs_mul_brackets(numer, last=False):
                    tex += r"\left(%s\right) / %s" % (snumer, sdenom)
                else:
                    tex += r"%s / %s" % (snumer, sdenom)
            elif len(snumer.split()) > ratio * ldenom:
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
                                len(convert(a * x).split()) > ratio * ldenom or \
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
    """A rudimentary printer for noevals.
    """
    return NoEvalLatexPrinter(settings).doprint(expr)


def noevalmapping():
    """Return a mapping from a sympy class to its noeval class.

    Note that for proper "noevalification", we need to have it as an ordered dict. This is so that
    when noevalify() iterates through the mapping, it replaces Add and Mul and Pow last.

    For example, if we have y = cos(x - pi/3, evaluate=False)...
        1. print(y) gives cos(x - pi/3)
        2. y.replace(sympy.Add, noevalAdd) gives sin(x + pi/6)     i.e. it immediately simplifies
        3. y.replace(sympy.cos, noevalcos) followed by y.replace(sympy.Add, noevalAdd) gives cos(x + pi/6)
            with all classes replaced by their correspondent noeval
    """
    return collections.OrderedDict([
        (sympy.Abs, noevalAbs),
        (sympy.sin, noevalsin),
        (sympy.cos, noevalcos),
        (sympy.tan, noevaltan),
        (sympy.exp, noevalexp),
        (sympy.log, noevallog),
        (sympy.Add, noevalAdd),
        (sympy.Mul, noevalMul),
        (sympy.Pow, noevalPow)
    ])


def noevalversion(function_type):
    """Return the noeval type of a sympy type.

    >>> noevalversion(sympy.Add)
    <class 'maths.utils.noevals.noevalAdd'>
    """

    return noevalmapping()[function_type]
