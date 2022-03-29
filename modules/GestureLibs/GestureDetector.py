import time
import sys
import os
import pyautogui
from modules.Exceptions import GestureNotDetermined
from Tools import findMajority, convert_dir_id
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
pparentdir = os.path.dirname(parentdir)
sys.path.append(pparentdir)

class FingerTips:

    def __init__(self, id: int, x_coord: list, y_coord: list, direction: str):
        self.id = id
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.direction = direction

class GestureDetector:
    detection_window = 3 
    detection_wait = 3
    FingerTipsData = [] 
    number_up = [] 
    detection_frames = []
    start_time = None 
    end_time = None 
    detection_start = False 
    done = False
    number_start = 0
    in_cooldown = False
    cooldown_time = 5
    cooldown_end = None

    def __init__(self, FingersList, GestureList, FingerTipList) -> None:
        self.FingerTipList = FingerTipList
        self.FingersList = FingersList
        self.GestureList = GestureList

    def create_fingertips(self):
        print(self.FingerTipList)
        for id in self.FingerTipList:
            p = FingerTips(id, x_coord=[], y_coord=[], direction="")
            self.FingerTipsData.append(p)
        print("Initial data,",self.FingerTipsData)

    def reset(self):
        print("resetting data")
        self.detection_start = False
        self.start_time = None
        self.end_time = None
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
                print(finger_is_up)
                
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
                time.sleep(self.detection_wait) #sleeps 3 seconds for the user to change to the actual gesture
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
                up_list = []
                for finger in self.FingersList:
                    finger_tip = finger.tip
                    fingertip_coord = finger.tip_coord(finger_tip, input_list)
                    print("fingertip_coord", fingertip_coord)
                    up_list.append(finger.is_up(input_list))
                    self.detection_frames.append(fingertip_coord) 
                for i in up_list:
                    if not i:
                        up_list.remove(i)
                self.number_up.append(len(up_list)) 
            elif now >= self.end_time:
                self.in_cooldown = True
                self.cooldown_end = now+5
                return_value = self.reset()
                self.parse_list()
                return return_value

    def parse_list(self):
        '''
        converts the detection_frames list to dataclass for easier processing
        '''
        print("detection_frames", self.detection_frames)
        for tip in self.FingerTipsData:
            tip.x_coord = []
            tip.y_coord = []
            for coord in self.detection_frames:
                if coord[0] == tip.id:
                    tip.x_coord.append(coord[1])
                    tip.y_coord.append(coord[2])
        print("fingertipsdata: ", self.FingerTipsData) 
        self.detection_frames = []  # Clears list after finish using it 
        self.identify_dir()

    def identify_dir(self):
        '''
        This function identifies the direction of travel of the finger through using 3 points of the fingertip's travel
        Should be mostly accurate
        '''
        for fingertip in self.FingerTipsData:
            first_x = fingertip.x_coord[0]
            final_x = fingertip.x_coord[-1]
            diff_x = abs(final_x - first_x)
            print(diff_x)
            
            first_y = fingertip.y_coord[0]
            final_y = fingertip.y_coord[-1]
            diff_y = abs(final_y-first_y)
            print(diff_y)

            if diff_x > diff_y:
                print(first_x, final_x)
                # goes left/right
                if first_x < final_x:
                    fingertip.direction = "r" # R for right
                elif first_x > final_x:
                    fingertip.direction = "l" # L for left
                
            elif diff_y > diff_x:
                #goes up/down      
                if first_y < final_y:
                    fingertip.direction = "u"
                elif first_y < final_y:
                    fingertip.direction = "d"
            print("direction", fingertip.direction)

        print("Gesture Direction Done")
        self.match_gesture()
        
    def match_gesture(self):
        # Match previous information to a gesture
        DirectionsList = []
        GestureDirection = ""

        for fingertip in self.FingerTipsData:
            DirectionsList.append(fingertip.direction)

        print(DirectionsList)

        # To find the majority of the directions of fingers, the fingers direction have to be mapped to an integer value 
        DirectionsList = convert_dir_id(DirectionsList)
        GestureDirection = findMajority(DirectionsList)
        self.number_up = findMajority(self.number_up)
        GestureDirection = convert_dir_id(GestureDirection) 
        print(GestureDirection)
        print(self.number_up)
        print(len(self.GestureList))
        dev_1plus = self.number_up + 1
        dev_1minus = self.number_up - 1
        for gesture in self.GestureList:
            print(gesture.direction, gesture.fingers_up, type(gesture.fingers_up))
            # Now matches gesture with the GestureList that was imported from main
            if GestureDirection == gesture.direction :
                if self.number_up == gesture.fingers_up or dev_1minus == gesture.fingers_up or dev_1plus == gesture.fingers_up:
                    pyautogui.alert('A gesture is detected', "Success")
                    gesture.exec_action()
                    print("Gesture Detected")

            else:
                print("No Gesture Detected") 

        self.FingerTipsData = []
        self.number_up = []
        self.create_fingertips() # Clears FingerTipsData and recreates empty template
