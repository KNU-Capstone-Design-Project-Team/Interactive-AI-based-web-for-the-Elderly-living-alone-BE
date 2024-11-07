import os
import openai
from dotenv import load_dotenv
from gtts import gTTS
import pygame
import chatbot
import speech_recognition as sr  # For STT

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
        recognizer = sr.Recognizer()
        attempts = 0  # 입력 시도 횟수

        while attempts < 3:
            with sr.Microphone() as source:
                # 주변 소음을 1초 동안 분석하여 인식 조정
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print(prompt + " (Listening...)")
                try:
                    audio = recognizer.listen(source, timeout=timeout)
                    input_text = recognizer.recognize_google(audio, language="ko-KR")
                    print("User (voice):", input_text)
                    return input_text
                except sr.WaitTimeoutError:
                    print("시간이 초과되었습니다.")
                except sr.UnknownValueError:
                    print("음성을 인식하지 못했습니다. 다시 시도해주세요.")
                except sr.RequestError:
                    print("STT 서비스 오류가 발생했습니다.")

                # 입력 시도 실패 시 시도 횟수 증가
                attempts += 1

        # 모든 시도가 실패하면 빈 문자열 반환
        print("입력을 여러 번 시도했으나 실패했습니다.")
        return ""

    def generate_summary(self):
        summary_request = [{"role": "system", "content": "이 대화를 50자 이내로 요약해줘."}]
        summary_request += self.context  # 전체 대화를 요약 요청에 포함
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=summary_request,
            max_tokens=50
        )
        self.summary = response['choices'][0]['message']['content']
        return self.summary  # 요약 문자열 반환

class TTSChatbot(Chatbot):
    def text_to_speech(self, text):
        # TTS 변환 및 파일 저장
        tts = gTTS(text=text, lang='ko')
        tts.save("response.mp3")
        
        # pygame을 사용해 mp3 파일 재생
        pygame.mixer.init()
        pygame.mixer.music.load("response.mp3")
        pygame.mixer.music.play()
        
        # 오디오가 끝날 때까지 대기
        while pygame.mixer.music.get_busy():
            continue

        pygame.mixer.quit()
        os.remove("response.mp3")  # 재생 후 파일 삭제

    def chat_loop(self):
        while self.exchange_count < 11:
            if self.exchange_count == 0:
                user_input = "너가 처음 질문하는 것처럼 일상적인 질문을 시작해줘. 한번에 한 문장만 말해. 일상적인 질문의 키워드는 식사, 날씨, 취미, 음악, 외출, 반려동물, 운동, 장보기, 추억 등이 있어."
            elif self.exchange_count == 9:
                user_input = self.get_input(600, "User: ") + " 이제 질문을 하지 말고 공감을 하며 대화를 끝내줘."
            else:
                user_input = self.get_input(600, "User: ")

            if user_input.strip() == '':
                summary = self.generate_summary()  # 요약 문자열 받기
                print("Summary:", summary)
                break
            else:
                self.add_user_message(user_input)

            response = self.send_request()
            self.add_response(response)
            ai_response = self.get_response_content()
            print("AI:", ai_response)
            self.text_to_speech(ai_response)
            self.exchange_count += 1

            if self.exchange_count == 11:
                summary = self.generate_summary()
                print("Summary:", summary)
                print("Conversation ended naturally.")

if __name__ == "__main__":
    chatbot = TTSChatbot("gpt-4")
    chatbot.chat_loop()
