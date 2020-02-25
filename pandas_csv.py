import pandas as pd
def get_plot(mark_x, mark_y, mark_c):
    #TODO: Make not constant
    year = "2018"
    x = pd.read_csv(mark_x.file, index_col = "country")[year].loc[mark_c.label]
    y = pd.read_csv(mark_y.file, index_col = "country")[year].loc[mark_c.label]
        # https://stackoverflow.com/questions/20107570/removing-index-column-in-pandas-when-reading-a-csv
        # https://brohrer.github.io/dataframe_indexing.html
    pair = [x, y, mark_c.label]
    return pair