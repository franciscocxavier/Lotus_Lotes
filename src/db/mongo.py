import pymongo

class MongoDBClient:
    def __init__(self, mongodb_uri, mongodb_db):
        self.client = pymongo.MongoClient(mongodb_uri)
        self.db = self.client[mongodb_db]

    def get_users_collection(self, collection_name):
        return self.db[collection_name]

    def get_settings_collection(self, collection_name):
        return self.db[collection_name]

    def get_query_collection(self, collection_name):
        return self.db[collection_name]

    def get_result_collection(self, collection_name):
        return self.db[collection_name]