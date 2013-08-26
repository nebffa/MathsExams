from maths.symbols import *
from sympy import latex


def probability_table(prob_table):

    try:
        values = ' & '.join([latex(float(value)) for value in prob_table.itervalues()])
    except:
        values = ' & '.join([r'${0}$'.format(latex(value.together())) for value in prob_table.itervalues()])

    return r'''
        \begin{{tabularx}}{{\textwidth}}{{ {0} }}
            \hline
            {1} & {2} \\
            \hline
            {3} & {4} \\
            \hline
        \end{{tabularx}}'''.format('|' + 'X|' * (len(prob_table) + 1),
                                    'x',
                                    ' & '.join([latex(key) for key in prob_table.keys()]),
                                    r'Pr(X = $x_{i}$)',
                                    values
                                )
