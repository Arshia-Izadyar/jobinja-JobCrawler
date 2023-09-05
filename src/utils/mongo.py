import pymongo


def save_to_mongo(data, category):
    try:
        with pymongo.MongoClient("mongodb://localhost:27017/") as cli:
            db = cli['jobs']
            jobs = db[category]
            jobs.insert_many(data)
        print("data saved!!!")

    except pymongo.errors.PyMongoError as e:
        print("error happend : ", e)


def search_DB(phrase, category):
    with pymongo.MongoClient("mongodb://localhost:27017/") as client:
        db = client["jobs"]
        jobs = db[category]
        result = jobs.find({"title": {"$regex": f".*{phrase}.*"}})
        return list(result)
