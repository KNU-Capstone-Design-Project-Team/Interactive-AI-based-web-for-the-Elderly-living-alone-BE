import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pymongo import MongoClient

'''
    AI 대화
'''
load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))

def getDate():
    today = datetime.now().strftime('%Y.%m.%d')

    return today

# 새로운 채팅을 생성하는 함수
def createConversation():
    # 날짜는 매일 새로 생성되므로 하루에 한 번만 Conversation을 생성
    today = getDate()

    # MongoDB에서 현재 앱의 MongoDB 데이터베이스 사용
    db = client.ElderCareNet

    # 오늘 날짜에 해당하는 채팅이 이미 있는지 확인
    existingConversation = db.Conversation.find_one({"date": today})

    if not existingConversation:
        newConversation = {
            "date": today,
            "responseRatio": 0.0  # 기본값
        }
        db.Conversation.insert_one(newConversation)
        print(f"New conversation created for {today}")
    else:
        print(f"Conversation for {today} already exists.")

# 시간마다 질문할 첫 question을 생성
def createQuestion(conversationId):
    now = datetime.now()
    db = client.ElderCareNet

    '''
    만약 현재 conversation_id를 가지고 있는 question이 없으면 time = 30
    question이 한개라도 존재한다면 time = 10
    '''
    existingQuestion = db.Question.find_one({"Conversation_id": conversationId})

    if not existingQuestion:
        time = 30
    else:
        time = 10

    newQuestion = {
        "Conversation_id": conversationId,
        "hour": now.hour,
        "startTime": now,
        "endTime": now + timedelta(minutes=time),  # 사용자가 답변할 수 있는 시간 10분 or 30분
        "responseTime": None,  # 응답 시간은 처음엔 None으로 설정
    }
    db.Question.insert_one(newQuestion)
    print(f"New question created for conversation {conversationId}")


# 시간당 처음 질문의 응답 시간을 업데이트
# ((+추가구현요망)만약 responseTime이 오차범위 내로 start time과 같다면)
def updateQuestion(responseTime):
    now = datetime.now()
    today = now.strftime('%Y.%m.%d')
    db = client.ElderCareNet

    convId = db.Conversation.find_one({"date": today})
    print(f"conversation find successfully")
    q = db.Question.find_one({"Conversation_id":(convId.get("_id"))}, {"hour":(now.hour)})
    print(f"question find successfully")
    db.Question.update_one({"_id": q.get('_id')}, {"$set":{"responseTime": responseTime}})

    print(f"update question successfully and response time is {responseTime}")


# 응답 기록하는 함수
def recordResponse(questionId):
    now = datetime.now()

    db = client.ElderCareNet

    # Question 업데이트 (응답 시간 기록)
    db.Question.update_one(
        {"_id": questionId},
        {"$set": {"responseTime": now}}
    )
    print(f"Response recorded for question {questionId}")


# 응답률 계산 함수
def calculateResponseRatio():
    db = client.ElderCareNet
    today = getDate()

    convdb = db.Conversation.find_one({"date": today})
    conversationId = convdb.get("_id")  # 오늘 자 conversation _id

    # 해당 Conversation의 질문들을 모두 가져옴
    questions = db.Question.find({"_id": conversationId})

    totalQuestions = questions.count()
    respondedQuestions = db.Question.count_documents({
        "_id": conversationId,
        "responseTime": {"$ne": None}
    })

    # 응답률 계산
    if totalQuestions > 0:
        responseRatio = respondedQuestions / totalQuestions * 100
    else:
        responseRatio = 0

    # Conversation에 응답률 저장
    db.Conversation.update_one(
        {"_id": conversationId},
        {"$set": {"responseRatio": responseRatio}}
    )


# gpt 대화
'''
    (init)첫번째로 services/gptGetReponse userInput에 initPropmt 넣어주고 호출해줌
    question 생성은 이미 됐으니까 사용자에게 "응답이 오면" conversation->question->response time = now

    (chat)이 다음 2번째로 services/gptGetReponse 호출해서 핑퐁 -> while 써서 response 받아오면 user도 주는 형식

    *(context)그 사이에 대화 개수 세어서 대화 5개정도 하면
    저장한 대화내용을 gpt에게 넘겨서 한 문장으로 요약해 달라고 한 후(-> services/requestContextStr())
    그 문장(contextStr)을 storeContext로 넘김.

    (terminate)세션 종료 조건도 여기 적어야 함.
    if 대화내용이 이러하면 then terminate.
'''
def setAIContent(myChatBot):
    response = myChatBot.send_request()  # AI의 첫 응답
    myChatBot.add_response(response)

    print("AI: ", myChatBot.get_response_content())

    myChatBot.exchange_count += 1  # 대화 횟수를 추적
    myChatBot.ai_count += 1  # ai 대화 횟수 카운트

    return None


# gpt에서 세션 중 요약된 context str을 저장하는 함수
def storeContext(contextStr):
    db = client.ElderCareNet
    today = getDate()

    convdb = db.Conversation.find_one({"date": today})
    convId = convdb.get("_id")    #오늘 자 conversation _id

    newContext = {
        "_id": convId,
        "context" : contextStr
    }
    db.Context.insert_one(newContext)
    print(f"Partial context is stored : {contextStr}")

