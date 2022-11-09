# Imports MongoClient for base level access to the local MongoDB
from pymongo import MongoClient
import urllib.parse

class Database:
    DB_Name = 'CabMe'
    def __init__(self):    
          
        # This will initiate connection to the mongodb
        self._db_conn = MongoClient("mongodb+srv://GLCapstone:"  + urllib.parse.quote("Capstone@2022") + "@cluster0.tfzkg67.mongodb.net/test")
        self._db = self._db_conn[Database.DB_Name]

    # This method finds a single document using field information provided in the key parameter
    # It assumes that the key returns a unique document. It returns None if no document is found
    def get_single_data(self, collection, key):
        db_collection = self._db[collection]
        document = db_collection.find_one(key)
        return document

    # This method inserts the data in a new document. It assumes that any uniqueness check is done by the caller
    def insert_single_data(self, collection, data):
        db_collection = self._db[collection]
        document = db_collection.insert_one(data)
        return document.inserted_id

    # This method updates a single document. It assumes that any uniqueness check is done by the caller
    def update_single_data(self, collection, query, data):
        db_collection = self._db[collection]
        document = db_collection.update_one(query, data)
        return document
