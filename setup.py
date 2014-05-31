import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="MathsExams",
    author="Ben Lucato",
    author_email="ben.lucato@gmail.com",
    description="Create maths questions for students to practice with",
    url="https://github.com/nebffa/MathsExams",
    packages=["maths"],
    long_description=read('README')
)