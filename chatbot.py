import os
import threading
from queue import Queue, Empty
import openai
from dotenv import load_dotenv

# OpenAI API 키 설정
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 프롬프트 메시지
content = """당신은 독거노인의 말동무 역할입니다. 사투리나 오타가 있을 수 있으니, 이를 바르게 이해하고 질문을 이어가세요. 띄어쓰기가 없거나 문장이 어색해도 의미를 파악해 자연스럽게 대화를 진행하세요. 한번 대화할때 50자 이내로 답해야합니다."""

class Chatbot:
    def __init__(self, model):
        self.context = [{"role": "system", "content": content}]
        self.model = model
        self.exchange_count = 0  # 대화 횟수를 추적
        self.summary = ""  # 대화 요약을 저장

    def add_user_message(self, message):
        self.context.append({"role": "user", "content": message})
    
    def send_request(self):
        response = openai.ChatCompletion.create(
            model=self.model, 
            messages=self.context,
            temperature=0.7,
            max_tokens=100,
            frequency_penalty=0.5
        )
        return response

    def add_response(self, response):
        self.context.append({
            "role": response['choices'][0]['message']["role"],
            "content": response['choices'][0]['message']["content"]
        })

    def get_response_content(self):
        return self.context[-1]['content']
    
    def get_input(self, timeout, prompt):
        print(prompt, end="", flush=True)
        input_queue = Queue()
        
        def read_input():
            input_text = input()
            input_queue.put(input_text)
        
        input_thread = threading.Thread(target=read_input)
        input_thread.start()
        input_thread.join(timeout)
        
        if input_thread.is_alive():
            print("\n시간이 초과되었습니다.")
            input_thread.join()
            return "\n"
        
        try:
            return input_queue.get_nowait()
        except Empty:
            return "\n"

    def generate_summary(self):
        # 모든 대화를 요약 요청에 포함
        summary_request = [{"role": "system", "content": "이 대화를 50자 이내로 요약해줘."}]
        summary_request += self.context  # 전체 대화를 요약 요청에 포함
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=summary_request,
            max_tokens=50
        )
        self.summary = response['choices'][0]['message']['content']
        return self.summary  # 요약 문자열 반환

    def chat_loop(self):
        while self.exchange_count < 11:
            # 사용자 입력을 먼저 받음
            #user_input = self.get_input(600, "User: ")
            if self.exchange_count == 0:
                user_input = "이 말에 대답하지 말고 너가 처음 질문하는 것처럼 일상적인 질문을 시작해줘.한번에 한 문장만 말해.일상적인 질문의 키워드는 식사, 날씨, 취미, 음악, 외출, 반려동물, 운동, 장보기, 추억등이 있어. "
            elif self.exchange_count == 1:
                user_input = self.get_input(3600, "User: ")
                self.exchange_count +=1
            elif self.exchange_count ==9:
                user_input = self.get_input(600, "User: ")
                user_input = user_input+"이제 질문을 하지 말고 공감을 하며 대화를 끝내줘."
                self.exchange_count +=1
            else:
                user_input = self.get_input(600, "User: ")
                self.exchange_count +=1

            if user_input.strip() == '':
                summary = self.generate_summary()  # 요약 문자열 받기
                print("Summary:", summary)
                break
            else:
                self.add_user_message(user_input)
                #self.exchange_count += 1
            
            # 사용자 입력 후에만 AI 응답을 생성
            response = self.send_request()
            self.add_response(response)
            print("AI:", self.get_response_content())
            self.exchange_count += 1

            if self.exchange_count == 11:
                summary = self.generate_summary()  # 요약 문자열 받기
                print("Summary:", summary)
                print("Conversation ended naturally.")
         

if __name__ == "__main__":
    chatbot = Chatbot("gpt-4")
    chatbot.chat_loop()
