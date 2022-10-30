from pymongo import MongoClient

from config import MONGO_URI, MONGO_DB, MONGO_COLLECTION


def insert_many(payload: list[dict]) -> None:
    myclient = MongoClient(MONGO_URI)
    mydb = myclient[MONGO_DB]
    mycol = mydb[MONGO_COLLECTION]
    mycol.insert_many(payload)

