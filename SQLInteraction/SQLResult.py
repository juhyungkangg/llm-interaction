from LLMInteraction.run.batch import *

class SQLResult(object):
    def __init__(self, table_name, query, params=None):
        self.table_name = table_name
        self.query = query
        self.params = params

        self.results = fetch_query(query, params)
