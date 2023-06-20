import argparse
import json
import os
import time
import tkinter as tk
import mttkinter
from tkinter import messagebox
from PIL import Image,ImageTk

import numpy as np
import pyautogui

import gui
import utility
import mythread

class Region:
    def __init__(self, region):
        self.__position = np.array(region[:2], dtype=np.float)
        self.__size = np.array(region[2:], dtype=np.float)

    def translation(self, diff):
        self.__position = self.__position + diff

    def scaling(self, scale, centor):
        self.__position = centor+(self.__position-centor)*scale
        self.__size = self.__size*scale
    
    def spacing(self, space):
        self.__position = self.__position-space
        self.__size = self.__size+2*space

    def region(self):
        r = (int(self.__position[0]),
             int(self.__position[1]),
             int(self.__size[0]),
             int(self.__size[1]))
        r = utility.region2rect(r)
        r = (max(r[0],mythread.rect_max[0]),
             max(r[1],mythread.rect_max[1]),
             min(r[2],mythread.rect_max[2]),
             min(r[3],mythread.rect_max[3]),)
        r = utility.rect2region(r)
        return r

    def diff(self, found):
        pos = np.array(found[:2], dtype=np.float)
        size = np.array(found[2:], dtype=np.float)
        return (pos-self.__position)+(size-self.__size)/2
        
class Symbol:
    def __init__(self):
        pass

    def __and__(self,other):
        return self

    def __or__(self,other):
        return self

    def search(self, hwnd):
        return None

    def default(self):
        code = {'_type':'Symbol','value':{}}
        return code

    def load(path):
        sym_path = os.path.join(utility.path_to_state(),f'{path}.sym.json')
        if os.path.exists(sym_path):
            # with mythread.mt.disc():
                with open(sym_path, 'rt') as f:
                    symbol = json.load(f, cls=SymbolDecoder)
        else: symbol = None
        return symbol

    def save(self, path):
        sym_path = os.path.join(utility.path_to_state(),f'{path}.sym.json')
        with mythread.mt.disc():
            with utility.openx(sym_path, 'wt') as f:
                json.dump(self, f, cls=SymbolEncoder, indent=2)

class LeafSymbol(Symbol):
    def __init__(self,image_path,region,accuracy=None):
        super().__init__()
        self.image_path = image_path
        self.region = region
        if accuracy: 
            a,b = accuracy
            self.accuracy = np.array(a),np.array(b)
        else: self.accuracy = np.array([0.01,0.01]),np.array([1.,1.])

    def __and__(self,other):
        return AndSymbol(self,other)

    def __or__(self,other):
        return OrSymbol(self,other)

    def search(self, hwnd):
        if self.image_path is None:
            return True

        scale = mythread.mt.local.scale
        mu,lam = mythread.mt.local.position
        a,b = self.accuracy
        eta = a/b

        r = Region(self.region)
        r.scaling(scale/50, mythread.centor)
        r.translation(mu)
        r.spacing(15+3*np.sqrt((1+eta/lam)/eta))
        if hwnd is not None:
            mythread.mt.rect(*r.region(), owner=hwnd)

        image = Image.open(self.image_path)
        size = int(image.width*scale/50),int(image.height*scale/50)
        image_resized = image.resize(size)
        
        # with mythread.mt.screen():
        found = pyautogui.locateOnScreen(
            image_resized, region=r.region(), confidence=0.8)

        if found:
            d = r.diff(found)
            _mu = (mu+(mu+d)*eta/lam)/(1+eta/lam)
            _lam = lam+eta
            # _a = a+(1+eta/lam)/2
            # _b = b+d**2/2
            mythread.mt.local.position = _mu,_lam
            # self.accuracy = _a,_b
            return found
        return None
    
    def capture(self):
        scale = mythread.mt.local.scale
        mu,lam = mythread.mt.local.position
        
        r = Region(self.region)
        r.scaling(scale/50, mythread.centor)
        r.translation(mu)
        img = pyautogui.screenshot(region=r.region())
        r.spacing(10)
        hwnd = mythread.mt.rect(*r.region())
        size = int(img.width*50/scale),int(img.height*50/scale)
        img = img.resize(size)
        img.save(self.image_path)
        time.sleep(0.6)
        mythread.mt.close(hwnd)

    def default(self):
        code = super().default()
        code['_type'] = 'LeafSymbol'
        code['value']['image_path'] = self.image_path
        code['value']['region'] = self.region
        a,b = self.accuracy
        code['value']['accuracy'] = (tuple(a), tuple(b))
        return code

