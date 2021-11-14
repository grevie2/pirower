from global_variables import flywheel_q
import datetime

def increaserev(channel):
    global flywheel_q
    flywheel_q.put(datetime.datetime.now())
