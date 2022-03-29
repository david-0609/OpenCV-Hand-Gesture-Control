from dataclasses import dataclass
import time
import sys
import os
from modules.Exceptions import DirectionNotDetermined, GestureNotDetermined
from Finger import FingerTipList
from Tools import findMajority, is_identical, convert_dir_id
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
pparentdir = os.path.dirname(parentdir)
sys.path.append(pparentdir)

@dataclass
class FingerTips:
    
    id: int
    x_coord: list
    y_coord: list
    direction: str

class GestureDetector:
    detection_window = 3 
    detection_wait = 3
    
    FINGERTIPS = FingerTipList
  
    FingerTipsData = []
    detection_frames = []
    start_time = None 
    end_time = None 
    detection_start = False 
    done = False
    number_start = 0
    in_cooldown = False
    cooldown_time = 5
    cooldown_end = None

    def __init__(self, FingersList, GestureList) -> None:
        self.FingersList = FingersList
        self.GestureList = GestureList

    def parse_fingertips(self):
        self.FingerTipsData = []
        for id in self.FINGERTIPS:
            self.FingerTipsData.append(FingerTips(id, [], [], ""))
    
    def reset(self):
        print("resetting data")
        self.detection_start = False
        self.start_time = None
        self.end_time = None
        self.detection_frames = []
        self.number_start = 0
        return False 

    def start_detection(self, input_list):
        if self.in_cooldown and self.cooldown_end != None: 
            print(f"In cooldown, cooldown ends in {0}",int(self.cooldown_end-time.time()))
            if int(time.time()) > self.cooldown_end:
                self.in_cooldown = False

        if self.detection_start == False and self.in_cooldown == False:
            fingers_up = []
            print(self.FingersList)
            for finger in self.FingersList:
                finger_is_up = finger.is_up(input_list) 
                
                if finger_is_up == True:
                    print("Up")
                    fingers_up.append(True)
                elif finger_is_up == 0:
                    print("Error in finger detection")
                    break
                elif finger_is_up == False:
                    print("not up")

            if len(fingers_up) == 5:
                print(f"Starting detection after {self.detection_wait} second")
                self.detection_start = True
                time.sleep(self.detection_wait) #sleeps 1 seconds for the user to change to the actual gesture
                print(fingers_up)

        if self.detection_start == True and self.number_start == 0:
            print("Detection started")
            if self.start_time == None:
                self.start_time = int(time.time())
            if self.end_time == None:
                self.end_time = time.time()+self.detection_window
            self.number_start = 1
            
        if self.detection_start == True and self.number_start == 1 and self.end_time != None:
            now = int(time.time()) 
            if now <= self.end_time:
               self.detection_frames.append(input_list) 
            elif now >= self.end_time:
                self.parse_list(self.detection_frames) 
                self.in_cooldown = True
                self.cooldown_end = now+5
                return self.reset()

    def parse_list(self, frames):
        '''
        converts the detection_frames list to dataclass for easier processing
        '''
        for coord in frames:
            for tip in self.FingerTipsData:
                if coord[0] == tip.id:
                    tip.x_coord.append(coord[1])
                    tip.y_coord.append(coord[2])
        print(self.FingerTipsData) 
        self.detection_frames = []  # Clears list after finish using it 
        self.identify_dir()

    def identify_dir(self):
        '''
        This function identifies the direction of travel of the finger through using 3 points of the fingertip's travel
        Should be mostly accurate
        '''
        for fingertip in self.FingerTipsData:
            first_x = fingertip.x_coord[0]
            middle_x = fingertip.x_coord[int(len(fingertip.x_coord)/2)]
            final_x = fingertip.x_coord[-1]
            diff_x = abs(final_x - first_x)
            
            first_y = fingertip.y_coord[0]
            middle_y = fingertip.y_coord[int(len(fingertip.y_coord)/2)]
            final_y = fingertip.y_coord[-1]
            diff_y = abs(final_y-first_y)
            
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
        self.parse_fingertips()
        print("Gesture Direction Done")
        self.match_gesture()
        
    def match_gesture(self):
        # Match previous information to a gesture
        DirectionsList = []
        number_fingers_up = int() 
        GestureDirection = ""
        """
        Plan for rewrite
        """
        for fingertip in self.FingerTipsData:
            DirectionsList.append(fingertip.direction)

        for finger in self.FingerTipsData:
            if finger.is_up:
                number_fingers_up += 1

        # To find the majority of the directions of fingers, the fingers direction have to be mapped to an integer value 
        DirectionsList = convert_dir_id(DirectionsList)
        GestureDirection = findMajority(DirectionsList)
        GestureDirection = convert_dir_id(GestureDirection) 
        try:
            for gesture in self.GestureList:
                # Now matches gesture with the GestureList that was imported from main
                if GestureDirection == gesture.direction and number_fingers_up == gesture.fingers_up:
                    gesture.exec_action()

                else:
                    raise GestureNotDetermined  
        except BaseException as e:
            print(e)

        finally:
            self.FingerTipsData = []
            self.parse_fingertips() # Clears FingerTipsData and recreates empty template
