import os
from pymongo import MongoClient
import datetime

client = MongoClient(os.getenv("MONGO_URI"))

def getNewMessagesCount():
    # is_read가 False인 메시지 수를 세서 반환
    db = client.ElderCareNet
    newMessagesCount = db.messages.countDocuments({"is_read": False})
    return newMessagesCount

def isNewData():
    pass
