from datetime import datetime
from pprint import pprint
from dotenv import load_dotenv
from openai import OpenAI
import select
import threading
import sys
import time
from queue import Queue, Empty
import os

# OpenAI API 키 설정
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 프롬프트 메시지
content = """"당신의 역할은 대화형 AI 기반 독거노인 고독사 예방 플랫폼에서 사용자의 말동무 역할을 하는 것입니다.
대화를 셀 때는 당신이 한 말과 사용자가 한 말을 각각 1개씩 세어야 합니다. 예를 들어, 사용자가 '우리 대화 몇 개 했지?'라고 물었고, 당신이 '지금까지 9개의 대화를 나누었어요! 하나 더 나누고 마무리할까요?'라고 대답했다면, 이는 2개의 대화로 셉니다.

대화는 최소 4개에서 최대 10개로 이루어져야 하며, 9번째나 10번째 대화에서는 새로운 질문을 던지지 않고 사용자의 대답에 공감하며 자연스럽게 마무리해야 합니다.

사투리나 오타가 있을 수 있으니, 이를 바르게 이해하고 질문을 이어가세요. 띄어쓰기가 없거나 문장이 어색해도 의미를 파악해 자연스럽게 대화를 진행하세요. 예를 들어, '나는 오널 라면도먹었다'라는 말을 '나는 오늘 라면도 먹었다'로 이해하고 대화를 이어가면 됩니다.

대화를 자연스럽게 이끌기 위해 아래의 키워드를 사용하세요: 식사, 날씨, 취미, 음악, 외출, 반려동물, 운동, 장보기, 추억.

대화 예시:

"요즘 즐겨 드시는 음식이 있나요?"
"밥이랑 김치랑 뽂아ㅂ먹는걸 좋아한다."
"김치랑 밥을 볶아 먹으면 정말 맛있죠! 혹시 그 요리에 특별히 추가하는 재료가 있나요?"
"게란후라이도꾸워먹고 햄도 구워가지고 먹는다."
"계란후라이랑 햄까지 더하면 정말 든든하겠네요! 그럼 혹시 그 요리를 주로 언제 자주 드시나요?"
"어제점심으로 먹고 오늘 점심으로도 먹을 예정이다."
"연속으로 드실 만큼 정말 좋아하시나 봐요! 앞으로도 자주 드실 계획이신가요?"
"질리기전까지는그럴거 같다."
"질리기 전까지는 계속 즐기실 것 같네요! 맛있게 드시고 좋은 하루 보내세요."
9번째 대화에서 대화를 자연스럽게 마무리했습니다.
이제 질문을 던져보세요."

"""

