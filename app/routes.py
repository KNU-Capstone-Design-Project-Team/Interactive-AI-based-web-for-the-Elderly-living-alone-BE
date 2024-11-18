from flask import Blueprint, request, jsonify, url_for, redirect
from app.models.chatModels import *
from app.models.joinMembershipModels import *
from app.services.joinMembershipServices import *
from app.models.loginInfoModels import *
from app.models.noticeModels import *
from app.services.chatServices import *
from chatbot import Chatbot
from datetime import datetime
import asyncio
import signal


main = Blueprint('main', __name__)
service = MembershipService()

chatHistory = []
myChatBot = Chatbot("gpt-4")
# 플래그 변수를 사용하여 이미 응답이 반환되었는지 추적
response_sent = False

'''
전체적으로 추가 구현해야할 사항:
    * JWT 토큰 라이브러리를 사용해서 인증 상태를 유지하는 거 메소드마다 추가하기
'''

#에러 처리 공통 함수
def error_response(message,status_code=400):
    return jsonify({"message":message}),status_code

@main.route('/', methods=['POST'])  #jwt 토큰 관련 추가
def login():
    try:
        '''
        +) JWT 토근 관련 code
        '''
        pass
    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/join', methods=['POST']) #ok-ok
def join():
    try:
        if request.method == 'POST':
            category = request.json.get('category')
            if category == 'supervisor':
                return redirect(url_for('main.joinSupervisor', joinId=1))
            elif category == 'senior':
                return redirect(url_for('main.joinSenior', joinId=1))
            else :
                return error_response("Invalid request value.")

    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/join/senior/<int:joinId>', methods=['POST', 'GET'])
def joinSenior(joinId):
    try:
        if request.method == 'GET':
            if isinstance(joinId, int):
                if 1 <= joinId <= 5:
                    return jsonify({
                        "message": "GET request successfully.",
                        "currentPage": joinId
                    }), 200
                else:
                    return jsonify({"message": "Parameter is not a valid value."}), 400
            else:
                return jsonify({"message": "Parameter is not an integer."}), 400

        elif request.method == 'POST':
            if joinId == 1:
                username = request.json.get('username')
                loginId = request.json.get('loginId')
                password = request.json.get('password')
                phoneNumber = request.json.get('phoneNumber')

                # DB에 senior 유저 정보 저장
                result = service.save_senior_user(username, loginId, password, phoneNumber)
                if result == "success":
                    return jsonify({"message": "User information saved successfully."}), 200
                else:
                    return jsonify({"error": "Failed to save user information."}), 500

            elif joinId == 2:
                year = request.json.get('year')
                month = request.json.get('month')
                day = request.json.get('day')

                # DB에 생일 정보 저장
                result = service.save_senior_birthday(loginId, year, month, day)
                if result == "success":
                    return jsonify({"message": "Birthday information saved successfully."}), 200
                else:
                    return jsonify({"error": "Failed to save birthday information."}), 500

            elif joinId == 3:
                si = request.json.get('si')
                gu = request.json.get('gu')
                dong = request.json.get('dong')

                # DB에 거주 정보 저장
                result = service.save_senior_residence(loginId, si, gu, dong)
                if result == "success":
                    return jsonify({"message": "Residence information saved successfully."}), 200
                else:
                    return jsonify({"error": "Failed to save residence information."}), 500

            elif joinId == 4:
                activities = request.json.get('activities', [])  # 사용자가 선택한 활동 리스트
                
                # 사용자가 버튼에서 선택한 활동들 저장
                if activities:
                    for activity in activities:
                        if activity not in ['요리', '운동', '바둑', '노래', '춤', '서예', '스마트폰', '식물재배']:
                            return jsonify({"error": f"Invalid activity: {activity}"}), 400

                        result = service.save_senior_activity(loginId, activity)
                        if result != "success":
                            return jsonify({"error": f"Failed to save activity: {activity}"}), 500

                    # 모든 활동 저장 후 5페이지로 이동
                    return redirect(url_for('main.joinSenior', joinId=5))

                return jsonify({"message": "No activities selected."}), 400

            elif joinId == 5:
                connectionNum = request.json.get('connectionNum')

                # 보호자 연결 번호로 DB 내 보호자와 연결
                result = service.link_guardian(loginId, connectionNum)
                if result == "success":
                    return redirect(url_for('main.welcome', loginId=loginId))
                else:
                    return jsonify({"error": "Failed to link guardian."}), 500

            # '다음으로' 버튼 눌렀을 시
            toTheNext = request.json.get('toTheNext')
            if toTheNext == False:
                return jsonify({"message": "잘못된 요청입니다."}), 400
            return redirect(url_for('main.joinSenior', joinId=joinId + 1))

        else:
            return jsonify({"message": "Method not allowed."}), 405

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/join/senior/<int:joinId>/addinfo', methods=['POST', 'GET']) # 아직 안함
def joinAddInfo(joinId):
    try:
        if request.method == 'POST':
            # 추가 정보 저장 로직 구현 (필요시)
            return jsonify({"message": "Additional info saved successfully"}), 200
        elif request.method == 'GET':
            return jsonify({"message": "GET request for add info received"}), 200
        else:
            return error_response("Method not allowed.", 405)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/join/supervisor/<int:joinId>', methods=['POST', 'GET']) # 추가 수정중
