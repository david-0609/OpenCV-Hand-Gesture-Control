ErrorLog = []
arguments = {}

# This will contain all the coordinates from the frames
lmList = []
# Other files will import this from run, not from FingersGenerator
processes = []

import sys, os
print(sys.path)
currpath = os.getcwd()
sys.path.append(currpath+"/modules")
sys.path.append(currpath+"/modules/GestureLibs")
print(sys.path)
import argparse
import cv2
import time
import modules.HandDetector as HandDetector

'''
TODO
- Have the Finger class functional (Done)
- Make the is_up function functional (Done)
- Initialise Fingers from a config file (Not Needed)
- Figure out a way to start the detection window and track frames (Done)
- Init gesture actions from config file. (Done)
- Refactor run.py (Mostly complete)
- Testing
'''

def get_arguments():
     # parses arguments passed in on launch
    ap = argparse.ArgumentParser()
    ap.add_argument("--debug", type=bool, required=False, help="Print out debug info in console")
    args = ap.parse_args()
  
    if args.debug:
        debug = True
    else:
        debug = False

    env = os.environ.copy()

    if "CAMERA_DIR" not in env:
        camera_dir = "/dev/video0"
    else:
        camera_dir = env.get("CAMERA_DIR")

    if "CONFIG_PATH" not in env:
        config_path = ".config"
    else:
        config_path = env.get("CONFIG_PATH")

    return {"debug":debug, "camera_dir":camera_dir, "config_path":config_path} 


class Run:
    
    gesture_detector = None

    FingersList = []
    GestureList = []

    def __init__(self, debug: bool, camera_dir: str, config_path: str):

        self.debug = debug
        self.camera_dir = camera_dir
        self.config_path = config_path
 
        import modules.FingersGenerator as FingersGenerator
        FingersGenerator = FingersGenerator.FingersGenerator()
        self.FingersList = FingersGenerator.create_fingers()
   
        import modules.GestureLibs.GestureGenerator as GestureGenerator
        GestureGenerator = GestureGenerator.GestureGenerator(self.config_path)
        self.GestureList = GestureGenerator.read_config()
        
        FingerTipList = []
        for finger in self.FingersList:
            FingerTipList.append(finger.tip) 
      
        import modules.GestureLibs.GestureDetector as GestureDetector
        GestureDetector = GestureDetector.GestureDetector(FingersList=self.FingersList, 
                                                          GestureList=self.GestureList,
                                                          FingerTipList = FingerTipList)
        self.gesture_detector = GestureDetector
        self.gesture_detector.create_fingertips()
       
        if self.debug:
            print(self.FingersList)
            print(self.GestureList)
            print(self.gesture_detector)

    def run(self):
        
        global lmList
        capture = cv2.VideoCapture(self.camera_dir)
        detector = HandDetector.HandDetector()
        prevTime = 0
        currTime = 0

        while True:
            _, frame = capture.read()
            frame = cv2.flip(frame, 1)
            frame = detector.fdHands(frame)

            currTime = time.time()
            fps = 1 / (currTime-prevTime)
            prevTime = currTime
 
            if self.debug:
               
                cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), thickness=3)
                cv2.imshow("Video", frame)
                cv2.waitKey(1)
               
            lmList = detector.fdPositions(frame)
            print(lmList)
            if self.gesture_detector.start_detection(lmList) == False:
                print("Gesture Detection not starting")

if __name__ == "__main__":
    arguments = get_arguments()
    run = Run(arguments["debug"],arguments["camera_dir"],arguments["config_path"])
    run.run()
