from openai import OpenAI
import os
from app.models.chatModels import storeContext

# context를 요약해달라 요청하는 함수
def requestContextStr(userInput):
    OpenAI.api_key = os.getenv("OPENAI_API_KEY")
    contextStr = ""
    
    # gpt한테 요청해서 context 받고(조건: userInput에 한줄만 적어달라고 해야 함.),
    # contextStr에 저장하기
    
    storeContext(contextStr)

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