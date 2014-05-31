import sys
import os


cur_dir = os.path.split(os.path.abspath(__file__))[0]
parent_dir = os.path.split(os.path.abspath(cur_dir))[0]
grandparent_dir = os.path.split(os.path.abspath(parent_dir))[0]
questions_dir = os.path.join(parent_dir, 'questions')
sys.path.append(grandparent_dir)


from maths.questions import relationships
import glob
import importlib
import random



def get_questions_dir():
    """Return the directory that houses the questions.
    """

    relationships_path = os.path.abspath(relationships.__file__)
    return os.path.split(relationships_path)[0]


def get_question_paths(questions_dir):
    """Get all the module paths that have questions in them.
    """

    pattern = os.path.join(questions_dir, r'*.py')

    module_paths = glob.glob(pattern)

    non_question_modules = ['__init__.py', 'relationships.py']

    question_modules = []
    for module_path in module_paths:
        module_name = os.path.split(module_path)[1]

        if module_name not in non_question_modules:
            question_modules.append(module_path)

    return question_modules


def import_question_modules(question_paths):
    """Import and return a list of imported question modules.
    """

    question_modules = []

    for question_path in question_paths:
        relative_path = os.path.relpath(question_path)
        module_name = os.path.splitext(os.path.split(relative_path)[1])[0]

        imported_module = importlib.import_module('.' + module_name, package='maths.questions')

        if hasattr(imported_module, 'question_not_complete'):
            continue

        question_modules.append(imported_module)

    return question_modules


def random_question():
    """Serve a random question along with its solution.
    """

    questions_dir = get_questions_dir()
    question_paths = get_question_paths(questions_dir)
    question_modules = import_question_modules(question_paths)

    choice = random.choice(question_modules)
    built_question = relationships.parse_structure(choice)[0]

    return built_question.question_statement(), built_question.solution_statement()
