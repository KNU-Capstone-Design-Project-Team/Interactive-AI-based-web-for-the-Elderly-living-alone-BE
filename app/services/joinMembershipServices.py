from app.models.joinMembershipModels import  SeniorMember, SupervisorMember
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

senior_collection = db["senior_users"]
supervisor_collection = db["supervisor_users"]

class MembershipService:
    def __init__(self):
        pass
    
    # Senior 회원 관련 서비스 메서드
    def register_senior_basic_info(self, username, loginId, password, phoneNumber):
        """Senior 회원의 기본 정보를 저장합니다."""
        senior_member = SeniorMember(username, loginId, password, phoneNumber)
        result = senior_member.save_basic_info()
        return result

    def update_senior_birthdate(self, loginId, year, month, day):
        """Senior 회원의 생년월일 정보를 저장합니다."""
        senior_member = SeniorMember.get_by_loginId(loginId)
        if not senior_member:
            return "Senior member not found"
        
        member_instance = SeniorMember(
            senior_member["username"], senior_member["loginId"],
            senior_member["password"], senior_member["phoneNumber"]
        )
        result = member_instance.update_birthdate(year, month, day)
        return result

    def update_senior_address(self, loginId, si, gu, dong):
        """Senior 회원의 주소 정보를 저장합니다."""
        senior_member = SeniorMember.get_by_loginId(loginId)
        if not senior_member:
            return "Senior member not found"
        
        member_instance = SeniorMember(
            senior_member["username"], senior_member["loginId"],
            senior_member["password"], senior_member["phoneNumber"]
        )
        result = member_instance.update_address(si, gu, dong)
        return result

    def connect_senior_to_guardian(self, loginId, connectionNum):
        """Senior 회원을 보호자와 연결합니다."""
        senior_member = SeniorMember.get_by_loginId(loginId)
        if not senior_member:
            return "Senior member not found"
        
        member_instance = SeniorMember(
            senior_member["username"], senior_member["loginId"],
            senior_member["password"], senior_member["phoneNumber"]
        )
        result = member_instance.connect_guardian(connectionNum)
        return result

    # Supervisor 회원 관련 서비스 메서드
    def register_supervisor_basic_info(self, username, loginId, password, phoneNumber):
        """Supervisor 회원의 기본 정보를 저장합니다."""
        supervisor_member = SupervisorMember(username, loginId, password, phoneNumber)
        result = supervisor_member.save_basic_info()
        return result

    def generate_supervisor_connection_num(self, loginId):
        """Supervisor 회원의 연결 번호를 생성하고 저장합니다."""
        supervisor_member = SupervisorMember.get_by_loginId(loginId)
        if not supervisor_member:
            return "Supervisor member not found"
        
        member_instance = SupervisorMember(
            supervisor_member["username"], supervisor_member["loginId"],
            supervisor_member["password"], supervisor_member["phoneNumber"]
        )
        result = member_instance.generate_connection_number()
        return result

    def get_senior_info(self, loginId):
        """특정 Senior 회원의 정보를 조회합니다."""
        senior_member = SeniorMember.get_by_loginId(loginId)
        if not senior_member:
            return "Senior member not found"
        return senior_member

    def get_supervisor_info(self, loginId):
        """특정 Supervisor 회원의 정보를 조회합니다."""
        supervisor_member = SupervisorMember.get_by_loginId(loginId)
        if not supervisor_member:
            return "Supervisor member not found"
        return supervisor_member

    def get_supervisor_by_connection_num(self, connectionNum):
        """연결 번호로 Supervisor 회원 정보를 조회합니다."""
        supervisor_member = SupervisorMember.get_connection_num(connectionNum)
        if not supervisor_member:
            return "Supervisor member not found"
        return supervisor_member

"""
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
        "1단계 회원 기본 정보 저장"
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
        "2단계 회원 생년월일 저장"
        self.birthdate = datetime(year, month, day)
        senior_collection.update_one(
            {"loginId": self.loginId},
            {"$set": {"birthdate": self.birthdate}}
        )
        return "Birthdate updated successfully"

    def update_address(self, si, gu, dong):
        "3단계 회원 주소 정보 저장"
        self.address = {"si": si, "gu": gu, "dong": dong}
        senior_collection.update_one(
            {"loginId": self.loginId},
            {"$set": {"address": self.address}}
        )
        return "Address updated successfully"

    def connect_guardian(self, connectionNum):
        "5단계 보호자와 연결"
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
        "특정 회원 정보를 loginId로 조회"
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
        "1단계 보호자 기본 정보 저장"
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
        "2단계 보호자 연결 번호 생성 및 저장"
        import random
        self.connectionNum = random.randint(100000, 999999)
        supervisor_collection.update_one(
            {"loginId": self.loginId},
            {"$set": {"connectionNum": self.connectionNum}}
        )
        return f"Connection number generated: {self.connectionNum}"

    @staticmethod
    def get_by_loginId(loginId):
        "특정 보호자 정보를 loginId로 조회"
        return supervisor_collection.find_one({"loginId": loginId})

    @staticmethod
    def get_connection_num(connectionNum):
        "보호자 연결 번호로 정보 조회"
        return supervisor_collection.find_one({"connectionNum": connectionNum})


"#보호자 코드를 생성하고 반환
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


    """
