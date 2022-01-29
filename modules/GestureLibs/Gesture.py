from pyautogui import keyDown, press, keyUp
import os, sys, time
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
pparentdir = os.path.dirname(parentdir)
sys.path.append(pparentdir)

from run import FingerList, logging_list

error_log = []

class Gesture():

    
    def __init__(self, action: list, fingers_up: list, direction: str, detection_time = 3) -> None:
        self.action = action
        self.fingers_up = fingers_up
        self.detection_time = detection_time
    
    def exec_action(self):
        
        global error_log
        
        try:
            for key in action:                
                keyDown(key)
                    
            for key in action:
                keyUp(key)
                
        except BaseException as e:
            print("Error: ", e)
            error_log.append(e)
        
        finally:
            return error_log
            
    def start_detection(self):
        fingers_up = []
        detection_frames = []
        for finger in FingerList:
            if finger.is_up == True:
                fingers_up.append(finger.is_up)
        if len(fingers_up) == 5:
            time.sleep(0.5) #sleeps 0.6 seconds for the user to change to the actual gesture
            start = time.time()
            while int(time.time())-start < 3: # 2 second detection window
                detection_frames.append(logging_list[-1]) 
                if logging_list[-1] == False:
                    print("No fingers found, exiting")
                    break
        return detection_frames
                

    
            
            
                
        