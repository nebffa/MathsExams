import sys
import subprocess
import os
import importlib
from maths.questions import relationships
from maths.questions.tests import question_tester


if __name__ == '__main__':
    module_path = sys.argv[1]
    project_path = sys.argv[2]

    module_name = os.path.split(module_path)[1]
    module_name = os.path.splitext(module_name)[0]

    relative_path = os.path.relpath(module_path, __file__)
    relative_path = os.path.split(relative_path)[0]
    relative_path = relative_path.replace('..', '.')
    relative_path = relative_path.replace('/', '')

    script_name = os.path.relpath(module_path, project_path).replace('/', '.')[:-3]
    module = importlib.import_module(script_name)

    question = relationships.parse_structure(module)

    try:
        with open(os.devnull, 'w') as fnull:
            # raises EV_IS_DOCUMENT error due to a bug in evince, which is fixed in an upcoming version of evince
            # https://bugs.launchpad.net/ubuntu/+source/evince/+bug/1247208
            subprocess.call(['killall', 'evince'], stdout=fnull, stderr=fnull)
        question_tester.question_tester(question, view_output=True)
    except Exception as e:
        raise e
