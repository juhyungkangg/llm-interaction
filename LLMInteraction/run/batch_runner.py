from distutils.command.clean import clean

from LLMInteraction.run.batch import *
import time
import ast
from datetime import datetime
import openai

load_dotenv()


class BatchRunner(object):
    def __init__(self, batch_list, limit=None):
        # Remove empty batch
        cleaned_batch_list = []
        for batch in batch_list:
            if batch.sql_results is not None:
                cleaned_batch_list.append(batch)
            else:
                print(f"Skipping batch {batch.table_name} since it's empty.")

        self.batch_list = cleaned_batch_list
        self.limit = limit
        self.completed = [False] * len(cleaned_batch_list)

    def run_batches(self):
        for batch in self.batch_list:
            # prepare batch
            batch.prepare_batch(self.limit)

            # upload batch
            batch.upload_batch()

            # create batch
            batch.create_batch()


    def retrieve_signals(self):
        batch_result = {}

        delay = 60

        iter = 0

        while True:
            try:
                # Set iter
                if iter >= len(self.batch_list):
                    iter = 0

                # Break if completed
                if all(self.completed):
                    break

                # Set variables
                batch = self.batch_list[iter]
                completed = self.completed[iter]
                status = batch.check_batch()

                # Go to next if completed
                if completed:
                    iter += 1
                    continue

                # Progress calculation
                client = OpenAI()
                request_counts = client.batches.retrieve(batch.batch_object.id).request_counts
                total_count = request_counts.total
                completed_count = request_counts.completed

                if total_count == 0:
                    progress = 0
                else:
                    progress = completed_count / total_count



                # Retrieve if batch is ready
                if (status == "completed") & (completed == False):
                    # mark completed as True
                    self.completed[iter] = True

                    # retrieve batch result
                    results = []
                    output_file_id = batch.status.output_file_id
                    client = OpenAI()
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

                        # Append result
                        results.append(result)

                    batch_result[batch.table_name] = results
                    print(f"batch{iter + 1}/{len(self.batch_list)}: {status} {round(progress * 100, 2)}%. Total: {total_count}. Time: {datetime.now().strftime('%m-%d %H:%M:%S')}")
                else:
                    print(f"batch{iter + 1}/{len(self.batch_list)}: {status} {round(progress * 100, 2)}%. Total: {total_count}. Time: {datetime.now().strftime('%m-%d %H:%M:%S')}")
                    time.sleep(90)

                iter += 1
            except openai.RateLimitError as e:
                print(f"Rate limit exceeded, retrying in {delay} seconds...")
                time.sleep(delay)  # Wait before retrying

                # Delay backoff
                delay *= 2
            except Exception as e:
                print(f"An error occurred: {e}")
                break

        print(f"All signals received.")

        return batch_result


    def retrieve_filters(self):
        batch_result = {}

        delay = 60

        iter = 0

        while True:
            try:
                # Set iter
                if iter >= len(self.batch_list):
                    iter = 0

                # Break if completed
                print(self.completed)
                if all(self.completed):
                    break

                # Set variables
                batch = self.batch_list[iter]
                completed = self.completed[iter]
                status = batch.check_batch()

                # Skip if added
                if completed:
                    iter += 1
                    continue

                # Progress calculation
                client = OpenAI()
                request_counts = client.batches.retrieve(batch.batch_object.id).request_counts
                total_count = request_counts.total
                completed_count = request_counts.completed

                if total_count == 0:
                    progress = 0
                else:
                    progress = completed_count / total_count



                # Retrieve if batch is ready
                if (status == "completed") & (completed == False):
                    # mark completed as True
                    self.completed[iter] = True

                    # retrieve batch result
                    results = []
                    output_file_id = batch.status.output_file_id
                    client = OpenAI()
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

                        # Set filter
                        result['filter'] = content['filter']

                        # Append result
                        results.append(result)

                    batch_result[batch.table_name] = results
                    print(f"batch{iter+1}/{len(self.batch_list)}: {status} {round(progress*100,2)}%. Total: {total_count} {datetime.now().strftime('%m-%d %H:%M:%S')}")
                else:
                    print(f"batch{iter+1}/{len(self.batch_list)}: {status} {round(progress*100,2)}%. Total: {total_count} {datetime.now().strftime('%m-%d %H:%M:%S')}")
                    time.sleep(90)

                iter += 1
            except openai.RateLimitError as e:
                print(f"Rate limit exceeded, retrying in {delay} seconds...")
                time.sleep(delay)  # Wait before retrying

                # Delay backoff
                delay *= 2
            except Exception as e:
                print(f"An error occurred: {e}")
                break

        print(f"All filters received.")

        return batch_result

