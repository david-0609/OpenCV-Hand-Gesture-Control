from configparser import ConfigParser
from Gesture import Gesture

class GestureGenerator:

    def __init__(self, config_file: str):
        self.config_file = config_file    

    def read_config(self):
        GestureList = []
        config = ConfigParser
        config.read(filenames=self.config_file)
        for section in config.sections():
            # Validates if all information in config can be used, raise errors that can be handled in run
            if type(parser[config][name]) != str:
                raise BaseException("Use string only for name of gesture")
            gesture_name = section[config][name]
            gesture_action = section[config][action]
            gesture_fingers_up = section[config][fingers_up]
            gesture_direction = section[config][direction] 
            GestureList.append(Gesture(str(gesture_name), str(gesture_action), str(gesture_fingers_up), str(gesture_direction)))           
        return GestureList

    def write_config(self, name, fingers_up, direction, action):
        pass
        # Will be implemented later, may connect to gui to record configs