def joinSupervisor(joinId):
    try:
        if request.method == 'GET':
            if isinstance(joinId, int) and 1 <= joinId <= 2:
                return jsonify({"message": "GET joinId successfully."}), 200
            else:
                return error_response("Parameter is not valid value or not an integer.", 400)

        elif request.method == 'POST':
            if joinId == 1:
                username = request.json.get('username')
                loginId = request.json.get('loginId')
                password = request.json.get('password')
                phoneNumber = request.json.get('phoneNumber')
                result = service.register_supervisor_basic_info(username, loginId, password, phoneNumber)
                if result == "success":
                    return jsonify({"message": "Supervisor info saved successfully"}), 200
                else:
                    return error_response("Failed to save supervisor info")

            elif joinId == 2:
                result = service.generate_supervisor_connection_num(loginId)
                if result == "success":
                    return redirect(url_for('main.welcome', loginId="2"))
                else:
                    return error_response("Failed to generate connection number")

            toTheNext = request.json.get('toTheNext')
            if toTheNext:
                return redirect(url_for('main.joinSupervisor', joinId=joinId+1))
            else:
                return error_response("잘못된 요청입니다.", 400)

        else:
            return jsonify({"message": "Method not allowed."}), 405

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@main.route('/welcome/senior/<int:guideId>', methods=['POST, GET']) #아직 안함
def welcomeSenior(guidId):
    try:
        pass
    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/welcome/supervisor/<int:guideId>', methods=['POST, GET']) #아직 안함
def welcomeSupervisor(guidId):
    try:
        pass
    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/senior/<loginId>', methods=['POST', 'GET']) #ok-ok
def seniorHome(loginId):
    try:
        if request.method == 'POST':
            # 클라이언트로부터 받은 데이터를 처리
            action = request.json.get('action')

            if action == 'chat':
                # '대화하기' 버튼을 누른 경우 /chat 경로로 리다이렉트
                return redirect(url_for('main.seniorChat', loginId='1'))
            elif action == 'recommend':
                # '추천하기' 버튼을 누른 경우 /recommend 경로로 리다이렉트
                return redirect(url_for('main.seniorRecommend', loginId='1'))
            else:
                return jsonify({"error": "Invalid request format"}), 400
        else:
            return jsonify({
                "message": "Method not allowed."
            }), 405

    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/supervisor/<loginId>', methods=['POST', 'GET']) #ok-ok
def supervisorHome(loginId):
    try:
        if request.method == 'POST':
            # 클라이언트로부터 받은 데이터를 처리
            action = request.json.get('action')

            if action == 'notice':
                # '대화하기' 버튼을 누른 경우 /chat 경로로 리다이렉트
                return redirect(url_for('main.supervisorNotice', loginId='1'))
            elif action == 'stats':
                # '추천하기' 버튼을 누른 경우 /recommend 경로로 리다이렉트
                return redirect(url_for('main.supervisorStats', loginId='1'))
            else:
                return jsonify({"error": "Invalid request format"}), 400

    # 서버 내부 오류 발생 시 500 에러 반환
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
@main.route('/chatPoll', methods=['GET'])   #일단 예외처리 빼고 ok
async def poll():
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
                print(f"대화 횟수를 초과하였으므로 대화를 할 수 없습니다.")
                return jsonify({
                    "error": "대화 횟수를 초과하였으므로 대화를 할 수 없습니다."
                }), 400

            # AI가 먼저 질문을 시작하는건 이미 비동기로 받아옴
            if myChatBot.exchange_count == 0:  # 대화가 끝나서 초기화된 상태 -> 대화를 할 수 없는 상태
                print(f"대화 횟수를 초과하였으므로 대화를 할 수 없습니다.")
                return jsonify({
                    "error": "대화 횟수를 초과하였으므로 대화를 할 수 없습니다."
                }), 400

            else:  # 첫 질문이 아닐 때
                userInput = request.json.get('userInput')   # request받아오기

                if myChatBot.exchange_count == 1:
                    if userInput == '\n':
                        # 대화 종료한 상태(응답안햇다고 저장하기 -> 사실 코드짤필요x 이미 None임.
                        return jsonify({
                            "message": "공백이 반환되어 대화가 종료됩니다. 해당 시간의 대화에 응답하지 않았습니다."
                        }), 300
                    else:
                        updateResponseTimeInQuestion(datetime.now())

                if userInput == '\n':
                    '''
                    대화 종료한 상태를 저장하기
                    '''
                    return jsonify({
                        "message": "공백이 반환되어 대화가 종료됩니다."
                    }), 300

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


