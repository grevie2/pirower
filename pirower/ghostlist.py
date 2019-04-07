from constants import PERSONAL_AVERAGES, PERSONAL_BESTS, PERSONAL_WORSTS
from os import listdir
from os.path import isfile, join
import re

class GhostList(object):
    def __init__(self, trial_length, filepath):
        self.trial_length = trial_length
        self.filepath = filepath
        self.files = []
        self.sorted_files = []

    def get_ghost_filelist(self, selector):
        onlyfiles = [f for f in listdir(self.filepath) if isfile(join(self.filepath, f))]

        padded_trial_length = (str(self.trial_length)).zfill(2)
        pattern = re.compile("session_" + padded_trial_length + "min_\d+_\d{14}.json")

        self.files = []
        for f in onlyfiles:
            if pattern.match(f):
                self.files.append(f)

        return self.sort_ghosts(selector)

    def sort_ghosts(self, selector):
        #only continue if we actually found some ghost files that matched the criteria
        if len(self.files) > 0:
            self.sorted_files = []
            if selector == PERSONAL_BESTS or selector == PERSONAL_AVERAGES:
                self.sorted_files = sorted(self.files, reverse=True)
            elif selector == PERSONAL_WORSTS:
                self.sorted_files = sorted(self.files, reverse=False)
            else:
                #average
                pass
        return self.sorted_files
