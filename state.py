import json
import os
import shutil

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import image
import gui

class DefState(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.focus_set()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        w = w - 600
        h = h - 300
        self.master.geometry("+"+str(w)+"+"+str(h))

        frame1 = tk.Frame(self.master)
        frame1.pack()

        self.dialog1 = gui.FileDialog(frame1, text="Symbol of State", dir="work", ext="*.sym.json")
        self.dialog1.pack(side=tk.LEFT)

        frame2 = tk.Frame(self.master)
        frame2.pack()

        self.dialog2 = gui.DirDialog(frame2, text="Save to ...", dir="state")
        self.dialog2.pack(side=tk.LEFT)

        frame3 = tk.Frame(self.master)
        frame3.pack()

        label1 = tk.Label(frame3,text="State Name")
        label1.pack(side=tk.LEFT)

        self.entry1 = tk.Entry(frame3)
        self.entry1.pack(side=tk.LEFT)

        frame4 = tk.Frame(self.master)
        frame4.pack()

        button1 = tk.Button(frame4, text="capture symbol", command=image.capture)
        button1.pack(side=tk.LEFT)

        button2 = tk.Button(frame4, text="merge symbol", command=image.merge_symbol)
        button2.pack(side=tk.LEFT)

        button3 = tk.Button(frame4, text="save", command=self.save)
        button3.pack(side=tk.LEFT)

        button4 = tk.Button(frame4, text="cancel", command=self.master.destroy)
        button4.pack(side=tk.LEFT)

    def save(self):
        symbol_path = self.dialog1.get()
        if not os.path.exists(symbol_path):
            messagebox.showerror("error","Invalid symbol path")
            return
        state_path = self.dialog2.get()
        if not os.path.exists(state_path):
            messagebox.showerror("error","Invalid state path")
            return
        state_name = self.entry1.get()
        if not state_name:
            messagebox.showerror("error","Please input state name")
            return
        state_dir = os.path.join(state_path,state_name)
        os.makedirs(state_dir)
        os.makedirs(os.path.join(state_dir,"img"))
        with open(symbol_path,'rt') as f:
            symbol = json.load(f,cls=image.SymbolDecoder)
        DefState.save_images(symbol, os.path.join(state_dir,"img"))
        shutil.copy(symbol_path, state_dir)
        messagebox.showinfo("success","state is successflly saved")
        self.master.destroy()
    
    def save_images(symbol, path):
        if hasattr(symbol,'image_path'):
            shutil.copy(os.path.join("work","img",symbol.image_path),path)
        if hasattr(symbol,'left'):
            DefState.save_images(symbol.left, path)
        if hasattr(symbol,'right'):
            DefState.save_images(symbol.right, path)
        
    def destroy(self):
        self.master.quit()

def def_state():
    root = tk.Toplevel()
    app = DefState(master=root)
    app.mainloop()

class ControllState(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.focus_set()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        w = w - 400
        h = h - 300
        self.master.geometry("+"+str(w)+"+"+str(h))

        frame1 = tk.Frame(self.master)
        frame1.pack()

        button1 = tk.Button(frame1, text="Define State", command=def_state)
        button1.pack(side=tk.LEFT)

        button2 = tk.Button(frame1, text="clear", command=self.clear)
        button2.pack(side=tk.LEFT)
    
    def clear(self):
        if messagebox.askyesno("confirm","clear work"):
            shutil.rmtree("work")
            os.makedirs(os.path.join("work","img"))

    def destroy(self):
        self.master.quit()

def controll_state():
    root = tk.Toplevel()
    app = ControllState(master=root)
    app.mainloop()

if __name__=='__main__':
    root = tk.Tk()
    app = ControllState(master=root)
    app.mainloop()