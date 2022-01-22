import Gesture
from dataclasses import dataclass

from modules.Finger import Finger
from modules.Exceptions import DirectionNotDetermined

FINGERTIPS = [4,8,12,16,20]
FingerTipList = []
@dataclass
class FingerTips:
    
    id: int
    x_coord: list
    y_coord: list
    direction: str
class GestureDetector:
    
    def __init__(self, detection_frames: list, gestures) -> None:
        self.detection_frames = detection_frames
        self.gestures = gestures
        
    def parse_fingertips(self):
        global FingerTipList
        for id in FINGERTIPS:
            FingerTipList.append(FingerTips(id, [], [], ""))
        
    def parse_list(self) -> list:
        for coord in self.detection_frames:
            for tip in FingerTipList:
                if coord[0] == tip.id:
                    tip.x_coord.append(coord[1])
                    tip.y_coord.append(coord[2])
                    
    def identify_dir(self):
        for fingertip in FingerTipList:
            first_x = fingertip.x_coord[0]
            middle_x = fingertip.x_coord[int(len(fingertip.x_coord)/2)]
            final_x = fingertip.x_coord[-1]
            diff_x = final_x - first_x
            
            first_y = fingertip.y_coord[0]
            middle_y = fingertip.y_coord[int(len(fingertip.y_coord)/2)]
            final_y = fingertip.y_coord[-1]
            diff_y = final_y-first_y
            
            if diff_x > diff_y:
                # goes left/right
                if first_x < middle_x < final_x:
                    fingertip.direction = "r" # R for right
                elif first_x > middle_x > final_x:
                    fingertip.direction = "l" # L for left
                else:
                    raise DirectionNotDetermined
                
            
                                    
    