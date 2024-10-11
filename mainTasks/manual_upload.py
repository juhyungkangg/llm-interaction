from openai import OpenAI
from dotenv import load_dotenv
from LLMInteraction.assets.json_schema import *
from LLMInteraction.assets.prompts import *
from SQLInteraction.queries import *
from SQLInteraction.SQL_utils import *
import json
import tempfile
from jinja2 import Template
import time


load_dotenv()

client = OpenAI()
connection = create_connection()
cursor = connection.cursor(dictionary=True)

batch_list = client.batches.list(limit=4).data
print(batch_list)

table_name_li = ['seeking_alpha_db', 'reddit_submission', 'nasdaq_db', 'benzinga_db']

for idx, batch in enumerate(batch_list):
    # try:
    output_file_id = batch.output_file_id


    file_response = client.files.content(output_file_id)
    txt_response = file_response.text.strip().split("\n")
    for txt in txt_response:
        result = {}

        # Set as json
        data = json.loads(txt)

        # Set id
        custom_id = ast.literal_eval(data["custom_id"])

        result['id'] = custom_id[0]
        result['source_id'] = custom_id[1]
        result['datetime'] = custom_id[2]

        # Get content
        content = data['response']['body']['choices'][0]['message']['content']
        content = json.loads(content)

        # Set sentiment
        result['sentiment'] = content['sentiment']

        # Set reliability
        result['reliability'] = content['reliability']

        # Set relevance
        relevance_list = content['relevance']
        if relevance_list is not None:
            new_dict = {}
            for relevance in relevance_list:
                if relevance is not None:
                    new_dict[relevance['ticker']] = relevance['relevance_score']
            result['relevance'] = new_dict
        else:
            result['relevance'] = {}

        result['has_processed'] = True

        signal_query = """
        INSERT INTO signal_db (id, datetime, source_id, sentiment, reliability, relevance)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            sentiment = VALUES(sentiment),
            reliability = VALUES(reliability),
            relevance = VALUES(relevance),
            datetime = VALUES(datetime);
        """


        if isinstance(result['relevance'], dict):
            # Proceed if signal_data is a dictionary
            relevance_json = json.dumps(result['relevance'])
        else:
            print(f"Error: Expected a dictionary but got {type(result['relevance'])}")
            relevance_json = {}

        cursor.execute(signal_query, (
            result['id'],
            result['datetime'],
            result['source_id'],
            result['sentiment'],
            result['reliability'],
            relevance_json
        ))
        connection.commit()
    # except Exception as e:
    #     print(e)


print("Updated signal.")


connection.close()