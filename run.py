ErrorLog = []
arguments = {}

# This will contain all the coordinates from the frames
logging_list = []
fps_list = []
# Other files will import this from run, not from FingersGenerator
processes = []

import sys, os
print(sys.path)
currpath = os.getcwd()
sys.path.append(currpath+"/modules")
sys.path.append(currpath+"/modules/GestureLibs")
print(sys.path)
import argparse
import multiprocessing
import cv2
import time
from pynput import keyboard
import modules.HandDetector as HandDetector
import modules.GestureLibs.GestureDetector as GestureDetector
import modules.GestureLibs.GestureGenerator as GestureGenerator
import modules.FingersGenerator as FingersGenerator

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

    '''
    camera_dir = os.environ["CAMERA_DIR"] 
    if camera_dir == "":
        camera_dir = "/dev/video0"
        print("No camera directory specified, going with default /dev/video0")
       
    config_path = os.environ["CONFIG_PATH"]
    if config_path == "":
        config_path = ".config"
        print("config file not specified, defaulting to '.config'")
    '''

    return {"debug":debug, "camera_dir":camera_dir, "config_path":config_path} 

class Run:
    
    gesture_detector = None

    FingersList = []
    GestureList = []

    def __init__(self, debug: bool, camera_dir: str, config_path: str):

        self.debug = debug
        self.camera_dir = camera_dir
        self.config_path = config_path

        global FingersGenerator
        FingersGenerator = FingersGenerator.FingersGenerator()

        global GestureGenerator
        GestureGenerator = GestureGenerator.GestureGenerator(self.config_path)
        self.GestureList = GestureGenerator.read_config()

        global GestureDetector
        GestureDetector = GestureDetector.GestureDetector()
        GestureDetector.parse_fingertips()
        self.gesture_detector = GestureDetector

    def run(self):
        
        global logging_list
        global fps_list
       
        capture = cv2.VideoCapture(0)
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
            fps_list.append(fps)
                
            lmList = detector.fdPositions(frame)
            logging_list.append(lmList)
            print(lmList)
            if self.gesture_detector.start_detection() == False:
                logging_list = []

            if self.debug:
               
                cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), thickness=3)
                cv2.imshow("Video", frame)
                cv2.waitKey(1)
'''
class Runner:

    run_proc = None

    def __init__(self):
        pass

    def start_run(self):
        self.run_proc = multiprocessing.Process(target=Run.run)
        return self.run_proc

    def kill_run(self, key):
        print("Press Q to stop program")
        try:
            if key.char == "q" or "Q":  
                self.run_proc.terminate()
                return False # Stops listener  
        except BaseException as e:
            print(f"Terminating process resulted in error %s" % e)

        return False # Stops listener

if __name__ == "__main__":
    arguments = get_arguments()
    Controller = ProcessController()
    run_proc =Controller.start_run()
    listener = keyboard.Listener(on_press=Controller.kill_run)
    processes.append(run_proc)
    processes.append(listener)
    for process in processes:
        process.start()
        process.join()
'''
if __name__ == "__main__":
    arguments = get_arguments()
    run = Run(arguments["debug"],arguments["camera_dir"],arguments["config_path"])
    run.run()
