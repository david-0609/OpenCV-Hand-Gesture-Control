from dataclasses import dataclass
import time
import sys
import os
import warnings
from modules.Exceptions import DirectionNotDetermined, GestureNotDetermined
from Finger import FingerTipList
from Tools import findMajority, is_identical, convert_dir_id

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
pparentdir = os.path.dirname(parentdir)
sys.path.append(pparentdir)

from run import Run
from run import logging_list

@dataclass
class FingerTips:
    
    id: int
    x_coord: list
    y_coord: list
    direction: str

class GestureDetector:
     
    FingersList = Run.FingersList
    GestureList = Run.GestureList
    FINGERTIPS = FingerTipList
  
    FingerTipsData = []
    detection_frames = []

    def __init__(self) -> None:
        pass

    def parse_fingertips(self):
        for id in self.FINGERTIPS:
            self.FingerTipsData.append(FingerTips(id, [], [], ""))
        
    def start_detection(self):
        fingers_up = []
        fingers_detected = None
        for finger in self.FingersList:
            if finger.is_up == True:
                fingers_up.append(finger.is_up)
        if len(fingers_up) == 5:
            time.sleep(0.5) #sleeps 0.6 seconds for the user to change to the actual gesture
            start = time.time()
            while int(time.time())-start < 3: # 2 second detection window
                self.detection_frames.append(logging_list[-1]) 
                if logging_list[-1] == False:
                    warnings.warn("No fingers found, detection window not starting")
                    fingers_detected = False
                    break
                else:
                    fingers_detected = True

            if fingers_detected:
                return self.detection_frames 
            else:
                return False

    def parse_list(self):
        for coord in self.detection_frames:
            for tip in self.FingerTipsData:
                if coord[0] == tip.id:
                    tip.x_coord.append(coord[1])
                    tip.y_coord.append(coord[2])
                    
    def identify_dir(self):
        '''
        This function identifies the direction of travel of the finger through using 3 points of the fingertip's travel
        Should be mostly accurate
        '''
        for fingertip in FingerTipList:
            first_x = fingertip.x_coord[0]
            middle_x = fingertip.x_coord[int(len(fingertip.x_coord)/2)]
            final_x = fingertip.x_coord[-1]
            diff_x = final_x - first_x
            
            first_y = fingertip.y_coord[0]
            middle_y = fingertip.y_coord[int(len(fingertip.y_coord)/2)]
            final_y = fingertip.y_coord[-1]
            diff_y = final_y-first_y
            
            if diff_x > diff_y:
                # goes left/right
                if first_x < middle_x < final_x:
                    fingertip.direction = "r" # R for right
                elif first_x > middle_x > final_x:
                    fingertip.direction = "l" # L for left
                else:
                    raise DirectionNotDetermined
                
            if diff_y > diff_x:
                #goes up/down      
                if first_y < middle_y < final_y:
                    fingertip.direction = "u"
                elif first_y < middle_y < final_y:
                    fingertip.direction = "d"
        
    def match_gesture(self):
        # Match previous information to a gesture
        UpIDList = []
        UpList = []
        DirectionsList = []
        GestureDirection = ""

        for finger in self.FingersList:
            if finger.is_up:
                UpIDList.append(finger.tip)
                UpList.append(finger)

        for fingertip in self.FingerTipsData:
            if fingertip.id in UpIDList:
                DirectionsList.append(fingertip.direction)
        
        # To find the majority of the directions of fingers, the fingers direction have to be mapped to an integer value 
        DirectionsList = convert_dir_id(DirectionsList)
        GestureDirection = findMajority(DirectionsList)
        GestureDirection = convert_dir_id(GestureDirection) 

        for gesture in self.GestureList:
            # Now matches gesture with the GestureList that was imported from main
            if GestureDirection == gesture.direction and is_identical(UpList, gesture.fingers_up):
                gesture.exec_action()
            else:
                raise GestureNotDetermined  

