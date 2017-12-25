import pymongo
from pymongo import MongoClient

class MongoDB:    
    def connect(self):
        client = MongoClient('mongodb://127.0.0.1:27017');
        db = client['blockchain']['chain']
        return db;
    
    def insert(self, collection, data, multiple = False):
        db = self.client[self.collection];
        if (multiple):
            result = db[collection].insert_many(data)
        else :
            result = db[collection].insert_one(data)
        return result;
 
    def fetch(self, document, condition = {}):
        db = self.client[self.collection]
        result = db[document].find(condition).sort([("post_date", pymongo.DESCENDING)]);
        return result;
    
    # def __del__(self):
    #     self.client.close();
        
    def delete(self, collection, data):
        db = self.client[self.collection];
        result = db[collection].delete_one(data)
        return result;
        