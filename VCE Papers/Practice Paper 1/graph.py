from mpl_toolkits.axes_grid.axislines import SubplotZero
from matplotlib.transforms import BlendedGenericTransform
import matplotlib.pyplot as plt
import numpy

if 1:
    fig = plt.figure(1)
    ax = SubplotZero(fig, 111)
    fig.add_subplot(ax)

    ax.axhline(linewidth=1.7, color="black")
    ax.axvline(linewidth=1.7, color="black")

    plt.xticks([1])
    plt.yticks([])

    ax.text(0, 1.05, 'y', transform=BlendedGenericTransform(ax.transData, ax.transAxes), ha='center')
    ax.text(1.05, 0, 'x', transform=BlendedGenericTransform(ax.transAxes, ax.transData), va='center')

    for direction in ["xzero", "yzero"]:
        ax.axis[direction].set_axisline_style("-|>")
        ax.axis[direction].set_visible(True)

    for direction in ["left", "right", "bottom", "top"]:
        ax.axis[direction].set_visible(False)

    x = numpy.linspace(-0.5, 1., 1000)
    ax.plot(x, numpy.sin(x*numpy.pi), linewidth=1.2, color="black")
    #plt.plot([0, 0.5], [0.5, 0.5], 'k--')
    #plt.arrow(0, 1, 0, 0.1, shape='full', lw=1.7, length_includes_head=True, head_width=.01)

    plt.show()
