#! /usr/bin/python3

from entity import *
from timestampbatcher import *
from newtimestampbatcher import *
from newirbatcher import *
#from irbatcher import *
import json
#from global_variables import *
from constants import WASH_COLOUR, OFFSCREEN_MARKER_FONT_SIZE, POINT_UP, POINT_DOWN, BOATWASH_SAMPLE_IN_MS
from constants import GREEN, WHITE
from constants import WIN_HEIGHT, GHOST_JSON_PATH
import datetime
from time_utils import *

data_filename = 'session_20min_026825_20180401111312.json'
s = data_filename

f = open(GHOST_JSON_PATH + '/' + data_filename, "r")
data = f.read()
json_data = json.loads(data)
f.close()
timestamp_ary = []
timestamp_ary = json_data['fanwheel_times']
ir_timestamp_ary = []
ir_timestamp_ary = json_data['ir_times']

#tb = TimestampBatcher(timestamp_ary)
#tb = NewTimestampBatcher(timestamp_ary)

#batched_ts_ary = []
#print "trial_length is ", trial_length
#print "display_sample is ", display_sample
#batched_ts_ary = tb.convert_ts_array_to_display_array(trial_length, display_sample)


#batched_boatwash_ts_ary = []
#batched_boatwash_ts_ary = tb.convert_ts_array_to_display_array(BOATWASH_SAMPLE_IN_MS)

#irtb = NewIRBatcher(ir_timestamp_ary)
#batched_ir_ts_ary = []
#batched_ir_ts_ary = irtb.convert_stroke_array_to_display_array(display_sample)

j = 0
start = datetime.datetime(1900, 1, 1, 0, 0, 0, 0)

#while j < len(timestamp_ary):
#       #print timestamp_ary[j]
#       j += 1
#       current_elapsed = datetime.datetime.strptime(timestamp_ary[j], '%H:%M:%S.%f')
#       td = current_elapsed - start
#       print timedelta_milliseconds(td)

new_ts_ary = []
new_ir_ary = []
for t in timestamp_ary:
    #print timestamp_ary[j]
    current_elapsed = datetime.datetime.strptime(t, '%H:%M:%S.%f')
    td = current_elapsed - start
    #print timedelta_milliseconds(td)
    new_ts_ary.append(timedelta_milliseconds(td))
    #max_boundary = datetime.timedelta(milliseconds=ms)

for ir in ir_timestamp_ary:
    elapsed = ir[0]
    current_elapsed = datetime.datetime.strptime(ir[0], '%H:%M:%S.%f')
    tmp_ir = current_elapsed - start
    ir_id = ir[1]

    new_ir_ary.append([timedelta_milliseconds(tmp_ir), ir_id])

python_dic = {'fanwheel_times':new_ts_ary, 'ir_times':new_ir_ary}
dictionary_to_json = json.dumps(python_dic, indent=4, sort_keys=False)
#print dictionary_to_json

GHOST_JSON_PATH + '/' + data_filename

new_filename = 'new_session_20min_026825_20180401111312.json'
data_file = open(GHOST_JSON_PATH + '/' + new_filename, "w")
data_file.write(dictionary_to_json)
data_file.close()
