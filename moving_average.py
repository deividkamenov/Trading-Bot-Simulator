# moving average
# moving average is a zbasic trading algorithm which is based mon the 2 averages for example 10 and 20 day median
# and uses the points where they intersect to create buy and sell signals
# for example if the ma_1 ia linear and static if ma_2 intersects it from ut to down it's a sell signal
# but ma_2 it intersects it from down to up it's a buy signal
# if they don't intersect it's a neutral signal (don't do anything)

import base_class

import matplotlib.pyplot as plt
import heapq
import yfinance as yf
import pandas as pd
import warnings

warnings.simplefilter("ignore")


class MovingAverage(base_class.BaseClass):
    def __init__(self, start_date, end_date, stock, interval='1d'):
        super().__init__(start_date, end_date, interval)
        self.start_date = start_date
        self.end_date = end_date
        self.stock = stock
        self.interval = interval

        self.data = yf.download(stock, start=self.start, end=self.end, interval=interval)

    def plot_graph(self, buy_signals, sell_signals, ma_1, ma_2):

        self.data['Buy Signals'] = buy_signals
        self.data['Sell Signals'] = sell_signals

        # # print(self.data)
        plt.plot(self.data[f'Adj Close'], label=f"Price per share {self.stock}", alpha=0.7)
        plt.plot(self.data[f'MA_{ma_1}'], label=f"MA_{ma_1}", color='orange', linestyle='--')
        plt.plot(self.data[f'MA_{ma_2}'], label=f"MA_{ma_2}", color='pink', linestyle='--')
        plt.scatter(self.data.index, self.data['Buy Signals'], label='Buy Signal', marker='^', color='#00ff00', lw=3)
        plt.scatter(self.data.index, self.data['Sell Signals'], label='Sell Signal', marker='v', color='#ff0000', lw=3)
        plt.legend(loc='upper left')

        # plt.savefig('destination_path.jpeg')
        plt.show()

    # find a single moving average solution and set the buy and sell times in the dataframe to be used for the plot
    def moving_average(self, invested_capital, ma_1=10, ma_2=20, to_plot=False):
        my_stocks = 0

        self.data[f'MA_{ma_1}'] = self.data['Adj Close'].rolling(window=ma_1).mean()
        self.data[f'MA_{ma_2}'] = self.data['Adj Close'].rolling(window=ma_2).mean()

        buy_signals = []
        sell_signals = []
        trigger = 0

        # for x, _ in enumerate(self.data.iterrows()): #works slower idk why :)
        for x in range(len(self.data)):
            # buy
            if self.data[f'MA_{ma_1}'].iloc[x] > self.data[f'MA_{ma_2}'].iloc[x] and trigger != 1:
                buy_signals.append(self.data['Adj Close'].iloc[x])
                sell_signals.append(float("nan"))
                trigger = 1

                # for simulation buy
                my_stocks = invested_capital / buy_signals[-1]

            # Sell
            elif self.data[f'MA_{ma_1}'].iloc[x] < self.data[f'MA_{ma_2}'].iloc[x] and trigger != -1:
                buy_signals.append(float('nan'))
                sell_signals.append(self.data['Adj Close'].iloc[x])
                trigger = -1

                # simulation sell
                invested_capital = my_stocks * sell_signals[-1]
            else:
                buy_signals.append(float('nan'))
                sell_signals.append(float('nan'))

        if to_plot:
            self.plot_graph(buy_signals, sell_signals, ma_1, ma_2)

        return invested_capital

    # A function to test with miultiple moving averages and find the most profitable one
    def find_best_average(self, min_ma1=0, min_ma2=0, max_ma1=101, max_ma2=101, step=10):
        dic_money_moving_average_values = {}
        invested_capital = 1

        # there must be a faster way bu they didn't work right  at least this one is reliable
        for ma_1 in range(min_ma1, max_ma1, step):
            for ma_2 in range(min_ma2, max_ma2, step):
                final_money = self.moving_average(invested_capital, ma_1, ma_2)

                print(f"You have made:$ {final_money * 100}% with {ma_1=}  and {ma_2=}")
                dic_money_moving_average_values[f"{ma_1} {ma_2}"] = final_money

        #get the highest returns
        max_element = max(dic_money_moving_average_values, key=dic_money_moving_average_values.get)
        #split ma1 & ma2
        ma_1, ma_2 = map(int, max_element.split())

        #sort and get the highst returns and the ma1 & 2 that were used
        sorted_dic = sorted(dic_money_moving_average_values.items(), key=lambda item: item[1], reverse=False)
        top_10 = heapq.nlargest(10, sorted_dic, key=lambda x: x[1])
        # print(top_10)

        #Print the top 10 highest returns
        for key, value in top_10:
            ma_1, ma_2 = map(int, key.split())
            self.moving_average(invested_capital, ma_1, ma_2, True)

            print(f"You have made the most money:{value * 100}% with {ma_1=} and {ma_2=}")

    #Run a simulation with a single ma1 and ma2 and show the results
    def run_simulation(self, invested_capital, ma_1=20, ma_2=50):
        final_balance = self.moving_average(invested_capital, ma_1, ma_2, True)
        print(f"Using Moving Average with {ma_1=}  and {ma_2=} your current balance is:$ {final_balance=} ")

        return final_balance
