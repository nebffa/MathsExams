import os
from setuptools import setup
from pip.req import parse_requirements


install_requirements = parse_requirements('requirements.txt')
requirements = [str(install_requirement.requirement) for install_requirement in install_requirements]


setup(
    name="MathsExams",
    author="Ben Lucato",
    author_email="ben.lucato@gmail.com",
    description="Create maths questions for students to practice with",
    url="https://github.com/nebffa/MathsExams",
    packages=["maths"],
    install_requires=requirements
)