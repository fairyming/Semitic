import pymongo


class Database():
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["Intelligence"]
        pass

    def insert(self, COLLECTION_NAME, document):
        mycol = self.mydb[COLLECTION_NAME]
        mycol.insert(document)

    def select(self, COLLECTION_NAME):
        pass

    def close(self):
        self.myclient.close()
