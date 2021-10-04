import os
import tkinter as tk
from tkinter import filedialog
           
class Entry(tk.Frame):
    def __init__(self, master=None, items=[]):
        super().__init__(master)
        w,h = 500,100
        x = self.winfo_screenwidth()-w
        y = self.winfo_screenheight()-h-50
        self.master.geometry(f'{w}x{h}+{x}+{y}')
        
        self.items = items
        self.entry = {}
        self.str = {}

        self.master.title('Entry')
        self.master.resizable(False, False)
        self.master.focus_set()

        frame1 = tk.Frame(self.master)
        frame1.pack()

        for i, item in enumerate(items):
            label = tk.Label(frame1, text=item)
            label.grid(row=i, column=0, sticky=tk.E)

            # Entry
            self.entry[item] = tk.Entry(frame1,width=20)
            self.entry[item].grid(row=i, column=1)
        
        frame2 = tk.Frame(self.master)
        frame2.pack()

        button1 = tk.Button(frame2, text='OK', command=self.getstr)
        button1.pack(side=tk.LEFT)

        button2 = tk.Button(frame2, text='Cancel', command=self.master.destroy)
        button2.pack(side=tk.LEFT)

    def getstr(self):
        for item in self.items:
            self.str[item] = self.entry[item].get()
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
    def __init__(self, master=None, text="", default="", initdir="", ext="*"):
        super().__init__(master)
        self.ext = ext
        self.default = default
        self.initdir = initdir

        label = tk.Label(self.master, text=text)
        label.pack(side=tk.LEFT)

        self.entry = tk.Entry(self.master, width=30)
        self.entry.pack(side=tk.LEFT)

        button1 = tk.Button(self.master, text="search...", command=self.filedialog)
        button1.pack(side=tk.LEFT)

    def filedialog(self):
        filetype = [("", self.ext)]
        filepath = filedialog.askopenfilename(filetype=filetype, initialdir=self.initdir)
        self.entry.delete(0,'end')
        self.entry.insert(0,filepath)

    def get(self):
        return self.entry.get()

    def set(self,text):
        self.entry.delete(0,'end')
        self.entry.insert(0,text)

class DirDialog(tk.Frame):
    def __init__(self, master=None, text="", default="", initdir=""):
        super().__init__(master)
        self.default = default
        self.initdir = initdir

        label = tk.Label(self.master, text=text)
        label.pack(side=tk.LEFT)

        self.entry = tk.Entry(self.master, width=30)
        self.entry.pack(side=tk.LEFT)

        button1 = tk.Button(self.master, text="search...", command=self.dirdialog)
        button1.pack(side=tk.LEFT)

    def dirdialog(self):
        dirpath = filedialog.askdirectory(initialdir=self.initdir)
        self.entry.delete(0,'end')
        self.entry.insert(0,dirpath)

    def get(self):
        return self.entry.get()

    def set(self,text):
        self.entry.delete(0,'end')
        self.entry.insert(0,text)

class DirEntry(tk.Frame):
    def __init__(self, master=None, items=[], **kwargs):
        super().__init__(master)
        w,h = 500,100
        x = self.winfo_screenwidth()-w
        y = self.winfo_screenheight()-h-50
        self.master.geometry(f'{w}x{h}+{x}+{y}')
        
        self.items = items
        self.entry = {}
        self.str = {}

        self.master.title('FileEntry')
        self.master.resizable(False, False)
        self.master.focus_set()

        frame1 = tk.Frame(self.master)
        frame1.pack()

        for i, item in enumerate(items):
            # Entry
            self.entry[item] = DirDialog(frame1, text=item, **kwargs)
            self.entry[item].pack()
        
        frame2 = tk.Frame(self.master)
        frame2.pack()

        button1 = tk.Button(frame2, text='OK', command=self.getstr)
        button1.pack(side=tk.LEFT)

        button2 = tk.Button(frame2, text='Cancel', command=self.master.destroy)
        button2.pack(side=tk.LEFT)

    def getstr(self):
        for item in self.items:
            self.str[item] = self.entry[item].get()
        self.master.destroy()

    def destroy(self):
        self.master.quit()

# メイン処理 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
if __name__ == "__main__":
    pass