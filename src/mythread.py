import time
import threading
import socket
import json
import tkinter as tk
import mttkinter
import queue
import numpy as np
import win32gui
import logging
from logging.handlers import RotatingFileHandler
import datetime

import log
import display
import action
import utility
import local
            
rect_max = (0,0,3839,1079)
# centor = np.array([952.5,275.5])
centor = np.array([0.0, 0.0])

class Syncronize:
    def __init__(self, n):
        self.__n = n
        self.__count = 0
        self.__lock = threading.Lock()
        self.__complete = threading.Event()
        self.__exit = threading.Event()

    def wait(self, timeout):
        with LockX(self.__lock):
            self.__count += 1
            if self.__count == self.__n:
                self.__exit.clear()
                self.__complete.set()
        self.__complete.wait(timeout=timeout)
        with LockX(self.__lock):
            self.__count -= 1
            if self.__count == 0:
                self.__complete.clear()
                self.__exit.set()
                return True
        self.__exit.wait(timeout=5)
        return False
        
class MyThread:
    def __init__(self, is_server=None):
        self.local = threading.local()
        self.glob = {}
        self.__screen_lock = threading.Lock()
        self.__mouse_lock = threading.Lock()
        self.__disc_lock = threading.Lock()
        self.__clipboard_lock = threading.Lock()
        self.__sync_lock = threading.Lock()
        self.__event_lock = threading.Lock()
        self.__message_lock = threading.Lock()
        self.__battle_lock = threading.Lock()
        self.__sync:dict[str,Syncronize] = {}
        self.__event:dict[str,threading.Event] = {}
        self.__display = display.Display(queue.Queue(96))
        self.__message = {}
        self.__battle = queue.Queue(1)
        self.__connect = queue.Queue()
        self.root = None
        self.is_server = is_server
        self.__thread_disp = threading.Thread(target=self.__display.mainloop, daemon=True)
        self.__thread_disp.start()
        self._thread_battle = threading.Thread(target=self.pop_battle, daemon=True)
        self._thread_battle.start()
    
    def start(self, q=None, qs=None, id=0, ids=None, timeout=None):
        self.timeout = timeout*3600 if timeout is not None else None
        if q:
            self.interactive = True
            root = tk.Tk()
            root.attributes("-topmost", True)
            self.__logger = log.IOLogFrame(root)
            thread = threading.Thread(
                target=controller, daemon=True,
                kwargs={'thread_id':id, 'q':q})
            thread.start()
        if qs:
            if ids is None:
                ids = list(range(1,25))
            self.interactive = False
            self.__logger = None
            # self.__logger = logging.getLogger(__name__)
            # self.__logger.setLevel(logging.DEBUG)

            # rh = RotatingFileHandler(
            #         r'C:/Users/tsuka/gitrepo/Macro/log/app.log', 
            #         encoding='utf-8',
            #         maxBytes=1024,
            #         backupCount=3
            #     )

            if self.is_server is None:
                sock = None
            elif self.is_server:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print('waiting connection...')
                server.bind((local.my_ip, 796))
                server.listen(1)
                sock, addr = server.accept()
                print(f'connect {addr}')
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print('trying connection...')
                sock.connect((local.pair_ip, 796))
                print('success to connect')
            
            send = threading.Thread(target=sender, daemon=True, kwargs={'sock': sock, 'q': self.__connect})
            recv = threading.Thread(target=receiver, daemon=True, kwargs={'sock': sock})
            send.start()
            recv.start()

            self.__thread = []
            # self.__logger.addHandler(rh)
            for id, q in zip(ids, qs):
                self.__thread.append(threading.Thread(
                    target=controller, daemon=True,
                    kwargs={'thread_id':id, 'q':q}))
            for t in self.__thread:
                t.start()

        self.local.thread_id = -1
        if type(self.__logger) is log.IOLogFrame:
            self.__logger.mainloop()
        else:
            monitor = action.KeyInput(['f3','f2'])
            monitor.start()
            time.sleep(1.0)
            timer = utility.Timer()
            while any([th.is_alive() for th in self.__thread]):
                if not monitor.is_alive():
                    if monitor.key == 'f3':
                        with self.screen(),self.mouse(),self.disc():
                            monitor = action.KeyInput(['f3','f2'])
                            monitor.start()
                            time.sleep(1.0)
                            while monitor.is_alive():
                                time.sleep(1.0)
                    if monitor.key == 'f2':
                        exit()
                    monitor = action.KeyInput(['f3','f2'])
                    monitor.start()
                if timer.timeout(self.timeout):
                    break
                time.sleep(1.0)
            self.__connect.put('##exit##')
            time.sleep(1.0)
        # self.__display.request("Close", -1, -1, -1)

    def screen(self):
        if self.local.thread_id == 0:
            return LockX()
        else:
            return LockX(self.__screen_lock)

    def mouse(self):
        if self.local.thread_id == 0:
            return LockX()
        else:
            return LockX(self.__mouse_lock)

    def disc(self):
        if self.local.thread_id == 0:
            return LockX()
        else:
            return LockX(self.__disc_lock)
        
    def battle(self, t):
        with LockX(self.__battle_lock):
            self.__battle.put(t)
            self.__battle.put(0)

    def pop_battle(self):
        while 1:
            t = self.__battle.get()
            time.sleep(t)

    def clipboard_aquire(self):
        self.__clipboard_lock.acquire()

    def clipboard_release(self):
        self.__clipboard_lock.release()

    def empty(self, owner=None):
        if owner is None: owner = self.root
        return self.__display.request('Empty', owner=owner)

    def rect(self, *region, owner=None):
        if owner is None: owner = self.root
        return self.__display.request('Rect', *region, owner=owner)

    def textinit(self, *region):
        region = region[0]+70, region[1], region[2]-70, region[3]
        self.__display.request('Back', self.local.thread_id, -1, 0, region, block=True)
        self.local.tregion1 = region[0], region[1],              region[2], region[3]//2
        self.local.tregion2 = region[0], region[1]+region[3]//2, region[2], region[3]//2
        self.__display.request('Text', self.local.thread_id, 0, 1, '', self.local.tregion1)
        self.__display.request('Text', self.local.thread_id, 0, 2, '', self.local.tregion2)
        self.local.state = ""
        self.local.trial = (0,0)
        self.local.time = (datetime.timedelta(), 0, datetime.datetime.combine(datetime.date.today(), datetime.time()), datetime.datetime.combine(datetime.date.today(), datetime.time()))

    def text(self, state=None, trial=None, time=None):
        if state: self.local.state = state
        if trial: 
            if trial[1] is None:
                trial = trial[0], 0
            self.local.trial = trial
        if time: self.local.time = time
        self.__display.request("Text", self.local.thread_id, 0, 1, f'{self.local.state}', self.local.tregion1)
        text2 = f'trial={self.local.trial[0]:4d}/{self.local.trial[1]:4d}, time={int(self.local.time[0].total_seconds())}, v={int(self.local.time[1])}/h ; {self.local.time[2].strftime("%m/%d %H:%M")} -> {self.local.time[3].strftime("%m/%d %H:%M")}'
        self.__display.request("Text", self.local.thread_id, 0, 2, text2, self.local.tregion2)

    def close(self, hwnd):
        self.__display.close(hwnd)

    def print(self, str, state='MESSAGE', end='\n'):
        if type(self.__logger) is log.IOLogFrame:
            self.__logger.print(str, state=state, end=end)
        elif type(self.__logger) is logging.Logger:
            self.__logger.debug(str)

    def request(self, gui, **kwargs):
        assert self.__logger is not None
        return self.__logger.request(gui, **kwargs)

    def syncronize(self, key, n, timeout=180, peer=False):
        with LockX(self.__sync_lock):
            if key+'_enter' not in self.__sync:
                self.__sync[key+'_enter'] = Syncronize(n)
        if self.__sync[key+'_enter'].wait(timeout):
            if key+'_enter' in self.__sync:
                del self.__sync[key+'_enter']
            if peer:
                self.syncronize_peer(key)
        with LockX(self.__sync_lock):
            if key+'_exit' not in self.__sync:
                self.__sync[key+'_exit'] = Syncronize(n)
        if self.__sync[key+'_exit'].wait(timeout=None):
            del self.__sync[key+'_exit']

    def send(self, uuid, key, message, peer=False):
        with LockX(self.__message_lock):
            if uuid not in self.__message:
                self.__message[uuid] = {}
            self.__message[uuid][key] = message
        if peer:
            self.send_peer(uuid, key, message)

    def receive(self, uuid, key):
        with LockX(self.__message_lock):
            if uuid not in self.__message:
                return None
            if key not in self.__message[uuid]:
                return None
            message = self.__message[uuid][key]
        return message
    
    def delete_message(self, uuid):
        with LockX(self.__message_lock):
            del self.__message[uuid]

    def send_peer(self, uuid:str, key:str, message:str):
        m = '#'.join(['send', uuid, key, message])
        self.__connect.put(m)

    def syncronize_peer(self, key):
        m = '#'.join(['syncronize', key])
        self.__connect.put(m)
        with LockX(self.__event_lock):
            if key not in self.__event:
                self.__event[key] = threading.Event()
        self.__event[key].wait()
        with LockX(self.__event_lock):
            if key in self.__event:
                del self.__event[key]

    def notify_peer(self, key):
        with LockX(self.__event_lock):
            if key not in self.__event:
                self.__event[key] = threading.Event()
        self.__event[key].set()


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
    def __init__(self, lock:threading.Lock=None):
        self.lock = lock

    def __enter__(self):
        if self.lock: self.lock.acquire()
        return None

    def __exit__(self, ex_type, ex_value, trace):
        if self.lock: self.lock.release()
        assert ex_type is None, ex_type
        return True

