from maths.symbols import *
from sympy import latex


def probability_table(prob_table):

    return r'''
    \begin{center}
        \begin{tabular}{ %s| p{5cm} |}
        x & %s \\ \hline
        Pr(X = x) & %s \\ \hline
        \hline
        \end{tabular}
    \end{center}''' % ((r'| l ' * len(prob_table)), 
                        ' & '.join([latex(option) for option in prob_table.keys()]),
                        ' & '.join([latex(option) for option in prob_table.values()])
                        )
