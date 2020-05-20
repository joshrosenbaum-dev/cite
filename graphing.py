#   graphing.py
#   -------------------------------------------------------
#   Point and point-plotting functions.

import matplotlib.pyplot as plt

def getPoint(xFrame, yFrame, popFrame, artifact, year):
    year = "2002"
    x = xFrame[year].loc[artifact.markerLabel]
    y = yFrame[year].loc[artifact.markerLabel]
    popSize = popFrame[year].loc[artifact.markerLabel]
    point = [x, y, popSize, artifact]
    return point

def plotPoints(points, label_x, label_y):      
    plt.clf()
    
    if label_x == None or label_y == None:
        plt.suptitle("Please place markers on the table to display a graph!")
    else:
        plt.suptitle(label_x + " vs. " + label_y)

    plt.xlabel(label_x)
    plt.ylabel(label_y)
    xCoords = []
    yCoords = []
    sizeList = []
    colors = []

    for p in points:
        x = p[0]
        y = p[1]
        popSize = p[2]
        artifact = p[3]
        xCoords.append(x)    
        yCoords.append(y)
        sizeList.append(popSize / 100000)
        colors.append(artifact.artifactColor)
        plt.annotate(artifact.artifactAbbr.upper(), (x, y))

    plt.scatter(xCoords, yCoords, sizeList, colors)