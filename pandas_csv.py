import pandas as pd

def getPoint(xFrame, yFrame, popFrame, artifact):
    # TODO: Make year not constant.
    year = "2002"
    x = xFrame[year].loc[artifact.label]
    y = yFrame[year].loc[artifact.label]
    popSize = popFrame[year].loc[artifact.label]
    point = [x, y, popSize, artifact.abbr]
    return point