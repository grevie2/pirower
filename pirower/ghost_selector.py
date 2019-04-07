from constants import PERSONAL_AVERAGES, NO_GHOST_FILES_PRESENT
from ghostlist import GhostList

def find_middle(l):
    if len(l) % 2 == 0:
        #print "idxE is ", int(len(l)/2)
        return int(len(l)/2)
    else:
        #print "idxO is ", int((len(l)/2.0) - 0.5)
        return int((len(l)/2.0) - .5)

class GhostSelector(object):
    def select_ghost_files(self, trial_length, max_players, selector, filepath):
        g = GhostList(trial_length, filepath)
        sorted_files = g.get_ghost_filelist(selector)

        if len(sorted_files) < max_players:
            max_ghosts = len(sorted_files)
        else:
            max_ghosts = max_players - 1

        #only continue if we actually found some ghost files that matched the criteria
        if len(sorted_files) > 0:
            if selector == PERSONAL_AVERAGES:
                mid = find_middle(sorted_files)

                if len(sorted_files) <= max_ghosts:
                    start_range = 0
                    end_range = len(sorted_files)
                else:
                    start_range = mid - max_ghosts/2
                    end_range = mid + max_ghosts/2
            else:
                if len(sorted_files) <= max_ghosts:
                    start_range = 0
                    end_range = len(sorted_files)
                else:
                    start_range = 0
                    end_range = max_ghosts

            selected_files = []
            selected_files = sorted_files[start_range:end_range]
            return selected_files
        else:
            return NO_GHOST_FILES_PRESENT
