def get_benzinga_query(date):
    query = """
    SELECT id, title, body, stocks, source_id, datetime
    FROM benzinga_db
    WHERE created >= %s
    AND has_processed = FALSE
    AND has_filtered = FALSE
    """
    params = (date,)  # Parameters should be passed separately
    return query, params

def get_nasdaq_query(date):
    query = """
    SELECT id, title, body, source_id, datetime
    FROM nasdaq_db
    WHERE datetime >= %s
    AND has_processed = FALSE
    AND has_filtered = FALSE
    """
    params = (date,)  # Parameters should be passed separately
    return query, params

def get_reddit_submission_query(date):
    query = """
    SELECT id, title, subreddit, selftext, source_id, datetime
    FROM reddit_submission
    WHERE created_utc >= %s
    AND has_filtered = FALSE
    AND has_processed = FALSE
    """
    params = (date,)  # Parameters should be passed separately
    return query, params

def get_seeking_alpha_query(date):
    query = """
    SELECT id, title, source_id, datetime, content, tickers_primary, tickers_secondary
    FROM seeking_alpha_db
    WHERE published_on >= %s
    AND has_filtered = FALSE
    AND has_processed = FALSE
    """
    params = (date,)  # Parameters should be passed separately
    return query, params

def get_signal_query(date):
    query = '''
    SELECT datetime, sentiment, reliability, relevance
    FROM signal_db
    WHERE datetime >= %s;
    '''
    params = (date,)  # Parameters should be passed separately
    return query, params