import sympy
import random
import pickle
from sympy.abc import *
from maths import not_named_yet
from latex.table import probability_table
from maths.names import first_names


class ProbTableKnown(object):
    def __init__(self):
        self.num_lines = 0
        self.num_marks = 0

        options = range(random.randint(4, 5))

        partition = random.choice([i for i in not_named_yet.partition(10) if len(i) == len(options)])
        partition = list(partition)

        random.shuffle(partition)
        partition = [i * 0.1 for i in partition]


        self.prob_table = dict(zip(options, partition))

    def write_question(self):
        self.name = random.choice(first_names.names)


        traffic_lights = '''When {0} drives to work each morning they pass a number of intersections with traffic lights. The number X of 
                            traffic lights that are green when {0} is driving to work is a random variable with probability distribution given by'''
        telephone_calls = '''Every thursday, the number X of telephone calls that {0} receives at work is a random variable with probability 
                            distribution given by'''
        marshmallows = '''Every tuesday, {0} goes to her local cafe for lunch and orders a hot chocolate. The number X of free marshmallows that are 
                            included with the hot chocolate is a random variable with probability distribution given by'''

        text = random.choice([traffic_lights, telephone_calls, marshmallows]).format(self.name)
        table = probability_table(self.prob_table)

        return text + table

    def write_solution(self):
        return ''


class Property():
    def __init__(self, part):
        assert isinstance(part, ProbTableKnown)
        
        self.question_type == random.choice(['mean', 'variance', 'mode'])
        self.prob_table = part.prob_table

        if self.question_type == 'mean':
            self.num_lines, self.marks = 4, 2

            self.answer = sum([k*v for k, v in self.prob_table.items()])
        elif self.question_type == 'variance':
            self.num_lines, self.marks = 7, 3

            expecation_x = sum([k*v for k, v in self.prob_table.items()])
            expectation_x_squared = sum([k**2*v for k, v in self.prob_table.items()])

            self.answer = expectation_x_squared - expecation_x**2
        elif self.question_type == 'mode':
            self.num_lines, self.marks = 2, 1
            self.answer = max(self.prob_table.iterkeys(), key=lambda key: self.prob_table[key])

    def write_question(self):
        if self.question_type == 'mean':
            return r'Find $E(X)$, the mean of X.'
        elif self.question_type == 'variance':
            return r'Find $Var(X)$, the mean of X.'
        elif self.question_type == 'mode':
            return r'Find the mode of X.'

    def write_solution(self):

            