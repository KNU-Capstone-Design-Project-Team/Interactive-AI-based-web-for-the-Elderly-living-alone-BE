import datetime

from bson import ObjectId
from flask import Flask, request
from app.models.chatModels import *
from app.scheduler import *
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from app.models.chatModels import *
from app.routes import scheduledTask, popAllMessageQueue
from flask_cors import CORS

'''
전체적으로 추가 구현해야할 사항:
    * 공공데이터 api를 써서 목록들을 하루 단위로 DB에 받아 옴.
'''



def create_app():

    app = Flask(__name__)

    app.logger.debug("Flask app created")
    CORS(app, resources={r"/*": {"origins": "*"}})  # 모든 출처에서의 접근을 허용

    @app.before_request
    def handle_options():
        if request.method == 'OPTIONS':
            response = app.response_class()
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            return response

    scheduler = BackgroundScheduler(timezone='Asia/Seoul')

    '''
    ******* SCHEDULING   methods *******
    '''

    def asyncFromFront():
        """
            8시부터 22시 사이에 2시간 간격으로 새로운 채팅을 생성하는 작업을 등록
        """
        # 매일 8시, 10시, 12시, 14시, 16시, 18시, 20시, 22시에 실행
        hours = [8, 10, 12, 14, 16, 18, 20, 21, 22]

        for hour in hours:
            scheduler.add_job(
                id=f"create first question at {hour}",
                func=scheduledTask,  # 여기서 ai의 첫 질문을 보내줘야 함.
                trigger="cron",
                hour=hour,
                minute=0
            )

    def popMessageQueue():
        hours = [9, 11, 13, 15, 17, 19, 21, 23]

        for hour in hours:

            scheduler.add_job(
                id=f"pop all messagequeue at {hour}, 50",
                func=popAllMessageQueue,
                trigger="cron",
                hour=hour,
                minute=53
            )

    def createConversatationTemp():
        # 현 날짜의 Conversation 생성하고 첫 질문 생성
        OI = ObjectId("672fa9e2c4f7ae5107be9b2e")
        createConversation(OI)

    ''' 
    *********** 추가할 내용 ***********8(위에 메소드랑 같이 수정봐야 함.)
    토근 관련해서 개발하면 그때 conversation(seniorUser)에 저걸 어떻게 넣어서 스케쥴링을 할지 정하기...
    '''
    def createsConversation():
        # 매일 7시30에 Conversation 생성
        scheduler.add_job(
            id=f"create conversation at 7:30",
            func=createConversatationTemp,
            trigger="cron",
            hour=7,
            minute=30
        )


    def calculateRatio():
        '''
        오후 10시 30분에 응답률을 계산하는 함수
        '''
        hour = 22

        scheduler.add_job(
            id=f"calculate response ratio at {hour}",
            func=calculateResponseRatio,  # 여기서 응답률 최신 10개를 list보내줘야함
            trigger="cron",
            hour=hour,
            minute=30
        )

    # 하루단위로 공공데이터 받아오는 것도 스케쥴링으로 나중에 구현하기

    def shutdownScheduler():
        """
        앱 종료 시 스케줄러도 종료
        """
        scheduler.shutdown()

    '''
    init
    '''
    scheduler.start()

    # 환경 변수에 따라 설정 적용
    #app.config.from_object(config[config_name])

    # MongoDB 연결 설정
    load_dotenv()
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client.ElderCareNet

    # 임시로 conversation 서버 시작하면 무조건 만들도록 저장해놨음
    createConversatationTemp()

    #원래는 스케줄러 타고 실행되어야하는 init 첫 question 생성 함수인데
    # 개발을 위해서 여기에 임의로 호출함
    '''
    today = datetime.now().strftime('%Y.%m.%d')
    temp = db.Conversation.find_one({"date": today})
    #createQuestion(temp.get("_id"))
    '''

    # Scheduling
    asyncFromFront()
    popMessageQueue()
    calculateRatio()
    createsConversation()

    '''
    # python console 실행 테스트용
    try:
        # 스케줄러가 백그라운드에서 작동 중이므로 메인 스레드가 계속 실행되게 함
        while True:
            print(f"running.........")
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        # 스케줄러 종료
        shutdownScheduler()
    '''
    '''
    # Swagger 설정
    app.config['SWAGGER'] = {
        'title': 'My API',
        'uiversion': 4
    }
    swagger = Swagger(app)  # Swagger 객체 초기화
    '''

    # 라우트 등록
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app



