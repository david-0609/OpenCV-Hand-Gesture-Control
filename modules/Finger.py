import Tools

class Finger():
    
    def __init__(self, ids: list, finger_id=None) -> None:
        self.ids = ids
        self.tip = ids[0]
        self.finger_id = finger_id

    @property
    def is_up(self):
        ylist = []
        cleaned_list = []
        
        cleaned_list = Tools.select_coords(self.ids)
        cleaned_list.sort(key = lambda x:x[0])
        print(cleaned_list)
        
        # If the finger is up, the y should be in a ascending order, which is sorted
        for pt in cleaned_list:
            ylist.append(pt[2])
            
        print(ylist)

        flag = 0
        if (all(ylist[i] <= ylist[i + 1] for i in range(len(ylist)-1))):
            flag = 1
            
        if flag == 1:
            return False
        else:
            return True
                
    @property
    def tip_coord(self):
        tip_coord = Tools.select_coords(self.tip)
        return tip_coord

class FingersFactory:

    def __init__(self, finger_ids) -> None:
        self,finger_ids = finger_ids
        return finger_ids

    def create_fingers(self):
        # Creates the fingers
        Thumb = Finger(finger_id=1, ids=[1,2,3,4])
        IndexFinger = Finger(finger_id=2, ids=[5,6,7,8])
        MiddleFinger = Finger(finger_id=3, ids=[9,10,11,12])
        RingFinger = Finger(finger_id=4, ids=[13,14,15,16])
        LittleFinger = Finger(finger_id=5, ids=[17,18,19,20])
        FingerList = [Thumb,IndexFinger,MiddleFinger,RingFinger,LittleFinger]
        
        return FingerList
