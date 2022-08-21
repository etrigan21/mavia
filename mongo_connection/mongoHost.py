from pymongo import MongoClient
from datetime import datetime

class MongoConnection:
    client = MongoClient("mongodb://localhost:27017/realTimeDetection")
    clientDB = client["realTimeDetection"]


