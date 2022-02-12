import cv2
import sys, os, time
from modules.HandDetector import HandDetector
from modules.GestureLibs import Gesture
from modules.GestureLibs import GestureGenerator
from modules.GestureLibs import GestureDetector
from modules.Finger import FingersGenerator

'''
TODO
- Have the Finger class functional (Done)
- Make the is_up function functional (Done)
- Initialise Fingers from a config file (Not Needed)
- Figure out a way to start the detection window and track frames
- Init gesture actions from config file. 
'''
# This will contain all the coordinates from the frames
logging_list = []
fps_list = []
FingersGenerator = FingersGenerator() 
FingerList = FingersGenerator.create_fingers()
# Other files will import this from run, not from FingersGenerator

def main():
    global logging_list
    global fps_list
    
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
        #print(lmList)
        print(IndexFinger.is_up)
                
        currTime = time.time()
        fps = 1 / (currTime-prevTime)
        prevTime = currTime
        fps_list.append(fps)
        
        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), thickness=3)
        cv2.imshow("Video", frame)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()
