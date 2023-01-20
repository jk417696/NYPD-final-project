import pandas as pd
import numpy as np
import argparse

def main(gdp_path, population_path, co2_path):
    gdp = pd.read_csv(gdp_path)
    population = pd.read_csv(population_path)
    co2 = pd.read_csv(co2_path)

#testowy komentarz
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("gdp", help="path to csv file with gdp data")
    parser.add_argument("population", help="path to csv file with population data")
    parser.add_argument("co2", help = "path to file with co2 emission data")
    arguments = parser.parse_args()
    return arguments

if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments.gdp, arguments.population, arguments.co2)
