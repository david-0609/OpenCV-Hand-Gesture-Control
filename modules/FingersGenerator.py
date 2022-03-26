import pickle
from pathlib import Path

class FingersGenerator:

    picklefile = ".pickled_fingerslist"
    
    def __init__(self) -> None:
        pass

    def create_fingers(self):
        import Finger
        # The FingersList variable is stored in a pickle file as it is constant, there is no need to create the list
        # every time the program runs
        path = Path(self.picklefile) 
        print(path.is_file())
        if not path.is_file():

            # Creates the fingers
            Thumb = Finger.Finger(name = "Thumb", finger_id=1, ids=[1,2,3,4])
            IndexFinger = Finger.Finger(name = "Indexfinger", finger_id=2, ids=[5,6,7,8])
            MiddleFinger = Finger.Finger(name = "MiddleFinger", finger_id=3, ids=[9,10,11,12])
            RingFinger = Finger.Finger(name = "RingFinger", finger_id=4, ids=[13,14,15,16])
            LittleFinger = Finger.Finger(name = "LittleFinger", finger_id=5, ids=[17,18,19,20])
            FingerList = [Thumb,IndexFinger,MiddleFinger,RingFinger,LittleFinger]
            
            with open(self.picklefile, "wb") as file:
                pickle.dump(FingerList, file) 
        else:
            with open(self.picklefile, "rb") as file:
                FingerList = pickle.load(file)

        return FingerList

    def create_fingertip_list(self):
        from Finger import FingerTipList

        for finger in FingerTipList:
        
            FingerTipList.append(finger.tip)
            return FingerTipList

