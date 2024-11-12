from app.models.joinMembershipModels import add_senior_member, produceConnectionNum,add_guardian_member
from werkzeug.security import generate_password_hash
import re
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


#보호자 코드를 생성하고 반환
def generate_guardian_code():
    connection_num = produceConnectionNum()
    return {"message": "보호자 코드가 생성되었습니다", "connection_num": connection_num}

#보호자 코드 유효성 검증
def validate_guardian_code(code):
    # MongoDB에서 코드 유효성 검사 (존재 여부 확인)
    guardian = guardians.find_one({"connection_num": code})
    if guardian:
        return {"message": "보호자 코드가 유효합니다"}
    else:
        return {"error": "유효하지 않은 보호자 코드입니다"}, 400
    
#사용자 이름의 형식을 검증
def validate_username(username):
    return re.match("^[a-zA-Z0-9_]{3,20}$", username) is not None

#전화번호 형식 검증
def validate_phone_number(phone_number):
    return re.match(r"^\\d{10,11}$", phone_number) is not None

#노인 회원 가입을 처리하는 함수
def register_senior_member(data):

    # 데이터 유효성 검사 (예: 이메일, 전화번호 형식 검사)
    if not validate_username(data["username"]):
        return {"error": "Invalid username format"}, 400

    # 비밀번호 해시화
    hashed_password = generate_password_hash(data["password"])

    # 데이터베이스에 저장할 데이터 가공
    senior_data = {
        "username": data["username"],
        "login_id": data["login_id"],
        "password": hashed_password,
        "phone_number": data["phone_number"],
        "birth_date": data["birth_date"],
        "address": data["address"],
        "interests": data["interests"],
        "guardian_code": data["guardian_code"]
    }

    # 모델 호출하여 데이터베이스에 저장
    saved_data = add_senior_member(**senior_data)
    return {"message": "회원가입이 완료되었습니다", "data": saved_data}, 201



#보호자 회원 가입을 처리하는 함수
def register_senior_member(data):

    # 데이터 유효성 검사 (예: 이메일, 전화번호 형식 검사)
    if not validate_username(data["username"]):
        return {"error": "Invalid username format"}, 400

    # 비밀번호 해시화
    hashed_password = generate_password_hash(data["password"])

    # 데이터베이스에 저장할 데이터 가공
    guardian_data = {
        "username": data["username"],
        "login_id": data["login_id"],
        "password": hashed_password,
        "phone_number": data["phone_number"],
        "guardian_code": data["guardian_code"]
    }

    # 모델 호출하여 데이터베이스에 저장
    saved_data = add_guardian_member(**guardian_data)
    return {"message": "회원가입이 완료되었습니다", "data": saved_data}, 201


