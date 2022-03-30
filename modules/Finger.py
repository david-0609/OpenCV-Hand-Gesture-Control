import Tools

FingerTipList = []

class Finger():

    # Factory Design Pattern    
    def __init__(self, name, ids: list, finger_id=None) -> None:
        self.name = name
        self.ids = ids
        self.tip = ids[0]
        self.finger_id = finger_id

    def is_up(self, in_list):
        ylist = []
        cleaned_list = []
        
        cleaned_list = Tools.select_coords(self.ids, in_list)

        if cleaned_list != False and cleaned_list != None:

            cleaned_list.sort(key = lambda x:x[0])
        
            # If the finger is up, the y should be in a ascending order, which is sorted
            for pt in cleaned_list:
                ylist.append(pt[2])
                    
            ylist_copy = ylist.copy()
            ylist.sort(reverse=True)
            if ylist == ylist_copy:
                print("Is up")
                return True
            else:
                print("not up")
                return False
        
    def tip_coord(self, ids, in_list):
        tip_coord = Tools.select_coords(ids, in_list)
        return tip_coord

