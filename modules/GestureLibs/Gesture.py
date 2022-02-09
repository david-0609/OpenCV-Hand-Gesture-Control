from pyautogui import keyDown, press, keyUp
import os, sys, time

error_log = []

class Gesture():

    
    def __init__(self, name: str, action: list, fingers_up: list, direction: str, detection_time = 3) -> None:
        self.name = name
        self.action = action
        self.fingers_up = fingers_up
        self.direction = direction
    
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
        
        else:
            return True
        
        finally:
            return error_log

                

    
            
            
                
        
