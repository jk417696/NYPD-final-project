import unittest
from package import functions
import pandas as pd


class MyTestCase(unittest.TestCase):
    def test_cut_years(self):
        years = pd.DataFrame({'Year': list(range(100))})
        self.assertTrue(
            all((functions.cut_years(years, 5, 90))['Year'] == range(5, 91)))
        self.assertEqual(
            len(functions.cut_years(years, 91, 90)), 0)
        self.assertEqual(
            len(functions.cut_years(years, 105, 110)), 0)


if __name__ == '__main__':
    unittest.main()
