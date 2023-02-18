import unittest
import datetime

from rsi_strategy import RsiStrategy


class TestRsiStrategy(unittest.TestCase):
    """"Test cases that test the functionality of the RSI trading algorithm"""

    def test_init(self):
        """"This is a test case tha tests the functionality of the init function"""

        start_date = datetime.date(2021, 1, 1)
        end_date = datetime.date(2021, 2, 1)
        stock = "AAPL"
        interval = "1d"
        rsi_strategy = RsiStrategy(start_date, end_date, stock, interval)
        self.assertEqual(rsi_strategy.start_date, start_date)
        self.assertEqual(rsi_strategy.end_date, end_date)
        self.assertEqual(rsi_strategy.stock, stock)
        self.assertEqual(rsi_strategy.interval, interval)
        self.assertIsNotNone(rsi_strategy.data)

    def test_adjust_data(self):
        """"This is a test case tha tests the functionality of the adjusting data"""

        start_date = datetime.date(2021, 1, 1)
        end_date = datetime.date(2021, 2, 1)
        stock = "AAPL"
        interval = "1d"
        rsi_strategy = RsiStrategy(start_date, end_date, stock, interval)
        rsi_strategy.adjust_data()
        self.assertIsNotNone(rsi_strategy.data['SMA'])
        self.assertIsNotNone(rsi_strategy.data['rsi'])
        self.assertIsNotNone(rsi_strategy.data['price'])
        self.assertIsNotNone(rsi_strategy.data['Buy'])
        self.assertIsNotNone(rsi_strategy.data['Sell'])

    def test_calculate_rsi(self):
        """"This is a test case tha tests the functionality whether the calculating rsi works correctly"""

        start_date = datetime.date(2021, 1, 1)
        end_date = datetime.date(2021, 2, 1)
        stock = "AAPL"
        interval = "1d"
        rsi_strategy = RsiStrategy(start_date, end_date, stock, interval)
        trades = rsi_strategy.calculate_rsi()
        self.assertIsNotNone(trades)

    def test_plot_rsi_index(self):
        """"This is a test case tha tests the functionality whether the plot function  for the rsi works correctly"""

        start_date = datetime.date(2021, 1, 1)
        end_date = datetime.date(2021, 2, 1)
        stock = "AAPL"
        interval = "1d"
        rsi_strategy = RsiStrategy(start_date, end_date, stock, interval)
        rsi_strategy.plot_rsi_index()

    def test_plot_money_balance_rsi(self):
        """"This is a test case tha tests the functionality whether the plot function for the ballance works correctly"""

        start_date = datetime.date(2021, 1, 1)
        end_date = datetime.date(2021, 2, 1)
        stock = "AAPL"
        interval = "1d"
        rsi_strategy = RsiStrategy(start_date, end_date, stock, interval)
        money_made = [100, 120, 80, 90]
        rsi_strategy.plot_money_balance_rsi(money_made)


if __name__ == '__main__':
    unittest.main()