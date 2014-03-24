import sympy
import random


def integer_domain(low=-5, high=5, minimum_distance=3):
    """ Return a sympy.Interval domain with min/max bounds of input variables low and high.

    The interval is chosen by selecting integers randomly: random.randint(low, high)

    """

    while True:
        b1 = random.randint(low, high)
        b2 = random.randint(low, high)

        if b1 + minimum_distance <= b2:
            return sympy.Interval(b1, b2, False, False)
        elif b2 + minimum_distance <= b1:
            return sympy.Interval(b2, b1, False, False)