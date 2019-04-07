"""This class writes the flywheel and ir results to a json file"""
import json
from datetime import datetime

class ReportWriter(object):
    def __init__(self, ts_array, ir_array, trial_time, json_folder):
        self.flywheel_ary = ts_array
        self.ir_ary = ir_array
        self.total_cnt = len(self.flywheel_ary)
        self.dist_trial_in_mins = trial_time
        self.json_folder = json_folder

    def write_json_report(self):
        padded_count = (str(self.total_cnt)).zfill(6)
        padded_trial_time = (str(self.dist_trial_in_mins)).zfill(2)
        timestamp = datetime.now()
        filename = self.json_folder + '/' + "session" + "_" + padded_trial_time + "min" + "_" + padded_count + "_" + timestamp.strftime("%Y%m%d%H%M%S") + ".json"

        python_dic = {'flywheel_times':self.flywheel_ary, 'ir_times':self.ir_ary}
        dictionary_to_json = json.dumps(python_dic, indent=4, sort_keys=False)
        #print dictionary_to_json
        data_file = open(filename, "w")
        data_file.write(dictionary_to_json)
        data_file.close()
        return filename
