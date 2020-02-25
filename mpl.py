import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def plotPoints(points, mark_x, mark_y):
    # TODO: Why don't my points show up???
    for p in points:
        plt.plot(p[0], p[1])
    plt.suptitle("CITE Matplotlib Test")
    plt.xlabel(mark_x.label)
    plt.ylabel(mark_y.label)
    plt.show()