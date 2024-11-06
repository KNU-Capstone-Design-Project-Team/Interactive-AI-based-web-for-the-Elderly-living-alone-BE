from openai import OpenAI
import os
from app.models.chatModels import storeContext
import datetime

# context를 요약해달라 요청하는 함수
def requestContextStr(userInput):
    OpenAI.api_key = os.getenv("OPENAI_API_KEY")
    contextStr = ""
    
    # gpt한테 요청해서 context 받고(조건: userInput에 한줄만 적어달라고 해야 함.),
    # contextStr에 저장하기
    
    storeContext(contextStr)
'''
latestTaskStatus = {
    "status": "incomplete",
    "task": None,
    "lastRunTime": None,
    "newTask": False  # 새 작업 완료 시 True로 설정
}

def myScheduledTask():
    print("Scheduled task executed")
    latestTaskStatus["status"] = "completed"
    latestTaskStatus["lastRunTime"] = datetime.datetime.now().isoformat()
    latestTaskStatus["newTask"] = True  # 새 작업 발생을 알림

def sendTask():
    return latestTaskStatus.get('task')
'''

'''
# push api 설정 -> 알림 보내기
def pushAlarms(preConversationId):
    if preConversationId.responseRatio >= 50:
        #주의 알림을 보냄
    elif preConversationId.responseRatio >= 100:
        #경고 알림을 보냄
    else:
        pass
'''
# stt, tts