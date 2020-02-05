import pandas as pd
    # install: pip install pandas
def get_plot(mark_x, mark_y, mark_c):
    year = "2018"
    x = pd.read_csv(mark_x.file, index_col = "country")[year].loc[mark_c.country]
    y = pd.read_csv(mark_y.file, index_col = "country")[year].loc[mark_c.country]
        # https://stackoverflow.com/questions/20107570/removing-index-column-in-pandas-when-reading-a-csv
        # https://brohrer.github.io/dataframe_indexing.html
    pair = [x, y, mark_c.country]
    return pair