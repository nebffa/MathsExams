import os
import textwrap




maths_path = os.path.split(os.getcwd())[0]
parts_path = os.path.join(maths_path, 'maths', 'parts')
tests_path = os.path.join(maths_path, 'maths', 'parts', 'tests')


irrelevant_tests_files = ['__init__.py', 'question_tester.py']
irrelevant_parts_files = ['__init__.py']

test_files = [filename for filename in os.listdir(tests_path) if filename.endswith('py') and filename not in irrelevant_tests_files]
part_files = [filename for filename in os.listdir(parts_path) if filename.endswith('py') and filename not in irrelevant_parts_files]


for file_string in part_files:
    test_filename = 'test_' + file_string


    stripped_extension = os.path.splitext(file_string)[0]
    test_class = stripped_extension.title().replace('_', '')

    if test_filename in test_files:
        continue

    full_path = os.path.join(tests_path, test_filename)
    with open(full_path, 'w') as f:
        test_content = textwrap.dedent('''\
                  from maths.parts import {0}
                  from maths.latex.questions import QuestionTree
                  from .question_tester import question_tester


                  def test_{1}():
                      q1 = {0}.{1}()
                      question_tester(QuestionTree(part=q1))'''.format(file_string[:-3], test_class))

        f.write(test_content)



