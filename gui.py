import os
import tkinter as tk
from tkinter import filedialog
import pyautogui  
from PIL import Image, ImageTk
            
class Entry(tk.Frame):
    def __init__(self, master=None, dict={}):
        super().__init__(master)
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        w = w - 400
        h = h - 300
        self.master.geometry("+"+str(w)+"+"+str(h))
        
        self.dict = dict
        self.entry = {}

        self.master.title('Easy Entry')
        self.master.resizable(False, False)
        self.master.focus_set()

        frame1 = tk.Frame(self.master)
        frame1.grid()

        for i, key in enumerate(dict.keys()):
            label = tk.Label(frame1, text=key)
            label.grid(row=i, column=0, sticky=tk.E)

            # Entry
            self.entry[key] = tk.Entry(frame1,width=20)
            self.entry[key].grid(row=i, column=1)
        
        frame2 = tk.Frame(frame1)
        frame2.grid(row=2, column=1, sticky=tk.W)

        button1 = tk.Button(
                frame2, text='OK', command=self.getstr
            )
        button1.pack(side=tk.LEFT)

        button2 = tk.Button(frame2, text='Cancel', command=self.master.destroy)
        button2.pack(side=tk.LEFT)
    
    def getstr(self):
        for key in self.dict.keys():
            self.dict[key] = self.entry[key].get()
        self.master.destroy()

    def destroy(self):
        self.master.quit()
  
def entry(dict):
    root = tk.Toplevel()
    app = Entry(master=root, dict=dict)
    app.mainloop()

class Select(tk.Frame):
    def __init__(self, master=None, cand=[]):
        super().__init__(master)
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        w = w - 400
        h = h - 300
        self.master.geometry("+"+str(w)+"+"+str(h))
        
        self.cand = cand
        
        self.master.title('Select')
        self.master.resizable(False, False)
        self.master.focus_set()

        frame = tk.Frame(self.master)
        frame.pack()

        lf = tk.LabelFrame(frame, text='Options')

        self.v = tk.StringVar()
        for value in cand:
            rb1 = tk.Radiobutton(lf, text=value, value=value, variable=self.v) 
            rb1.pack()
        
        button = tk.Button(frame, text='OK', command=self.destroy)
        button.pack()
    
    def destroy(self):
        self.master.quit()
  
def select(cand):
    root = tk.Toplevel()
    app = Select(master=root, cand=cand)
    app.mainloop()
    return app.v.get()

class FileDialog(tk.Frame):
    def __init__(self, master=None, text="", default="", dir="", ext="*"):
        super().__init__(master)
        self.ext = ext
        self.default = default
        self.dir = dir

        label = tk.Label(self.master, text=text)
        label.pack(side=tk.LEFT)

        self.entry = tk.Entry(self.master, width=30)
        self.entry.pack(side=tk.LEFT)

        button1 = tk.Button(self.master, text="search...", command=self.filedialog)
        button1.pack(side=tk.LEFT)

    def filedialog(self):
        filetype = [("", self.ext)]
        if self.default:
            initdir = self.default
        else:
            initdir = os.path.abspath(os.path.dirname(__file__))
            if self.dir:
                initdir = os.path.join(initdir, self.dir)
        filepath = filedialog.askopenfilename(filetype=filetype, initialdir=initdir)
        self.entry.delete(0,'end')
        self.entry.insert(0,filepath)

    def get(self):
        return self.entry.get()

    def set(self,text):
        self.entry.delete(0,'end')
        self.entry.insert(0,text)

class DirDialog(tk.Frame):
    def __init__(self, master=None, text="", default="", dir=""):
        super().__init__(master)
        self.default = default
        self.dir = dir

        label = tk.Label(self.master, text=text)
        label.pack(side=tk.LEFT)

        self.entry = tk.Entry(self.master, width=30)
        self.entry.pack(side=tk.LEFT)

        button1 = tk.Button(self.master, text="search...", command=self.dirdialog)
        button1.pack(side=tk.LEFT)

    def dirdialog(self):
        if self.default:
            initdir = self.default
        else:
            initdir = os.path.abspath(os.path.dirname(__file__))
            if self.dir:
                initdir = os.path.join(initdir, self.dir)
        dirpath = filedialog.askdirectory(initialdir=initdir)
        self.entry.delete(0,'end')
        self.entry.insert(0,dirpath)

    def get(self):
        return self.entry.get()

    def set(self,text):
        self.entry.delete(0,'end')
        self.entry.insert(0,text)

# メイン処理 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
if __name__ == "__main__":
    pass