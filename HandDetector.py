import cv2
import mediapipe as mp
import time

class HandDetector():
    
    def __init__(self, mode = False, max_hands = 2):

        self.mode = mode
        self.max_hands = max_hands
        
        self.capture = cv2.VideoCapture(0)

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.max_hands)
        self.mpDraw = mp.solutions.drawing_utils
    
    def fdHands(self, frame, draw = True):

        results = self.hands.process(frame)
        
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)
                else:
                    print("Not drawing")
                    
        return frame

def main():
    capture = cv2.VideoCapture(0)
    detector = HandDetector()
    
    prevTime = 0
    currTime = 0
    
    while True:
        isTrue, frame = capture.read()
        frame = cv2.flip(frame, 1)
        frame = detector.fdHands(frame)
        
        currTime = time.time()
        fps = 1 / (currTime-prevTime)
        prevTime = currTime
        
        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), thickness=3)
        cv2.imshow("Video", frame)
        cv2.waitKey(1)
        
main()