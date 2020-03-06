import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime as dt

# DEBUG_Y = 0

def plotPoints(points, label_x, label_y): #mark_x, mark_y):
    # print("Plotting points", dt.datetime.now())
    # global DEBUG_Y
    plt.clf()
    plt.suptitle(label_x + " vs. " + label_y)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    xc = []
    yc = []
    for p in points:
        xc.append(p[0])    
        yc.append(p[1])
        # print(p)
    # yc[-1] += DEBUG_Y
    plt.plot(xc, yc, 'bo')
    # DEBUG_Y += 1.0
    # print("\n")