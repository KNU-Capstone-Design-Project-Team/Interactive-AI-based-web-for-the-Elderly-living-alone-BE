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
        temp = db.Conversation.find_one({"SeniorUser_id": temp2.get('SeniorUser_id')}, {"date":previousDay})

        if temp == None:
            for j in range(i, N): noticeList.append(None)
            break
        else:
            noticeList.append(temp.get('responseRatio'))

    return noticeList

def getNameListByLoginId(loginId):
    names = []
    supervisor = db.SupervisorUser.find_one({"loginId":loginId})
    seniorList = db.SeniorUser.find({"SupervisorCode_id": supervisor.get('SupervisorCode_id')})

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
'''
오늘을 기준으로
0시~23시까지 -> 전날 응답률
10시반에 응답률계산
23시~24시까지 -> 오늘 응답률

'''
def getResponseTimesAndNamesBySeniors(supervisorLoginId):
    result = []
    prevDate = -1
    names = getNameListByLoginId(supervisorLoginId)
    for i in range(len(names)):
        temp2 = db.SeniorUser.find_one({"loginId": names[i][1]})

        nowHour = datetime.datetime.now().hour
        if 0 <= nowHour <= 22:  # 0시0분0초~22시59분59초
            prevDate = -2
        elif nowHour == 23:    # 23시0분0초~23시59분59초까지
            prevDate = -1
        else:   pass

        temp = db.Conversation.find_one({"SeniorUser_id": temp2.get('SeniorUser_id')}, sort=[{"date", prevDate}])

        result.append([names[i], temp.get('responseRatio')])

    return temp.get('date'), result
