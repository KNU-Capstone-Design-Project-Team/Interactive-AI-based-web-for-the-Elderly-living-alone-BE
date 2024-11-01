import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pymongo import MongoClient


load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))

def produceConnectionNum():
    pass


