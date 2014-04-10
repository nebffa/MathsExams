import random
import sympy
from ..latex.table import probability_table
from ..latex import expressions, latex
from .. import not_named_yet
from ..symbols import *
from . import relationships
from collections import OrderedDict


@relationships.root
class ProbTableUnknown(object):
    def __init__(self):
        # 2010 Q8 [12 lines] [3 marks]

        self.num_lines, self.num_marks = 12, 3

        lb = random.randint(-2, -1)
        keys = list(range(lb, lb + 4))

        self._question_params = {}

        while True:
            # ensure we will have only one positive root for k
            pos_root_numerator = random.randint(1, 3)
            pos_root_denom = pos_root_numerator + random.randint(1, 2)

            neg_root_numerator = random.randint(3, 7)
            neg_root_denom = neg_root_numerator + random.randint(1, 2)

            quadratic = ((pos_root_denom*k - pos_root_numerator) * (neg_root_denom*k + neg_root_numerator) / neg_root_denom).expand()
            self._question_params['quadratic_shrinkage_factor'] = neg_root_denom

            self._question_params['quadratic_solutions'] = (sympy.Rational(pos_root_numerator, pos_root_denom), 
                                                            sympy.Rational(-neg_root_numerator, neg_root_denom))
            self._question_params['answer'] = sympy.Rational(pos_root_numerator, pos_root_denom)

            # because we will be making sure that the sum of probabilities = 1, to preserve our pre-made solution we will add 1 to the quadratic
            quadratic += 1


            # now we want to take partitions of this quadratic (e.g. p^2/4, or (4p + 1)/8 and have them be the values for the probability table)
            # let's say that we can either take a partition of the p^2 component, or of the (p^1 + p^0) component
            match = quadratic.match(x0*k**2 + x1*k + x2)
            if match[x1] == 0 or match[x2] == 0 or match[x0].p > 16 or match[x1].p > 16 or match[x2].p > 16:
                # we want non-zero coefficients for all powers of k, as well as small coefficients so the partition algorithm
                # doesn't take ages trying to compute them all
                continue

            # randomly partition the different parts of the quadratic to the different cells of the probability table
            p_square_partition = list(random.choice([i for i in not_named_yet.partition(abs(match[x0].p), include_zero=True) if 1 < len(i) < len(keys)]))
            p_linear_partition = list(random.choice([i for i in not_named_yet.partition(abs(match[x1].p), include_zero=True) if 1 < len(i) < len(keys)]))
            p_zeroth_partition = list(random.choice([i for i in not_named_yet.partition(abs(match[x2].p), include_zero=True) if 1 < len(i) < len(keys)]))
            
            p_square_partition += [0] * (len(keys) - len(p_square_partition))
            p_linear_partition += [0] * (len(keys) - len(p_linear_partition))
            p_zeroth_partition += [0] * (len(keys) - len(p_zeroth_partition))

            random.shuffle(p_square_partition)
            random.shuffle(p_linear_partition)
            random.shuffle(p_zeroth_partition)

            if match[x0].could_extract_minus_sign():
                p_square_partition = [-i for i in p_square_partition]
            if match[x1].could_extract_minus_sign():
                p_linear_partition = [-i for i in p_linear_partition]
            if match[x2].could_extract_minus_sign():
                p_zeroth_partition = [-i for i in p_zeroth_partition]
            partitions = list(zip(p_square_partition, p_linear_partition, p_zeroth_partition))

            if not all([partition[0]*self._question_params['answer']**2 + partition[1]*self._question_params['answer'] + 
                    partition[2] > 0 for partition in partitions]):
                continue  # some probabilities are negative

            if all([partition.count(0) != 3 for partition in partitions]):
                values = [partition[0]*k**2/match[x0].q + partition[1]*k/match[x1].q + sympy.Rational(partition[2], match[x2].q) for partition in partitions]
                break

        self._question_params['prob_table'] = OrderedDict(list(zip(keys, values)))

    def question_statement(self):        
        table = probability_table(self._question_params['prob_table'])
        text = r'''The discrete random variable X has the probability distribution \\ {0} \\ Find the value of k.'''

        return text.format(table)

    def solution_statement(self):
        line_1 = r'''$E(X) = \sum\limits_{{i=1}}^{{n}} x_{{i}} \times Pr(X = x_{{i}}) = {0} = 1$'''.format(
                sympy.latex(sum(self._question_params['prob_table'].values())))

        quadratic = sum(self._question_params['prob_table'].values()) - 1
        line_2 = r'''${0} = 0$'''.format(sympy.latex(quadratic))

        quadratic *= self._question_params['quadratic_shrinkage_factor']
        line_3 = r'''${0} = 0$'''.format(sympy.latex(quadratic))        

        line_4 = r'''$k = {0} = {1}, {2}$'''.format(expressions.quadratic_formula(quadratic, var=k), 
                                                        sympy.latex(self._question_params['quadratic_solutions'][0]), 
                                                        sympy.latex(self._question_params['quadratic_solutions'][1]))

        line_5 = r'''but $k > 0$ so k = ${0}$'''.format(sympy.latex(self._question_params['answer']))

        return latex.latex_newline().join([line_1, line_2, line_3, line_4, line_5])

    def sanity_check(self):

        # check the answer gives positive probabilities
        for value in self._question_params['prob_table'].values():
            if value.subs({k: self._question_params['answer']}) < 0:
                raise ValueError('This answer (the value of k) is giving negative values in the probability table.')

        quadratic = sum(self._question_params['prob_table'].values())

        for solution in self._question_params['quadratic_solutions']:
           if quadratic.subs({k: solution}) != 1:
               raise ValueError('One of the pre-determined solutions for the probability table is not giving a total probability of 1.')
