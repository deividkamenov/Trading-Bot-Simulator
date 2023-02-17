import base_class
import moving_average
import rsi_strategy
import fibonacci_strategy
import top_companies_strategy
import adx_strategy

invested_capital = 1000
stock = 'AAPL'
start_date = '2000-01-01'
end_date = '2023-02-17'
ma_1 = 10
ma_2 = 20

if __name__ == "__main__":
    # invested_capital = int(input("How much $$$$$$ money do you want to invest: "))

    #DONE
    moving_average_str = moving_average.MovingAverage(stock=stock, start_date=start_date, end_date=end_date)
    # moving_average.find_best_average(min_ma1=10, min_ma2=0, max_ma1=201, max_ma2=201, step=10)
    moving_average_str.run_simulation(invested_capital=invested_capital, ma_1=ma_1, ma_2=ma_2)

    # # DONE
    rsi_str = rsi_strategy.RsiStrategy(stock=stock, start_date=start_date, end_date=end_date)
    rsi_str.run_simulation(invested_capital=invested_capital)
    # #
    # # # DONE
    # fibonacci_str = fibonacci_strategy.FibonacciStrategy(stock=stock, start_date=start_date, end_date=end_date)
    # fibonacci_str.run_simulation(invested_capital=invested_capital)

    # # # DONE
    # top_companies_str = top_companies_strategy.TopCompaniesStrategy(start_date=start_date, end_date=end_date)
    # top_companies_str.run_simulation(invested_capital=invested_capital)

    # # # Done
    # atx_str = adx_strategy.ADXTradingStrategy(stock=stock, start_date=start_date, end_date=end_date)
    # atx_str.run_simulation(invested_capital)
