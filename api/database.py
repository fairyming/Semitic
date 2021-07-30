import pymongo


class Database():
    def __init__(self, database_name):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient[database_name]
        pass

    def insert(self, COLLECTION_NAME, document):
        mycol = self.mydb[COLLECTION_NAME]
        mycol.insert_many(document)

    def select(self, COLLECTION_NAME, query, sort = "time"):
        mycol = self.mydb[COLLECTION_NAME]
        return mycol.find(query).sort(sort, -1)

    def count(self, COLLECTION_NAME):
        mycol = self.mydb[COLLECTION_NAME]
        return mycol.count()

    def close(self):
        self.myclient.close()
