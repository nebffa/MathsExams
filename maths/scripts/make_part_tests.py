import os
import textwrap


def create_tests():
    """Creates a new test for every question that doesn't have one.
    """

    maths_path = os.path.split(os.getcwd())[0]
    questions_path = os.path.join(maths_path, 'questions')
    tests_path = os.path.join(maths_path, 'questions', 'tests')

    irrelevant_tests_files = ['__init__.py', 'question_tester.py']
    irrelevant_parts_files = ['__init__.py', 'relationships.py']

    test_files = [filename for filename in os.listdir(tests_path) if filename.endswith('py') and filename not in irrelevant_tests_files]
    question_files = [filename for filename in os.listdir(questions_path) if filename.endswith('py') and filename not in irrelevant_parts_files]

    for question_file in question_files:
        module_name = os.path.splitext(question_file)[0]
        test_filename = 'test_' + question_file

        if test_filename in test_files:
            continue

        new_testfile_path = os.path.join(tests_path, test_filename)

        with open(new_testfile_path, 'w') as f:
            test_content = textwrap.dedent('''\
                from .. import relationships, {module_name}
                from .question_tester import question_tester


                def test_{module_name}():
                    question = relationships.parse_structure({module_name})
                    question_tester(question)'''.format(module_name=module_name)
            )

            f.write(test_content)


if __name__ == '__main__':
    create_tests()
