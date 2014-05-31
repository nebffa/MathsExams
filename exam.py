from maths.questions import relationships
from maths.latex import latex
from maths.api import api
import os


def generate_exam():
    """Generate an exam with multiple questions, with solutions for each question!

    It's quite simple for now.
    """

    cur_dir = os.path.split(__file__)[0]
    questions_dir = os.path.join(cur_dir, 'maths', 'questions')
    question_paths = api.get_question_paths(questions_dir)

    question_modules = api.import_question_modules(question_paths)

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
