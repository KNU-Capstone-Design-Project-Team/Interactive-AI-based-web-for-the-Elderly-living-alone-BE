import os
from pymongo import MongoClient
import datetime

client = MongoClient(os.getenv("MONGO_URI"))
db = client.ElderCareNet

# 최근 10개의 conversation의 응답률을 가져와서 list에 담아 반환하는 함수
def recent10DaysNotice(N, loginId):
    noticeList = []

    today = datetime.datetime.now()
    for i in range(N):
        previousDay = today + datetime.timedelta(days=(i))
        previousDay = previousDay.strftime('%Y.%m.%d')
        temp2 = db.SeniorUser.find_one({"loginId": loginId})
        temp = db.Conversation.find_one({"seniorUser_id": temp2.get('seniorUser_id')}, {"date":previousDay})

        if temp == None:
            for j in range(i, N): noticeList.append(None)
            break
        else:
            noticeList.append(temp.get('responseRatio'))

    return noticeList

def getNameListByLoginId(loginId):
    names = []
    supervisor = db.SupervisorUser.find_one({"loginId":loginId})
    seniorList = db.SeniorUser.find({"supervisorCode_id": supervisor.get('supervisorCode_id')})

    for i in seniorList:
        names.append((i.get('name'), i.get('loginId')))

    return names

# /stats
def getResponseTimeListByLoginId(nameList):
    responseTimeList = []

    for i in nameList:
        responseTimeList.append(recent10DaysNotice(7, i[1]))

    return responseTimeList

# /notice
def getResponseTimesAndNamesBySeniors(supervisorLoginId):
    result = []
    names = getNameListByLoginId(supervisorLoginId)
    for i in range(len(names)):
        temp2 = db.SeniorUser.find_one({"loginId": names[i][1]})
        temp = db.Conversation.find_one({"seniorUser_id": temp2.get('seniorUser_id')}, {"date": -1})

        result.append((names[i], temp.get('responseRatio')))

    return result
