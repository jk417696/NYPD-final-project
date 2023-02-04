import argparse
import pandas as pd
import numpy as np


# parse arguments (paths to csv files and years to analyse) from command line
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('gdp', help='path to csv file with gdp data')
    parser.add_argument('population', help='path to csv file with population data')
    parser.add_argument('co2', help='path to file with co2 emission data')
    parser.add_argument('-start', type=int, default=None, help='start year for data analysis')
    parser.add_argument('-end', type=int, default=None, help='end year for data analysis')
    arguments = parser.parse_args()
    return arguments


# clean data
def clean(data):
    # change the format of country names such that it's the same in all csv files
    if 'Country Name' in data.columns:
        data = data.rename(columns={'Country Name': 'Country'})
        data['Country'] = data['Country'].str.upper()
    # remove columns with only NaN values
    data = data.dropna(axis=1, how='all')
    return data


# returns a list of years that are included in all three files
def years(gdp, population, co2):
    years_co2 = co2['Year'].drop_duplicates()
    years_gdp = pd.DataFrame({'Year': list(gdp.columns[4:])})
    years_gdp = years_gdp['Year'].astype('int64')
    years_population = pd.DataFrame({'Year': list(population.columns[4:])})
    years_population = years_population['Year'].astype('int64')
    years = pd.merge(years_co2, years_gdp, how='inner')
    years = pd.merge(years, years_population, how='inner')
    years = (years['Year'])
    return years


# cut years to those specified in the command line (if possible)
def cut_years(years, start, end):
    if start is None:
        start = min(years)
    if end is None:
        end = max(years)
    if start <= end:
        years = years[(years >= start) & (years <= end)].dropna()
        if len(years):
            return years
        else:
            print('Error: no data available for years ', start, ' to ', end)
            return []
    else:
        print('Error: start year higher than end year')
        return []


# merge data on years and countries
def merge_data(gdp, population, co2, years):
    # only look at co2 data for years that show up in all csv files
    data = co2[co2['Year'].isin(years)]
    # create data frame with gdp data such that
    # one row contains data about gdp in one country for a specific year
    # (format closer to co2 data)
    gdp_split = pd.DataFrame(columns=gdp.columns[0:4])
    gdp_one_year = gdp.iloc[:, 0:4]
    gdp_one_year['GDP'] = np.nan
    for year in years:
        gdp_one_year['Year'] = [year] * len(gdp)
        gdp_one_year['GDP'] = gdp[str(year)]
        gdp_split = pd.concat([gdp_split, gdp_one_year])
    # merge co2 data with gdp data in a new format
    data = data.merge(gdp_split, on=['Country', 'Year'], how='outer')
    # create data frame with population in the same format as above
    pop_split = pd.DataFrame(columns=population.columns[0:4])
    pop_one_year = population.iloc[:, 0:4]
    pop_one_year['Population'] = np.nan
    for year in years:
        pop_one_year['Year'] = [year] * len(population)
        pop_one_year['Population'] = population[str(year)]
        pop_split = pd.concat([pop_split, pop_one_year])
    # merge data about co2, gdp and population in new format
    data = data.merge(pop_split, on=['Country', 'Year', 'Country Code'], how='outer')
    data['Year'] = data['Year'].astype('int64')
    return data


# check how many countries have been lost while merging the data
def check_loss(gdp, population, co2, data):
    before = pd.concat([gdp['Country'], population['Country'], co2['Country']]).drop_duplicates()
    after = data['Country'].drop_duplicates()
    countries_lost = before[-(before.isin(after))]
    print('Warning: merge function lost ', (1 - (len(after)/len(before)))*100, '% of all countries')
    print('Countries not included in merged data: \n', countries_lost)
    return countries_lost


# returns a table with 5 most emitting countries (per capita) for all years
# all the information needed is in co2 data therefore we only put this file as an argument
def worst_emitters(co2, years):
    # include only columns of interest
    df = co2[['Year', 'Country', 'Total', 'Per Capita']]
    # create empty data frame for the results
    emitters = pd.DataFrame(columns=['Year', 'Country', 'Total', 'Per Capita'])
    # for each year find top 5 emitting countries (per capita) and add them to emitters data frame
    for year in years:
        df_temp = df[df['Year'] == year]
        df_temp = df_temp.sort_values(by=['Per Capita'], ascending=False)
        emitters = pd.concat([emitters, df_temp.head(5)])
    return emitters


# returns a table with 5 countries with the highest gdp per capita in each year
# as an argument we put the merged data
def highest_gdp(data, years):
    # include only columns of interest
    df = data[['Year', 'Country', 'GDP', 'Population']]
    # create empty data frame for the results
    richest = pd.DataFrame(columns=['Year', 'Country', 'GDP', 'Population', 'Per Capita'])
    # for each year find top 5 countries with the highest gdp per capita and add them to the richest data frame
    for year in years:
        df_temp = df[df['Year'] == year]
        df_temp['Per Capita'] = df_temp['GDP'] / df_temp['Population']
        # sort the values and find top 5
        df_temp = df_temp.sort_values(by=['Per Capita'], ascending=False)
        richest = pd.concat([richest, df_temp.head(5)])
    # drop  column population since we don't need it in our results
    richest = richest.drop(columns=['Population'])
    return richest


# returns a change in co2 emission in the last 10 years for each country
def emission_change(co2, year):
    # include only columns of interest
    df = co2[['Year', 'Country', 'Per Capita']]
    # find emission in the last years and 10 years prior
    emission_now = df[df['Year'].isin([year])]
    emission_then = df[df['Year'].isin([year - 10])]
    change = emission_now.merge(emission_then, on=['Country'])
    # calculate the change in emission per capita
    change['Change'] = change['Per Capita_x'] - change['Per Capita_y']
    # sort the values+
    change = change[['Country', 'Change']].sort_values(by=['Change'])
    return change
