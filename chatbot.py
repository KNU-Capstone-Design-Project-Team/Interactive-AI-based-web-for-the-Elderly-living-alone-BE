import os
import openai
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

content = """당신은 독거노인의 말동무 역할입니다. 사투리나 오타가 있을 수 있으니, 이를 바르게 이해하고 질문을 이어가세요. 띄어쓰기가 없거나 문장이 어색해도 의미를 파악해 자연스럽게 대화를 진행하세요. 한번 대화할때 50자 이내로 답해야합니다."""

class Chatbot:
    def __init__(self, model):
        self.context = [{"role": "system", "content": content}]
        self.model = model
        self.exchange_count = 0  
        self.summary = "" 
        self.ai_count = 0  

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

   
    def get_response(self, user_input):
        if self.exchange_count >= 11:
            return None


        if self.exchange_count == 0:
            user_input = "이 말에 대답하지 말고 너가 처음 질문하는 것처럼 일상적인 질문을 시작해줘. 한번에 한 문장만 말해. 일상적인 질문의 키워드는 식사, 날씨, 취미, 음악, 외출, 반려동물, 운동, 장보기, 추억 등이 있어."
        
        elif self.exchange_count == 9:
            user_input += " 이제 질문을 하지 말고 공감을 하며 대화를 끝내줘."
        
        
        self.add_user_message(user_input)
        self.exchange_count += 1

       
        response = self.send_request()
        self.add_response(response)
        
       
        return self.get_response_content()


if __name__ == "__main__":
    chatbot = Chatbot("gpt-4")
    
   