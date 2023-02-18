import base_class
import moving_average
import rsi_strategy
import fibonacci_strategy
import top_companies_strategy
import adx_strategy

import warnings
warnings.simplefilter("ignore")

# invested_capital = int(input("How much $ money do you want to invest: "))
invested_capital = 1000
stock = 'AAPL'
start_date = '2000-01-01'
end_date = '2023-02-17'
ma_1 = 10
ma_2 = 20

if __name__ == "__main__":
    #Moving Average
    moving_average_str = moving_average.MovingAverage(stock=stock, start_date=start_date, end_date=end_date)
    # moving_average_str.find_best_average(min_ma1=10, min_ma2=0, max_ma1=201, max_ma2=201, step=10)
    moving_average_str.run_simulation(invested_capital=invested_capital, ma_1=ma_1, ma_2=ma_2)

    # RSI
    rsi_str = rsi_strategy.RsiStrategy(stock=stock, start_date=start_date, end_date=end_date)
    rsi_str.run_simulation(invested_capital=invested_capital)

    # Fibonacci
    fibonacci_str = fibonacci_strategy.FibonacciStrategy(stock=stock, start_date=start_date, end_date=end_date)
    fibonacci_str.run_simulation(invested_capital=invested_capital)

    # ATX
    atx_str = adx_strategy.ADXTradingStrategy(stock=stock, start_date=start_date, end_date=end_date)
    atx_str.run_simulation(invested_capital)

    # Top companies
    top_companies_str = top_companies_strategy.TopCompaniesStrategy(start_date=start_date, end_date=end_date)
    top_companies_str.run_simulation(invested_capital=invested_capital)
