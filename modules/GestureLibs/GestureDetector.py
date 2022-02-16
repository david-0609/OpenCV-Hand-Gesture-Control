import Gesture
from dataclasses import dataclass
import time
import sys
import os
from modules.Exceptions import DirectionNotDetermined

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
pparentdir = os.path.dirname(parentdir)
sys.path.append(pparentdir)

from Finger import FingerTipList
from run import Run
from run import logging_list
from modules.Tools import findMajority

FingersList = Run.FingersList

FINGERTIPS = FingerTipList

FingerTipsData = []

@dataclass
class FingerTips:
    
    id: int
    x_coord: list
    y_coord: list
    direction: str

class GestureDetector:
    
    def __init__(self, detection_frames: list, gestures) -> None:
        self.detection_frames = detection_frames
        self.gestures = gestures
        
    def start_detection(self):
        fingers_up = []
        detection_frames = []
        for finger in FingersList:
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
        
    def parse_fingertips(self):
        global FingerTipsData 
        for id in FINGERTIPS:
            FingerTipsData.append(FingerTips(id, [], [], ""))
        
    def parse_list(self):
        global FingerTipsData
        for coord in self.detection_frames:
            for tip in FingerTipsData:
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
        
        return FingerTipList
    
    def match_gesture(self):
        # Match previous information to a gesture
        UpIDList = []
        UpList = []
        DirectionsList = []
        GestureDirection = ""

        for finger in FingersList:
            if finger.is_up:
                UpIDList.append(finger.tip)
                UpList.append(finger)

        for fingertip in FingerTipsData:
            if fingertip.id in UpIDList:
                DirectionsList.append(fingertip.direction)
        
        for dir in DirectionsList:
            if dir == "r":
                dir = 1
            elif dir == "l":
                dir = 2
            elif dir == "u":
                dir = 3
            elif dir == "d":
                dir = 4

        GestureDirection = findMajority(DirectionsList)
        
        return GestureDirection                
