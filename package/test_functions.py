import unittest
import pytest
from package import functions
import pandas as pd


# dataframes for testing
df1 = pd.DataFrame(columns = ['Year','Country','Total','Solid Fuel','Liquid Fuel','Gas Fuel','Cement','Gas Flaring',
                               'Per Capita', 'Bunker fuels (Not in Total)', 'Country Code','Indicator Name_x',
                               'Indicator Code_x','GDP', 'Indicator Name_y','Indicator Code_y','Population'],
                   data = [[1960, 'AFGHANISTAN', 113.0, 35.0, 74.0, 0.0, 5.0, 0.0, 0.01, 0.0, 'AFG', 'GDP (current US$)',
                             'NY.GDP.MKTP.CD', 537777811.111111, "Population, total", 'SP.POP.TOTL', 8996967.0],
                            [1960, 'ALBANIA', 552.0, 89.0, 430.0, 23.0, 10.0, 0.0, 0.34, 0.0, 'ALB', 'GDP (current US$)',
                             'NY.GDP.MKTP.CD', 6000004209.23459, "Population, total", 'SP.POP.TOTL', 1608800.0]]
                   )

df2 = pd.DataFrame(columns = ['Year', 'Country' , 'GDP', 'Per Capita'],
                   data = [[1960, 'ALBANIA', 6000004209.23459, 3729.4904333879845],
                           [1960, 'AFGHANISTAN', 537777811.111111, 59.773233703214764]],
                   index = [1,0])


df3 = pd.DataFrame(columns = ['Year','Country','Total','Solid Fuel','Liquid Fuel','Gas Fuel','Cement','Gas Flaring',
                               'Per Capita', 'Bunker fuels (Not in Total)', 'Country Code','Indicator Name_x',
                               'Indicator Code_x','GDP', 'Indicator Name_y','Indicator Code_y','Population'],
                   data = [[2005, 'SWITZERLAND', 11273.0, 150.0, 8838.0, 1738.0, 547.0, 0.0, 1.51, 988.0, 'CHE',
                            'GDP (current US$)', 'NY.GDP.MKTP.CD', 420544947799.55, "Population, total", 'SP.POP.TOTL',
                            7437115.0],
                           [2005, 'POLAND', 82503.0, 57585.0, 15549.0, 7641.0, 1720.0, 7.0, 2.16, 546.0, 'POL',
                            'GDP (current US$)', 'NY.GDP.MKTP.CD', 306144336269.51, "Population, total", 'SP.POP.TOTL',
                            38165445.0]])

df4 = pd.DataFrame(columns = ['Year', 'Country' , 'GDP', 'Per Capita'],
                   data = [[2005, 'SWITZERLAND', 420544947799.55, 56546.78565539863],
                           [2005, 'POLAND', 306144336269.51, 8021.505743467947]]
                   )

df5 = pd.DataFrame(columns = ['Year','Country','Total','Solid Fuel','Liquid Fuel','Gas Fuel','Cement',
                              'Gas Flaring', 'Per Capita', 'Bunker fuels (Not in Total)'],
                   data = [[2000,'AFGHANISTAN',211,1,136,61,7,6,0.01,4],
                           [2000,'ALBANIA',824,19,776,6,24,0,0.27,34],
                           [2000,'ALGERIA',23960,537,8424,10838,1129,3032,0.78,416]])


df6 = pd.DataFrame(columns = ['Year', 'Country', 'Total', 'Per Capita'],
                   data = [[2000, 'ALGERIA', 23960, 0.78],
                           [2000, 'ALBANIA', 824, 0.27],
                           [2000, 'AFGHANISTAN', 211, 0.01]],
                   index = [2,1,0])

df7 = pd.DataFrame(columns = ['Year','Country','Total','Solid Fuel','Liquid Fuel','Gas Fuel','Cement',
                              'Gas Flaring', 'Per Capita', 'Bunker fuels (Not in Total)'],
                   data = [[1979, 'SWEDEN', 23160, 1877, 20958, 0, 325, 0, 2.79, 914],
                           [1979, 'NORWAY', 9338, 1001, 7438, 442, 299, 158, 2.29, 313],
                           [1978, 'FINLAND', 14157, 4199, 9216, 510, 232, 0, 2.98, 330]])

df8 = pd.DataFrame(columns = ['Year', 'Country', 'Total', 'Per Capita'],
                   data = [[1978, 'FINLAND', 14157, 2.98],
                           [1979, 'SWEDEN', 23160, 2.79],
                           [1979, 'NORWAY', 9338, 2.29]],
                   index = [2, 0, 1])


# tests
class MyTestCase(unittest.TestCase):
    def test_cut_years(self):
        years = pd.DataFrame({'Year': list(range(100))})
        self.assertTrue(
            all((functions.cut_years(years, 5, 90))['Year'] == range(5, 91)))
        self.assertEqual(
            len(functions.cut_years(years, 91, 90)), 0)
        self.assertEqual(
            len(functions.cut_years(years, 105, 110)), 0)


@pytest.mark.parametrize("df, years, res", [(df1, [1960], df2), (df3, [2005], df4)])
def test_highest_gdp(df, years, res):
    assert functions.highest_gdp(df, years).equals(res)


@pytest.mark.parametrize("df, years, res", [(df5, [2000], df6), (df7, [1978, 1979], df8)])
def test_worst_emitters(df, years, res):
    assert functions.worst_emitters(df, years).equals(res)


if __name__ == '__main__':
    unittest.main()

