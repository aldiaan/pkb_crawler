import pymongo

from igcrawler_config.config import DB_HOST, DB_AUTH

class Database:
    def __init__(self):
        self.create_connection()
        self.db = self.connection["pkb"]
        self.lvl1 = self.db["level1"]
        self.lvl2 = self.db["level2"]
           
    def create_connection(self):
        self.connection = pymongo.MongoClient(DB_HOST)        
