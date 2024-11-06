import speech_recognition as sr  # 추가된 부분
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Audio
import os
from chatbot import Chatbot
from common import OPEN_API_KEY

# 환경 변수 로드
load_dotenv()
client = OpenAI(api_key=OPEN_API_KEY)

class TTSChatbot(Chatbot):
    def __init__(self, model):
        super().__init__(model)
    
    def text_to_speech(self, text):
        response = client.audio.speech.create(
            model="tts-1",
            input=text,
            voice="shimmer",
            response_format="mp3",
            speed=1.1,
        )
        
        # 오디오 파일 저장
        speech_file_path = "tts_audio.mp3"
        with open(speech_file_path, "wb") as f:
            f.write(response.content)
        
        return Audio(speech_file_path)

    def stt_input(self, timeout=20):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Please say something:")
            r.adjust_for_ambient_noise(source)  # 주변 소음 조정
            audio = r.listen(source, timeout=timeout)

        try:
            # Google Speech Recognition을 사용하여 음성을 텍스트로 변환
            user_input = r.recognize_google(audio, language='ko')
            print("You said: " + user_input)
            return user_input
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return ''
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return ''

    # chat_loop에 TTS 추가
    def chat_loop(self):
        time = None
        while self.exchange_count < 9:
            if self.exchange_count == 0:  # 첫 질문일 때
                response = self.send_request()
                self.add_response(response)
                print("AI: ", self.get_response_content())
                self.text_to_speech(self.get_response_content())
                self.exchange_count += 1
                self.ai_count += 1

                # 사용자의 음성 입력을 기다림  
                user_input = self.stt_input(timeout=3600)

                if user_input=='':
                     self.add_response('죄송합니다. 알아듣지 못해서 그런데 다시 말씀해주실 수 있으신가요?라고 말해줘.')
                    # self.text_to_speech("죄송합니다. 알아듣지 못해서 그런데 다시 말씀해주실수 있으신가요?")
                if user_input:
                    self.add_user_message(user_input)
                    self.exchange_count += 1

            else:  # 첫 질문이 아닐 때
                response = self.send_request()
                self.add_response(response)
                self.exchange_count += 1
                self.ai_count += 1
                print("AI: ", self.get_response_content())
                self.text_to_speech(self.get_response_content())
                if self.exchange_count == 9:
                    print("Conversation ended naturally.")
                    continue
                
                # 사용자의 음성 입력을 기다림
                user_input = self.stt_input(timeout=20)
                if user_input=='':
                     self.add_response('죄송합니다. 알아듣지 못해서 그런데 다시 말씀해주실 수 있으신가요?라고 말해줘.')
                if user_input:
                    self.add_user_message(user_input)
                    self.exchange_count += 1

        return {
            "responseTime": time
        }

if __name__ == "__main__":
    chatbot = TTSChatbot("gpt-4")
    chatbot.chat_loop()
