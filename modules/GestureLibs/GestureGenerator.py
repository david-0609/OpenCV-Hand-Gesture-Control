from configparser import ConfigParser
import Gesture

class GestureGenerator:

    def __init__(self, config_file: str):
        self.config_file = config_file    

    def read_config(self):
        GestureList = []
        config = ConfigParser()
        config.read(filenames=str(self.config_file))
        for section in config.sections():
            # Validates if all information in config can be used, raise errors that can be handled in run
            
            gesture_name = config[section]["name"]
            gesture_action = config[section]["action"]
            gesture_fingers_up = config[section]["fingers_up"]
            gesture_direction = config[section]["direction"]
            GestureList.append(Gesture.Gesture(str(gesture_name), gesture_action.split(","), gesture_fingers_up.split(","), str(gesture_direction)))
        return GestureList

