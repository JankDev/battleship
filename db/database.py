import pymongo as mg

myclient = mg.MongoClient("mongodb://localhost:27017/")

mydb = myclient["battleship"]
mycol = mydb["scores"]


class Database:
    def __init__(self):
        self.database = mydb

    def save(self, name, score):
        record = {"name": name, "score": score}
        self.database["scores"].insert_one(record)
