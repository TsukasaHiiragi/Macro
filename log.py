import win32gui
import win32con
import queue
import sys
import time
import threading
import tkinter as tk
import mttkinter as mtk
from tkinter import scrolledtext

import mythread

TEXT_COLORS = {
    'MESSAGE' : 'white',
    'INPUT' : 'blue',
    'OUTPUT' : 'green',
    'ERROR' : 'red',
    'DEBUG' : 'yellow',
    'KEYWORD' : 'cyan',
    'KEY' : 'magenta'    
    }

# Initial value = flag=True or False
class SimpleCheck(tk.Checkbutton):
    def __init__(self, parent, *args, **kw):
        self.flag = kw.pop('flag')
        self.var =  tk.BooleanVar()
        if self.flag:
            self.var.set(True)
        self.txt = kw["text"]
        tk.Checkbutton.__init__(self, parent, *args, **kw, variable=self.var)

    def get(self):
        return self.var.get()

class IOLogFrame(tk.Frame):
    def __init__(self, master):    
        tk.Frame.__init__(self, master)
        master.title("Log Window")
        w,h = 700,350
        x = self.winfo_screenwidth()-w
        y = self.winfo_screenheight()-h-50
        self.master.geometry(f'{w}x{h}+{x}+{y}')

        #view/hide choice
        select_frame = tk.LabelFrame(master, text= "Log text disable",relief = 'groove')

        self.ckboxs = []
        for key in TEXT_COLORS:
            cb = SimpleCheck(select_frame, text=key, command=self.callback, flag=False)
            self.ckboxs.append(cb)
            cb.pack(side='left')
        select_frame.pack(side = 'top', fill = 'x')

        self.txt = scrolledtext.ScrolledText(master)
        self.txt.configure(bg='black')
        self.txt.pack(fill=tk.BOTH, expand=1)
        self.txt.bind('<Control-c>', self.finish)
        self.txt.focus_set()
        for key in TEXT_COLORS:
            self.txt.tag_config(key, foreground=TEXT_COLORS[key])

        self.lock = threading.Lock()
        self.event = threading.Event()
        self.flag_req = False
        self.gui = None
        self.kwargs = {}
        self.app = None
        self.after(1, self.response)

    def callback(self):
        count = 0
        for key in TEXT_COLORS:
            if(self.ckboxs[count].get()):
                self.hide(key)
            else:
                self.view(key)
            count += 1

    def print(self, str, state='MESSAGE', end='\n'):
        self.txt.insert(tk.END, str+end, state)
        self.txt.see(tk.END)

    def hide(self, tag):
        self.txt.tag_config(tag, elide=True)

    def view(self, tag):
        self.txt.tag_config(tag, elide=False)

    def write(self, str, state='MESSAGE'):
        self.txt.insert(tk.END, str+'\n', state)
        self.txt.see(tk.END)

    def flush(self):
        pass

    def destroy(self):
        self.master.quit()

    def finish(self, event):
        self.destroy()

    def request(self, gui, **kwargs):
        self.lock.acquire()
        self.gui = gui
        self.kwargs = kwargs
        self.flag_req = True
        self.event.wait()
        self.event.clear()
        self.lock.release()
        return self.app

    def response(self):
        if self.flag_req:
            root = tk.Toplevel()
            root.attributes("-topmost", True)
            self.app = self.gui(root, **self.kwargs)
            self.app.mainloop()
            self.gui = None
            self.kwargs = {}
            self.flag_req = False
            self.event.set()
        self.after(1, self.response)

logger:IOLogFrame
