from datetime import datetime
import numpy as np
import tensorflow as tf
import os

from data_pipeline.fetch_polygon import PolygonParser
from data_pipeline.data_preprocess import preprocess_all_tickers
from dataset_construction.binary_constructor import binary_constructor
from utils.utils import get_file_name

raw_data_path = '../prediction/data'
processed_data_path = '../prediction/processed'

### TODO: change this when necessary ###
# nasdaq
# neutral_threshold_model_path = "../training/results/hybrid/neutral/trained_model"
# positive_threshold_model_path = "../training/results/hybrid/positive/trained_model"
# negative_threshold_model_path = "../training/results/hybrid/negative/trained_model"

### TODO: change this when necessary ###
# sp500
neutral_threshold_model_path = "../training/results/sp500/neutral/trained_model"
positive_threshold_model_path = "../training/results/sp500/positive/trained_model"
negative_threshold_model_path = "../training/results/sp500/negative/trained_model"

lag = 10


def fetch_data(data_to_predict):
    parser = PolygonParser(raw_data_path)
    date_start = "2023-04-01"  # TODO: needs more efficient timplementation
    date_end = datetime.now().strftime("%Y-%m-%d")
    if data_to_predict == 'nasdaq':
        parser.parse_nasdaq_tickers(date_start, date_end)
    elif data_to_predict == 'sp500':
        parser.parse_sp500_tickers(date_start, date_end)


def preprocess_data():
    preprocess_all_tickers(raw_data_path, processed_data_path)


def get_model_positive_predictions(data, neutral_model, positive_model, negative_model, neutral_threshold, positive_threshold, negative_threshold):
    neutral_classifier_predictions = neutral_model(
        data, training=False)
    neutral_classifier_predictions = (
        np.array(neutral_classifier_predictions) > neutral_threshold).astype(int)
    positive_classifier_predictions = positive_model(
        data, training=False)
    positive_classifier_predictions = (
        np.array(positive_classifier_predictions) > positive_threshold).astype(int)
    negative_classifier_predictions = negative_model(
        data, training=False)
    negative_classifier_predictions = (
        np.array(negative_classifier_predictions) > negative_threshold).astype(int)

    hybrid_predictions = []
    positive_prediction_idx = []

    for i in range(len(neutral_classifier_predictions)):
        neu = neutral_classifier_predictions[i]
        pos = positive_classifier_predictions[i]
        neg = negative_classifier_predictions[i]
        if neu == 1 and pos == 1 and neg == 0:
            hybrid_predictions.append(1)
            positive_prediction_idx.append(i)
        else:
            hybrid_predictions.append(0)
    hybrid_predictions = np.array(hybrid_predictions)

    ticker_symbols = []
    for ticker_file in os.listdir(processed_data_path):
        ticker_symbols.append(get_file_name(ticker_file))

    print(f"Made {np.count_nonzero(hybrid_predictions == 1)} predictions")

    ticker_symbols = []
    for ticker_file in os.listdir(processed_data_path):
        ticker_symbols.append(get_file_name(ticker_file))
    print(
        f"The stocks you should buy are: {np.array(ticker_symbols)[positive_prediction_idx]}")


def get_model_negative_predictions(data, neutral_model, positive_model, negative_model, neutral_threshold, positive_threshold, negative_threshold):
    neutral_classifier_predictions = neutral_model(
        data, training=False)
    neutral_classifier_predictions = (
        np.array(neutral_classifier_predictions) > neutral_threshold).astype(int)
    positive_classifier_predictions = positive_model(
        data, training=False)
    positive_classifier_predictions = (
        np.array(positive_classifier_predictions) > positive_threshold).astype(int)
    negative_classifier_predictions = negative_model(
        data, training=False)
    negative_classifier_predictions = (
        np.array(negative_classifier_predictions) > negative_threshold).astype(int)

    hybrid_predictions = []
    positive_prediction_idx = []

    for i in range(len(neutral_classifier_predictions)):
        neu = neutral_classifier_predictions[i]
        pos = positive_classifier_predictions[i]
        neg = negative_classifier_predictions[i]
        if neu == 0 and pos == 0 and neg == 1:
            hybrid_predictions.append(1)
            positive_prediction_idx.append(i)
        else:
            hybrid_predictions.append(0)
    hybrid_predictions = np.array(hybrid_predictions)

    ticker_symbols = []
    for ticker_file in os.listdir(processed_data_path):
        ticker_symbols.append(get_file_name(ticker_file))

    print(f"Made {np.count_nonzero(hybrid_predictions == 1)} predictions")

    ticker_symbols = []
    for ticker_file in os.listdir(processed_data_path):
        ticker_symbols.append(get_file_name(ticker_file))
    print(
        f"The stocks you should sell are: {np.array(ticker_symbols)[positive_prediction_idx]}")


def make_predictions_for_tomorrow():
    # get the data
    dataset_constructor = binary_constructor(lag, np.NAN, processed_data_path)
    data = dataset_constructor.construct_prediction_dataset()

    # load the model
    neutral_model = tf.keras.models.load_model(
        neutral_threshold_model_path)
    positive_model = tf.keras.models.load_model(
        positive_threshold_model_path)
    negative_model = tf.keras.models.load_model(
        negative_threshold_model_path)

    neutral_model_threshold = 0.6
    positive_model_threshold = 0.7
    negative_model_threshold = 0.7

    get_model_positive_predictions(
        data,
        neutral_model, positive_model, negative_model,
        neutral_model_threshold, positive_model_threshold, negative_model_threshold)

    # get_model_negative_predictions(
    #     data,
    #     neutral_model, positive_model, negative_model,
    #     neutral_model_threshold, positive_model_threshold, negative_model_threshold)


if __name__ == '__main__':
    # fetch_data('sp500')
    # preprocess_data()
    make_predictions_for_tomorrow()


####### FUTURE WORK #######
# # threshold ranges to consider
#     thresholds = [0.5, 0.6, 0.7, 0.8, 0.9]
#     range_start = len(thresholds) - 1
#     range_end = len(thresholds) - 1
#     stocks_to_buy_threshold = 10
#     stocks_to_buy = []
#     # while we need to get more stocks to buy for next week
#     while True:

#         stocks_to_buy = []

#         # search only through the given ranges
#         for neutral_threshold in range(range_end, range_start - 1, -1):
#             for positive_threshold in range(range_end, range_start - 1, -1):
#                 for negative_threshold in range(range_end, range_start - 1, -1):
#                     get_model_predictions(
#                         neutral_threshold, positive_threshold, negative_threshold)
