# Average Directional Index used to measure the strength of a trend in a financial market.
# if over 25% is believed to be a strong trend (to continue going up/down)

import base_class

import yfinance as yf
import pandas as pd
import ta.trend as tr
import warnings
import matplotlib.pyplot as plt

warnings.simplefilter("ignore")


class ADXTradingStrategy(base_class.BaseClass):
    def __init__(self, stock, start_date, end_date, interval='1d', adx_strenght_percentage=25):
        super().__init__(start_date, end_date, interval)
        self.stock = stock
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.adx_strenght_percentage = adx_strenght_percentage
        self.stock_data = yf.download(self.stock, self.start_date, self.end_date, self.interval)

    def apply_atx_strategy(self):
        adx_indicator = tr.ADXIndicator(high=self.stock_data['High'], low=self.stock_data['Low'],
                                        close=self.stock_data['Close'],
                                        window=14, fillna=True)
        self.stock_data['ADX'] = adx_indicator.adx()

        # Long signal with a value 1 and 0 for both
        # long 1 and short 0 = long
        # long 0 and short -1 = short
        # long 0 and short 0 = neutral
        self.stock_data['long_signal'] = 0
        self.stock_data.loc[self.stock_data['ADX'] > self.adx_strenght_percentage, 'long_signal'] = 1
        self.stock_data['long_position'] = self.stock_data['long_signal'].diff()
        self.stock_data.loc[self.stock_data['long_position'] == -1, 'long_signal'] = 0

        # Short signal with value -1
        self.stock_data['short_signal'] = 0
        self.stock_data.loc[self.stock_data['ADX'] > self.adx_strenght_percentage, 'short_signal'] = -1
        self.stock_data['short_position'] = self.stock_data['short_signal'].diff()
        self.stock_data.loc[self.stock_data['short_position'] == 1, 'short_signal'] = 0

        # Combine long and short signals to create position
        self.stock_data['position'] = self.stock_data['long_signal'] + self.stock_data['short_signal']

        # Calculate returns
        self.stock_data['returns'] = self.stock_data['Close'].pct_change()

        # Return the final cumulative returns
        return self.stock_data['returns']

    def plot_returns(self, invested_capital):
        # Run the simulation and calculate cumulative returns
        cumulative_returns = self.apply_atx_strategy()
        balance = invested_capital * (1 + cumulative_returns).cumprod()

        # Plot the account balance
        fig, ax = plt.subplots()
        ax.plot(balance)
        ax.set_title(f"Account Balance with {self.adx_strenght_percentage}% ADX Strength Strategy")
        ax.set_xlabel("Date")
        ax.set_ylabel("Account Balance ($)")
        ax.grid(True)
        plt.show()

    def run_simulation(self, invested_capital):
        returns = self.apply_atx_strategy()
        # print(returns)
        cumulative_returns = invested_capital

        for i, ret in enumerate(returns):
            if not pd.isna(ret):  # check if the value is not NaN
                cumulative_returns *= (1 + ret)  # multiply by (1 + return)
                date = self.stock_data.index[i].date()
                print(f"Using ATX strategy on the {date} your current balance is {cumulative_returns}$")

        self.plot_returns(invested_capital)
