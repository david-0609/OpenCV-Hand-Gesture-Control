from itertools import groupby

def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

def select_coords(ids, in_list):
    cleaned_list = []
    try:
        for coord in in_list:
            print(coord)
            for id in ids:
                if coord[0] == id:
                    cleaned_list.append(coord)
    except IndexError:
        pass
    
    if cleaned_list != []:
        return cleaned_list
    else:
        return False

def findMajority(arr):
    majority = None
    maxCount = 0
    index = -1  # sentinels
    n = len(arr)
    for i in range(n):
 
        count = 0
        for j in range(n):
 
            if(arr[i] == arr[j]):
                count += 1
 
        # update maxCount if count of
        # current element is greater
        if(count > maxCount):
 
            maxCount = count
            index = i
 
    # if maxCount is greater than n/2
    # return the corresponding element
    if (maxCount > n//2):
       majority = arr[index] 

    return majority

def is_identical(list_a, list_b):
    if len(list_a) != len(list_b):
        return False
    for i in list_a:
        if i not in list_b:
            return False
    return True

def convert_dir_id(dir):
        if type(dir) == list:
            for d in dir:
                if d == "r":
                    d = 1
                elif d == "l":
                    d = 2
                elif d == "u":
                    d = 3
                elif d == "d":
                    d = 4
        if type(dir) == int:
            if dir == 1:
                dir = "r"
            elif dir == 2:
                dir = "l"
            elif dir == 3:
                dir = "u"
            elif dir == 4:
                dir = "d"
        return dir
    

