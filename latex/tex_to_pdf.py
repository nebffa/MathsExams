import os
from subprocess import call


def make_pdf(tex_filename):
    """ Convert a .tex file to a .pdf file, removing the .tex and other intermediates in the process.
    """

    call(['pdflatex -halt-on-error', tex_filename + '.tex'])
    
    # Remove intermediate files
    os.remove(tex_filename + '.tex')
    os.remove(tex_filename + '.aux')
    os.remove(tex_filename + '.log')
