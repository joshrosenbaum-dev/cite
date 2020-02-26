import pandas as pd

def getPoint2(mark_x, mark_y, mark_c):
    #TODO: Make not constant
    year = "2018"
    x = pd.read_csv(mark_x.file, index_col = "country")[year].loc[mark_c.label]
    y = pd.read_csv(mark_y.file, index_col = "country")[year].loc[mark_c.label]
        # https://stackoverflow.com/questions/20107570/removing-index-column-in-pandas-when-reading-a-csv
        # https://brohrer.github.io/dataframe_indexing.html
    point = [x, y, mark_c.label]
    return point

def getPoint(xFrame, yFrame, artifactLabel):
    # TODO: Make year not constant.
    year = "2018"
    x = xFrame[year].loc[artifactLabel]
    y = yFrame[year].loc[artifactLabel]
    point = [x, y, artifactLabel]
    return point