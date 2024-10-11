from flask import Flask
from app.models.chatModels import *
from pymongo import MongoClient
from app.scheduler import scheduleJobs, shutdownScheduler

#def create_app(config_name):
def create_app():
    app = Flask(__name__)

    # 환경 변수에 따라 설정 적용
    #app.config.from_object(config[config_name])

    # MongoDB 연결 설정
    load_dotenv()
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client.ElderCareNet

    # 현 날짜의 Conversation 생성하고 첫 질문 생성
    createConversation()

    #원래는 스케줄러 타고 실행되어야하는 init 첫 question 생성 함수인데
    # 개발을 위해서 여기에 임의로 호출함
    today = datetime.now().strftime('%Y.%m.%d')
    temp = db.Conversation.find_one({"date": today})
    createQuestion(temp.get("_id"))

    '''
    # 첫 번째 HTTP 요청이 처리되기 전에 한 번만 스케줄러 작업 등록
    def initialize():
        scheduleJobs()
    app.before_request(initialize)
    '''

    '''
    # 앱 종료 시 스케줄러 종료
    @app.teardown_appcontext
    def shutdownSession(exception=None):
        shutdownScheduler()
    '''
    # 라우트 등록
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
