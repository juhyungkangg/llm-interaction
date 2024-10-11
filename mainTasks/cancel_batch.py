
from SQLInteraction.SQL_utils import *
import json
import tempfile
from jinja2 import Template
import time

load_dotenv()

from openai import OpenAI
client = OpenAI()

batch_li = client.batches.list(limit=10).data



from openai import OpenAI
client = OpenAI()

for batch in batch_li:
    client.batches.cancel(batch.id)