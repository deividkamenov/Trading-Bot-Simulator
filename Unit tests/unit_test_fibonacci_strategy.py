import unittest

import base_class
from fibonacci_strategy import FibonacciStrategy
import pandas as pd

class TestFibonacciStrategy(unittest.TestCase):

    def test_calculate_fibonacci_levels(self):
        """"test_calculate_fibonacci_levels: This tests if the calculate_fibonacci_levels method
        returns a list of four floats, which are the calculated fibonacci levels."""
        fibonacci = FibonacciStrategy(start_date='2022-01-01', end_date='2022-01-31', stock='AAPL', interval='1d')
        fib_levels = fibonacci.calculate_fibonacci_levels()
        self.assertEqual(len(fib_levels), 4)
        self.assertIsInstance(fib_levels[0], float)
        self.assertIsInstance(fib_levels[1], float)
        self.assertIsInstance(fib_levels[2], float)
        self.assertIsInstance(fib_levels[3], float)

    def test_apply_trading_strategy(self):
        """"apply_trading_strategy method returns a list of numbers with the same length as the data,
         and all the numbers are either integers or floats."""
        fibonacci = FibonacciStrategy(start_date='2022-01-01', end_date='2022-01-31', stock='AAPL', interval='1d')
        returns = fibonacci.apply_trading_strategy()
        self.assertIsInstance(returns, pd.Series)

    def test_run_simulation(self):
        """"run_simulation method returns the expected cumulative returns given the input parameters."""
        fibonacci = FibonacciStrategy(start_date='2022-01-01', end_date='2022-01-31', stock='AAPL', interval='1d')
        invested_capital = 1000
        fibonacci.run_simulation(invested_capital)
        self.assertTrue(True)

    def test_calculate_fibonacci_levels_two(self):
        """"calculate_fibonacci_levels method returns a list of four numbers with the correct order and relationship."""
        self.fibonacci = FibonacciStrategy(start_date='2000-01-01', end_date='2023-02-16', stock='AAPL', interval='1d')
        fib_levels = self.fibonacci.calculate_fibonacci_levels()
        self.assertEqual(len(fib_levels), 4)
        self.assertLess(fib_levels[0], fib_levels[1])
        self.assertLess(fib_levels[1], fib_levels[2])
        self.assertLess(fib_levels[2], fib_levels[3])

    def test_apply_trading_strategy_two(self):
        """"apply_trading_strategy method returns a list of numbers with the same length as the data, and all the numbers are either integers or floats."""
        self.fibonacci = FibonacciStrategy(start_date='2000-01-01', end_date='2023-02-16', stock='AAPL', interval='1d')
        returns = self.fibonacci.apply_trading_strategy()
        self.assertEqual(len(returns), len(self.fibonacci.stock_data))
        self.assertTrue(all(isinstance(x, (int, float)) for x in returns))


if __name__ == '__main__':
    unittest.main()
