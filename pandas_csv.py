import pandas as pd

def getPoint(xFrame, yFrame, popFrame, artifactLabel):
    # TODO: Make year not constant.
    year = "2002"
    x = xFrame[year].loc[artifactLabel]
    y = yFrame[year].loc[artifactLabel]
    popSize = popFrame[year].loc[artifactLabel]
    point = [x, y, popSize, artifactLabel]
    return point