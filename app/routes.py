from flask import Blueprint, request, jsonify, url_for, redirect
from app.models.chatModels import *
from chatbot import Chatbot
from asyncio import sleep
import threading
from queue import Queue, Empty

main = Blueprint('main', __name__)
#api = Api(main, doc='/api-docs')  # /api-docs 경로에 Swagger 문서 생성


chatHistory = []
myChatBot = Chatbot("gpt-4")
# 플래그 변수를 사용하여 이미 응답이 반환되었는지 추적
response_sent = False


@main.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        # 클라이언트로부터 받은 데이터를 처리
        action = request.json.get('action')

        if action == 'chat':
            # '대화하기' 버튼을 누른 경우 /chat 경로로 리다이렉트
            return redirect(url_for('main.chat'))
        elif action == 'recommend':
            # '추천하기' 버튼을 누른 경우 /recommend 경로로 리다이렉트
            return redirect(url_for('main.recommend'))
        else:
            return jsonify({"error": "잘못된 요청입니다."}), 400

    if request.method == 'GET':
        return jsonify({"message": "성공적으로 ""get"" 받았습니다."}), 200

'''
URL: /chat
Method: post
Description: 사용자가 입력한 메세지를 gpt api에 전달하고, 그에 대한 응답을 반환하는 엔드포인트

Request
{
    "userInput" : "user가 입력한 텍스트"
}

Response
200 ok[성공시]
{
    "aiContentSentence": "AI의 응답 또는 질문 텍스트"
}
400 Bad Request [잘못된 요청 시]
{
    "error" : "Invalid request format"
}
500 internal server error [서버 오류시]
{
    "error" : "Internal server error"
}
'''
@main.route('/chat', methods=['POST'])
def chat():
    global response_sent
    response_sent = False  # 새로운 요청이 들어올 때마다 플래그를 리셋

    if request.method == 'POST':
        try:
            '''
                일단 채은이가 해놓은대로 9번 대화하도록 만들어 놨음. -> ***나중에 수정 필수***
            '''
            if myChatBot.exchange_count >= 9:  # 9번 대화 교환
                print(f"대화 횟수를 초과하였으므로 대화를 할 수 없습니다.")
                return jsonify({
                    "error": "대화 횟수를 초과하였으므로 대화를 할 수 없습니다."
                }), 400


            # AI가 먼저 질문을 시작함
            if myChatBot.exchange_count == 0:  # 첫 질문일 때
                setAIContent(myChatBot)

            else:  # 첫 질문이 아닐 때
                userInput = request.json.get('userInput')   # request받아오기

                if myChatBot.exchange_count == 1:
                    if userInput == '\n':
                        return jsonify({
                            "aiContentSentence" : '1\n'
                        }), 200
                    else:
                        updateResponseTimeInQuestion(datetime.now())

                myChatBot.add_user_message(userInput)  # 사용자가 입력을 했다면 대화 히스토리에 추가
                myChatBot.exchange_count += 1

                # AI 응답
                setAIContent(myChatBot)


            return jsonify({
                "aiContentSentence": myChatBot.get_response_content()
            }), 200


        # 서버 내부 오류 발생 시 500 에러 반환
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@main.route('/recommend', methods=['POST', 'GET'])
def recommand():
    if request.method == 'POST':
        return jsonify({
            "message": "성공적으로 ""post"" 받았습니다."
        }), 200

    if request.method == 'GET':
        return jsonify({
            "message": "성공적으로 ""get"" 받았습니다."
        }), 200


@main.before_request
def clear_chat_history():
    # 현재 요청의 경로를 확인
    if request.path != '/chat':
        #global chatHistory
        #chatHistory.clear()  # chat_history 초기화

        myChatBot.chatBotInit() # gpt와 대화하기 전으로 돌아가기

