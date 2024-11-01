import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flask import jsonify
from pymongo import MongoClient


load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))

# 현재 DB 내에 해당 유저 아이디가 존재하는지 Boolean으로 판단함.
def isLoginIdInDB(loginId):
    # MongoDB에서 현재 앱의 MongoDB 데이터베이스 사용
    db = client.ElderCareNet
    user = db.SeniorUser.find_one({"loginId": loginId})

    if user:
        return True
    else:
        user = db.SupervisorUser.find_one({"loginId": loginId})
        if user:
            return True

    return False

#
