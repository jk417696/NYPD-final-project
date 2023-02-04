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
    # return years that appear in all files
    years = f.years(gdp, population, co2)
    # cut the years of analysis if some were specified in the command line
    if (arguments.start is not None) | (arguments.end is not None):
        years = f.cut_years(years, arguments.start, arguments.end)
        # if incorrect years were specified - show the warning and stop the program
        if not len(years):
            return 0
    # analyse the data
    data = f.merge_data(gdp, population, co2, years)
    f.check_loss(gdp, population, co2, data)
    change = f.emission_change(co2, years)
    worst_emitters = f.worst_emitters(co2, years)
    highest_gdp = f.highest_gdp(data, years)
    # print results
    print('Top 5 co2 emitting countries for each year: \n',
          worst_emitters)
    print('Top 5 countries with the highest GDP per capita for each year: \n',
          highest_gdp)
    # show countries with the biggest change in emission only if there are at least two years in the data
    if len(years) < 2:
        print('Time interval too short: no change in emission observed')
    else:
        print('Country with  the biggest increase in emission per capita from ', change[2], ' to ', change[1], ': \n',
              change[0].iloc[-1])
        print('Country with the biggest decrease in emission per capita from ', change[2], ' to ', change[1], ': \n',
              change[0].iloc[0])
    # create csv files with output dataframes for easier reading
    data.to_csv('data_merged.csv')
    worst_emitters.to_csv('worst_emitter.csv')
    highest_gdp.to_csv('highest_gdp.csv')
    return 0


if __name__ == '__main__':
    main()
