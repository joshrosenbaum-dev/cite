#   graphing.py
#   -------------------------------------------------------
#   Point and point-plotting functions.

#   TODO: Remove labels and create graph key instead.
#   Currently, the labels are made illegible by darker
#   colors.

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
        plt.annotate(artifact.artifactAbbr.upper(), (x, y))

    plt.scatter(xCoords, yCoords, sizeList, colors)