import Gesture
from dataclasses import dataclass

from modules.Finger import Finger

FINGERTIPS = [4,8,12,16,20]
FingerTipList = []
@dataclass
class FingerTips:
    
    id: int
    x_coord: list
    y_coord: list
class GestureDetector:
    
    def __init__(self, detection_frames: list, gestures) -> None:
        self.detection_frames = detection_frames
        self.gestures = gestures
        
    def parse_fingertips(self):
        global FingerTipList
        for id in FINGERTIPS:
            FingerTipList.append(FingerTips(id, [], []))
        
    def parse_list(self) -> list:
        for coord in self.detection_frames:
            for tip in FingerTipList:
                if coord[0] == tip.id:
                    tip.x_coord.append(coord[1])
                    tip.y_coord.append(coord[2])
    

                                    
    