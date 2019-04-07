"""This class writes program settings to a JSON file"""
import json

class SettingsWriter(object):
    def __init__(self, settings_file):
        self.settings_file = settings_file
        self.python_dic = ""
        self.dictionary_to_json = ""

    def write_json_settings(self, session_time, num_ghost_players, num_fish, refresh_rate, selector, batch_mode, game_view):
    #def write_json_settings(self, session_time, num_ghost_players, num_fish, refresh_rate, selector):
        settings_dict = {'session_time': session_time, \
                          'num_ghost_players': num_ghost_players, \
                          'num_fish': num_fish, \
                          'refresh_rate': refresh_rate, \
                          #'selector': selector}
                          'selector': selector, \
                          'batch_mode': batch_mode, \
                          'game_view': game_view}
        self.python_dic = {'settings':settings_dict}
        self.dictionary_to_json = json.dumps(self.python_dic, indent=4, sort_keys=False)
        #print dictionaryToJson
        data_file = open(self.settings_file, "w")
        data_file.write(self.dictionary_to_json)
        data_file.close()

    def read_json_settings(self):
        data_file = open(self.settings_file, "r")
        data = json.load(data_file)
        data_file.close()
        settings = data['settings']
        return settings
