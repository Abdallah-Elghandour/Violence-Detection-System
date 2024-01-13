from pymongo import MongoClient 
from config import Config

#connect to MongoDB
client = MongoClient(Config.MONGO_DB)
VDS_DB = client['violence_detection']