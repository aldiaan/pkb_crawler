import pymongo

from igcrawler_config.config import DB_HOST

class Database:
    def __init__(self):
        self.create_connection()
        self.db = self.connection["pkb"]
        self.lvl1 = self.db["level1"]
           
    def create_connection(self):
        self.connection = pymongo.MongoClient(DB_HOST)        
