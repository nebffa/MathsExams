import sympy
import random
from sympy.abc import *
from maths import not_named_yet
from latex.table import probability_table


class ProbTableKnown(object):
    def __init__(self):
        self.num_lines = 0
        self.num_marks = 0

        options = range(random.randint(4, 5))

        partition = random.choice([i for i in not_named_yet.partition(10) if len(i) == len(options)])
        partition = list(partition)
        print partition
        random.shuffle(partition)
        print partition
        partition = [i * 0.1 for i in partition]


        self.prob_table = dict(zip(options, partition))

    def write_question(self):
        table = probability_table(self.prob_table)

    def write_solution(self):
        return ''

