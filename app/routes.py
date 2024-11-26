from flask import Blueprint, request, jsonify, url_for, redirect
from app.models.chatModels import *
from app.models.joinMembershipModels import *
from app.services.joinMembershipServices import *
from app.models.localProgramModels import *
from app.models.loginInfoModels import *
from app.models.noticeModels import *
from app.services.chatServices import *
from chatbot import Chatbot
from chatbot1 import Chatbot1
from datetime import datetime
from app.services.loginInfoServices import *
import asyncio
import signal


main = Blueprint('main', __name__)
service = MembershipService()

chatHistory = []
myChatBot = Chatbot1("gpt-4")
# 플래그 변수를 사용하여 이미 응답이 반환되었는지 추적
response_sent = False

'''
전체적으로 추가 구현해야할 사항:
    * JWT 토큰 라이브러리를 사용해서 인증 상태를 유지하는 거 메소드마다 추가하기
'''

#에러 처리 공통 함수
def error_response(message,status_code=400):
    return jsonify({"message":message}),status_code
@main.route('/test', methods=['GET', 'POST'])
def test():
    return jsonify({"message":"1"}), 200


@main.route('/login', methods=['POST'])
def login():
    try:
        loginId = request.json.get("loginId")
        password = request.json.get("password")

        if not loginId or not password:
            return jsonify({"error": "loginId and password are required"}), 400

        service = LoginInfoService()
        response, status_code = service.authenticate_user(loginId, password)

        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/join', methods=['POST'])
