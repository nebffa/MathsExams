import random
import sympy
from ..latex.table import probability_table
from ..latex import expressions, solutions
from .. import not_named_yet
from ..symbols import k, coeff0, coeff1, coeff2
from . import relationships
from collections import OrderedDict


@relationships.root
class ProbTableUnknown(relationships.QuestionPart):
    """
    Question description
    ====================

    Create a probability table where some keys or values are unknown (they are expressed in terms of an unknown). Calculate
    the value of this unknown.


    Real-life instances
    ===================

    2010 8: [12 lines] [3 marks]
    """

    def __init__(self):
        self.num_lines, self.num_marks = 12, 3

        lb = random.randint(-2, -1)
        keys = list(range(lb, lb + 4))

        self._qp = {}

        while True:
            # ensure we will have only one positive root for k
            pos_root_numerator = random.randint(1, 3)
            pos_root_denom = pos_root_numerator + random.randint(1, 2)

            neg_root_numerator = random.randint(3, 7)
            neg_root_denom = neg_root_numerator + random.randint(1, 2)

            quadratic = ((pos_root_denom * k - pos_root_numerator) * (neg_root_denom * k + neg_root_numerator) / neg_root_denom).expand()
            self._qp['quadratic_shrinkage_factor'] = neg_root_denom

            self._qp['quadratic_solutions'] = (
                sympy.Rational(pos_root_numerator, pos_root_denom),
                sympy.Rational(-neg_root_numerator, neg_root_denom)
            )

            self._qp['answer'] = sympy.Rational(pos_root_numerator, pos_root_denom)

            # because we will be making sure that the sum of probabilities = 1, to preserve our pre-made solution we will add 1 to the quadratic
            quadratic += 1

            # now we want to take partitions of this quadratic (e.g. p^2 / 4, or (4p + 1) / 8 and have them be the values for the probability table)
            # let's say that we can either take a partition of the p^2 component, or of the (p^1 + p^0) component
            match = quadratic.match(coeff0 * k ** 2 + coeff1 * k + coeff2)
            if match[coeff1] == 0 or match[coeff2] == 0 or match[coeff0].p > 16 or match[coeff1].p > 16 or match[coeff2].p > 16:
                # we want non-zero coefficients for all powers of k, as well as small coefficients so the partition algorithm
                # doesn't take ages trying to compute them all
                continue

            # randomly partition the different parts of the quadratic to the different cells of the probability table
            possible_square_partitions = [i for i in not_named_yet.partition(abs(match[coeff0].p), include_zero=True) if
                                          1 < len(i) < len(keys)]
            possible_linear_partitions = [i for i in not_named_yet.partition(abs(match[coeff1].p), include_zero=True) if
                                          1 < len(i) < len(keys)]
            possible_zeroth_partitions = [i for i in not_named_yet.partition(abs(match[coeff2].p), include_zero=True) if
                                          1 < len(i) < len(keys)]

            p_square_partition = list(random.choice(possible_square_partitions))
            p_linear_partition = list(random.choice(possible_linear_partitions))
            p_zeroth_partition = list(random.choice(possible_zeroth_partitions))

            p_square_partition += [0] * (len(keys) - len(p_square_partition))
            p_linear_partition += [0] * (len(keys) - len(p_linear_partition))
            p_zeroth_partition += [0] * (len(keys) - len(p_zeroth_partition))

            random.shuffle(p_square_partition)
            random.shuffle(p_linear_partition)
            random.shuffle(p_zeroth_partition)

            if match[coeff0].could_extract_minus_sign():
                p_square_partition = [-i for i in p_square_partition]
            if match[coeff1].could_extract_minus_sign():
                p_linear_partition = [-i for i in p_linear_partition]
            if match[coeff2].could_extract_minus_sign():
                p_zeroth_partition = [-i for i in p_zeroth_partition]
            partitions = list(zip(p_square_partition, p_linear_partition, p_zeroth_partition))

            probabilities = [partition[0] * self._qp['answer'] ** 2 + partition[1] * self._qp['answer'] +
                             partition[2] for partition in partitions]
            if not all([probability > 0 for probability in probabilities]):
                continue  # some probabilities are negative

            if all([partition.count(0) != 3 for partition in partitions]):
                break

        values = [partition[0] * k ** 2 / match[coeff0].q +
                  partition[1] * k / match[coeff1].q + sympy.Rational(partition[2], match[coeff2].q) for partition in partitions]
        self._qp['prob_table'] = OrderedDict(list(zip(keys, values)))

    def question_statement(self):
        return r'The discrete random variable X has the probability distribution \\ {probability_table} \\ Find the value of k.'.format(
            probability_table=probability_table(self._qp['prob_table'])
        )

    def solution_statement(self):
        lines = solutions.Lines()

        lines += r'$E(X) = {symbolic_expectation_of_x} = {total_probability} = 1$'.format(
            symbolic_expectation_of_x=expressions.symbolic_discrete_expectation_x(),
            total_probability=sympy.latex(sum(self._qp['prob_table'].values()))
        )

        quadratic = sum(self._qp['prob_table'].values()) - 1
        lines += r'${0} = 0$'.format(
            sympy.latex(quadratic)
        )

        quadratic *= self._qp['quadratic_shrinkage_factor']
        lines += r'${0} = 0$'.format(
            sympy.latex(quadratic)
        )

        lines += r'$k = {quadratic_formula} = {solution_1}, {solution_2}$'.format(
            quadratic_formula=expressions.quadratic_formula(quadratic, var=k),
            solution_1=sympy.latex(self._qp['quadratic_solutions'][0]),
            solution_2=sympy.latex(self._qp['quadratic_solutions'][1])
        )

        lines += r'''but $k > 0$ so k = ${answer}$'''.format(
            answer=sympy.latex(self._qp['answer'])
        )

        return lines.write()

    def sanity_check(self):
        # check the answer gives positive probabilities
        for value in self._qp['prob_table'].values():
            if value.subs({k: self._qp['answer']}) < 0:
                raise ValueError('This answer (the value of k) is giving negative values in the probability table.')

        quadratic = sum(self._qp['prob_table'].values())

        for solution in self._qp['quadratic_solutions']:
            if quadratic.subs({k: solution}) != 1:
                raise ValueError('One of the pre-determined solutions for the probability table is not giving a total probability of 1.')
