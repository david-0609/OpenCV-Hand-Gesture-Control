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

