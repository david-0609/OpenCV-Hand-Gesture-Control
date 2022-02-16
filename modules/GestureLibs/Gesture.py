from pyautogui import keyDown, press, keyUp
import os, sys, time

error_log = []

class Gesture():

    
    def __init__(self, name: str, action: list, fingers_up: list, direction: str) -> None:
        self.name = name
        self.action = action
        self.fingers_up = fingers_up
        self.direction = direction
    
    def exec_action(self):
        
        global error_log
        
        try:
            for key in self.action:                
                keyDown(key)
                    
            for key in self.action:
                keyUp(key)
                
        except BaseException as e:
            print("Error: ", e)
            error_log.append(e)
    
            if e == None:
                return True
            else:
                return error_log
            

