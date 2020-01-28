import pandas as pd     # install: python pip pandas

x_file = "csv/income.csv"
y_file = "csv/life_expectancy.csv"
    # We would use the <self.file> attribute of the marker to get 
    # this data from the X bucket's marker and Y bucket's marker, respectively.
year = "2018"
country = "Afghanistan"

x = pd.read_csv(x_file)
y = pd.read_csv(y_file)
x_val = x[x.country == country][year][0]    # Sourced from: https://data36.com/pandas-tutorial-1-basics-reading-data-files-dataframes-data-selection/
y_val = y[y.country == country][year][0]

data_pair = [x_val, y_val]
print(data_pair)