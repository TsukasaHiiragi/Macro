import os
import time

def unique_name(name,ext=''):
    if not os.path.exists(f"{name}{ext}"):
        return name
    i = 1
    while os.path.exists(f"{name}{i}{ext}"):
        i += 1
    return f"{name}{i}"

def path_to_state():
    
    return 'C:\\Users\\miyas\\Macro\\state'

class OpenX:
    def __init__(self, file, mode):
        self.file = file
        self.mode = mode

    def __enter__(self):
        try:
            self.fp = open(self.file, self.mode)
        except FileNotFoundError:
            if self.mode == 'wt':
                os.makedirs(os.path.dirname(self.file), exist_ok=True)
            self.fp = open(self.file, self.mode)

        return self.fp

    def __exit__(self, ex_type, ex_value, trace):
        if ex_type: 
            print('openx exception: file = ', self.file)
            print(ex_type, ex_value, trace)
        self.fp.close()
        return True

def openx(file, mode):
    return OpenX(file, mode)

class Timer:
    def __init__(self):
        self.start = time.time()

    def elapse(self):
        return time.time() - self.start

    def timeout(self, max):
        return self.elapse() > max

def rect2region(rect):
    return rect[0],rect[1],rect[2]-rect[0],rect[3]-rect[1]

def region2rect(region):
    return region[0],region[1],region[0]+region[2],region[1]+region[3]