def joinSenior():
    try: 
        if request.method == 'POST':
                 if request.json.get('usertype') == "senior":
          
                    username = request.json.get('username')
                    loginId = request.json.get('loginId')
                    password = request.json.get('password')
                    phoneNumber = request.json.get('phoneNumber')

                    # DB에 senior 유저 정보 저장
                    result = service.register_senior_basic_info(username, loginId, password, phoneNumber)
                    if result == "success":
                        return jsonify({"message": "User information saved successfully."}), 200
                    else:
                        return jsonify({"error": "Failed to save user information."}), 500

                
                    year = request.json.get('year')
                    month = request.json.get('month')
                    day = request.json.get('day')

                    # DB에 생일 정보 저장
                    result = service.update_senior_birthdate(loginId, year, month, day)
                    if result == "success":
                        return jsonify({"message": "Birthday information saved successfully."}), 200
                    else:
                        return jsonify({"error": "Failed to save birthday information."}), 500

               
                    si = request.json.get('si')
                    gu = request.json.get('gu')
                    dong = request.json.get('dong')

                    # DB에 거주 정보 저장
                    result = service.update_senior_address(loginId, si, gu, dong)
                    if result == "success":
                        return jsonify({"message": "Residence information saved successfully."}), 200
                    else:
                        return jsonify({"error": "Failed to save residence information."}), 500

                
                    activities = request.json.get('activities', [])  # 사용자가 선택한 활동 리스트
                    
                    # 사용자가 버튼에서 선택한 활동들 저장
                    if activities:
                        for activity in activities:
                            if activity not in ['요리', '운동', '바둑', '노래', '춤', '서예', '스마트폰', '식물재배']:
                                return jsonify({"error": f"Invalid activity: {activity}"}), 400

                            result = service.save_senior_activity(loginId, activity)
                            if result != "success":
                                return jsonify({"error": f"Failed to save activity: {activity}"}), 500


                
                    connectionNum = request.json.get('connectionNum')

                    # 보호자 연결 번호로 DB 내 보호자와 연결
                    result = service.connect_senior_to_guardian(loginId, connectionNum)
                    if result == "success":
                        return redirect(url_for('main.welcome', loginId=loginId))
                    else:
                        return jsonify({"error": "Failed to link guardian."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


'''
    ***** CHAT *****
'''
messageQueue = []
shutdown_flag = False  # 서버 종료 시 비동기 작업 중단을 위한 플래그 변수

# 스케줄링 작업 (특정 시간에 메시지를 전송함)
def scheduledTask():    #ok
    # create question
    today = datetime.now().strftime('%Y.%m.%d')
    temp = db.Conversation.find_one({"date": today})
    createQuestion(temp.get("_id"))

    # 비동기
    #conv = setAIContent(myChatBot)
    response = myChatBot.send_request()  # AI의 첫 응답
    myChatBot.add_response(response)

    print("AI: ", myChatBot.get_response_content())

    myChatBot.exchange_count += 1  # 대화 횟수를 추적
    myChatBot.ai_count += 1  # ai 대화 횟수 카운트
    messageQueue.append(myChatBot.get_response_content())  # queue에 사용자 입력을 push -> 담아놨다가 시간되면 ...

    print(f"create first question at time.")

def popAllMessageQueue():
    if messageQueue:
        messageQueue.clear()

'''
# Long Polling 엔드포인트
@main.route('/chatPoll', methods=['GET'])
def poll():
    def waitForMessage():
        while not messageQueue:
            time.sleep(1)  # 메시지가 없을 때 대기
        return messageQueue.pop(0)  # 새로운 메시지가 있으면 큐에서 제거하여 반환

    # 새로운 메시지를 대기하고 반환하는 함수를 호출
    message = waitForMessage()
    return jsonify({"message": message}), 200
'''
# Long Polling 엔드포인트
@main.route('/chatLongPoll', methods=['GET'])   #일단 예외처리 빼고 ok
async def longPoll():
    try:
        # 새로운 메시지를 대기하고 반환하는 함수를 호출
        while not messageQueue:
            '''
            if shutdown_flag:  # 종료 플래그를 확인하여 루프 탈출
                return jsonify({"error": "Server is shutting down"}), 503
            '''
            await asyncio.sleep(1)  # 메시지가 없을 때 대기

        # 새로운 메시지가 있으면 큐에서 제거하여 반환
        message = messageQueue.pop(0)
        return jsonify({"message": message}), 200
    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/chatShortPoll', methods=['GET'])   #일단 예외처리 빼고 ok
async def shortPoll():
    try:
    # 새로운 메시지가 있으면 큐에서 제거하여 반환
        if (messageQueue):
            message = messageQueue.pop(0)
            return jsonify({"message": message}), 200
        else:
            return jsonify({"error": "not message"}), 400
    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500
'''
# Flask 서버 종료 시 플래그 업데이트
def shutdown_handler(*args):
    global shutdown_flag
    shutdown_flag = True

# 종료 시그널을 받으면 shutdown_handler가 호출되어 플래그를 변경
signal.signal(signal.SIGINT, shutdown_handler)  # Ctrl+C 시그널
signal.signal(signal.SIGTERM, shutdown_handler)  # 시스템 종료 시그널
'''
@main.route('/senior/<loginId>/chat', methods=['GET', 'POST']) #비동기 ok-ok
def seniorChat(loginId):
    global response_sent
    response_sent = False  # 새로운 요청이 들어올 때마다 플래그를 리셋

    if request.method == 'GET':
        try:
            if (isLoginIdInDB(loginId) == False):
                return jsonify({
                    "error": "" + loginId + "does not exists."
                }), 400
            else:
                return jsonify({
                    "message": "" + loginId + "exists."
                }), 200

        # 서버 내부 오류 발생 시 500 에러 반환
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == 'POST':
        '''
            gpt와 행복 어르신이 9번 대화하도록 함.
        '''
        try:
            # 혹시 모를 예외처리
            if myChatBot.exchange_count >= 9:  # 9번 대화 교환
                print(f"The number of conversations has been exceeded.")
                return jsonify({
                    "error": "The number of conversations has been exceeded."
                }), 429

            # AI가 먼저 질문을 시작하는건 이미 비동기로 받아옴
            if myChatBot.exchange_count == 0:  # 대화가 끝나서 초기화된 상태 -> 대화를 할 수 없는 상태
                print(f"The number of conversations has been exceeded.")
                return jsonify({
                    "error": "The number of conversations has been exceeded."
                }), 429

            else:  # 첫 질문이 아닐 때
                userInput = request.json.get('userInput')   # request받아오기

                if myChatBot.exchange_count == 1:
                    if userInput == '\n':
                        # 대화 종료한 상태(응답안햇다고 저장하기 -> 사실 코드짤필요x 이미 None임.
                        return jsonify({
                            "message": "Accept the blank request and end the conversation."
                        }), 204
                    else:
                        updateResponseTimeInQuestion(datetime.now())

                if userInput == '\n':
                    '''
                    대화 종료한 상태를 저장하기
                    '''
                    return jsonify({
                        "message": "Accept the blank request and end the conversation."
                    }), 204

                # 사용자가 입력을 했다면 대화 히스토리에 추가
                myChatBot.add_user_message(userInput)
                myChatBot.exchange_count += 1

                # AI 응답
                message = setAIContent(myChatBot)
                if (myChatBot.exchange_count == 9):
                    myChatBot.exchange_count = 0  # 대화 횟수를 추적
                    myChatBot.ai_count = 0  # ai 대화 횟수

            return jsonify({
                "aiContentSentence": message
            }), 200


        # 서버 내부 오류 발생 시 500 에러 반환
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({
            "message": "Method not allowed."
        }), 405


@main.route('/senior/<loginId>/recommend', methods=['POST', 'GET']) # 구현중
def seniorRecommend(loginId):
    try:
        if request.method == 'GET':
            '''
                #__init__에서 공공데이터를 받아옴 -> PreferredCategory, MatchProgram을 이미 구별해놓은 상태
                #그래서 전체 : "RegionalProgram"에서 date가 오늘로부터 가장 빠른 것부터 최대 30개를 보내줌.
                # 위치 : "MatchProgram"에서 date가 오늘로부터 가장 빠른 것부터 최대 30개를 보내줌.
                # 취향 : "PreferredCategory"에서 date가 오늘로부터 가장 빠른 것부터 최대 30개를 보내줌.
            '''
            # loginId가 실제 user인지 확인
            if (isLoginIdInDB(loginId) == False):
                return jsonify({
                    "error": "" + loginId + "does not exists."
                }), 400

            # 전체, 위치, 취향
            category = request.args.get('category', 'total')

            if category == 'total' or category == 'location' or category == 'preference':
                pageList = get30totalPrograms(category)
            else:
                return jsonify({"error": "Invalid request format"}), 400

            return jsonify({
                "pageList": pageList,
                "message": "Returned the data list for that category successfully and " + loginId + "exists."
            }), 200

        elif request.method == 'POST':
            ''' 
               2. post를 request로 받아옴
                postId를 request로 얻어오면 이를 redirection하도록 값을 넘겨줌
            '''
            postId = request.json.get('postId')
            
            return redirect(url_for('main.seniorRecommendPost', loginId=loginId, postId=postId))
        else:
            return jsonify({
                "message": "Method not allowed."
            }), 405

    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/senior/<loginId>/recommend/<int:postId>', methods=['GET'])    #ok-사진만 받아오기 확인되면 다른건 다 ok
def seniorRecommendPost(loginId, postId):
    try:
        if request.method == 'GET':
            # loginId가 실제 user인지 확인
            if (isLoginIdInDB(loginId) == False):
                return jsonify({
                    "error": "" + loginId + "does not exists."
                }), 400
            '''
            postid 받아오고, 유효성 검사하고, 이 post의 모든 것들을 json 데이터로 보내주기
            '''
            postInfo = getPostInfo(postId)
            if (postInfo == None):
                return jsonify({
                    "error": "Failed to send post data."
                }), 400
            else:
                return jsonify({
                    "postInfo": postInfo,
                    "message": "sent post data successfully."
                }), 200
        else:
            return jsonify({
                "message": "Method not allowed."
            }), 405

    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

'''
페이지에 실시간으로 알림이 떠오르는 걸로 나중에 여건이 되면 하는걸로
근데 일단 하루치 보호자마다 담당하고있는 senior들의 응답률을 보내줌.

->아니 근데 비동기로 하면 금방 될거같은데? 알림은 예원이 쪽에서 보내는거고. ->일단은 나중에 하기로 함.
'''
@main.route('/supervisor/<loginId>/notice', methods=['GET']) #ok-OK
def supervisorNotice(loginId):
    try:
        if request.method == 'GET':
            # loginId
            if (isLoginIdInDB(loginId) == False):
                return jsonify({
                    "error": "" + loginId + "does not exists."
                }), 400
            
            # 보호자당 senior들의 알림을 23시 전까지 유지
            date, seniorList = getResponseRatioAndNamesBySeniors(loginId)


            return jsonify({
                "date": date,
                "seniorNoticeList": seniorList,
                "messages": "" + loginId + "exists and notice list[(name, response time),(), ...] is sent successfully."
            }), 200
        else:
            return jsonify({
                "message": "Method not allowed."
            }), 405

    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 날짜 보내주는 거 추가하기
@main.route('/supervisor/<loginId>/stats', methods=['GET']) #ok-OK
def supervisorStats(loginId):
    try:
        if request.method == 'GET':
            if (isLoginIdInDB(loginId) == True):
                nameList = getNameListByLoginId(loginId)    #(이름,loginId)
                nameList2 = []  #(이름)
                for i in nameList:  nameList2.append(i[0])

                responseRatioList = getResponseRatioListByLoginId(nameList)

                return jsonify({
                    "nameList": nameList2,
                    "responseRatioList": responseRatioList,
                    "message": "" + loginId + "exists and names, responseRatio is sent successfully."
                }), 200
            else:
                return jsonify({
                    "error": "" + loginId + "does not exists."
                }), 400
        else:
            return jsonify({
                "message": "Method not allowed."
            }), 405

    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500



