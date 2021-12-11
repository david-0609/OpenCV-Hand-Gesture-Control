import cv2
import mediapipe as mp
import time
from collections import namedtuple

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

class DetectFinger:
    
    def __init__(self, finger_ids, landmarkList) -> None:
        self.finger_ids == finger_ids
        self.landmarkList = landmarkList
    
    def finger_up(finger_ids, landmarkList) -> bool:
        
        Point = namedtuple("Point", ["x", "y"])
        ptList = []
        cleanLMlist = []
        
        for coord in landmarkList:
            for id in finger_ids:
                if id == coord[0]:
                    cleanLMlist.append(coord)
        
        for coord in cleanLMlist:
            del coord[0]
            coord_x = coord[0]
            coord_y = coord[1]
            pt = Point(coord_x, coord_y)
            ptList.append(pt)
        previous_y = None
        
        times_run = 0
        result_list = []
        for point in ptList:
            curr_y = point[1]
            if times_run == 0:
                previous_y = curr_y
                times_run += 1
            elif times_run > 0 and curr_y != previous_y and previous_y < curr_y:
                print("true")
                result_list.append(True)
                times_run +=1
        
        if all(x == True for x in result_list):
            return True
        
def main():
    capture = cv2.VideoCapture(0)
    detector = HandDetector()
    prevTime = 0
    currTime = 0
    
    def findLandmark(lmList, lmIDs: list) -> list:
        lmIDlist = []
        for id in lmIDs:
            lmIDlist.append(lmList[id])
        return lmIDlist
            
            
    while True:
        _, frame = capture.read()
        frame = cv2.flip(frame, 1)
        frame = detector.fdHands(frame)
        
        lmList = detector.fdPositions(frame)
        try:
            print(findLandmark(lmList, [4, 8, 12, 16, 20]))
        except IndexError:
            print("Not Found")
        
        currTime = time.time()
        fps = 1 / (currTime-prevTime)
        prevTime = currTime
        
        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), thickness=3)
        cv2.imshow("Video", frame)
        cv2.waitKey(1)
        
main()