#클래스 chatbot은 AI 모델과의 대화 흐름을 관리하는 역할.
#gpt 기반 모델과 대화를 나누고, 사용자의 입력을 추가하고, 모델의 응답을 받아 처리하는 구조로 설게됨.
class Chatbot:
    
    #클래스 객체를 생성하고 초기화
    #model : 대화에 사용할 모델을 지정함.
    #self.context : 시스템 메시지를 담은 리스트, 대화의 맥락을 저장함.처음에는 시스템 메시지만 포함됨.
    def __init__(self, model):
        self.context = [{"role": "system", "content": content}]
        self.model = model
        self.exchange_count = 0  # 대화 횟수를 추적
        self.ai_count=0 #ai 대화 횟수

    def chatBotInit(self):
        self.context = [{"role": "system", "content": content}] #프롬프트 엔지니어링으로 지금까지의 내역 전부를 잊어버리라고 명령
        self.exchange_count = 0  # 대화 횟수를 추적
        self.ai_count = 0  # ai 대화 횟수
    

    #사용자가 메시지를 self.context에 추가하는 함수
    #message :사용자가 입력한 메시지
    #대화 히스토리에 "role":"user"로 사용자의 메시지를 저장
    def add_user_message(self, message):
        self.context.append({"role": "user", "content": message})
    
    #AI 모델에 요청을 보내 응답을 받음, 그 결과를 반환하는 함수
    #client.chat.completions.create: 지정된 모델과 대화 맥락을 바탕으로 AI 응답을 생성함.
    #model_dump():반환된 응답 객체를 JSON 형식으로 변환하는 역할을 함.
    def send_request(self):
        response = client.chat.completions.create(
            model=self.model, 
            messages=self.context,
            temperature=0.7,
            top_p=1,
            max_tokens=256,
            frequency_penalty=0.5
        ).model_dump()
        return response

    #AI 응답을 대화 히스토리(self.context)에 추가함
    #response:AI의 응답으로, response['choices'][0]['message']에서 AI가 보낸 메시지와 그 역할을 가져와 저장함.
    #AI의 응답은 "role":"assistant"으로 저장됨.
    def add_response(self, response):
        self.context.append({
            "role": response['choices'][0]['message']["role"],
            "content": response['choices'][0]['message']["content"]
        })


    #가장 최근 응답을 확인하고 가져옴 
    #self.context에서 마지막 메시지의 "content"를 반환
    def get_response_content(self):
        return self.context[-1]['content']
    
    #사용자의 입력을 비동기적으로 받기 위해 스레드와 큐를 사용하여, 
    #입력 대기중에 타임아웃을 설정하고 타임아웃이 발생하면 기본값을 반환하는 구조임
    def get_input(self, timeout, prompt):
        print(prompt, end="", flush=True) #프롬프트 메시지 출력,end=""를 사용하여 출력 후 개행하지 않고 flush=True로 즉시 화면에 출력되도록 함.

        # 입력을 비동기적으로 받기 위한 Queue와 스레드 생성
        input_queue = Queue()#큐 생성

        def read_input():#입력값을 받아서 큐에 저장하는 함수
            input_text = input()
            input_queue.put(input_text)  # 입력값을 Queue에 저장

        input_thread = threading.Thread(target=read_input)
        input_thread.start()#생성된 스레드 시작
        input_thread.join(timeout)  # timeout 시간만큼 스레드 대기

        if input_thread.is_alive():#스레드가 여전히 실행중인지를 확인
            print("\n시간이 초과되었습니다.")
            input_thread.join()  # 스레드를 완전히 종료
            return "\n"  # 기본값 반환 (또는 원하는 값으로 설정)
        
        # 입력값이 Queue에 들어왔다면 반환
        try:
            return input_queue.get_nowait()#입력이 성공적으로 큐에 저장되었을 경우, 그 값을 즉시 반환
        except Empty:#큐에 값이 없을 경우 기본값 반환
            return "\n"  # 입력값이 없으면 기본값 반환

    #chat_loop() 함수: 대화의 핵심 루프. AI가 첫 질문을 한 후, 사용자가 입력하면 AI가 응답을 다시 생성. 
    # 대화 횟수는 AI와 사용자 각각의 메시지를 하나씩 세어 총 9번의 메시지 교환 후 종료.
    def chat_loop(self):
        time = None
        # AI가 먼저 질문을 시작함
        while self.exchange_count < 9:
            if self.exchange_count == 0:  # 첫 질문일 때
                response = self.send_request()  # AI의 첫 응답
                self.add_response(response)
                print("AI: ", self.get_response_content())
                self.exchange_count += 1
                self.ai_count += 1

                # 사용자의 입력을 1시간(3600초) 동안 기다림  
                user_input = self.get_input(3600, "User: ")

                # 사용자가 입력을 했다면 대화 히스토리에 추가
                if user_input:
                    self.add_user_message(user_input)
                    self.exchange_count += 1

            else:  # 첫 질문이 아닐 때
                response = self.send_request()  # AI 응답
                self.add_response(response)
                self.exchange_count += 1
                self.ai_count += 1
                print("AI: ", self.get_response_content())
                if self.exchange_count == 9:
                    print("Conversation ended naturally.")  # 대화 종료
                # 사용자의 입력을 10분(600초) 동안 기다림
                #input_with_timeout = InputWithTimeout(timeout=600)
                user_input = self.get_input(600, "User: ")

                

                if user_input == '\n':#빈문자열이 날라오면 break
                    break
                elif user_input:
                    self.add_user_message(user_input)# 사용자가 입력을 했다면 대화 히스토리에 추가
                    self.exchange_count += 1
       

        return {
            "responseTime": time
        }

if __name__ == "__main__":
    chatbot = Chatbot("gpt-4")
    chatbot.chat_loop()
