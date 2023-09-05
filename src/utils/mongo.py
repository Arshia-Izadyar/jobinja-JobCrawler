import pymongo


def save_to_mongo(data):
    try:
        with pymongo.MongoClient("mongodb://localhost:27017/") as cli:
            db = cli['DB']
            jobs = db["jobs"]
            jobs.insert_many(data)
        print("data saved!!!")

    except pymongo.errors.PyMongoError as e:
        print("error happend : ", e)


def search_DB(phrase):
    with pymongo.MongoClient("mongodb://localhost:27017/") as client:
        db = client["DB"]
        jobs = db["jobs"]
        result = jobs.find({"title": {"$regex": f".*{phrase}.*"}})
        return list(result)
