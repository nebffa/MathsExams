from maths.symbols import *
from sympy import latex


def probability_table(prob_table):

    return r'''
        \begin{{tabularx}}{{\textwidth}}{{ {0} }}
            \hline
            {1} \\
            \hline
            {2} \\
            \hline
        \end{{tabularx}}'''.format('|' + 'X|' * len(prob_table),
                                    ' & '.join([latex(option) for option in prob_table.keys()]),
                                    ' & '.join([latex(float(option)) for option in prob_table.values()])
                                )
