import json
import os
import tkinter as tk
from tkinter import messagebox,filedialog
from PIL import Image,ImageTk

import pyautogui
from pyscreeze import ImageNotFoundException

import gui

class LeafSymbol:
    def __init__(self,image_path,region):
        self.image_path = image_path
        self.region = region

    def __and__(self,other):
        return AndSymbol(self,other)

    def __or__(self,other):
        return OrSymbol(self,other)

    def search(self):
        try:
            return pyautogui.locateOnScreen(self.image_path,region=self.region)
        except ImageNotFoundException:
            return None

class AndSymbol:
    def __init__(self,left,right):
        self.left = left
        self.right = right
    
    def __and__(self,other):
        return AndSymbol(self,other)

    def __or__(self,other):
        return OrSymbol(self,other)

    def search(self):
        return self.right.search() if self.left.search() else None

class OrSymbol:
    def __init__(self,left,right):
        self.left = left
        self.right = right

    def __and__(self,other):
        return AndSymbol(self,other)

    def __or__(self,other):
        return OrSymbol(self,other)

    def search(self):
        left = self.left.search()
        return left if left else self.right.seach()

class SymbolEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, LeafSymbol):
            return {'_type': 'LeafSymbol', 
                    'value': {'image_path':o.image_path,
                              'region':o.region}}
        if isinstance(o, AndSymbol):
            return {'_type': 'AndSymbol', 
                    'value': {'left':o.left,
                              'right':o.right}}
        if isinstance(o, OrSymbol):
            return {'_type': 'OrSymbol', 
                    'value': {'left':o.left,
                              'right':o.right}}
        return json.JSONEncoder.default(self, o)

class SymbolDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook,
                                  *args, **kwargs)

    def object_hook(self, o):
        if '_type' not in o:
            return o
        type = o['_type']
        if type == 'LeafSymbol':
            return LeafSymbol(**o['value'])
        if type == 'AndSymbol':
            return AndSymbol(**o['value'])
        if type == 'OrSymbol':
            return OrSymbol(**o['value'])

class Capture(tk.Frame):
    # https://qiita.com/hisakichi95/items/47f6d37e6f425f29c8a8
    def __init__(self, master=None, resize_rate=2):
        super().__init__(master)
        self.resize_rate = resize_rate

        # 表示する画像の取得（スクリーンショット）
        self.img = pyautogui.screenshot()
        # スクリーンショットした画像は表示しきれないので画像リサイズ
        self.img_resized = self.img.resize(size=(int(self.img.width / self.resize_rate),
                                                 int(self.img.height / self.resize_rate)),
                                                 resample=Image.BILINEAR)

        # tkinterで表示できるように画像変換
        self.img_tk = ImageTk.PhotoImage(self.img_resized)

        # Canvasウィジェットの描画
        self.canvas = tk.Canvas(self.master,
                                bg="black",
                                width=self.img_resized.width,
                                height=self.img_resized.height)
        # Canvasウィジェットに取得した画像を描画
        self.canvas.create_image(0, 0, image=self.img_tk, anchor=tk.NW)

        # Canvasウィジェットを配置し、各種イベントを設定
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self.start_point_get)
        self.canvas.bind("<Button1-Motion>", self.rect_drawing)
        self.canvas.bind("<ButtonRelease-1>", self.release_action)

        self.button1 = tk.Button(
                self.master,
                text='crop image',
                command=self.crop_image
            )
        self.button1.pack()

        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_x = None

    # ドラッグ開始した時のイベント - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def start_point_get(self,event):
        self.canvas.delete("rect1")  # すでに"rect1"タグの図形があれば削除

        # canvas1上に四角形を描画（rectangleは矩形の意味）
        self.canvas.create_rectangle(event.x,
                                     event.y,
                                     event.x + 1,
                                     event.y + 1,
                                     outline="red",
                                     tag="rect1")
        # グローバル変数に座標を格納
        self.start_x, self.start_y = event.x, event.y

    # ドラッグ中のイベント - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def rect_drawing(self,event):
        # ドラッグ中のマウスポインタが領域外に出た時の処理
        if event.x < 0:
            self.end_x = 0
        else:
            self.end_x = min(self.img_resized.width, event.x)
        if event.y < 0:
            self.end_y = 0
        else:
            self.end_y = min(self.img_resized.height, event.y)

        # "rect1"タグの画像を再描画
        self.canvas.coords("rect1", self.start_x, self.start_y, self.end_x, self.end_y)

    # ドラッグを離したときのイベント - - - - - - - - - - - - - - - - - - - - - - - - - - 
    def release_action(self,event):
        # "rect1"タグの画像の座標を元の縮尺に戻して取得
        self.start_x, self.start_y, self.end_x, self.end_y = [
            round(n * self.resize_rate) for n in self.canvas.coords("rect1")
        ]

    def crop_image(self):
        region = (self.start_x,
                  self.start_y,
                  self.end_x,
                  self.end_y)
        img_crop = self.img.crop(region)
        # img_crop.show()
        dict = {'filename':None}
        gui.entry(dict)
        filename = dict['filename']
        if filename:
            img_crop.save(os.path.join("work","img",f"{filename}.png"))
            sym = LeafSymbol(f"{filename}.png",region)
            with open(os.path.join("work",f"{filename}.sym.json"),'xt') as f:
                json.dump(sym,f,cls=SymbolEncoder,indent=2)

