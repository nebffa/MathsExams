import os
from setuptools import setup


setup(
    name="MathsExams",
    author="Ben Lucato",
    author_email="ben.lucato@gmail.com",
    description="Create maths questions for students to practice with",
    url="https://github.com/nebffa/MathsExams",
    packages=[
        'maths',
        'maths.api',
        'maths.debug',
        'maths.exams',
        'maths.latex',
        'maths.phrasing',
        'maths.plot',
        'maths.probability',
        'maths.questions',
        'maths.relations',
        'maths.rich_requests',
        'maths.scripts',
        'maths.templates',
        'maths.tests',
        'maths.utils'
    ],
    install_requires=[
        "gmpy==1.17",
        "numpy==1.8.0",
        "matplotlib==1.3.1",
        "pytest==2.5.2",
        "sympy==0.7.5"
    ]
)
