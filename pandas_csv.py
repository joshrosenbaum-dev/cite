import pandas as pd

def getPoint(xFrame, yFrame, artifactLabel):
    # TODO: Make year not constant.
    year = "2002"
    x = xFrame[year].loc[artifactLabel]
    y = yFrame[year].loc[artifactLabel]
    point = [x, y, artifactLabel]
    return point