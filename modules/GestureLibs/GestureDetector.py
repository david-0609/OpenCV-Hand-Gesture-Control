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
        """
        Determines if the start condition is met (all 5 fingers up) and records raw data within the detection window
        """
        if self.in_cooldown and self.cooldown_end != None: 
            print(f"In cooldown, cooldown ends in {int(self.cooldown_end-time.time())}")
            if int(time.time()) > self.cooldown_end:
                self.in_cooldown = False

        if self.detection_start == False and self.in_cooldown == False:
            fingers_up = []
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
                time.sleep(self.detection_wait) #sleeps 3 seconds for the user to change to the actual gesture

        if self.detection_start == True and self.number_start == 0: 
            print("Detection started")
            if self.start_time == None:
                self.start_time = int(time.time())
            if self.end_time == None:
                self.end_time = time.time()+self.detection_window
            self.number_start = 1 # The number_start variable prevents this from running twice and constantly resetting the time
            
        if self.detection_start == True and self.number_start == 1 and self.end_time != None:
            now = int(time.time()) 
            if now <= self.end_time:
                up_list = []
                for finger in self.FingersList:
                    finger_tip = finger.tip
                    fingertip_coord = finger.tip_coord(finger_tip, input_list)
                    up_list.append(finger.is_up(input_list))
                    # self.detection_frames used to store data from within the detection window
                    self.detection_frames.append(fingertip_coord) 
                for i in up_list:
                    if not i:
                        # Removes all fingers that are not up
                        up_list.remove(i)
                try:
                    self.number_up.append(len(up_list)) # For every frame, the number of fingers up is collected 
                except BaseException as e:
                    print(e)
            elif now >= self.end_time:
                self.in_cooldown = True
                self.cooldown_end = now+5
                self.parse_list()
                return self.reset() # This return value tells run.py to print out a message 

    def parse_list(self):
        '''
        converts the detection_frames list to dataclass for easier processing
        '''
        for tip in self.FingerTipsData:
            tip.x_coord = []
            tip.y_coord = []
            for coord in self.detection_frames:
                try:
                    if coord[0] == tip.id:
                        tip.x_coord.append(coord[1])
                        tip.y_coord.append(coord[2])
                except BaseException as e:
                    print(e)
        self.detection_frames = []  # Clears list after finish using it 
        self.identify_dir()

    def identify_dir(self):
        '''
        This function identifies the direction of travel of the finger through using 3 points of the fingertip's travel
        Should be mostly accurate
        '''
        for fingertip in self.FingerTipsData:
            # Simple mechanism to determine gesture, compares change in x with change in y to determine 
            # horizontal or vertical movement etc, simple logic
            first_x = fingertip.x_coord[0]
            final_x = fingertip.x_coord[-1]
            diff_x = abs(final_x - first_x)
            
            first_y = fingertip.y_coord[0]
            final_y = fingertip.y_coord[-1]
            diff_y = abs(final_y-first_y)
            print(diff_x, diff_y)
            if diff_x > diff_y:
                print("Left or right")
                # goes left/right
                if first_x < final_x:
                    print("right")
                    fingertip.direction = "r" # R for right
                elif first_x > final_x:
                    print("left")
                    fingertip.direction = "l" # L for left
                
            elif diff_y > diff_x:
                print("Up or down")
                print(first_y, final_y)
                #goes up/down      
                if first_y > final_y:
                    print("up")
                    fingertip.direction = "u"
                elif first_y < final_y:
                    print("Down")
                    fingertip.direction = "d"
            else:
                print("Direction cannot be determined")

        print("Gesture Direction Done")
        self.match_gesture()
        
    def match_gesture(self):
        # Match previous information to a gesture
        DirectionsList = []
        GestureDirection = ""

        for fingertip in self.FingerTipsData:
            DirectionsList.append(fingertip.direction)
        print("Directions", DirectionsList)

        # To find the majority of the directions of fingers, the fingers direction have to be mapped to an integer value 
        DirectionsList = convert_dir_id(DirectionsList)
        GestureDirection = findMajority(DirectionsList) # Finds most common value
        self.number_up = findMajority(self.number_up)
        print("Num of fingers up:", self.number_up)
        GestureDirection = convert_dir_id(GestureDirection) 
        # Allows the number of fingers detected to be one more or one less to compensate for error
        print("GestureDirection", GestureDirection)

        if GestureDirection == "u" or GestureDirection == "d":
            print("Adjusting")
            if self.number_up >= 3:
                self.number_up = self.number_up - 2 # Adjust for error from observation

        try:
            dev_1plus = self.number_up + 1
            dev_1minus = self.number_up - 1
        except TypeError:
            print("Error in Gesture Detection")
        for gesture in self.GestureList:
            # Now matches gesture with the GestureList that was imported from main
            if GestureDirection == gesture.direction and GestureDirection != "u" and GestureDirection != "d":
                if self.number_up == gesture.fingers_up or dev_1minus == gesture.fingers_up or dev_1plus == gesture.fingers_up:
                    pyautogui.alert('A gesture is detected, Gesture name: '+gesture.name, title="Success")
                    gesture.exec_action()
                    print("Gesture Detected")

            elif GestureDirection == "u" or GestureDirection == "d":
                if self.number_up == gesture.fingers_up:
                    pyautogui.alert('A gesture is detected, Gesture name: '+gesture.name, title="Success")
                    gesture.exec_action()

            else:
                print("No Gesture Detected") 
            
        # Resets the variables for next run
        self.FingerTipsData = []
        self.number_up = []
        self.create_fingertips() # Clears FingerTipsData and recreates empty template
