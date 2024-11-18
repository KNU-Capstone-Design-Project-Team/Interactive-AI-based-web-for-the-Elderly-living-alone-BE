import os
from pymongo import MongoClient
import datetime

client = MongoClient(os.getenv("MONGO_URI"))
db = client.ElderCareNet


def get30totalPrograms(category):
    # 1. postId랑 2. 이름이랑 3. 사진만 보내주면 됨
    programList = []

    if category == 'total':
        # 전체 30개
        programList.append(db.ReginalProgram.find_one(sort=[{"date", -1}]))
        for i in range(1, 30):
            temp = db.ReginalProgram.find_one(sort=[{"date", -1}], skip=i)
            if temp:
                programList.append(temp)
            else:
                for j in range(i, 30):
                    programList.append(None)
                    return programList
        return programList

    if category == 'location':
        # 전체에서 지역을 search해서 가장 최근것들을 30개 받아옴
        # 단 지금은 hardcoding 되어 있으므로 임의의 지역을 search해서 최대 30개를 가져옴
        programList.append(db.ReginalProgram.find_one(sort=[{"date", -1}]))
        for i in range(1, 30):
            temp = db.ReginalProgram.find_one(sort=[{"date", -1}], skip=i)
            if temp:
                programList.append(temp)
            else:
                for j in range(i, 30):
                    programList.append(None)
                    return programList
        return programList

    if category == 'preference':
        # 전체에서 취향(여러 개)을 search해서 가장 최근 것들으 최대 30개 받아옴
        # 단 지름은 hardcoding 되어 있으므로 01028435533의 취향을
        programList.append(db.ReginalProgram.find_one(sort=[{"date", -1}]))
        for i in range(1, 30):
            temp = db.ReginalProgram.find_one(sort=[{"date", -1}], skip=i)
            if temp:
                programList.append(temp)
            else:
                for j in range(i, 30):
                    programList.append(None)
                    return programList
        return programList


    return programList


def getPostInfo(postId):    #ok(단 현재는 하드코딩 상태임)

    postInfo = db.ReginalProgram.find_one({'postId':postId})

    if postInfo:
        return {
            'title': postInfo.get('title'),
            'date': postInfo.get('date'),
            'location': postInfo.get('location'),
            'content': postInfo.get('content'),
            'reception': postInfo.get('reception'),
            'ask': postInfo.get('ask'),
            'poster': postInfo.get('poster')    # poster 값은 base64인코딩된 이미지이며 data:image/jpeg;base64, 접두사가 이미 추가되어 있습니다.
        }

    return None