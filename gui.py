import os
import tkinter as tk
from tkinter import filedialog
import pyautogui  
from PIL import Image, ImageTk
            
class EasyEntry(tk.Frame):
    def __init__(self, key, master=None):
        super().__init__(master)
        self._key = key

        self.master.title('Easy Entry')
        self.master.resizable(False, False)
        frame1 = tk.Frame(self.master)
        frame1.grid()

        label = tk.Label(frame1, text=key)
        label.grid(row=0, column=0, sticky=tk.E)

        # Entry
        self.str = None
        self.entry = tk.Entry(
            frame1,
            width=20)
        self.entry.grid(row=0, column=1)
        
        frame2 = tk.Frame(frame1)
        frame2.grid(row=2, column=1, sticky=tk.W)

        button1 = tk.Button(
                frame2, text='OK', command=self.getstr
            )
        button1.pack(side=tk.LEFT)

        button2 = tk.Button(frame2, text='Cancel', command=self.master.destroy)
        button2.pack(side=tk.LEFT)
    
    def getstr(self):
        self.str = self.entry.get()
        self.master.destroy()
  
def entry(key):
    root = tk.Tk()
    app = EasyEntry(key, master=root)
    app.mainloop()
    return app.str

# メイン処理 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
if __name__ == "__main__":
    pass