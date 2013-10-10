import pickle
import os
import random


def full_path():
    return os.getcwd()


def read_names(gender=False):
    ''' Return a list of first names, with their corresponding genders if gender is True
    '''
    dirname = os.path.split(__file__)[0]
    path = os.path.join(dirname, 'first_names.pickle')

    with open(path, 'rb') as f:
        if gender:
            return pickle.load(f)
        else:
            return [i[0] for i in pickle.load(f)]


def random_first_name(gender=False):
    ''' Return a random first name, including the gender if gender is True.
    '''
    if gender:
        return random.choice(read_names(gender))
    else:
        return random.choice(read_names(gender))[0]
