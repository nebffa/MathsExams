from maths.utils import noevals
from maths.symbols import x
import sympy


def test_noevalify():
    noeval_expr = noevals.noevalify(sympy.log(x + 2) + sympy.sin(x))
    assert noevals.is_eval_free(noeval_expr)
