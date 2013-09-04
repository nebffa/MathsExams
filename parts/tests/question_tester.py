from maths.latex import latex
import uuid
import os
import subprocess
import errno


def question_tester(question_tree):
    """ Test whether a question's latex is compilable to a PDF.

    """ 

    full_path = r'C:\Users\Ben\Desktop\Dropbox\maths\parts\tests'
    uid = str(uuid.uuid1())

    file_name = os.path.join(full_path, 'test' + uid + '.tex')

    with open(file_name, 'w') as f:
        _write_question(f, question_tree)


    # change dir to C:\Users\Ben\Desktop\Dropbox\maths\parts\tests so that the byproduct tex compilation files are created there
    # in case something goes wrong in compilation and we want to view them
    prev_path = os.getcwd()
    os.chdir(full_path)
    retcode = subprocess.call(['xelatex', '-halt-on-error', file_name])
    if retcode != 0:
        raise RuntimeError("This questions' latex could not be compiled.")


    # cleanup after .tex compilation
    silentremove(os.path.join(full_path, 'test' + uid + '.log'))
    silentremove(os.path.join(full_path, 'test' + uid + '.aux'))
    #silentremove(os.path.join(full_path, 'test' + uid + '.pdf'))
    silentremove(os.path.join(full_path, 'test' + uid + '.tex'))

    os.chdir(prev_path)


def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError as e:" in python 3.x
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occured


def _write_question(f, question_tree):
    """ A helper function to test_question - writes a single question as a standalone .tex file.

    """

    #f.write('asdasfasfuhsafjo12313<1k23124$$$$$$')
    latex.begin_tex_document(f)
    question_tree.write_question(f)
    question_tree.write_solution(f)
    latex.end_tex_document(f)


def to_string(lines):
    for i in range(len(lines)):
        if i != len(lines) - 1:
            lines[i] += latex.latex_newline()

    return ''.join(lines)
