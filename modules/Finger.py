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

        if cleaned_list != False:

            cleaned_list.sort(key = lambda x:x[0])
        
            # If the finger is up, the y should be in a ascending order, which is sorted
            for pt in cleaned_list:
                ylist.append(pt[2])
                    
            print(ylist)

            index = 0
            TrueList = []
            for _ in ylist:
                try:
                    if ylist[index] > ylist[index+1]:
                        TrueList.append(True)
                        index += 1
                except IndexError:
                    break

            true_number = 0
            TrueListLength = len(TrueList)
            for i in TrueList:
                if i:
                    true_number += 1
            if true_number-1 == TrueListLength or true_number == TrueListLength:
                return True
            else:
                return False
        elif cleaned_list == False:
            return 0 

    @property
    def tip_coord(self):
        from run import lmList
        tip_coord = Tools.select_coords(self.tip, lmList)
        return tip_coord

