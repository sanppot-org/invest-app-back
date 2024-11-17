import time
from apscheduler.schedulers.background import BackgroundScheduler
from domain.type import TriggerType


class Func:
    def execute(self, id: int):
        print(f"func Called id={id}")


sched = BackgroundScheduler(timezone="Asia/Seoul")  # 시간대 설정
sched.add_job(
    func=Func().execute, kwargs={"id": 1}, trigger=TriggerType.INTERVAL.value, seconds=2
)
sched.start()

time.sleep(100)
