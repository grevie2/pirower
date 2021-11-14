from constants import NUM_SECONDS_INACTIVITY_PERIOD, SCREEN_MSG, WHITE
from global_variables import flywheel_q, gui_q
import time

class Flywheel(object):
    def __init__(self):
        self.flywheel_updates = []

    def wait_for_flywheel_to_stop(self, gui_q):
        #wait for flywheel to stop spinning and clear the queue
        flywheel_stopped = False
        count = 0

        update_lst = []

        while not flywheel_stopped:
            time_remaining = NUM_SECONDS_INACTIVITY_PERIOD - count
            update_lst.append([SCREEN_MSG, "waiting for flywheel to stop..." + \
                str(time_remaining), WHITE])
            gui_q.put(update_lst)

            if not flywheel_q.empty():
                flywheel_q.get()
                count = 0
            else:
                time.sleep(1)
                count += 1

            if count >= NUM_SECONDS_INACTIVITY_PERIOD:
                flywheel_stopped = True

        update_lst = []
        update_lst.append([SCREEN_MSG, "", WHITE])
        gui_q.put(update_lst)
        return count
