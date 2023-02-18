import moving_average
from moving_average import MovingAverage
import pandas as pd

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from moving_average import MovingAverage
import yfinance as yf

class TestMovingAverage(unittest.TestCase):
    """"This is a test case tha tests the functionality of the moving average trading algorithm"""
    def setUp(self):
        """"This sets example data for the instance of the cass"""
        self.start_date = '2022-01-01'
        self.end_date = '2022-01-31'
        self.stock = 'AAPL'
        self.interval = '1d'
        self.moving_average = MovingAverage(self.start_date, self.end_date, self.stock, self.interval)

    def test_moving_average_actual(self):
        """"This tests with some random dataframe """
        self.moving_average.data = pd.DataFrame({'Adj Close': [100, 112, 113, 114,101, 102, 103,115, 116, 117, 118, 119, 109, 110, 111,   104, 105, 106, 107, 108, ]})
        self.assertEqual(self.moving_average.run_simulation(1000, 1, 2), 911.1089890501655 )

    def test_moving_average_wrong(self):
        """"This tests with some negative dataframe which should result in zero """
        self.moving_average.data = pd.DataFrame({'Adj Close': [100, -112, 113, 114, 101, 102, 103, 115, 116, -117, 118,
                                                               119, 109, 110, 111, -104, 105, 106, 107, 108 ]})
        self.assertEqual(self.moving_average.run_simulation(1000, 1, 2), 0)

    def test_moving_average_empty(self):
        """"This tests with some negative dataframe with empty dataframe """
        self.moving_average.data = pd.DataFrame({'Adj Close': []})
        self.assertEqual(self.moving_average.run_simulation(1000, 1, 2), 1000)

    def test_basic_initialization(self):
        """"This tests for basic initialization of the cass"""

        ma = MovingAverage('2022-01-01', '2022-02-01', 'AAPL')

if __name__ == '__main__':
    unittest.main()