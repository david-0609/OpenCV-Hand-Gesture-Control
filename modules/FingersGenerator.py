from Finger import FingerTipList
from Finger import Finger
class FingersGenerator:

    def __init__(self) -> None:
        pass

    def create_fingers(self):
        # Creates the fingers
        Thumb = Finger(name = "Thumb", finger_id=1, ids=[1,2,3,4])
        IndexFinger = Finger(name = "Indexfinger", finger_id=2, ids=[5,6,7,8])
        MiddleFinger = Finger(name = "MiddleFinger", finger_id=3, ids=[9,10,11,12])
        RingFinger = Finger(name = "RingFinger", finger_id=4, ids=[13,14,15,16])
        LittleFinger = Finger(name = "LittleFinger", finger_id=5, ids=[17,18,19,20])
        FingerList = [Thumb,IndexFinger,MiddleFinger,RingFinger,LittleFinger]
        
        return FingerList

    def create_fingertip_list(self):
        global FingerTipList 
        for finger in FingerTipList:
        
            FingerTipList.append(finger.tip)
            return FingerTipList