class AndSymbol(Symbol):
    def __init__(self,left,right):
        super().__init__()
        self.left:Symbol = left
        self.right:Symbol = right
    
    def __and__(self,other):
        return AndSymbol(self,other)

    def __or__(self,other):
        return OrSymbol(self,other)

    def search(self, level=0):
        return self.right.search(level) if self.left.search(level) else None

    def default(self):
        code = super().default()
        code['_type'] = 'AndSymbol'
        code['value']['left'] = self.left
        code['value']['right'] = self.right
        return code
    
class OrSymbol(Symbol):
    def __init__(self,left,right):
        super().__init__()
        self.left:Symbol = left
        self.right:Symbol = right

    def __and__(self,other):
        return AndSymbol(self,other)

    def __or__(self,other):
        return OrSymbol(self,other)

    def search(self, level=0):
        left = self.left.search(level)
        return left if left else self.right.search(level)

    def default(self):
        code = super().default()
        code['_type'] = 'OrSymbol'
        code['value']['left'] = self.left
        code['value']['right'] = self.right
        return code

class SymbolEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Symbol): return o.default()
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
    def __init__(self, master=None, resize_rate=2, scale=None, position=None):
        super().__init__(master)
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        w = w - 1000
        h = h - 700
        self.master.geometry("+"+str(w)+"+"+str(h))
        self.master.focus_set()
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

        frame1 = tk.Frame(self.master)
        frame1.pack()

        self.button1 = tk.Button(frame1,text='crop image',command=self.crop_image)
        self.button1.pack(side=tk.LEFT)

        self.button2 = tk.Button(frame1,text='cancel',command=self.master.destroy)
        self.button2.pack(side=tk.LEFT)


        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_x = None
        self.region = None
        self.img_crop = None
        self.scale = scale
        self.position = position

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
        rect = (
                self.start_x,
                self.start_y,
                self.end_x,
                self.end_y
            )
        self.img_crop = self.img.crop(rect)
        
        self.region = utility.rect2region(rect)

        if self.scale:
            r = Region(self.region)
            r.translation(-self.position)
            r.scaling(50/self.scale, mythread.centor)
            self.region = r.region()

            size = int(self.img_crop.width*50/self.scale),int(self.img_crop.height*50/self.scale)
            self.img_crop = self.img_crop.resize(size)

        self.master.destroy()

    def destroy(self):
        self.master.quit()

def capture():
    root = tk.Toplevel()
    app = Capture(master=root)
    app.mainloop()

class MergeSymbol(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.focus_set()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        w = w - 600
        h = h - 300
        self.master.geometry("+"+str(w)+"+"+str(h))

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

        button_canncel = tk.Button(frame4, text=("Canncel"), command=self.master.destroy)
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

    def destroy(self):
        self.master.quit()

def merge_symbol():
    root = tk.Toplevel()
    app = MergeSymbol(master=root)
    app.mainloop()

def main():
    with open(os.path.join("work","gui.sym.json"),'rt') as f:
        sym = json.load(f,cls=SymbolDecoder)

    print(type(sym))
    print(sym.image_path)
    print(sym.region)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('id',type=int)
    args = parser.parse_args()
    root = tk.Tk()
    position =(
            (np.array([0.,0.]),np.array([np.inf,np.inf])),
            (np.array([-711., -84.]),np.array([0.01,0.01])),
            (np.array([-711., 266.]),np.array([0.01,0.01])),
            (np.array([-711., 616.]),np.array([0.01,0.01])),
            (np.array([-230., -84.]),np.array([0.01,0.01])),
            (np.array([-230., 266.]),np.array([0.01,0.01])),
            (np.array([-230., 616.]),np.array([0.01,0.01])),
            (np.array([ 251., -84.]),np.array([0.01,0.01])),
            (np.array([ 251., 266.]),np.array([0.01,0.01])),
            (np.array([ 251., 616.]),np.array([0.01,0.01])),
            (np.array([ 732., -84.]),np.array([0.01,0.01])),
            (np.array([ 732., 266.]),np.array([0.01,0.01])),
            (np.array([ 732., 616.]),np.array([0.01,0.01]))
        )[args.id][0]
    app = Capture(master=root,scale=50,position=position)
    app.mainloop()
    if app.img_crop is not None:
        img_name = utility.unique_name('sym.png','.png')
        img_path = f'{img_name}.png'
        app.img_crop.save(img_path)
        symbol = LeafSymbol(img_path, app.region)
        symbol.save(img_path)