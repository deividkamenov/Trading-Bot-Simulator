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


    def setUp(self):
        """"This sets example data for the instance of the cass"""
        self.start_date = '2022-01-01'
        self.end_date = '2022-01-31'
        self.stock = 'TSLA'
        self.interval = '1d'
        self.moving_average = MovingAverage(self.start_date, self.end_date, self.stock, self.interval)

    def test_adequate_extraction_of_data(self):
        self.moving_average.data = pd.DataFrame({'Adj Close': [100, 112, 113, 114, 101, 102, 103, 115, 116,117, 118,
                                                               119, 109, 110, 111, 104, 105, 106, 107, 108]})
        self.assertEqual(self.moving_average.run_simulation(1000, 1, 2), 0)


# def test_find_best_average(self):
    #     with patch.object(self.moving_average, 'moving_average', return_value=1.1):
    #         self.moving_average.find_best_average(min_ma1=10, max_ma1=11, min_ma2=20, max_ma2=21, step=10)
    #     self.assertTrue(self.moving_average.plot_graph.called)
    #
    # def test_data_download(self):
    #     data = self.ma.data
    #     self.assertIsInstance(data, yf.Ticker)
    #     self.assertGreater(len(data), 0)
    #
    # def test_moving_average(self):
    #     invested_capital = 100
    #     ma_1 = 10
    #     ma_2 = 20
    #     result = self.ma.moving_average(invested_capital, ma_1, ma_2)
    #     self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()