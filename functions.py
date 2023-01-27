import argparse
import pandas as pd
import numpy as np

#parsing arguments (paths to csv files) from command line
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("gdp", help="path to csv file with gdp data")
    parser.add_argument("population", help="path to csv file with population data")
    parser.add_argument("co2", help="path to file with co2 emission data")
    arguments = parser.parse_args()
    return arguments

def clean(data):
    if 'Country Name' in data.columns:
        data = data.rename(columns = {'Country Name':'Country'})
        data['Country'] = data['Country'].str.upper()
        data = data.iloc[:,:-1]
    return data


#returning years that are included in all three files
def years(gdp, population, co2):
    years_co2 = co2['Year'].drop_duplicates()
    years_gdp = pd.DataFrame({'Year':list(gdp.columns[4:-1])})
    years_gdp = years_gdp['Year'].astype('int')
    years_population = pd.DataFrame({'Year':list(population.columns[4:-1])})
    years_population = years_population['Year'].astype('int')
    years = pd.merge(years_co2, years_gdp, how = 'inner')
    years = pd.merge(years, years_population, how = 'inner')
    years = (years['Year'])
    return years

#merging data on years and countries
def merge_data(gdp, population, co2, years):
    #only look at co2 data for years that show up in all csv files
    data = co2[co2['Year'].isin(years)]
    #create data frame with gdp data such that one row contains data about gdp in one country for a specific year (format closer to co2 data)
    gdp_split = pd.DataFrame(columns = gdp.columns[0:4])
    gdp_one_year = gdp.iloc[:,0:4]
    gdp_one_year['GDP'] = np.nan
    for year in years:
        gdp_one_year['Year'] = [year] * len(gdp)
        gdp_one_year['GDP'] = gdp[str(year)]
        gdp_split = gdp_split.append(gdp_one_year)
    #merge co2 data with gdp data in a new format
    data = data.merge(gdp_split, on = ['Country', 'Year'], how = 'outer')
    #create data frame with population data such that one row contains data about population in one country for a specific year (format closer to co2 data)
    pop_split = pd.DataFrame(columns=population.columns[0:4])
    pop_one_year = population.iloc[:, 0:4]
    pop_one_year['Population'] = np.nan
    for year in years:
        pop_one_year['Year'] = [year] * len(population)
        pop_one_year['Population'] = population[str(year)]
        pop_split = pop_split.append(pop_one_year)
    #merge data about co2, gdp and population in new format
    data = data.merge(pop_split, on=['Country', 'Year', 'Country Code'], how='outer')
    return data