@main.route('/senior/<loginId>/recommend', methods=['POST', 'GET']) #아직 안함-> 먼저 db에 30개정도 데이터 넣어 놓고 하드코딩 해야 함. api는 보류
def seniorRecommend(loginId):
    try:
        if request.method == 'GET':
            '''
            기본 : 전체
            가장 최근의 공공데이터들을 DB에서 30개를 추출해서 최대 30개를 LIST로 보내줌
            (list에는 postId는 꼭 넣어줘야 함.)***
            
            ->일단을 하드코딩으로 백쪽에서 DB에 30개의 데이터를 넣어놓고 주는 방식으로 하는데
                ->공공데이터 API를 쓰려면 위치 기반의 데이터를 나누는 방식이랑
                취향 기반의 데이터를 나누는 방식(EX. GPT에 프롬프트 넣어서 구분해서 넣는다던지)을 나누어서
                DB에 저장한 후, 하는 걸 하루 단위로 하는 방식으로 코딩하기
            '''

            return jsonify({
                "message": "성공적으로 ""GET"" 받았습니다."
            }), 200

        elif request.method == 'POST':
            '''
               1. 전체, 위치, 취향 - category를 request로 받아옴
                category마다 해당되는 공공데이터들을 DB에서 30개를 추출해서
                프론트에서 category마다 요청이 들어오면
                해당되는 것들의 데이터를 보내 줌.(list에는 postId는 꼭 넣어줘야 함.)***
                
               2. post를 request로 받아옴
                postId를 request로 얻어오면 이를 redirection하도록 값을 넘겨줌
                
                postId = ...(db에서 가져옴.)
                return redirect(url_for(seniorRecommendPost, data=json.dumps(postId)))
                
                이런식으로 넘겨주기
            '''

            return jsonify({
                "message": "성공적으로 ""POST"" 받았습니다."
            }), 200
        else:
            return jsonify({
                "message": "Method not allowed."
            }), 405

    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#post마다 id를 부여하고(db에 각 프로그램마다 넣을때 이미 id를 부여했음.) 이를 받아옴
#/senior/<loginId>/recommend에서 리디렉션할 때 postId도 같이 넘겨줌
@main.route('/senior/<loginId>/recommend/<int:postId>', methods=['GET'])
def seniorRecommendPost(loginId):
    try:
        if request.method == 'GET':
            '''
            postid 받아오고, 유효성 검사하고, 이 post의 모든 것들을 json 데이터로 보내주기
            ***페이지 구성에 필요한 것들을 프론트에게 물어보기***
            ***리스트로 보내줄까 하나하나 보내줄까 그것도 물어보기***
            '''

            return jsonify({
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

->아니 근데 비동기로 하면 금방 될거같은데? 알림은 예원이 쪽에서 보내는거고.
'''
@main.route('/supervisor/<loginId>/notice', methods=['GET']) #ok
def supervisorNotice(loginId):
    try:
        if request.method == 'GET':
            # loginId
            if (isLoginIdInDB(loginId) == False):
                return jsonify({
                    "error": "" + loginId + "does not exists."
                }), 400
            
            # 보호자당 senior들의 알림을 23시 전까지 유지
            date, seniorList = getResponseTimesAndNamesBySeniors(loginId)

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
@main.route('/supervisor/<loginId>/stats', methods=['POST', 'GET']) #ok
def supervisorStats(loginId):
    try:
        if request.method == 'GET':
            if (isLoginIdInDB(loginId) == True):
                nameList = getNameListByLoginId(loginId)
                nameList2 = []
                for i in nameList: nameList2.append(i[0])

                responseTimeList = getResponseTimeListByLoginId(nameList)

                return jsonify({
                    "names": nameList2,
                    "responseTimes": responseTimeList,
                    "message": "" + loginId + "exists and names, responseTime is sent successfully."
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



