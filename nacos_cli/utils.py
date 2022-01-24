import threading
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

# 启动nacos心跳服务
class StartNacosBeat(object):
    instance = None
    event_lock = threading.Event()

    def __new__(cls, *args, **kwargs):
        if StartNacosBeat.instance:
            return StartNacosBeat.instance
        else:
            StartNacosBeat.instance = object.__new__(cls)
            return StartNacosBeat.instance

    def __init__(self, data, nacos_client, seconds=5):
        self.data = data
        self.nacos_client = nacos_client
        self.seconds = seconds

    def call_nacos_beat(self):
        if not self.event_lock.is_set():
            t = threading.Thread(target=self.start_nacos_beat, args=())
            t.setDaemon(True)
            t.start()
        self.event_lock.set()

    def start_nacos_beat(self):
        sched = BlockingScheduler()
        sched.add_job(self.nacos_beat_job, 'interval', seconds=self.seconds)
        sched.start()

    def nacos_beat_job(self):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "-------------> 发送心跳给nacos服务！！！")
        self.nacos_client.send_heartbeat(**self.data)

