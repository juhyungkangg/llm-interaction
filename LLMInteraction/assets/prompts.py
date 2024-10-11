from jinja2 import Template

# ------------------
# System prompt
# ------------------

# Filter prompt
FILTER_PROMPT = """
You are a trading and investment expert. 
Can you extract meaningful US stock tickers and 
provide sentiment analysis from the following text? 
Return True if yes, False if No.
"""
FILTER_PROMPT = FILTER_PROMPT.replace('\n', ' ').strip()

# Sentiment prompt
SENTIMENT_PROMPT = """
You are a trading and investment expert. Analyze the sentiment of the following text and provide:

1. **Sentiment Score**: A score ranging from -1 (very negative) to +1 (very positive), precise to two decimal places.
2. **Reliability Score**: A score ranging from 0 (not reliable) to +1 (very reliable), precise to two decimal places.
3. **Relevance Scores for US Stock Tickers**: Identify or infer US stock tickers and provide a relevance score ranging from 0 (not relevant) to 1 (very relevant), precise to two decimal places. Can be null.

**Note**: US stock tickers follow the regex pattern: `'^[A-Z0-9]{1,5}(\.[A-Z])?$'`
"""


# ------------------
# User prompt
# ------------------

# Benzinga prompt
BENZINGA_PROMPT = """
## Title
{{ title }}
{% if stocks %}
## Related Tickers
{{ stocks }}
{% endif %}
## BODY
{{ body }}
"""
BENZINGA_PROMPT = Template(BENZINGA_PROMPT)

# Nasdaq prompt
NASDAQ_PROMPT = """
## Title
{{ title }}

## BODY
{{ body }}
"""
NASDAQ_PROMPT = Template(NASDAQ_PROMPT)

# Reddit submissions prompt
REDDIT_SUBMISSION_PROMPT = """
## Title
{{ title }}
{% if selftext %}
## Selftext
{{ selftext }}
{% endif %}
## Subreddit
{{ subreddit }}
## Score
{{ score }}
## Number of comments
{{ num_comments }}
"""
REDDIT_SUBMISSION_PROMPT = Template(REDDIT_SUBMISSION_PROMPT)

# Seeking alpha prompt
SEEKING_ALPHA_PROMPT = """
## Title
{{ title }}
{% if tickers_primary %}
## Primary tickers
{{ tickers_primary }}
{% endif %}
{% if tickers_secondary %}
## Secondary tickers
{{ tickers_secondary }}
{% endif %}
{% if content %}
## Content
{{ content }}
{% endif %}
"""
SEEKING_ALPHA_PROMPT = Template(SEEKING_ALPHA_PROMPT)