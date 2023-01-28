import functions as f
import pandas as pd


def main(gdp_path, population_path, co2_path, start, end):
    # reading csv files
    # files gdp and population had comments in first 4 rows, so we need to skip these rows
    gdp = f.clean(pd.read_csv(gdp_path, skiprows=4))
    population = f.clean(pd.read_csv(population_path, skiprows=4))
    co2 = f.clean(pd.read_csv(co2_path))
    # return years for which the analysis will be conducted
    years = f.years(gdp, population, co2)
    # if some years were specified in the command line
    if ((start is not None) | (end is not None)):
        years = f.cut_years(years, start, end)
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
    # parsing arguments from command line
    arguments = f.parse_arguments()
    # main function
    main(arguments.gdp, arguments.population, arguments.co2, arguments.start, arguments.end)
