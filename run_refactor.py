import argparse
import multiprocessing
import cv2
import os, time, signal
from modules.HandDetector import HandDetector
from modules.GestureLibs.Gesture import Gesture
from modules.GestureLibs.GestureGenerator import GestureGenerator
from modules.GestureLibs.GestureDetector import GestureDetector
from modules.Finger import FingersGenerator

'''
TODO
- Have the Finger class functional (Done)
- Make the is_up function functional (Done)
- Initialise Fingers from a config file (Not Needed)
- Figure out a way to start the detection window and track frames (Done)
- Init gesture actions from config file. (Done)
- Refactor run.py
'''

# This will contain all the coordinates from the frames
logging_list = []
fps_list = []
FingersList = []
#Other files will import this from run, not from FingersGenerator

def on_run():

    ap = argparse.ArgumentParser()
    ap.add_argument("-g", "--gui", type=bool, required=False, help="Run with GUI")
    ap.add_argument("-d", "--debug", type=bool, required=False, help="Print out debug info in console")
    ap.add_argument("--camera-dir", type=str, required=True, help="Directory of webcam e.g. /dev/video0")
    ap.add_argument("--set_config_path", type=str, required=False, help="Set the path of the config file")
    args = vars(ap.parse_args())

    gui = args["gui"]
    debug = args["debug"]
    camera_dir = args["camera_dir"]
    config_path = args["--set_config_path"]

    Runner = Run(gui, debug, camera_dir, config_path)
    Runner.run()
        
    return gui, debug, camera_dir, config_path

class Run:

    def __init__(self, gui: bool = True, debug: bool = False,  camera_dir = "/dev/video0", config_path="config"):
        self.gui = gui
        self.debug = debug
        self.camera_dir = camera_dir
        self.config = config_path

    def run(self):
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
                    
            currTime = time.time()
            fps = 1 / (currTime-prevTime)
            prevTime = currTime
            fps_list.append(fps)
            
            cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), thickness=3)
            cv2.imshow("Video", frame)
            cv2.waitKey(1)

class ProcessController:

    run_pid = int()

    def __init__(self, run_proc):
       self.run_proc = run_proc

    def start_run(self):
        global run_pid
        run_args = on_run()
        Runner = Run(gui=run_args[0], debug=run_args[1], camera_dir=run_args[2], config_path=run_args[3])
        run_proc = multiprocessing.Process(target=Runner.run)
        run_proc.start()
        run_pid = os.getpid()

    def kill_run(self):
        try:
            os.kill(run_pid, signal.SIGTERM) 
        except BaseException as e:
            print(f"Terminating process with pid %s resulted in error %s" % (run_pid, e))

    def get_run_info(self):
        global run_pid

        print(f"Process ID: %s \n" % run_pid)
       


if __name__ == "__main__":
    on_run()
