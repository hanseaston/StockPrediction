import requests
import datetime
import csv

from utils.utils import remove_all_files_from_dir


class PolygonAPI:
    def __init__(self):
        self.base_url = 'https://api.polygon.io/'
        self.headers = {
            'Authorization': 'Bearer cC8AtpZvOZlXEfTeQp7nI5oCxmePPQ7j',
        }

    def fetch(self, endpoint, params=None):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print('Request failed with status code:', response.status_code)
            print('Requested endpoint is:', url)
            print('More detail:', response.json()['error'])
            raise ValueError()

    def fetch_from_next_url(self, response):
        response = requests.get(response['next_url'], headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            print('Request got next url failed with status code:',
                  response.status_code)
            return None

    def has_next_url(self, response):
        return 'next_url' in response


class PolygonParser:
    def __init__(self):
        self.polygon_api = PolygonAPI()
        self.data_base_url = "../raw_data/polygon"

    def parse_sp500_tickers(self):

        file_path = "../raw_data/s&p_500.csv"
        date_start = "2021-01-01"
        date_end = "2023-05-01"

        remove_all_files_from_dir(self.data_base_url)

        ticker_symbols = []
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                ticker_symbols.append(row[0])

        for ticker in ticker_symbols:
            polygon_parser.parse_individual_ticker_within_time_range(
                ticker, date_start, date_end)

    def parse_tickers_from_stock_exchange(self):

        num_ticker_to_fetch = 1000
        date_start = "2020-06-01"
        date_end = "2023-05-21"
        stock_exchange = "XNYS"

        remove_all_files_from_dir(self.data_base_url)

        tickers_symbols = []

        response = self.polygon_api.fetch(
            f"v3/reference/tickers?type=CS&market=stocks&exchange={stock_exchange}&active=true")

        tickers_symbols.extend([obj['ticker'] for obj in response['results']])

        while len(tickers_symbols) < num_ticker_to_fetch and self.polygon_api.has_next_url(response):
            response = self.polygon_api.fetch_from_next_url(response)
            tickers_symbols.extend([obj['ticker']
                                   for obj in response['results']])

        for ticker in tickers_symbols:
            polygon_parser.parse_individual_ticker_within_time_range(
                ticker, date_start, date_end)

    def parse_individual_ticker_within_time_range(self, ticker, date_start, date_end):

        response = self.polygon_api.fetch(
            f"v2/aggs/ticker/{ticker}/range/1/day/{date_start}/{date_end}?adjusted=true&sort=asc")

        if response is None or 'results' not in response:
            return

        ticker_history = response['results']
        ticker_name = response['ticker']

        file_name = f'{self.data_base_url}/{ticker_name}.csv'

        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['date', 'open_price', 'close_price',
                            'lowest_price', 'highest_price', 'volume'])

            for ticker_info in ticker_history:

                date = str(datetime.datetime.fromtimestamp(
                    ticker_info['t'] / 1000)).split(' ')[0]

                open_price = ticker_info['o']
                close_price = ticker_info['c']
                lowest_price = ticker_info['l']
                highest_price = ticker_info['h']
                volume = ticker_info['v']

                writer.writerow([date, open_price, close_price,
                                 lowest_price, highest_price, volume])


if __name__ == '__main__':
    polygon_parser = PolygonParser()
    # polygon_parser.parse_tickers_from_stock_exchange()
    polygon_parser.parse_sp500_tickers()
