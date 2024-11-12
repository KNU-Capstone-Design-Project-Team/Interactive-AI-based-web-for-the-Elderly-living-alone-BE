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

# 노인 회원 정보를 디비에 저장
def add_senior_member(username, login_id, password, phone_number, birth_date, address, interests, guardian_phone):
    senior_data = {
        "username": username,
        "login_id": login_id,
        "password": password,  # 암호화 적용 해야함.
        "phone_number": phone_number,
        "birth_date": birth_date,
        "address": address,
        "interests": interests,
        "guardian_phone": guardian_phone,
        "created_at": datetime.now()
    }

    db.seniors.insert_one(senior_data)
    return senior_data  # 저장된 데이터를 반환

#보호자 회원 정보를 디비에 저장
def add_guardian_member(username, login_id, password, phone_number):
    senior_data = {
        "username": username,
        "login_id": login_id,
        "password": password,  # 암호화 적용 해야함.
        "phone_number": phone_number,
        "created_at": datetime.now()
    }

    db.seniors.insert_one(senior_data)
    return senior_data  # 저장된 데이터를 반환
