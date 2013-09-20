import sympy
import numpy
from maths.symbols import *

from matplotlib.transforms import BlendedGenericTransform
from mpl_toolkits.axes_grid.axislines import SubplotZero
import matplotlib.pyplot as plt

import re
import uuid
import os


def f7(seq):
    # removes repeating items in lists, preserving order
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]


def get_undefined_points(expr):
    match = expr.match(x0 / (x1 * x + x2) + x3)
    print(expr)
    print(match)
    if match is not None:
        return -match[x2] / match[x1]


def numpify(expr):
    ''' 
    Takes a sympy expression and returns a numpy expression that accepts a darray "x_values".
    '''

    numpified = re.sub(r'(tan|cos|sin|sec|csc|cot|exp|log)', r'numpy.\1', repr(expr))
    numpified = re.sub(r'Abs', r'numpy.abs', numpified)
    return re.sub(r'x', r'x_values', numpified)


def asymptote_proof(array):
    ''' 
    Takes a numpy.ndarray and asymptote-proofs the values so we don't plot over asymptotes.
    '''
    
    threshold = 1000
    array[array > threshold] = numpy.inf
    array[array < -threshold] = numpy.inf

    return array


def latex(path):
    '''
    Return the latex to include an Encapsulated PostScript (.eps) file as an image.
    '''

    relative_path = os.path.relpath(path)
    latex_friendly_path = relative_path.replace('\\', '/')

    return r'''\\ \includegraphics[scale=0.5]{{{0}}} \\'''.format(latex_friendly_path.strip('.eps'))


def _blank_plot(domain):
    # make the plot
    fig = plt.figure(1)
    ax = SubplotZero(fig, 111)
    fig.add_subplot(ax)

    # thicken the axis lines
    ax.axhline(linewidth=1.7, color="k")
    ax.axvline(linewidth=1.7, color="k")

    x_lower, x_upper = int(domain.left), int(domain.right)  # needs to be changed, is just a temporary type changer
    y_lower, y_upper = -5, 5

    # remove tick lines on the axes
    plt.xticks([])
    plt.yticks([])
    plt.ylim(y_lower, y_upper)
    plt.xlim(x_lower, x_upper)

    # add axes labels
    ax.text(1.05, 0, r'$x$', transform=BlendedGenericTransform(ax.transAxes, ax.transData), va='center')
    ax.text(0, 1.05, r'$y$', transform=BlendedGenericTransform(ax.transData, ax.transAxes), ha='center')

    # end-of-axis arrows
    x_width = (abs(plt.xlim()[0]) + abs(plt.xlim()[1]))
    y_width = (abs(plt.ylim()[0]) + abs(plt.ylim()[1]))
    plt.arrow(plt.xlim()[1], -0.003, 0.00000000001, 0,
              width=x_width*0.0015*0.5, color="k", clip_on=False,
              head_width=y_width*0.12/7, head_length=x_width*0.024*0.5)
    plt.arrow(0.003, plt.ylim()[1], 0, 0.00000000001,
              width=y_width*0.0015*0.5, color="k", clip_on=False,
              head_width=x_width*0.12/7, head_length=y_width*0.024*0.5)

    # only show cartesian axes
    for direction in ["xzero", "yzero"]:
        ax.axis[direction].set_visible(True)
    for direction in ["left", "right", "bottom", "top"]:
        ax.axis[direction].set_visible(False)


def _save_plot():
    # save the image and return the path name so the caller can include it in the latex
    uid = uuid.uuid1()
    path = os.path.join(r'C:\Users\Ben\Desktop\Dropbox\maths\questions\figures', str(uid) + '.eps')
    plt.savefig(path)

    return path


def blank_plot(domain):
    _blank_plot(domain)
    path = _save_plot()

    return path



def plot(expr, plot_domain, expr_domain=None):
    if len(expr.atoms(sympy.Symbol)) != 1:
        raise ValueError(r'The supplied expression, {0}, must rely on only one symbol.'.format(expr))
    else:
        # ensure we are just plotting y against x for simplicity. We will label axes according to the original symbols though
        expr = expr.replace(expr.atoms(sympy.Symbol).pop(), x)

    if plot_domain.left == -sympy.oo or plot_domain.right == sympy.oo:
        raise ValueError('The supplied plot_domain goes to infinity: {0}'.format(plot_domain))

    if expr_domain is None:
        expr_domain = plot_domain
    elif expr_domain.left == -sympy.oo or expr_domain.right == sympy.oo:
        raise ValueError('The supplied expr_domain goes to infinity: {0}'.format(plot_domain))


    _blank_plot(plot_domain)    


    # plot each part of a piecewise individually    
    if isinstance(expr, sympy.Piecewise):

        # get a list of the ends of domains for the piecewise parts
        domains = [numpy.float64( i[1].rhs ) for i in expr.args]
        domains.insert(0, expr_domain.left)
        domains.append(expr_domain.right)
        domains = f7(domains)

        for i in range(len(expr.args)):
            numpified = numpify( expr.args[i][0] )
            
            x_values = numpy.linspace(domains[i], domains[i + 1], num=2000)
            #undefined_points = get_undefined_points(expr.args[i][0])
            #undefined_indices = numpy.where(x_values == undefined_points)
            #x_values = numpy.delete(undefined_indices)
            
            y_values = eval(r'{0}'.format(numpified))
            y_values = asymptote_proof(y_values)
    
            plt.plot(x_values, y_values, color="k")

    else:
        numpified = numpify(expr)

        x_values = numpy.linspace(expr_domain.left, expr_domain.right, num=2000)

        y_values = eval(r'{0}'.format(numpified))
        y_values = asymptote_proof(y_values)

        plt.plot(x_values, y_values, color="k")

    path = _save_plot()
    return path
