import cv2
import mediapipe as mp
import time
from collections import namedtuple
from itertools import groupby

'''
TODO
- Have the Finger class functional
- Make the is_up function functional
- Initialise Fingers from a config file
'''
logging_list = []

class HandDetector():
    
    def __init__(self, mode = False, max_hands = 2):

        self.mode = mode
        self.max_hands = max_hands
        
        self.capture = cv2.VideoCapture(0)

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.max_hands)
        self.mpDraw = mp.solutions.drawing_utils
    
    def fdHands(self, frame, draw = True):

        self.results = self.hands.process(frame)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)
                else:
                    print("Not drawing")
                    
        return frame
    
    def fdPositions(self, frame):
        landmarks_list = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            for id, lm in enumerate(hand.landmark):
                h, w, _= frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks_list.append([id, cx, cy])
                        
        return landmarks_list
    
def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

Point = namedtuple("Point", ["id", "x", "y"])

def select_coords(ids):
    cleaned_list = []
    orig_list = logging_list[-1]
    for coord in orig_list:
        for id in ids:
            if coord[0] == id:
                cleaned_list.append(coord)
                
    return cleaned_list
                
class Finger():
    
    def __init__(self, ids: list) -> None:
        self.ids = ids.sort()
    
    def is_up(self):
        ptlist = []
        ylist = []
        result_list = []
        
        cleaned_list = select_coords(self.ids)
        for coord in cleaned_list:
            pt = Point(coord[0],coord[1],coord[2])
            ptlist.append(pt)
        
        
        # If the finger is up, the y should be in a ascending order, which is sorted
        for pt in ptlist:
            ylist.append(pt.y)
        if ylist == ylist.sort():
            return True
        else:
            return False
        
def main():
    global lmList
    global logging_list
    capture = cv2.VideoCapture(0)
    detector = HandDetector()
    prevTime = 0
    currTime = 0
    
            
    while True:
        _, frame = capture.read()
        frame = cv2.flip(frame, 1)
        frame = detector.fdHands(frame)
        
        lmList = detector.fdPositions(frame)
        logging_list.append(lmList)
        print(lmList)
                
        currTime = time.time()
        fps = 1 / (currTime-prevTime)
        prevTime = currTime
        
        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), thickness=3)
        cv2.imshow("Video", frame)
        cv2.waitKey(1)
        
main()