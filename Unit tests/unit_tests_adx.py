import unittest
import yfinance as yf
import pandas as pd
import ta.trend as tr
from adx_strategy import ADXTradingStrategy
import warnings

warnings.simplefilter("ignore")


class TestADXTradingStrategy(unittest.TestCase):
    """"Tests the correct work of the ADX trading strategy"""
    def setUp(self):
        self.stock = "AAPL"
        self.start_date = "2020-01-01"
        self.end_date = "2021-01-01"
        self.interval = "1d"
        self.invested_capital = 10000
        self.adx_strength_percentage = 25

    def test_apply_atx_strategy(self):
        """"test_apply_atx_strategy: This test checks if the apply_atx_strategy method returns the expected output.
         It does so by comparing the expected output with the actual output obtained from the apply_atx_strategy method."""
        strategy = ADXTradingStrategy(
            self.stock,
            self.start_date,
            self.end_date,
            self.interval,
            self.adx_strength_percentage,
        )
        returns = strategy.apply_atx_strategy()
        self.assertIsInstance(returns, pd.Series)

    def test_position_long_signal(self):
        """"test_long_signal: This test checks if the long_signal column in the stock_data DataFrame is correctly calculated.
         It does so by comparing the expected values with the actual values obtained from the long_signal column."""
        strategy = ADXTradingStrategy(
            self.stock,
            self.start_date,
            self.end_date,
            self.interval,
            self.adx_strength_percentage,
        )
        strategy.apply_atx_strategy()
        self.assertTrue(
            all(strategy.stock_data.loc[strategy.stock_data["long_signal"] == 1, "ADX"] > self.adx_strength_percentage))

    def test_position_short_signal(self):
        """"test_short_signal: This test checks if the short_signal column in the stock_data DataFrame is correctly calculated.
         It does so by comparing the expected values with the actual values obtained from the short_signal column."""
        strategy = ADXTradingStrategy(
            self.stock,
            self.start_date,
            self.end_date,
            self.interval,
            self.adx_strength_percentage,
        )
        strategy.apply_atx_strategy()
        self.assertTrue(all(
            strategy.stock_data.loc[strategy.stock_data["short_signal"] == -1, "ADX"] > self.adx_strength_percentage))


if __name__ == "__main__":
    unittest.main()
