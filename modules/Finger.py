import Tools
from run import logging_list

FingerTipList = []

class Finger():

    # Factory Design Pattern    
    def __init__(self, name, ids: list, finger_id=None) -> None:
        self.name = name
        self.ids = ids
        self.tip = ids[0]
        self.finger_id = finger_id

    @property
    def is_up(self):
        ylist = []
        cleaned_list = []
        
        cleaned_list = Tools.select_coords(self.ids, logging_list)
        cleaned_list.sort(key = lambda x:x[0])
        print(cleaned_list)
        
        # If the finger is up, the y should be in a ascending order, which is sorted
        for pt in cleaned_list:
            ylist.append(pt[2])
            
        #print(ylist)

        flag = 0
        if (all(ylist[i] <= ylist[i + 1] for i in range(len(ylist)-1))):
            flag = 1
            
        if flag == 1:
            return False
        else:
            return True
                
    @property
    def tip_coord(self):
        tip_coord = Tools.select_coords(self.tip, logging_list)
        return tip_coord

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

