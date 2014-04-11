import os
import inspect


def maths_path():
    return os.path.abspath(os.path.split(__file__)[0])