class Function:
    def __init__(self, f, *args, pre=False, **kwargs):
        self.f = f
        self.args = args
        self.kwargs = kwargs
        self.pre = pre

    def __call__(self, *args, **kwargs):
        return self.f(*self.args, *args, **kwargs, **self.kwargs)

def th(i, q):
    thread = threading.Thread(
        target=controller, daemon=True,
        kwargs={'thread_id':i, 'q':q})
    thread.start()

def controller(thread_id, q:queue.Queue):
    time.sleep(1)
    mt.print(f'start thread id = {thread_id}', state='DEBUG')
    mt.local.thread_id = thread_id
    if thread_id == 0:
        mt.local.position = (np.array([0.,0.]),np.array([np.inf,np.inf]))
        region = ( 711, 85,390,27)
    else:
        x = ((thread_id - 1) // 3)
        y = (thread_id - 1) % 3
        mt.local.position = (np.array([479. * x, 350. * y]),np.array([0.01,0.01]))
        region = (4 + 480*x, 350*y, 390, 27)
    # mt.local.position = (
    #                         (np.array([0.,0.]),np.array([np.inf,np.inf])),
    #                         (np.array([-711., -84.]),np.array([0.01,0.01])),
    #                         (np.array([-711., 266.]),np.array([0.01,0.01])),
    #                         (np.array([-711., 616.]),np.array([0.01,0.01])),
    #                         (np.array([479., -84.]),np.array([0.01,0.01])),
    #                         (np.array([-232., 266.]),np.array([0.01,0.01])),
    #                         (np.array([-232., 616.]),np.array([0.01,0.01])),
    #                         (np.array([ 958., -84.]),np.array([0.01,0.01])),
    #                         (np.array([ 247., 266.]),np.array([0.01,0.01])),
    #                         (np.array([ 247., 616.]),np.array([0.01,0.01])),
    #                         (np.array([ 1437., -84.]),np.array([0.01,0.01])),
    #                         (np.array([ 726., 266.]),np.array([0.01,0.01])),
    #                         (np.array([ 726., 616.]),np.array([0.01,0.01])),
    #                         (np.array([1916., -84.]),np.array([0.01,0.01])),
    #                         (np.array([1205., 266.]),np.array([0.01,0.01])),
    #                         (np.array([1205., 616.]),np.array([0.01,0.01])),
    #                         (np.array([2395., -84.]),np.array([0.01,0.01])),
    #                         (np.array([1684., 266.]),np.array([0.01,0.01])),
    #                         (np.array([1684., 616.]),np.array([0.01,0.01])),
    #                         (np.array([2874., -84.]),np.array([0.01,0.01])),
    #                         (np.array([2163., 266.]),np.array([0.01,0.01])),
    #                         (np.array([2163., 616.]),np.array([0.01,0.01])),
    #                         (np.array([3353., -84.]),np.array([0.01,0.01])),
    #                         (np.array([2642., 266.]),np.array([0.01,0.01])),
    #                         (np.array([2642., 616.]),np.array([0.01,0.01]))
    #                     )[thread_id]
    mt.local.position_org = mt.local.position
    
    mt.local.scale = 50

    mt.local.driver = None
    mt.local.actions = None
    mt.local.current = None
    
    # region = (
    #             ( 711, 85,390,27),
    #             (   4,  0,390,27),
    #             (   4,350,390,27),
    #             (   4,700,390,27),
    #             ( 484,  0,390,27),
    #             ( 484,350,390,27),
    #             ( 484,700,390,27),
    #             ( 964,  0,390,27),
    #             ( 964,350,390,27),
    #             ( 964,700,390,27),
    #             (1444,  0,390,27),
    #             (1444,350,390,27),
    #             (1444,700,390,27),
    #             (1924,  0,390,27),
    #             (1924,350,390,27),
    #             (1924,700,390,27),
    #             (2404,  0,390,27),
    #             (2404,350,390,27),
    #             (2404,700,390,27),
    #             (2884,  0,390,27),
    #             (2884,350,390,27),
    #             (2884,700,390,27),
    #             (3364,  0,390,27),
    #             (3364,350,390,27),
    #             (3364,700,390,27),
    #           )[thread_id]
    mt.textinit(*region)
    pre = None
    while 1:
        try:
            f:Function = q.get_nowait()
            if f.pre:
                pre = f(pre=pre)
            else:
                pre = f()
        except queue.Empty:
            return

def sender(sock:socket.socket, q:queue.Queue):
    while True:
        message:str = q.get()
        if message == "##exit##":
            break
        if sock is not None:
            print('send ' + message)
            message = message + '__sep__'
            sock.sendall(message.encode())
    if sock is not None:
        sock.close()
        

def receiver(sock:socket.socket):
    if sock is not None:
        buffer = ''
        while True:
            data = sock.recv(1024)
            if not data:
                break
            message = data.decode()
            buffer = buffer + message
            while buffer.find('__sep__') >= 0:
                message, buffer = buffer.split('__sep__', maxsplit=1)
                print('receive ' + message)
                message_type, content = message.split('#', maxsplit=1)
                if message_type == 'syncronize':
                    key = content
                    mt.notify_peer(key)
                elif message_type == 'send':
                    uuid, key, message = content.split('#', maxsplit=2)
                    mt.send(uuid, key, message, peer=False)
        sock.close()
