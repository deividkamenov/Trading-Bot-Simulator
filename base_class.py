class BaseClass:
    def __init__(self, start_date, end_date, interval = '1d'):
        # stock name  and start & end date to extract from
        self.start = start_date
        self.end = end_date
        self.interval = interval


    # save data to csv
    def save_data(self):
        self.data.to_csv(f'{self.stock} market data.csv', index=False)