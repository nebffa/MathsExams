import pickle
import os
import random


def full_path():
    return os.getcwd()


def read_names():
    dirname = os.path.split(__file__)[0]
    path = os.path.join(dirname, 'first_names.pickle')

    with open(path, 'rb') as f:
        return pickle.load(f)


def random_name():
    return random.choice(read_names())
