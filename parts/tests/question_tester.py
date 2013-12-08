from maths.latex import latex
import uuid
import os
import subprocess
import errno
from maths import maths_path
import glob


def question_tester(questions, view_output=False):
    """ Test whether a question's latex is compilable to a PDF.

    """ 

    #full_path = os.path.split(os.path.abspath(__file__))[0]
    full_path = os.path.join(maths_path.maths_path(), 'debug')
    uid = str(uuid.uuid1())

    file_name = os.path.join(full_path, 'test' + uid + '.tex')

    with open(file_name, 'w') as f:
        latex.begin_tex_document(f)
        if isinstance(questions, (list, tuple)):
            for question in questions:
                _write_question(f, question)
                latex.new_page(f)
        else:
            _write_question(f, questions)
        latex.end_tex_document(f)


    # change dir to ../maths/debug so that the byproduct tex compilation files are created there
    # in case something goes wrong in compilation and we want to view them
    prev_path = os.getcwd()
    os.chdir(full_path)
    
    with open(os.devnull, 'w') as f:
        retcode = subprocess.call(['xelatex', '-halt-on-error', file_name], stdout=f)

    if retcode != 0:
        # wipe all other files in ../maths/debug so we can easily find the files we want

        keep_files = [os.path.join(full_path, 'test' + uid + i) for i in ['.log', '.aux', '.tex']]

        for filename in glob.glob(os.path.join(full_path, '*')):
            if filename not in keep_files:
                os.remove(filename)

        subprocess.Popen(['texmaker', os.path.join(full_path, 'test' + uid + '.tex')])

        raise RuntimeError("This questions' latex could not be compiled.")



    if view_output:
        subprocess.call(['evince', os.path.join(full_path, 'test' + uid + '.pdf')])
        # if retcode != 0:
        #     pass
            #subprocess.call([''])

    # cleanup after .tex compilation
    silentremove(os.path.join(full_path, 'test' + uid + '.log'))
    silentremove(os.path.join(full_path, 'test' + uid + '.aux'))
    silentremove(os.path.join(full_path, 'test' + uid + '.tex'))

    os.chdir(prev_path)


def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occured


def _write_question(f, question):
    """ A helper function to test_question - writes a single question as a standalone .tex file.
    """
    question.write_question(f)
    question.write_solution(f)
