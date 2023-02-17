import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import base_class
import moving_average
import rsi_strategy
import fibonacci_strategy
import top_companies_strategy
import adx_strategy
import main

invested_capital = main.invested_capital
stock = main.stock
start_date = main.start_date
end_date = main.end_date
ma_1 = main.ma_1
ma_2 = main.ma_2

class TradingApp:
    def __init__(self, master):
        self.master = master
        master.title("Trading Simulation")


        # Create the radio buttons for selecting the trading strategy
        self.strategy_label = ttk.Label(master, text="Select a Trading Strategy:")
        self.strategy_label.pack()
        self.strategy = tk.StringVar()

        self.strategy.set("Moving Average")
        self.strategy1 = ttk.Radiobutton(master, text="Moving Average", variable=self.strategy, value="Moving Average")
        self.strategy1.pack()

        self.strategy2 = ttk.Radiobutton(master, text="RSI", variable=self.strategy, value="RSI")
        self.strategy2.pack()

        self.strategy3 = ttk.Radiobutton(master, text="Strategy 3", variable=self.strategy, value="Strategy 3")
        self.strategy3.pack()

        self.strategy4 = ttk.Radiobutton(master, text="Strategy 4", variable=self.strategy, value="Strategy 4")
        self.strategy4.pack()

        self.strategy5 = ttk.Radiobutton(master, text="Strategy 5", variable=self.strategy, value="Strategy 5")
        self.strategy5.pack()

        # Create the text box for inputting the test money
        self.money_label = ttk.Label(master, text="Enter Test Money (USD):")
        self.money_label.pack()
        self.money = tk.Entry(master)
        self.money.pack()

        # Create the button for running the simulation
        self.simulate_button = ttk.Button(master, text="Simulate", command=self.run_simulation)
        self.simulate_button.pack()

        # Create the label for displaying the results
        self.results_label = ttk.Label(master, text="Output")
        self.results_label.pack()

        # Create the graph area
        self.plot_area = plt.subplot(111)
        self.plot_area.set_xlabel("Time")
        self.plot_area.set_ylabel("Account Value (USD)")
        self.figure = plt.gcf()
        self.figure.set_size_inches(8, 4)

        # Create the canvas for displaying the graph
        self.canvas = plt.gcf().canvas
        self.canvas_widget = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas_widget.get_tk_widget().pack()

    def run_simulation(self):
        # Get the selected strategy and test money
        strategy = self.strategy.get()
        try:
            test_money = float(self.money.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount of test money")
            return

        # Run the selected strategy and get the results
        if strategy == "Moving Average":
            moving_average_str = moving_average.MovingAverage(stock=stock, start_date=start_date, end_date=end_date)
            results = moving_average_str.run_simulation(invested_capital=invested_capital, ma_1=ma_1, ma_2=ma_2)
        elif strategy == "RSI":
            rsi_str = rsi_strategy.RsiStrategy(stock=stock, start_date=start_date, end_date=end_date)
            results = rsi_str.run_simulation(invested_capital=invested_capital)
        elif strategy == "Strategy 3":
            results = Strategy3(test_money).run()
        elif strategy == "Strategy 4":
            results = Strategy4(test_money).run()
        elif strategy == "Strategy 5":
            results = Strategy5(test_money).run()
        else:
            messagebox.showerror("Error", "Please select a trading strategy")
            return
        # results = 1000

        # Display the results in the label
        self.results_label.config(text=f"Final Account Value: {results[-1]:} $")

        # Plot the results on the graph
        time = np.arange(len(results))
        self.plot_area.plot(time, results)

        # Redraw the canvas to display the updated graph
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingApp(root)
    root.mainloop()