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

senior_collection = db["SeniorUser"]
supervisor_collection = db["SupervisorUser"]
supervisor_code=db["SupervisorCode"]

# Senior 회원 정보 저장
class SeniorMember:
    def __init__(self, username, loginId, password, phoneNumber):
        self.username = username
        self.loginId = loginId
        self.password = password
        self.phoneNumber = phoneNumber
        self.birthdate = None
        self.address = None
        self.guardian_connection = None
        self.join_date = datetime.now()

    def save_basic_info(self):
        """1단계 회원 기본 정보 저장"""
        senior_data = {
            "username": self.username,
            "loginId": self.loginId,
            "password": self.password,
            "phoneNumber": self.phoneNumber,
            "join_date": self.join_date,
        }
        senior_collection.insert_one(senior_data)
        return "Basic info saved successfully"

    def update_birthdate(self, year, month, day):
        """2단계 회원 생년월일 저장"""
        self.birthdate = datetime(year, month, day)
        senior_collection.update_one(
            {"loginId": self.loginId},
            {"$set": {"birthdate": self.birthdate}}
        )
        return "Birthdate updated successfully"

    def update_address(self, si, gu, dong):
        """3단계 회원 주소 정보 저장"""
        self.address = {"si": si, "gu": gu, "dong": dong}
        senior_collection.update_one(
            {"loginId": self.loginId},
            {"$set": {"address": self.address}}
        )
        return "Address updated successfully"

    def connect_guardian(self, connectionNum):
        """5단계 보호자와 연결"""
        guardian = supervisor_collection.find_one({"connectionNum": connectionNum})
        if guardian:
            self.guardian_connection = connectionNum
            senior_collection.update_one(
                {"loginId": self.loginId},
                {"$set": {"guardian_connection": connectionNum}}
            )
            return "Guardian connected successfully"
        else:
            return "Guardian not found with the provided connection number"

    @staticmethod
    def get_by_loginId(loginId):
        """특정 회원 정보를 loginId로 조회"""
        return senior_collection.find_one({"loginId": loginId})


# Supervisor 회원 정보 저장
class SupervisorMember:
    def __init__(self, username, loginId, password, phoneNumber):
        self.username = username
        self.loginId = loginId
        self.password = password
        self.phoneNumber = phoneNumber
        self.connectionNum = None
        self.join_date = datetime.now()

    def save_basic_info(self):
        """1단계 보호자 기본 정보 저장"""
        supervisor_data = {
            "username": self.username,
            "loginId": self.loginId,
            "password": self.password,
            "phoneNumber": self.phoneNumber,
            "join_date": self.join_date,
        }
        supervisor_collection.insert_one(supervisor_data)
        return "Basic info saved successfully"

    def generate_connection_number(self):
        """2단계 보호자 연결 번호 생성 및 저장"""
        import random
        self.connectionNum = random.randint(100000, 999999)
        supervisor_code.update_one(
            {"loginId": self.loginId},
            {"$set": {"connectionNum": self.connectionNum}}
        )
        return f"Connection number generated: {self.connectionNum}"

    @staticmethod
    def get_by_loginId(loginId):
        """특정 보호자 정보를 loginId로 조회"""
        return supervisor_collection.find_one({"loginId": loginId})

    @staticmethod
    def get_connection_num(connectionNum):
        """보호자 연결 번호로 정보 조회"""
        return supervisor_collection.find_one({"connectionNum": connectionNum})

"""
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
def add_senior_member(username, login_id, password, phone_number, birth_date, address, interests, guardian_code):
    senior_data = {
        "username": username,
        "login_id": login_id,
        "password": password,  # 암호화 적용 해야함.
        "phone_number": phone_number,
        "birth_date": birth_date,
        "address": address,
        "interests": interests,
        "guardian_code": guardian_code,
        "created_at": datetime.now()
    }

    db.seniors.insert_one(senior_data)
    return senior_data  # 저장된 데이터를 반환

#보호자 회원 정보를 디비에 저장
def add_guardian_member(username, login_id, password, phone_number):
    guardian_data = {
        "username": username,
        "login_id": login_id,
        "password": password,  # 암호화 적용 해야함.
        "phone_number": phone_number,
        "created_at": datetime.now()
    }

    db.guardians.insert_one(guardian_data)
    return guardian_data  # 저장된 데이터를 반환
"""