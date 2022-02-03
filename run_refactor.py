import argparse
import multiprocessing

class Run:
    
    def __init__(self, gui: bool = True, debug: bool = False,  camera_dir = "/dev/video0"):
        self.gui = gui
        self.debug = debug
        self.camera_dir = camera_dir
        
    def run(self):
        pid = None
        return pid
        pass
    
    def stop(self):
        pass
        #kill(pid)

    def status(self):
        pass
        #return pid
        
ap = argparse.ArgumentParser()
ap.add_argument("-g", "--gui", required=False, help="Run with GUI")
ap.add_argument("-d", "--debug", required=False, help="Print out debug info in console")
ap.add_argument("--camera-dir", required=True, help="Directory of webcam e.g. /dev/video0")
args = vars(ap.parse_args())

Runner = Run( True if args["gui"] else False, True if args["debug"] else False, args["camera_dir"])


