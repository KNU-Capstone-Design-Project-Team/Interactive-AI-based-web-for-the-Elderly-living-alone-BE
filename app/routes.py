from flask import Blueprint, request, jsonify, url_for, redirect
from app.models.chatModels import *
from chatbot import Chatbot

main = Blueprint('main', __name__)
#api = Api(main, doc='/api-docs')  # /api-docs 경로에 Swagger 문서 생성


chatHistory = []
myChatBot = Chatbot("gpt-4")


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


@main.route('/chat', methods=['POST', 'GET'])
def chat():
    if request.method == 'POST':

        if myChatBot.exchange_count >= 9:  # 9번 대화 교환
            print(f"대화 횟수를 초과하였으므로 대화를 할 수 없습니다.")
            return jsonify({
                "error": "대화 횟수를 초과하였으므로 대화를 할 수 없습니다."
            }), 400


        if myChatBot.exchange_count == 0:  # 첫 질문일때
            setAIContent(myChatBot)
            chatHistory.append({"ai": myChatBot.get_response_content()})

        else:  # 첫 질문이 아닐때
            userInput = request.json.get('userInput')  # 사용자 입력
            myChatBot.add_user_message(userInput)
            chatHistory.append({"user": userInput})

            # 사용자의 첫 질문의 첫 대답일 경우
            if myChatBot.ai_count == 1:
                updateQuestion(datetime.now())
            myChatBot.exchange_count += 1

            # 사용자 입력 후 응답 생성
            setAIContent(myChatBot)
            chatHistory.append({"ai": myChatBot.get_response_content()})


        return jsonify({
            "aiContentSentence": myChatBot.get_response_content(),
            "message": "대화가 성공적으로 종료되었습니다."
        }), 200

    if request.method == 'GET':
        return jsonify(chatHistory), 200


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
        global chatHistory
        chatHistory.clear()  # chat_history 초기화

        myChatBot.chatBotInit() # gpt와 대화하기 전으로 돌아가기

