#   graphing.py
#   -------------------------------------------------------
#   Point and point-plotting functions.

import matplotlib.pyplot as plt

def getPoint(xFrame, yFrame, popFrame, artifact, year):
    year = "2002"
    x = xFrame[year].loc[artifact.markerLabel]
    y = yFrame[year].loc[artifact.markerLabel]
    popSize = popFrame[year].loc[artifact.markerLabel]
    point = [x, y, popSize, artifact.artifactAbbr]
    return point

def plotPoints(points, label_x, label_y):      
    plt.clf()
    
    if label_x == None or label_y == None:
        plt.suptitle("Please place markers on the table to display a graph!")
    else:
        plt.suptitle(label_x + " vs. " + label_y)

    plt.xlabel(label_x)
    plt.ylabel(label_y)
    xc = []
    yc = []
    sl = []

    for p in points:
        xc.append(p[0])    
        yc.append(p[1])
        sl.append(p[2] / 100000)
        plt.annotate(p[3].upper(), (p[0], p[1]))

    plt.scatter(xc, yc, sl)