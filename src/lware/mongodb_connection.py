import os
import sys
import logging

from pymongo import MongoClient


class Connect(object):
    @staticmethod
    def get_connection():
        logging.warning(f"Mongo DB connection string {os.getenv('MONGO_CONNECTION_STRING')}")
        return MongoClient(os.getenv("MONGO_CONNECTION_STRING"))



mongo_db = Connect.get_connection()
