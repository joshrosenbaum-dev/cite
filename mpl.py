import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
DEBUG_Y = 0
def plotPoints(points, mark_x, mark_y):
    global DEBUG_Y
    plt.clf()
    plt.suptitle(mark_x.label + " vs. " + mark_y.label)
    plt.xlabel(mark_x.label)
    plt.ylabel(mark_y.label)
    xc = []
    yc = []
    for p in points:
        xc.append(p[0])    
        yc.append(p[1])
        print(p)
    yc[-1] += DEBUG_Y
    plt.plot(xc, yc, 'bo')
    DEBUG_Y += 1.0