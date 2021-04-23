import os
from pymongo import MongoClient


def get_mongo_connection():
    return MongoClient(os.getenv("MONGO_CONNECTION_STRING"))


