import os
import time
import datetime

def unique_name(name,ext=''):
    if not os.path.exists(f"{name}{ext}"):
        return name
    i = 1
    while os.path.exists(f"{name}{i}{ext}"):
        i += 1
    return f"{name}{i}"

def path_to_state():
    return 'C:\\Users\\tsuka\\gitrepo\\Macro\\state'

def path_to_repo():
    return 'C:\\Users\\tsuka\\gitrepo\\Macro'


class OpenX:
    def __init__(self, file, mode):
        self.file = file
        self.mode = mode

    def __enter__(self):
        while 1:
            try:
                self.fp = open(self.file, self.mode)
            except FileNotFoundError:
                if self.mode == 'wt':
                    os.makedirs(os.path.dirname(self.file), exist_ok=True)
            except Exception as e:
                print(e)
                time.sleep(1)
            else:
                break

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
        self.start = datetime.datetime.now()
        self.latest = self.start

    def elapse(self):
        return datetime.datetime.now() - self.start

    def lap(self):
        t = datetime.datetime.now()
        d = t - self.latest
        self.latest = t
        return d
    
    def timeout(self, max):
        if max is None: return False
        return self.elapse().total_seconds() > max
    
    def reset(self):
        self.start = datetime.datetime.now()
        self.latest = self.start

def rect2region(rect):
    return rect[0],rect[1],rect[2]-rect[0],rect[3]-rect[1]

def region2rect(region):
    return region[0],region[1],region[0]+region[2],region[1]+region[3]