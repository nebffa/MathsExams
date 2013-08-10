import os, errno
from subprocess import call


def silentremove(filename):
    try:
        os.remove(filename)
    except OSError, e: # this would be "except OSError as e:" in python 3.x
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occured


def make_pdf(tex_filename):
    """ Convert a .tex file to a .pdf file, removing the .tex and other intermediates in the process.
    """

    dirname = os.path.dirname(os.path.abspath(tex_filename + '.tex'))
    full_path = os.path.join(dirname, tex_filename + '.tex')
    print dirname
    print full_path

    call(['pdftex', '-halt-on-error', full_path])
    
    # calling pdftex seems to produce different intermediate files than pdflatex
    #silentremove(os.path.join(dirname, tex_filename + '.aux'))
    silentremove(os.path.join(dirname, tex_filename + '.txt'))
    #silentremove(os.path.join(dirname, tex_filename + '.pdf'))
    silentremove(os.path.join(dirname, tex_filename + '.tex'))
    #silentremove(os.path.join(dirname, 'texput.txt'))
