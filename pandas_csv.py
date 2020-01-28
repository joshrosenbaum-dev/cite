import pandas as pd
    # install: python pip pandas

x_file = "csv/income.csv"
y_file = "csv/life_expectancy.csv"
    # We would use the <self.file> attribute of the marker to get 
    # this data from the X bucket's marker and Y bucket's marker, respectively.
year = "2018"
country = "United States"
x = pd.read_csv(x_file, index_col = "country")[year].loc[country]
y = pd.read_csv(y_file, index_col = "country")[year].loc[country]
    # https://stackoverflow.com/questions/20107570/removing-index-column-in-pandas-when-reading-a-csv
    # https://brohrer.github.io/dataframe_indexing.html
pair = [x, y]
print(pair)
