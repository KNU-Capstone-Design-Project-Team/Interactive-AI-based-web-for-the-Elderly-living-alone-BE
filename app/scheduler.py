from apscheduler.schedulers.background import BackgroundScheduler
from app.models.chatModels import *
from app.routes import scheduledTask

scheduler = BackgroundScheduler(timezone='Asia/Seoul')

def asyncFromFront():
    # 매일 8시, 10시, 12시, 14시, 16시, 18시, 20시, 22시에 실행
    hours = [8, 10, 12, 14, 16, 18, 20, 22]

    for hour in hours:
        scheduler.add_job(
            id=f"create question at {hour}",
            func=scheduledTask, # 여기서 ai의 첫 질문을 보내줘야 함.
            trigger="cron",
            hour=hour,
            minute=0
        )

    scheduler.start()


def scheduleJobs():
    """
    8시부터 22시 사이에 2시간 간격으로 새로운 채팅을 생성하는 작업을 등록
    """
    # 매일 8시, 10시, 12시, 14시, 16시, 18시, 20시, 22시에 실행
    hours = [7, 9, 11, 13, 15, 17, 19, 21]

    for hour in hours:

        scheduler.add_job(
            id=f"create question at {hour}",
            func=scheduledTask,
            trigger="cron",
            hour=hour,
            minute=50
        )

    scheduler.start()


def calculateRatio():
    '''
    오후 10시 30분에 응답률을 계산하는 함수
    '''
    hour = 22

    scheduler.add_job(
        id=f"calculate response ratio at {hour}",
        func=calculateResponseRatio,    # 여기서 응답률 최신 10개를 list보내줘야함
        trigger="cron",
        hour=hour,
        minute=30
    )

    scheduler.start()

def shutdownScheduler():
    """
    앱 종료 시 스케줄러도 종료
    """
    scheduler.shutdown()


'''
def pushAlarm():

    #오후 11시에 알림을 보내는 작업을 등록

    hour = 23

    scheduler.add_job(
        id=f"push alarm at {hour}",
        func=recent10DaysNotice(),
        trigger="cron",
        hour=hour,
        minute=0
    )

    scheduler.start()
'''