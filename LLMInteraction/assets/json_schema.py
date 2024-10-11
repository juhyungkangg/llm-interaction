from pydantic import BaseModel, Field, ValidationError, validator, ConfigDict
from typing import Optional, Dict
from pydantic import BaseModel

# Filter json_schema
class FilterFormat(BaseModel):
    filter: bool = Field(
        ...,
        description="Filter the text if not useful."
    )

# Sentiment json_schema
class SentimentFormat(BaseModel):
    sentiment: float = Field(
        ...,
        description="Sentiment score from -1 (very negative) to +1 (very positive)."
    )
    reliability: float = Field(
        ...,
        description="Reliability score from 0 (not reliable) to +1 (very reliable)."
    )
    relevance: Optional[Dict[str, float]] = Field(
        None,
        description=(
            "Relevance scores for tickers. "
            "Values range from 0 (not relevant) to 1 (very relevant). "
            "Can be null."
        )
    )

# Generating JSON schema
filter_schema = {
    "type": "json_schema",
    "json_schema":{
        "name":"sentiment",
        "strict": True,
        "schema":{
    "type": "object",
    "properties": {
        "filter": {
            "type": "boolean",
            "description": "Indicates whether the text should be filtered out (True) or kept (False)."
        }
    },
    "required": ["filter"],
    "additionalProperties": False
}
}
}

# sentiment_schema = SentimentFormat.model_json_schema()
sentiment_schema = {
    "type": "json_schema",
    "json_schema":{
        "name":"sentiment",
        "strict": True,
        "schema":{
    'type': 'object',
    'properties': {
        'sentiment': {
            'type': 'number',
            'description': 'Sentiment score from -1 (very negative) to +1 (very positive).'
        },
        'reliability': {
            'type': 'number',
            'description': 'Reliability score from 0 (not reliable) to +1 (very reliable).'
        },
        'relevance': {
            'anyOf': [
                {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'ticker': {
                                'type': 'string',
                                'description': 'Ticker symbol.'
                            },
                            'relevance_score': {
                                'type': 'number',
                                'description': 'Relevance score from 0 (not relevant) to 1 (very relevant).'
                            }
                        },
                        'required': ['ticker', 'relevance_score'],
                        'additionalProperties': False
                    },
                    'description': 'A list of tuples containing ticker symbols and their relevance scores.'
                },
                {
                    'type': 'null',
                    'description': 'No relevance data available.'
                }
            ],
            'description': 'Relevance scores for tickers. Can be null or an empty list.'
        }
    },
    'required': ['sentiment', 'reliability', 'relevance'],
    'additionalProperties': False
}
}
}

