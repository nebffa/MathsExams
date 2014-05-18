from maths.questions import relationships
from maths.latex import latex
import glob
import os
import importlib


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

        package = os.path.split(relative_path)[0].replace('/', '.')
        module_name = os.path.splitext(os.path.split(relative_path)[1])[0]

        imported_module = importlib.import_module('.' + module_name, package=package)

        if hasattr(imported_module, 'question_not_complete'):
            continue

        question_modules.append(imported_module)

    return question_modules


def generate_exam():
    """Generate an exam with multiple questions, with solutions for each question!

    It's quite simple for now.
    """

    cur_dir = os.path.split(__file__)[0]
    questions_dir = os.path.join(cur_dir, 'maths', 'questions')
    question_paths = get_question_paths(questions_dir)

    question_modules = import_question_modules(question_paths)

    with open('exam.tex', 'w') as exam_file:
        latex.begin_tex_document(exam_file)

        for question in question_modules:
            possible_questions = relationships.parse_structure(question)

            for i in possible_questions:
                i.write_question(exam_file)

                latex.decrement_question_counter(exam_file)

                i.write_solution(exam_file)
                latex.new_page(exam_file)

        latex.end_tex_document(exam_file)


if __name__ == '__main__':
    generate_exam()
