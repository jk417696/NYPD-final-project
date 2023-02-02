import functions as f
import pandas as pd


def main():
    # disable warnings about chained assignments
    pd.options.mode.chained_assignment = None
    # parse arguments from command line
    arguments = f.parse_arguments()
    # read csv files
    # files gdp and population had comments in first 4 rows, so we need to skip these rows
    gdp = f.clean(pd.read_csv(arguments.gdp, skiprows=4))
    population = f.clean(pd.read_csv(arguments.population, skiprows=4))
    co2 = f.clean(pd.read_csv(arguments.co2))
    # return years for which the analysis will be conducted
    years = f.years(gdp, population, co2)
    # if some years were specified in the command line
    if ((arguments.start is not None) | (arguments.end is not None)):
        years = f.cut_years(years, arguments.start, arguments.end)
        # if incorrect years were specified - show the warning and stop the program
        if not len(years):
            return 0
    # analyse the data
    data = f.merge_data(gdp, population, co2, years)
    change = f.emission_change(co2, max(years))
    worst_emitters = f.worst_emitters(co2, years)
    highest_gdp = f.highest_gdp(data, years)
    print('Top 5 co2 emitting countries for each year: \n',
          worst_emitters)
    print('Top 5 countries with the highest GDP per capita for each year: \n',
          highest_gdp)
    print('Country with the biggest increase in emission per capita from ', max(years)-10, ' to ', max(years),': \n',
          change.iloc[-1])
    print('Country with the biggest decrease in emission per capita from ', max(years)-10, ' to ', max(years),': \n',
          change.iloc[0])
    return 0

if __name__ == '__main__':
    # main function
    main()
