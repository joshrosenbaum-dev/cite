#   graphing.py
#   -------------------------------------------------------
#   Point and point-plotting functions.

#   https://matplotlib.org/3.2.1/tutorials/text/annotations.html

import matplotlib.pyplot as plt

def getPoint(xFrame, yFrame, popFrame, artifact, year):
    x = xFrame[year].loc[artifact.markerLabel]
    y = yFrame[year].loc[artifact.markerLabel]
    popSize = popFrame[year].loc[artifact.markerLabel]
    point = [x, y, popSize, artifact]
    return point

def plotPoints(points, xLabel, yLabel, xRange, yRange, year):      
    plt.clf()
    
    if xLabel == None or yLabel == None:
        plt.suptitle("Please place markers on the table to display a graph!")
        plt.xlim(xmin = 0.0)
        plt.ylim(ymin = 0.0)
    else:
        plt.suptitle(xLabel + " vs. " + yLabel + " (" + year + ")")
    
    if xRange != None:
        plt.xlim(xRange)

    if yRange != None:
        plt.ylim(yRange)

    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
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
        plt.annotate(artifact.artifactAbbr.upper(), xy = (x - x/2, y - y/2), backgroundcolor = (1, 1, 1, 0.3))

    plt.scatter(xCoords, yCoords, sizeList, colors)