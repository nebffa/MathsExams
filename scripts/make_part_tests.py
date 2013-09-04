import os
import textwrap


parts_path = r'C:\Users\Ben\Desktop\Dropbox\maths\parts\\'
tests_path = r'C:\Users\Ben\Desktop\Dropbox\maths\parts\tests'


irrelevant_tests_files = ['__init__.py', 'question_tester.py']
irrelevant_parts_files = ['__init__.py']

test_files = [filename for filename in os.listdir(tests_path) if filename.endswith('py') and filename not in irrelevant_tests_files]
part_files = [filename for filename in os.listdir(parts_path) if filename.endswith('py') and filename not in irrelevant_parts_files]


for file_string in part_files:
    # slice [:-3] removes the '.py'
    test_filename = 'test_' + file_string
    test_class = file_string[:-3].title().replace('_', '')

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
                      question_tester(QuestionTree(1, q1))'''.format(file_string[:-3], test_class))

        f.write(test_content)



