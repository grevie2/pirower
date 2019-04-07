from multiprocessing import Queue
import datetime

flywheel_q = Queue()
IRq = Queue()
gui_q = Queue()
user_event_q = Queue()
button_panel_event_q = Queue()

ghosts = []

max_players = 5
num_lanes = max_players

refresh_rate_hz = 10
display_sample = 1000/refresh_rate_hz
