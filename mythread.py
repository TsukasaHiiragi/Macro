import time
import threading
import tkinter as tk
import mttkinter
import queue
import numpy as np
import win32gui

import log
import display
import action
            
rect_max = (0,0,1919,1079)
centor = np.array([945.,415.])

class Syncronize:
    def __init__(self, n):
        self.__n = n
        self.__count = 0
        self.__lock = threading.Lock()
        self.__complete = threading.Event()
        self.__exit = threading.Event()

    def wait(self):
        with LockX(self.__lock):
            self.__count += 1
            if self.__count == self.__n:
                self.__exit.clear()
                self.__complete.set()
        self.__complete.wait()
        with LockX(self.__lock):
            self.__count -= 1
            if self.__count == 0:
                self.__complete.clear()
                self.__exit.set()
        self.__exit.wait()
        
class MyThread:
    def __init__(self, q=None, qs=None):
        self.local = threading.local()
        self.glob = {}
        self.__screen_lock = threading.Lock()
        self.__mouse_lock = threading.Lock()
        self.__disc_lock = threading.Lock()
        self.__cripboard_lock = threading.Lock()
        self.__sync_lock = threading.Lock()
        self.__sync:dict[str,Syncronize] = {}
        self.__display = display.Display()
        self.root = None
        if q:
            root = tk.Tk()
            root.attributes("-topmost", True)
            self.__logger = log.IOLogFrame(root)
            thread = threading.Thread(
                target=controller, daemon=True,
                kwargs={'thread_id':0, 'q':q})
            thread.start()
        if qs:
            self.__logger = None
            for i, q in enumerate(qs):
                thread = threading.Thread(
                    target=controller, daemon=True,
                    kwargs={'thread_id':i+1, 'q':q})
                thread.start()
    
    def start(self):
        thread = threading.Thread(target=self.__display.mainloop, daemon=True)
        thread.start()
        self.root = self.__display.request('Empty')
        if self.__logger:
            self.__logger.mainloop()
        else:
            key = None
            while key != 'f2':
                key = action.key_input(['f1','f2'])
                if key == 'f1':
                    with self.screen(),self.mouse(),self.disc():
                        key = action.key_input(['f1','f2'])


    def screen(self):
        return LockX(self.__screen_lock)

    def mouse(self):
        return LockX(self.__mouse_lock)

    def disc(self):
        return LockX(self.__disc_lock)

    def cripboard_aquire(self):
        self.__cripboard_lock.acquire()

    def cripboard_release(self):
        self.__cripboard_lock.release()

    def empty(self, owner=None):
        if owner is None: owner = self.root
        return self.__display.request('Empty', owner=owner)

    def rect(self, *region, owner=None):
        if owner is None: owner = self.root
        return self.__display.request('Rect', *region, owner=owner)

    def textinit(self, *region):
        self.local.textbox = self.__display.request('Back', *region, owner=self.root)
        self.local.tregion1 = region[0], region[1], region[2], 25
        self.local.tregion2 = region[0], region[1]+25, region[2], 25
        self.local.thwnd1 = self.__display.request('Text', '', *self.local.tregion1, owner=self.local.textbox)
        self.local.thwnd2 = self.__display.request('Text', '', *self.local.tregion2, owner=self.local.textbox)
        mt.local.state = ""
        mt.local.trial = (0,0)
        mt.local.member = []
    
    def text(self, state=None, trial=None, member=None):
        if state: self.local.state = state
        if trial: self.local.trial = trial
        if member: self.local.member = member.__str__()
        hwnd1 = self.__display.request("Text", 
            f'{self.local.state}', 
            *self.local.tregion1, owner=self.local.textbox)
        hwnd2 = self.__display.request("Text", 
            f'trial = {self.local.trial[0]:4d}/{self.local.trial[1]:4d}, member = {self.local.member}',
            *self.local.tregion2, owner=self.local.textbox)
        self.close(self.local.thwnd1)
        self.close(self.local.thwnd2)
        self.local.thwnd1 = hwnd1
        self.local.thwnd2 = hwnd2

    def close(self, hwnd):
        self.__display.close(hwnd)

    def print(self, str, state='MESSAGE', end='\n'):
        if self.__logger:
            self.__logger.print(str, state=state, end=end)

    def request(self, gui, **kwargs):
        assert self.__logger is not None
        return self.__logger.request(gui, **kwargs)

    def syncronize(self, key, n):
        with LockX(self.__sync_lock):
            if key not in self.__sync:
                self.__sync[key] = Syncronize(n)
        self.__sync[key].wait()

mt:MyThread

class Window:
    def __init__(self, owner=None):
        self.owner = owner
        self.hwnd = None

    def __enter__(self):
        self.hwnd = mt.empty(self.owner)
        return self.hwnd

    def __exit__(self, ex_type, ex_value, trace):
        assert ex_type is None, ex_type 
        mt.close(self.hwnd)
        return True

def window(owner=None):
    return Window(owner=owner)

class LockX:
    def __init__(self, lock:threading.Lock):
        self.lock = lock

    def __enter__(self):
        self.lock.acquire()
        return None

    def __exit__(self, ex_type, ex_value, trace):
        self.lock.release()
        assert ex_type is None, ex_type
        return True

class Function:
    def __init__(self, f, *args, **kwargs):
        self.f = f
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return self.f(*self.args, **self.kwargs)

def th(i, q):
    thread = threading.Thread(
        target=controller, daemon=True,
        kwargs={'thread_id':i, 'q':q})
    thread.start()

def controller(thread_id, q:queue.Queue):
    time.sleep(1)
    mt.print(f'start thread id = {thread_id}', state='DEBUG')
    mt.local.thread_id = thread_id
    mt.local.position = ((np.array([0.,0.]),np.array([np.inf,np.inf])),
                         (np.array([-625.,-150.]),np.array([0.01,0.01])),
                         (np.array([-625., 360.]),np.array([0.01,0.01])),
                         (np.array([   5.,-150.]),np.array([0.01,0.01])),
                         (np.array([   5., 360.]),np.array([0.01,0.01])),
                         (np.array([ 640.,-150.]),np.array([0.01,0.01])),
                         (np.array([ 640., 360.]),np.array([0.01,0.01])))[thread_id]
    mt.local.scale = (50,44,44,44,44,44,44)[thread_id]
    region = (( 580,110,730,50),
              (   0,470,635,50),
              (   0,990,635,50),
              ( 635,470,635,50),
              ( 635,990,635,50),
              (1270,470,635,50),
              (1270,990,635,50))[thread_id]
    mt.textinit(*region)
    while 1:
        try:
            f:Function = q.get_nowait()
            f()
        except queue.Empty:
            return
