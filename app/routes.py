from flask import Blueprint, request, jsonify, url_for, redirect
from app.models.chatModels import *
from app.models.joinMembershipModels import *
from app.models.loginInfoModels import *
from app.models.noticeModels import *
from chatbot import Chatbot
from asyncio import sleep

main = Blueprint('main', __name__)


chatHistory = []
myChatBot = Chatbot("gpt-4")
# 플래그 변수를 사용하여 이미 응답이 반환되었는지 추적
response_sent = False

'''
전체적으로 추가 구현해야할 사항:
    * JWT 토큰 라이브러리를 사용해서 인증 상태를 유지하는 거 메소드마다 추가하기

'''

@main.route('/', methods=['POST'])
def login():
    try:
        '''
        +) JWT 토근 관련 code
        '''
        pass
    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/join', methods=['POST, GET'])
def join():
    try:
        if request.method == 'POST':
            category = request.json.get('category')
            if category == 'supervisor':
                return redirect(url_for(joinSupervisor(1)))
            elif category == 'senior':
                return redirect(url_for(joinSenior(1)))
            else :
                return jsonify({
                    "message": "잘못된 요청입니다."
                }), 400
    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/join/senior/<int:joinId>', methods=['POST, GET'])
def joinSenior(joinId):
    try:
        if request.method == 'GET':
            if isinstance(joinId, int):
                if (1 <= joinId <= 5):
                    return jsonify({
                        "message" : "get request successfully."
                    }), 200
                else:
                    return jsonify({
                        "message": "parameter is not integer."
                    }), 400
            else:
                return jsonify({
                    "message": "parameter is not valid value."
                }), 400

        if request.method == 'POST':
            if joinId == 1:
                username = request.json.get('username')
                loginId = request.json.get('loginId')
                password = request.json.get('password')
                phoneNumber = request.json.get('phoneNumber')
                
                '''
                    code : DB에 senior 유저 정보 저장하기
                '''
                
            if joinId == 2:
                '''
                이름 보내줘야하는지 프론트랑 상의하기
                '''

                year = request.json.get('year')
                month = request.json.get('month')
                day = request.json.get('day')

                '''
                    code : DB에 senior 생일 정보 저장하기
                '''

            if joinId == 3:
                si = request.json.get('si')
                gu = request.json.get('gu')
                dong = request.json.get('dong')

                '''
                    code : DB에 senior 거주 정보 저장하기
                '''

            if joinId == 4:
                others = request.json.get('others')
                if others == True:
                    return redirect(url_for(joinAddInfo))

                
            if joinId == 5:
                connectionNum = request.json.get('connectionNum')

                '''
                # 보호자 연결변호로 DB내에 있는 보호자와 연결하기
                '''
                return redirect(url_for(welcome))

            # '다음으로' 버튼 눌렀을 시,
            toTheNext = request.json.get('toTheNext')
            if toTheNext == False:
                return jsonify({
                    "message": "잘못된 요청입니다."
                }), 400
        return redirect(url_for(joinSenior(joinId+1)))

    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/join/senior/<int:joinId>/addinfo', methods=['POST, GET'])
def joinAddInfo():
    try:
        pass
    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/join/supervisor/<int:joinId>', methods=['POST, GET'])
def joinSupervisor(joinId):
    try:
        if request.method == 'GET':
            if isinstance(joinId, int):
                if (1 <= joinId <= 2):
                    return jsonify({
                        "message" : "get joinId successfully."
                    }), 200
                else:
                    return jsonify({
                        "message": "parameter is not integer."
                    }), 400
            else:
                return jsonify({
                    "message": "parameter is not valid value."
                }), 400

        if request.method == 'POST':
            if joinId == 1:
                username = request.json.get('username')
                loginId = request.json.get('loginId')
                password = request.json.get('password')
                phoneNumber = request.json.get('phoneNumber')

                '''
                    code : DB에 senior 유저 정보 저장하기
                '''

            if joinId == 2:
                produceConnectionNum()

                return redirect(url_for(welcome))

            # '다음으로' 버튼 눌렀을 시,
            toTheNext = request.json.get('toTheNext')
            if toTheNext == False:
                return jsonify({
                    "message": "잘못된 요청입니다."
                }), 400
        return redirect(url_for(joinSupervisor(joinId + 1)))

    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/welcome/<loginId>', methods=['POST, GET'])
def welcome():
    try:
        # if -> loginId가 senior에서 찾을 수 있다면
        # return redirect(url_for(joinSenior(welcomeSenior)))

        # if -> loginId가 supervisor에서 찾을 수 있다면
        # return redirect(url_for(joinSenior(welcomeSupervisor)))

        pass
    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/welcome/senior/<int:guideId>', methods=['POST, GET'])
def welcomeSenior():
    try:
        pass
    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/welcome/supervisor/<int:guideId>', methods=['POST, GET'])
