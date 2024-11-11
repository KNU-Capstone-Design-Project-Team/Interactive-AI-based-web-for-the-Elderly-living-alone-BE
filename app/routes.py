from flask import Blueprint, request, jsonify, url_for, redirect
from app.models.chatModels import *
from app.models.joinMembershipModels import *
from app.models.localProgramModels import *
from app.models.loginInfoModels import *
from app.models.noticeModels import *
from app.services.chatServices import *
from chatbot import Chatbot
from chatbot1 import Chatbot1
from datetime import datetime
import asyncio
import signal


main = Blueprint('main', __name__)


chatHistory = []
myChatBot = Chatbot1("gpt-4")
# 플래그 변수를 사용하여 이미 응답이 반환되었는지 추적
response_sent = False

'''
전체적으로 추가 구현해야할 사항:
    * JWT 토큰 라이브러리를 사용해서 인증 상태를 유지하는 거 메소드마다 추가하기
'''


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
                return jsonify({
                    "message": "Invalid request value."
                }), 400


    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/join/senior/<int:joinId>', methods=['POST, GET']) #추가 수정중
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
                        "message": "parameter is not valid value."
                    }), 400
            else:
                return jsonify({
                    "message": "parameter is not integer."
                }), 400

        elif request.method == 'POST':
            if joinId == 1:
                username = request.json.get('username')
                loginId = request.json.get('loginId')
                password = request.json.get('password')
                phoneNumber = request.json.get('phoneNumber')
                
                '''
                    code : DB에 senior 유저 정보 저장하기
                '''
                
            if joinId == 2:
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
                    return redirect(url_for('main.joinAddInfo', joinId=5))

                
            if joinId == 5:
                connectionNum = request.json.get('connectionNum')

                '''
                # 보호자 연결변호로 DB내에 있는 보호자와 연결하기
                '''
                return redirect(url_for('main.welcome', loginId="1"))   # !!welcome으로 갈지 로그인페이지로 갈지 결정하기!!

            # '다음으로' 버튼 눌렀을 시,
            toTheNext = request.json.get('toTheNext')
            if toTheNext == False:
                return jsonify({
                    "message": "잘못된 요청입니다."
                }), 400
            return redirect(url_for('main.joinSenior', joinId=joinId+1))
        else:
            return jsonify({
                "message": "Method not allowed."
            }), 405

    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/join/senior/<int:joinId>/addinfo', methods=['POST, GET']) #아직 안함
def joinAddInfo(joinId):
    try:
        pass
    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/join/supervisor/<int:joinId>', methods=['POST, GET']) #추가 수정중
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
                        "message": "parameter is not valid value."
                    }), 400
            else:
                return jsonify({
                    "message": "parameter is not integer."
                }), 400

        elif request.method == 'POST':
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

                return redirect(url_for('welcome', loginId='2'))

            # '다음으로' 버튼 눌렀을 시,
            toTheNext = request.json.get('toTheNext')
            if toTheNext == False:
                return jsonify({
                    "message": "잘못된 요청입니다."
                }), 400
            return redirect(url_for('joinSupervisor', joinId=joinId+1))
        else:
            return jsonify({
                "message": "Method not allowed."
            }), 405

    # 서버 내부 오류 발생 시 500 에러 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/welcome/<loginId>', methods=['POST, GET']) #아직 안함
def welcome(loginId):
    try:
        # if -> loginId가 senior에서 찾을 수 있다면
        # return redirect(url_for(joinSenior(welcomeSenior)))

        # if -> loginId가 supervisor에서 찾을 수 있다면
        # return redirect(url_for(joinSenior(welcomeSupervisor)))

        pass
    # 서버 내부 오류 발생 시 500 에러 반환
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
                    "nameList": nameList,
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



