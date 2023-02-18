import sys

import base_class

# fibonacci trading strategy with key values 23.6%, 38.2%, and 61.8% from the golden ratio of fibonacci
# These levels are considered to be areas where the price may experience a change in direction,
# as they represent potential levels of support or resistance.
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter("ignore")

VALUE_1 = 0.236
VALUE_2 = 0.382
VALUE_3 = 0.618


class FibonacciStrategy:
    def __init__(self, stock, start_date, end_date, interval='1d'):
        self.stock = stock
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        try:

            self.stock_data = yf.download(tickers=self.stock, start=self.start_date, end=self.end_date,
                                          interval=self.interval)
        except Exception as e:
            print(f"Error downloading data: {e}")
            sys.exit(-1)

        if self.stock_data is not None and self.stock_data.empty:
            print("No data downloaded, check your internet connection and if the data provided for the stock API (stock name, dates, interval) is adequate")
            sys.exit(-1)

        self.fib_levels = self.calculate_fibonacci_levels()

    #calculate the fibonacci levels from the coefficients for the certain stock
    def calculate_fibonacci_levels(self):
        high_price = self.stock_data["High"].max()
        low_price = self.stock_data["Low"].min()
        diff = high_price - low_price
        fib_levels = [low_price + VALUE_1 * diff, low_price + VALUE_2 * diff, low_price + VALUE_3 * diff, high_price]
        return fib_levels


    def apply_trading_strategy(self):
        fib_levels = self.calculate_fibonacci_levels()
        trading_signal = 0
        position = 0
        #loop through and check between which coefficients it is
        for i in range(1, len(self.stock_data)):
            prev_close = self.stock_data.iloc[i - 1]["Close"]
            open_price = self.stock_data.iloc[i]["Open"]
            # Buy
            if open_price < fib_levels[1] < prev_close:
                trading_signal = 1
            # Sell
            elif open_price > fib_levels[1] > prev_close:
                trading_signal = -1
            # None
            else:
                trading_signal = 0
            if trading_signal != 0:
                position = trading_signal
            self.stock_data.at[self.stock_data.index[i], "Position"] = position

        self.stock_data["Returns"] = self.stock_data["Close"].pct_change().fillna(0) + 1
        returns = self.stock_data["Returns"]
        return returns

    #plot the results
    def plot_stock_data(self):
        fig, ax = plt.subplots(figsize=(16, 8))
        ax.plot(self.stock_data.index, self.stock_data['Close'], label='Close Price')
        ax.axhline(y=self.fib_levels[0], color='gray', label=f'Fibonacci {VALUE_1}')
        ax.axhline(y=self.fib_levels[1], color='gray', label=f'Fibonacci {VALUE_2}')
        ax.axhline(y=self.fib_levels[2], color='gray', label=f'Fibonacci {VALUE_3}')
        ax.axhline(y=self.fib_levels[3], color='gray', label='All Time High')
        ax.legend(loc='best')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price ($)')
        ax.set_title(f'{self.stock} Stock Price with Fibonacci Levels')
        plt.show()



    # Simulate the startegy for a given capital
    def run_simulation(self, invested_capital):
        returns = self.apply_trading_strategy()
        cumulative_returns = invested_capital

        for i, ret in enumerate(returns):
            cumulative_returns *= ret
            date = self.stock_data.index[i].date()
            print(f"Using Fibonacci strategy on the {date} your current balance is {round(cumulative_returns, 2)}$")

        self.plot_stock_data()