def welcomeSupervisor():
    try:
        pass
    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/senior/<loginId>', methods=['POST', 'GET'])
def seniorHome(loginId):
    try:
        if request.method == 'POST':
            # 클라이언트로부터 받은 데이터를 처리
            action = request.json.get('action')

            if action == 'chat':
                # '대화하기' 버튼을 누른 경우 /chat 경로로 리다이렉트
                return redirect(url_for(seniorChat))
            elif action == 'recommend':
                # '추천하기' 버튼을 누른 경우 /recommend 경로로 리다이렉트
                return redirect(url_for(seniorRecommend))
            else:
                return jsonify({"error": "잘못된 요청입니다."}), 400

    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/supervisor/<loginId>', methods=['POST', 'GET'])
def supervisorHome(loginId):
    try:
        if request.method == 'POST':
            # 클라이언트로부터 받은 데이터를 처리
            action = request.json.get('action')

            if action == 'notify':
                # '대화하기' 버튼을 누른 경우 /chat 경로로 리다이렉트
                return redirect(url_for(supervisorNotice))
            elif action == 'recommend':
                # '추천하기' 버튼을 누른 경우 /recommend 경로로 리다이렉트
                return redirect(url_for(supervisorStats))
            else:
                return jsonify({"error": "잘못된 요청입니다."}), 400

    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/senior/<loginId>/chat', methods=['POST'])
def seniorChat(loginId):
    global response_sent
    response_sent = False  # 새로운 요청이 들어올 때마다 플래그를 리셋

    try:
        if request.method == 'GET':
            if (isLoginIdInDB(loginId) == True):
                return jsonify({
                    "message": "" + loginId + "exists."
                }), 200
            else:
                return jsonify({
                    "error": "" + loginId + "does not exists."
                }), 400

        if request.method == 'POST':
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


@main.route('/senior/<loginId>/recommend', methods=['POST', 'GET'])
def seniorRecommend(loginId):
    try:
        if request.method == 'GET':
            '''
            기본 : 전체
            가장 최근의 공공데이터들을 DB에서 30개를 추출해서 최대 30개를 LIST로 보내줌
            '''

            return jsonify({
                "message": "성공적으로 ""GET"" 받았습니다."
            }), 200

        if request.method == 'POST':
            '''
                전체, 위치, 취향
                category마다 해당되는 공공데이터들을 DB에서 30개를 추출해서
                프론트에서 category마다 요청이 들어오면
                해당되는 것들의 데이터들을 최대 30개씩 보내 줌.
                
                ->일단을 하드코딩으로 백쪽에서 DB에 30개의 데이터를 넣어놓고 주는 방식으로 하는데
                ->공공데이터 API를 쓰려면 위치 기반의 데이터를 나누는 방식이랑
                취향 기반의 데이터를 나누는 방식(EX. GPT에 프롬프트 넣어서 구분해서 넣는다던지)을 나누어서
                DB에 저장한 후, 하는 걸 하루 단위로 하는 방식으로 코딩하기
            '''

            return jsonify({
                "message": "성공적으로 ""POST"" 받았습니다."
            }), 200


    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/senior/<loginId>/recommend/<int:postId>', methods=['POST', 'GET'])
def seniorRecommendPost(loginId):
    try:
        if request.method == 'POST':
            '''
            통계 데이터 요청받으면 json으로 보내주기
            '''

            return jsonify({
                "message": "성공적으로 ""post"" 받았습니다."
            }), 200


    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/supervisor/<loginId>/notice', methods=['POST', 'GET'])
def supervisorNotice(loginId):
    try:
        if request.method == 'GET':
            if (isLoginIdInDB(loginId) == True):
                return jsonify({
                    "message": "" + loginId + "exists."
                }), 200
            else:
                return jsonify({
                    "error": "" + loginId + "does not exists."
                }), 400

        if request.method == 'POST':
            '''
            알림페이지의 최근 N일 까지의 응답률을 달라고 요청보내주면
            백에서 현재 <=N 까지의 최근 응답률들을 전부 JSON으로 list를 보내 줌. 
            '''
            noticeList = []
            '''
            for i in range(10):
                if (responseRatio)
            '''
            return jsonify({
                "message": "성공적으로 ""post"" 받았습니다."
            }), 200


    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/senior/<loginId>/stats', methods=['POST', 'GET'])
def supervisorStats(loginId):
    try:
        if request.method == 'POST':
            '''
            통계 데이터 요청받으면 json으로 보내주기
            '''

            return jsonify({
                "message": "성공적으로 ""post"" 받았습니다."
            }), 200


    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.before_request
def clear_chat_history():
    # 현재 요청의 경로를 확인
    if request.path != '/chat':
        #global chatHistory
        #chatHistory.clear()  # chat_history 초기화

        myChatBot.chatBotInit() # gpt와 대화하기 전으로 돌아가기

