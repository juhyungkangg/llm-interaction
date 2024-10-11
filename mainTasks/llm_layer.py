from datetime import timedelta

from LLMInteraction.run.batch_runner import *
from SQLInteraction.SQLResult import *
from SQLInteraction.queries import *
from LLMInteraction.assets.prompts import *
from LLMInteraction.assets.json_schema import *
import schedule
import time

load_dotenv()

def llm_filter(date=None):
    if date is None:
        date = datetime.now()-timedelta(days=10)
        date = date.strftime("%Y-%m-%d")
    print(date)
    # Get results
    query, params = get_benzinga_query(date)
    benzinga_results = SQLResult('benzinga_db', query, params)

    query, params = get_nasdaq_query(date)
    nasdaq_results = SQLResult('nasdaq_db', query, params)

    query, params = get_reddit_submission_query(date)
    reddit_submission_results = SQLResult('reddit_submission', query, params)

    query, params = get_seeking_alpha_query(date)
    seeking_alpha_results = SQLResult('seeking_alpha_db', query, params)

    # Make filter batch
    batch1 = Batch(benzinga_results, FILTER_PROMPT, BENZINGA_PROMPT, filter_schema)
    batch2 = Batch(nasdaq_results, FILTER_PROMPT, NASDAQ_PROMPT, filter_schema)
    batch3 = Batch(reddit_submission_results, FILTER_PROMPT, REDDIT_SUBMISSION_PROMPT, filter_schema)
    batch4 = Batch(seeking_alpha_results, FILTER_PROMPT, SEEKING_ALPHA_PROMPT, filter_schema)

    # retrieve filter batch result
    filter_runner = BatchRunner(batch_list=[batch1, batch2, batch3, batch4], limit=450)
    filter_runner.run_batches()
    time.sleep(90)
    batch_results = filter_runner.retrieve_filters()

    # update has_filtered
    update_has_filtered(batch_results)

def llm_sentiment_analysis(date=None):
    if date is None:
        date = datetime.now()-timedelta(days=10)
        date = date.strftime("%Y-%m-%d")

    # Get results
    query, params = get_benzinga_query(date)
    benzinga_results = SQLResult('benzinga_db', query, params)

    query, params = get_nasdaq_query(date)
    nasdaq_results = SQLResult('nasdaq_db', query, params)

    query, params = get_reddit_submission_query(date)
    reddit_submission_results = SQLResult('reddit_submission', query, params)

    query, params = get_seeking_alpha_query(date)
    seeking_alpha_results = SQLResult('seeking_alpha_db', query, params)

    # Make signal batch
    batch1 = Batch(benzinga_results, SENTIMENT_PROMPT, BENZINGA_PROMPT, sentiment_schema, limit=3000)
    batch2 = Batch(nasdaq_results, SENTIMENT_PROMPT, NASDAQ_PROMPT, sentiment_schema, limit=3000)
    batch3 = Batch(reddit_submission_results, SENTIMENT_PROMPT, REDDIT_SUBMISSION_PROMPT, sentiment_schema,
                   limit=3000)
    batch4 = Batch(seeking_alpha_results, SENTIMENT_PROMPT, SEEKING_ALPHA_PROMPT, sentiment_schema, limit=3000)

    # retrieve signal batch result
    signal_runner = BatchRunner(batch_list=[batch1, batch2, batch3, batch4])
    signal_runner.run_batches()
    time.sleep(30)
    batch_results = signal_runner.retrieve_signals()

    # update signal
    update_signal(batch_results)

    # update has_processed
    update_has_processed(batch_results)



def main():

    llm_filter()
    llm_sentiment_analysis()
