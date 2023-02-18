# momentum strategy top 50 most profitable companies for 12 months
# being top 30 most profitable for 6mo being top 10 most profitable for 3 mo
# in NASDAQ100

import base_class

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import warnings
warnings.simplefilter("ignore")


class TopCompaniesStrategy(base_class.BaseClass):
    def __init__(self, start_date, end_date, interval='1d',
                 stocks_adress='https://en.wikipedia.org/wiki/Nasdaq-100'):
        super().__init__(start_date, end_date, interval)
        stocks_data = pd.read_html(stocks_adress)[4]
        self.stocks = stocks_data.Ticker.to_list()

        self.market_data = yf.download(self.stocks, start=start_date, end=end_date, interval=interval)['Adj Close']
        self.monthly_return = (self.market_data.pct_change() + 1)[1:].resample('M').prod()

        # get the best companies by highest montly return for the past n months
        self.best_12_month = self.monthly_return.rolling(12).apply(np.prod)
        self.best_6_month = self.monthly_return.rolling(6).apply(np.prod)
        self.best_3_month = self.monthly_return.rolling(3).apply(np.prod)

    # get the n highest companies of the highest performers
    def get_best_companies(self, date):
        highest_50 = self.best_12_month.loc[date].nlargest(50).index  # top 50 in the year
        highest_30 = self.best_6_month.loc[date, highest_50].nlargest(
            30).index  # top 30 in the 6 months being top 50 yearly
        highest_10 = self.best_3_month.loc[date, highest_30].nlargest(10).index  # top 10 in the
        return highest_10

    # Returns the average monthly return for the best performing companies in the portfolio from a given date.
    def calculate_portfolio_performance(self, date):
        portfolio = self.monthly_return.loc[date:, self.get_best_companies(date)][1:2]
        return portfolio.mean(axis=1).values[0]

    # The strategy involves selecting a portfolio of stocks that have performed well in the past
    # and then holding those stocks for a fixed period of time
    def momentum_strategy(self):
        returns = []

        for date in self.monthly_return.index[:-1]:
            returns.append(self.calculate_portfolio_performance(date))

        return pd.Series(returns, index=self.monthly_return.index[1:]).cumprod()

    # plots a graph of the returns
    def plot_simulation(self, invested_capital):
        returns = self.momentum_strategy()
        simulation_results = invested_capital * returns

        # Plot the simulation results
        fig, ax = plt.subplots()
        ax.plot(simulation_results.index, simulation_results.values)
        ax.set_title('Momentum Trading Strategy Simulation Results')
        ax.set_xlabel('Date')
        ax.set_ylabel('Investment Value')

        plt.show()

    # runs a simulation with a example value of invested capital
    def run_simulation(self, invested_capital):
        # Simulate
        returns = self.momentum_strategy()

        for date, value in zip(returns.index, returns.values):
            print(f"Using momentum strategy on date {date.strftime('%Y-%m-%d')},"
                  f" you have made {invested_capital * value}$ with  ")

        self.plot_simulation(invested_capital)
