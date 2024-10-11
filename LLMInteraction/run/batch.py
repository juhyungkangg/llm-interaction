from openai import OpenAI
from SQLInteraction.SQL_utils import *
import json
import tempfile


load_dotenv()

class Batch(object):
    def __init__(self,
                 SQLResult,
                 system_prompt,
                 user_prompt,
                 response_format=None,
                 model="gpt-4o-mini",
                 limit=None
                 ):
        self.sql_results = SQLResult.results
        self.table_name = SQLResult.table_name
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.response_format = response_format
        self.model = model
        self.limit = limit

        self.temp_file_name = None

    # Prepare batch
    def prepare_batch(self, limit):
        batch = []
        # Create a temporary batch jsonl file
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False, mode='w') as temp_file:
            self.temp_file_name = temp_file.name  # Get the name of the file

            # Write jsonl data to temporary file
            for row in self.sql_results:
                dt_str = row['datetime'].strftime('%Y-%m-%d %H:%M:%S')

                row_id = str([row["id"], row["source_id"], dt_str])
                system_prompt = self.system_prompt
                user_prompt = self.user_prompt.render(row)

                if limit != None: # Batch limit is priority
                    user_prompt = user_prompt[:limit]
                elif self.limit != None: # Batch run limit is secondary net
                    user_prompt = user_prompt[:self.limit]

                line = {
                    "custom_id": row_id,
                    "method": "POST",
                    "url": "/v1/chat/completions",
                    "body": {
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}],
                        "response_format": self.response_format,
                    }
                }
                temp_file.write(json.dumps(line) + "\n")
                jsonl_line = json.dumps(line)
                batch.append(jsonl_line)

        return batch

    # Upload batch
    def upload_batch(self):
        client = OpenAI()

        self.batch_input_file = client.files.create(
            file=open(self.temp_file_name, "rb"),
            purpose="batch"
        )

    # Create batch
    def create_batch(self):
        self.batch_input_file_id = self.batch_input_file.id
        client = OpenAI()
        self.batch_object = client.batches.create(
            input_file_id=self.batch_input_file_id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
            metadata={
                "description": "test batch"
            }
        )

    # Check batch id
    def check_batch_id(self):
        client = OpenAI()
        print(client.batches.retrieve(self.batch_object.id))

    # Check the status of a batch
    def check_batch(self):
        client = OpenAI()
        self.status = client.batches.retrieve(self.batch_object.id)
        return self.status.status

    # Cancel batch
    def cancel_batch(self):
        pass

    # Get a list of all batches
    def get_batch_list(self):
        pass

    # Destructor
    def __del__(self):
        # Delete the temporary file
        if self.temp_file_name is not None:
            os.remove(self.temp_file_name)
