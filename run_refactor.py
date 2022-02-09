import argparse
import multiprocessing
import os
'''
from modules import HandDetector
from modules import Exceptions
'''
class Run:
    
    def __init__(self, gui: bool = True, debug: bool = False,  camera_dir = "/dev/video0"):
        self.gui = gui
        self.debug = debug
        self.camera_dir = camera_dir
        
    def run(self):
        pass
        # This will start the detection
    
    def get_info(self):
        '''
        Check if the pid above is running, using multiprocessing library
        '''
        print("Process ID:", os.getpid())

    def stop(self):
        try:
            run_proc.terminate()
        except BaseException as e:
            print("Error terminating PID", e)
       
ap = argparse.ArgumentParser()
ap.add_argument("-g", "--gui", required=False, help="Run with GUI")
ap.add_argument("-d", "--debug", required=False, help="Print out debug info in console")
ap.add_argument("--camera-dir", required=True, help="Directory of webcam e.g. /dev/video0")
ap.add_argument("--set_config_path", required=False, help="Set the path of the config file")
args = vars(ap.parse_args())

Runner = Run( True if args["gui"] else False, True if args["debug"] else False, args["camera_dir"])

if __name__ == "__main__":
    run_proc = multiprocessing.Process(target=Runner.run)
    run_proc.start()
    
    #run_proc.join()

