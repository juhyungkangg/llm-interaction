import os
import warnings
import re
from SQLInteraction.queries import *
warnings.simplefilter(action='ignore', category=FutureWarning)
from datetime import datetime, timedelta
from SQLInteraction.SQLResult import *
import dropbox
from dropbox.exceptions import AuthError, ApiError
import os
import pandas as pd
import ast

load_dotenv()

def get_signals():
    # Get 10-day-ago date
    current_date = datetime.now()
    date_10_days_ago = current_date - timedelta(days=60)
    date_10_days_ago_str = date_10_days_ago.strftime("%Y-%m-%d")

    # Get signal data from SQL db
    query, params = get_signal_query(date_10_days_ago_str)
    signal_results = SQLResult('signal_db', query, params).results

    # Make it into dataframe
    df = pd.DataFrame(signal_results)

    # Make relevance data to dictionary
    df['relevance'] = df['relevance'].apply(safe_literal_eval)

    # Make dictionary values to float
    df['relevance'] = df['relevance'].apply(convert_dict_values_to_float)

    # Shift 9 hours 30 minutes to sync the day start with the market
    df['datetime'] = df['datetime'] - pd.to_timedelta(6, unit='h')

    # Set date
    df['date'] = df['datetime'].dt.floor('D')

    # Set date as index
    df = df.set_index('date', inplace=False)
    df = df.sort_index()
    df = df[['sentiment', 'reliability', 'relevance']]

    # Task 1: Multiply sentiment by relevance for each ticker to get relevant sentiment values
    df['relevant_sentiment'] = df.apply(compute_relevant_sentiment, axis=1)

    # Task 2: Group by date and merge sentiment and relevant sentiment values using reliability as weight
    df = df.groupby(df.index).apply(weighted_merge)

    # Keep only sentiment and confidence
    df = df[['sentiment', 'confidence']]
    print(df)

    # Save the file in dropbox
    df.to_csv('/Users/juhyung/Dropbox/signals.csv')


# ----------------------
# Util functions
# ----------------------
# Set date as index, set data as usable format, drop useless columns
def safe_literal_eval(val):
    if isinstance(val, str):
        try:
            return ast.literal_eval(val)
        except (ValueError, SyntaxError):
            return val
    return val

# convert dictionary values to float
def convert_dict_values_to_float(d):
    if isinstance(d, dict):
        return {key: float(value) for key, value in d.items()}
    return {}

# Task 1: Multiply sentiment by relevance for each ticker to get relevant sentiment values
def compute_relevant_sentiment(row):
    return {ticker: row['sentiment'] * rel for ticker, rel in row['relevance'].items()}

# Task 2: Group by date and merge sentiment and relevant sentiment values using reliability as weight
def weighted_merge(group):
    merged_sentiment = 0
    merged_relevant_sentiment = {}
    merged_relevant_sentiment_weights = {}

    for _, row in group.iterrows():
        reliability = row['reliability']
        merged_sentiment += row['sentiment'] * reliability
        for ticker, sentiment_value in row['relevant_sentiment'].items():

            # Remove special characters if there is any
            if re.search(r'[&^%$#@!|]', ticker):
                ticker = re.sub(r'[&^%$#@!|]', '', ticker)

            # Clean ticker names
            ticker = ticker.strip().replace(" ", "").upper()

            merged_relevant_sentiment[ticker] = merged_relevant_sentiment.get(ticker, 0) + row[
                'relevant_sentiment'].get(ticker, 0) * reliability

            merged_relevant_sentiment_weights[ticker] = merged_relevant_sentiment_weights.get(ticker, 0) + reliability


    if group['reliability'].sum() != 0:
        merged_sentiment /= group['reliability'].sum()
    else:
        merged_sentiment = 0

    merged_ticker_sentiment = {}
    for key in merged_relevant_sentiment.keys():

        if merged_relevant_sentiment_weights[key] != 0:
            merged_ticker_sentiment[key] = round(merged_relevant_sentiment[key] / merged_relevant_sentiment_weights[key], 4)
        else:
            merged_ticker_sentiment[key] = 0


    return pd.Series({'sentiment': merged_sentiment, 'confidence': merged_ticker_sentiment})
