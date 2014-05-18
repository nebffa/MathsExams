import sympy
import random
from ..symbols import x
from ..latex import solutions, expressions
from . import relationships


@relationships.root
class HiddenQuadratic(relationships.QuestionPart):
    """
    Question description
    ====================

    Solve an equation involving exponentials by treating it as a quadratic.


    Real-life instances
    ===================

    2011 2b: [11 lines] [3 marks]
    """

    def __init__(self):
        self.num_lines, self.num_marks = 11, 3
        self._qp = {}

        negative_x_intercept = random.choice(list(range(-5, 0)))
        positive_x_intercept = random.choice(list(range(6)))

        self._qp['equation'] = ((sympy.exp(x) + negative_x_intercept) * (sympy.exp(x) + positive_x_intercept)).expand()

    def question_statement(self):
        return r'Solve ${equation}$ for $x$.'.format(
            equation=sympy.latex(self._qp['equation'])
        )

    def solution_statement(self):
        lines = solutions.Lines()

        X = sympy.Symbol('X')
        lines += r'Let $X = {exp_of_x}$'.format(
            exp_of_x=sympy.latex(sympy.exp(x))
        )

        hidden_quadratic = self._qp['equation'].replace(sympy.exp(x), X). replace(sympy.exp(2 * x), X ** 2)
        lines += r'$\therefore {equation} = {hidden_quadratic}$'.format(
            equation=sympy.latex(self._qp['equation']),
            hidden_quadratic=sympy.latex(hidden_quadratic)
        )

        lines += r'$= {factorised_hidden_quadratic}$'.format(
            factorised_hidden_quadratic=sympy.latex(hidden_quadratic.factor())
        )

        lines += expressions.shrink_solution_set(expr=hidden_quadratic, domain=sympy.Interval(0, sympy.oo), var=X)

        valid_solution = [i for i in sympy.solve(hidden_quadratic) if i > 0][0]
        lines += r'${exp_of_x} = {valid_solution}$'.format(
            exp_of_x=sympy.latex(sympy.exp(x)),
            valid_solution=valid_solution
        )

        answer = sympy.log(valid_solution)
        lines += r'$x = {answer}$'.format(
            answer=sympy.latex(answer)
        )

        return lines.write()
