import yfinance as yf

class Stock:

    def __init__(self, stock_name):
        self.name = stock_name


    def get_info(self):
        data = yf.Ticker(self.name)
        print(type(data.info))
        return data.info
