import threading
from utils import play_alarm

def trigger_alarm():
    alarm_thread = threading.Thread(target=play_alarm, args=("alarm.wav",))
    alarm_thread.start()
