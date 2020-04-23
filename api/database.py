import pymongo


class Database():
    def __init__(self, database_name):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient[database_name]
        pass

    def insert(self, COLLECTION_NAME, document):
        mycol = self.mydb[COLLECTION_NAME]
        mycol.insert_many(document)

    def select(self, COLLECTION_NAME, query):
        mycol = self.mydb[COLLECTION_NAME]
        return mycol.find(query)

    def close(self):
        self.myclient.close()
