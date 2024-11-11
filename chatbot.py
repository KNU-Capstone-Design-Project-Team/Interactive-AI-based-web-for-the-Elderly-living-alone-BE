import os
import openai
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

content = """독거노인 말동무 역할 사투리·오타 이해,띄어쓰기 없거나 어색해도 의미 파악 후 질문 이거가기 답변은 50자 이내"""

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
            user_input = "답하지 말고 먼저 일상적인 질문 한 문장 시작"
        
        elif self.exchange_count == 9:
            user_input += "질문 그만,공감하며 대화 끝내"
        
        
        self.add_user_message(user_input)
        self.exchange_count += 1

       
        response = self.send_request()
        self.add_response(response)
        
       
        return self.get_response_content()


if __name__ == "__main__":
    chatbot = Chatbot("gpt-4")
    
   