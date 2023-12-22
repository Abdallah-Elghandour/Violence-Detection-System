from pymongo import MongoClient 
from config import Config

client = MongoClient(Config.MONGO_DB)

VDS_DB = client['violence_detection']