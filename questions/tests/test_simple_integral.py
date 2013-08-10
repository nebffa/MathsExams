from .. import questions, simple_integral


def test_SimpleDefiniteIntegral():
    q1 = simple_integral.SimpleDefiniteIntegral()
    questions.test_question(q1)


def test_DefiniteIntegralEquality():
    q1 = simple_integral.DefiniteIntegralEquality()
    questions.test_question(q1)
