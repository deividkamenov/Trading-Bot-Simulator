import base_class

# rsi trading strategy
import yfinance as yf
import pandas as pd
import ta  # technical analysis
import matplotlib.pyplot as plt

SAM_DAYS = 200
RSI_INDEX = 10
DAYS_AVERAGE = 30


class RsiStrategy(base_class.BaseClass):
    def __init__(self, start_date, end_date, stock, interval='1d'):
        super().__init__(start_date, end_date, interval)
        self.start_date = start_date
        self.end_date = end_date
        self.stock = stock
        self.interval = interval
        self.data = yf.download(self.stock, start=self.start_date, end=self.end_date, interval=interval)

    def adjust_data(self):
        # Calulate 200 day average
        self.data['SMA'] = self.data.Close.rolling(SAM_DAYS).mean()
        # Calculate the rsi index
        self.data['rsi'] = ta.momentum.rsi(self.data.Close, window=RSI_INDEX)

        self.data['price'] = self.data.Open.shift(-1)

        # Set the date for buy when date close price i greater than SAM 200 days average & (bitwise and)  rsi < 30 day average
        self.data['Buy'] = (self.data.Close > self.data.SMA) & (self.data.rsi < DAYS_AVERAGE)
        self.data['Sell'] = self.data.rsi > DAYS_AVERAGE + RSI_INDEX

    def calculate_rsi(self):
        self.adjust_data()

        right_position = False
        buy_orders = []
        sell_orders = []
        days_count = 0

        for index, row in self.data.iterrows():
            if not right_position:
                # Open long position
                if row.Buy:
                    buy_orders.append(row.price)
                    right_position = True
                    days_count = 0
            if right_position:
                days_count += 1
                # Close buy position
                if row.Sell:
                    sell_orders.append(row.price)
                    right_position = False
                # 10 days sell
                elif days_count >= RSI_INDEX:
                    sell_orders.append(row.price)
                    right_position = False

        trades = pd.DataFrame([buy_orders, sell_orders], index=['Buys', 'Sells'])
        trades = trades.T

        trades['PnL'] = (trades.Sells - trades.Buys) / trades.Buys + 1

        # returns = trades['PnL']
        return trades


    def plot_rsi_index(self):
        self.adjust_data()

        plt.figure(figsize=(12, 6))
        plt.plot(self.data.index, self.data['rsi'])
        plt.axhline(y=DAYS_AVERAGE, color='r', linestyle='-')
        plt.axhline(y=RSI_INDEX, color='r', linestyle='-')
        plt.title(f'RSI Index for {self.stock}')
        plt.xlabel('Date')
        plt.ylabel('RSI')
        plt.show()

    def plot_money_balance_rsi(self, money_made):
        # plot money made over time
        plt.plot(money_made)
        plt.title("Money made with RSI strategy")
        plt.xlabel("Trade number")
        plt.ylabel("Amount")
        plt.show()


    def run_simulation(self, invested_capital):
        trades = self.calculate_rsi()

        success_rate = (trades[trades.PnL > 1].shape[0] / trades.shape[0]) * 100
        trade_num = 1
        cumulative_returns = invested_capital
        money_made = [invested_capital]

        for el in trades['PnL']:
            cumulative_returns *= el
            current_sum = round(cumulative_returns, 2)
            print(f'Using RSI on trade {trade_num} you have made {current_sum}$')
            trade_num += 1
            money_made.append(current_sum)

        print(f"{success_rate}% of the trades had a positive profit using RSI on {self.stock}")

        self.plot_rsi_index()
        self.plot_money_balance_rsi(money_made)
