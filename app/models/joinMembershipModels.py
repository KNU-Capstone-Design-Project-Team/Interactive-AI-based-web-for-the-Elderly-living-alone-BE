import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pymongo import MongoClient
import random
import string

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client.ElderCareNet # 사용할 데이터베이스
guardians = db.guardians  # 보호자 정보를 저장할 컬렉션

#6자리 보호자의 고유 코드를 생성하고 DB에 저장하는 함수!
def produceConnectionNum():

    # 6자리의 보호자 코드 생성 (영문 대문자와 숫자로 구성)
    connection_num = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    # 현재 시간을 기준으로 보호자 코드 데이터 생성
    guardian_data = {
        "connection_num": connection_num,
        "created_at": datetime.now()  # 코드 생성 시간
    }
    #return connection_num -> test

    # MongoDB에 데이터 삽입
    guardians.insert_one(guardian_data)
    return connection_num  # 생성한 보호자 코드를 반환

#test= produceConnectionNum()
#print(test)