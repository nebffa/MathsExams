import sympy
from sympy.abc import *


def canonise_log(equation):
    expanded_log = sympy.expand_log(equation, force=True)

    terms = expanded_log.as_ordered_terms()

    a, b = sympy.Wild('a'), sympy.Wild('b')

    total_interior = 1
    for term in terms:

        if sympy.ask(sympy.Q.complex(term)):
            term_interior *= -1
        else:
            term_interior = term.match(sympy.log(a) / b)[a]

            if term.could_extract_minus_sign():
                total_interior /= term_interior
            else:
                total_interior *= term_interior

    if isinstance(total_interior, sympy.Add):
        invert = False
    elif isinstance(total_interior, sympy.Mul):

        match = total_interior.together().match(x / b)  # for some reason, (x/3).match(a/b) gives {a: 1/3, b: 1/x} so we have to use a workaround
        if match is not None:
            invert = False
        else:
            match = total_interior.together().match(a / b)

            degree_numerator = 0 if isinstance(match[a], sympy.Rational) else match[a].as_poly().degree()
            degree_denominator = 0 if isinstance(match[b], sympy.Rational) else match[b].as_poly().degree()

            if degree_numerator < degree_denominator:
                invert = True
            else:
                invert = False
    elif isinstance(total_interior, sympy.Pow):
        index = total_interior.as_base_exp()[1]
        if index < 0:
            invert = True
        else:
            invert = False

    else:  # for debugging - wtf kind of c-c-c-class is it???
        print total_interior, type(total_interior)

    if invert:
        return -sympy.log((1 / total_interior).together(), evaluate=False) / terms[0].as_coeff_Mul()[0].q
    else:
        return sympy.log(total_interior.together(), evaluate=False) / terms[0].as_coeff_Mul()[0].q
