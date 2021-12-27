from pyautogui import keyDown, press, keyUp
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from main import FingerList


class Gesture():

    def __init__(self, action: list, fingers_up: list, direction: str, detection_time = 5) -> None:
        self.action = action
        self.fingers_up = fingers_up
        self.direction = direction
        self.detection_time = detection_time
    
    def exec_action(self):
    
        try:
            for key in action:                
                keyDown(key)
                    
            for key in action:
                keyUp(key)
                
        except BaseException as e:
            print("Error: ", e)
            
    def __start_detection(self):
        fingers_up = []
        detection_frames = []
        for finger in FingerList:
            if finger.is_up == True:
                fingers_up.append(finger.is_up)

    
            
            
                
        