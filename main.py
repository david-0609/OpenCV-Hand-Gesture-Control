import time
from itertools import groupby
import Finger, Gesture, HandDetector

'''
TODO
- Have the Finger class functional
- Make the is_up function functional
- Initialise Fingers from a config file
'''
# This will contain all the coordinates from the frames
logging_list = []
fps_list = []

# Creates the fingers
Thumb = Finger([1,2,3,4])
IndexFinger = Finger([5,6,7,8])
MiddleFinger = Finger([9,10,11,12])
RingFinger = Finger([13,14,15,16])
LittleFinger = Finger([17,18,19,20])
FingerList = [Thumb,IndexFinger,MiddleFinger,RingFinger,LittleFinger]
    
def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

def select_coords(ids):
    cleaned_list = []
    orig_list = logging_list[-1]
    for coord in orig_list:
        for id in ids:
            if coord[0] == id:
                cleaned_list.append(coord)
                
    return cleaned_list

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