def capture():
    root = tk.Tk()
    app = Capture(master=root)
    app.mainloop()

class MergeSymbol(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        frame1 = tk.Frame(self.master)
        frame1.grid(row=0, column=1, sticky=tk.E)

        self.fd1 = gui.FileDialog(frame1, text="Symbol1>>", ext="*.sym.json", dir="work")
        self.fd1.pack()

        frame2 = tk.Frame(self.master)
        frame2.grid(row=2, column=1, sticky=tk.E)

        self.fd2 = gui.FileDialog(frame2, text="Symbol2>>", ext="*.sym.json", dir="work")
        self.fd2.pack()

        frame3 = tk.Frame(self.master)
        frame3.grid(row=4, column=1, sticky=tk.E)

        label3 = tk.Label(frame3, text="Symbol3>>")
        label3.pack(side=tk.LEFT)

        self.entry3 = tk.Entry(frame3, width=30)
        self.entry3.pack(side=tk.LEFT)

        frame4 = tk.Frame(self.master)
        frame4.grid(row=5,column=1,sticky=tk.W)

        button_and = tk.Button(frame4, text="And", command=self.and_symbol)
        button_and.pack(fill = "x", padx=30, side = "left")

        button_or = tk.Button(frame4, text=("Or"), command=self.or_symbol)
        button_or.pack(fill = "x", padx=30, side = "left")

        button_canncel = tk.Button(frame4, text=("Canncel"), command=quit)
        button_canncel.pack(fill = "x", padx=30, side = "left")    

    def and_symbol(self):
        path1 = self.fd1.get()
        if not os.path.exists(path1):
            messagebox.showerror("error", "Invalid file path for Symbol1")
            return
        path2 = self.fd2.get()
        if not os.path.exists(path2):
            messagebox.showerror("error", "Invalid file path for Symbol2")
            return
        path3 = self.entry3.get()
        if not path3:
            messagebox.showerror("error", "Invalid file path for Symbol3")
            return

        with open(path1,'rt') as f:
            sym1 = json.load(f,cls=SymbolDecoder)
        with open(path2,'rt') as f:
            sym2 = json.load(f,cls=SymbolDecoder)
        sym3 = AndSymbol(sym1,sym2)
        with open(os.path.join("work",f"{path3}.sym.json"),'xt') as f:
            json.dump(sym3,f,cls=SymbolEncoder,indent=2) 

        self.fd1.set("")
        self.fd2.set("")
        self.entry3.delete(0,'end')

        messagebox.showinfo("success","And-merge successfully finished")  

    def or_symbol(self):
        path1 = self.fd1.get()
        if not os.path.exists(path1):
            messagebox.showerror("error", "Invalid file path for Symbol1")
            return
        path2 = self.fd2.get()
        if not os.path.exists(path2):
            messagebox.showerror("error", "Invalid file path for Symbol2")
            return
        path3 = self.entry3.get()
        if not path3:
            messagebox.showerror("error", "Invalid file path for Symbol3")
            return

        with open(path1,'rt') as f:
            sym1 = json.load(f,cls=SymbolDecoder)
        with open(path2,'rt') as f:
            sym2 = json.load(f,cls=SymbolDecoder)
        sym3 = OrSymbol(sym1,sym2)
        with open(os.path.join("work",f"{path3}.sym.json"),'xt') as f:
            json.dump(sym3,f,cls=SymbolEncoder,indent=2)
        
        self.fd1.set("")
        self.fd2.set("")
        self.entry3.delete(0,'end')

        messagebox.showinfo("success","Or-merge successfully finished")

def merge_symbol():
    root = tk.Tk()
    app = MergeSymbol(master=root)
    app.mainloop()

def main():
    with open(os.path.join("work","gui.sym.json"),'rt') as f:
        sym = json.load(f,cls=SymbolDecoder)

    print(type(sym))
    print(sym.image_path)
    print(sym.region)

if __name__=="__main__":
    merge_symbol()