try:
    import pymongo as mg
except ImportError:
    print("pymongo not installed")
    exit()

maxSevSelDelay = 2
try:
    myclient = mg.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=maxSevSelDelay)
except mg.errors.ServerSelectionTimeoutError as err:
    print(err)
    exit()

mydb = myclient["battleship"]
mycol = mydb["scores"]


class Database:
    def __init__(self):
        self.database = mydb

    def save(self, score, name=""):
        if name:
            record = {"name": name, "score": score}
            self.database["scores"].insert_one(record)

    def get_all(self):
        rows = list()
        records = list(self.database["scores"].find({}, {"_id": 0, "name": 1, "score": 1}).sort("score").limit(10))
        for item in records:
            rows.append((item["name"], int(item["score"])))

        return rows
