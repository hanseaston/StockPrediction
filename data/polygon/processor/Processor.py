import os
import pandas as pd

from config import get_raw_dataset_path_from_name, get_processed_dataset_path_from_name

from data.polygon.processor.indicators.SMA import SMA
from data.polygon.processor.generators.AttributeRatio import AttributeRatio
from data.polygon.processor.generators.LagRatio import LagRatio

from utils.utils import remove_all_files_from_dir, is_csv


class PolygonDataProcessor:
    """
    Takes in the raw ticker data and processes the data using indicators and generators.
    Finally, writes the processed ticker data into a new file
    """

    def __init__(self, dataset_name):
        self.raw_dataset_path = get_raw_dataset_path_from_name(
            dataset_name)
        self.processed_dataset_path = get_processed_dataset_path_from_name(
            dataset_name)
        remove_all_files_from_dir(self.processed_dataset_path)

    def process_data(self):
        for file_name in os.listdir(self.raw_dataset_path):

            if not is_csv(file_name):
                continue

            raw_file_path = os.path.join(self.raw_dataset_path, file_name)
            processed_file_path = os.path.join(
                self.processed_dataset_path, file_name)
            data = pd.read_csv(raw_file_path)
            # ratio of today's closing price and yesterdays' closing price
            self.L1_CP_R(data)
            # ratio of today's closing price and today's highest price
            self.CP_HP_R(data)
            # ratio of today's closing price and today's lowest price
            self.CP_LP_R(data)
            # ratio of today's closing price and 5 day SMA
            self.L5_CP_SMA_R(data)
            # ratio of today's closing price and 10 day SMA
            self.L10_CP_SMA_R(data)
            # ratio of today's closing price and 20 day SMA
            self.L20_CP_SMA_R(data)
            # ratio of today's closing price and 30 day SMA
            self.L30_CP_SMA_R(data)
            # ratio of today's tradying volume and 5 day SMA
            self.L5_TV_SMA_R(data)
            # ratio of today's tradying volume and 10 day SMA
            self.L10_TV_SMA_R(data)
            # ratio of today's tradying volume and 20 day SMA
            self.L20_TV_SMA_R(data)
            # ratio of today's tradying volume and 30 day SMA
            self.L30_TV_SMA_R(data)
            data.to_csv(processed_file_path, index=False)

    def L1_CP_R(self, data):
        LagRatio(data, 'close_price', 'L1_CP_R', 1)

    def CP_HP_R(self, data):
        AttributeRatio(data, 'close_price', 'highest_price', 'CP_HP_R')

    def CP_LP_R(self, data):
        AttributeRatio(data, 'close_price', 'lowest_price', 'CP_LP_R')

    def L5_CP_SMA(self, data):
        SMA(data, 'close_price', 'L5_CP_SMA', 5)

    def L10_CP_SMA(self, data):
        SMA(data, 'close_price', 'L10_CP_SMA', 10)

    def L20_CP_SMA(self, data):
        SMA(data, 'close_price', 'L20_CP_SMA', 20)

    def L30_CP_SMA(self, data):
        SMA(data, 'close_price', 'L30_CP_SMA', 30)

    def L5_TV_SMA(self, data):
        SMA(data, 'volume', 'L5_TV_SMA', 5)

    def L10_TV_SMA(self, data):
        SMA(data, 'volume', 'L10_TV_SMA', 10)

    def L20_TV_SMA(self, data):
        SMA(data, 'volume', 'L20_TV_SMA', 20)

    def L30_TV_SMA(self, data):
        SMA(data, 'volume', 'L30_TV_SMA', 30)

    def L5_CP_SMA_R(self, data):
        self.L5_CP_SMA(data)
        AttributeRatio(data, 'close_price', 'L5_CP_SMA', 'L5_CP_SMA_R')

    def L10_CP_SMA_R(self, data):
        self.L10_CP_SMA(data)
        AttributeRatio(data, 'close_price', 'L10_CP_SMA', 'L10_CP_SMA_R')

    def L20_CP_SMA_R(self, data):
        self.L20_CP_SMA(data)
        AttributeRatio(data, 'close_price', 'L20_CP_SMA', 'L20_CP_SMA_R')

    def L30_CP_SMA_R(self, data):
        self.L30_CP_SMA(data)
        AttributeRatio(data, 'close_price', 'L30_CP_SMA', 'L30_CP_SMA_R')

    def L5_TV_SMA_R(self, data):
        self.L5_TV_SMA(data)
        AttributeRatio(data, 'volume', 'L5_TV_SMA', 'L5_TV_SMA_R')

    def L10_TV_SMA_R(self, data):
        self.L10_TV_SMA(data)
        AttributeRatio(data, 'volume', 'L10_TV_SMA', 'L10_TV_SMA_R')

    def L20_TV_SMA_R(self, data):
        self.L20_TV_SMA(data)
        AttributeRatio(data, 'volume', 'L20_TV_SMA', 'L20_TV_SMA_R')

    def L30_TV_SMA_R(self, data):
        self.L30_TV_SMA(data)
        AttributeRatio(data, 'volume', 'L30_TV_SMA', 'L30_TV_SMA_R')
