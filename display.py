import win32api
import win32con
import win32gui
import threading
import queue
import time

hInstance = win32api.GetModuleHandle()

class EmptyWindow:
    def __init__(self):
        #get instance handle

        # the class name
        className = 'Empty'


        # create and initialize window class
        wndClass                = win32gui.WNDCLASS()
        wndClass.lpfnWndProc    = self.wndProc
        wndClass.hInstance      = hInstance
        wndClass.hbrBackground  = win32gui.GetStockObject(win32con.WHITE_BRUSH)
        wndClass.lpszClassName  = className

        # register window class
        self.wndClassAtom = None
        try:
            self.wndClassAtom = win32gui.RegisterClass(wndClass)
        except Exception as e:
            print(e)
            raise e

    def instanciate(self, owner=None):
        hWindow = win32gui.CreateWindowEx(
            win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST,
            self.wndClassAtom,                   #it seems message dispatching only works with the atom, not the class name
            '',
            win32con.WS_POPUP,
            0, 0, 0, 0, owner, 0, hInstance, None)
        win32gui.SetLayeredWindowAttributes(hWindow, 0x00FFFFFF, 0x00, win32con.LWA_COLORKEY)

        # Show & update the window
        win32gui.ShowWindow(hWindow, win32con.SW_SHOWNORMAL)
        win32gui.UpdateWindow(hWindow)
        return hWindow

    def wndProc(self, hWnd, message, wParam, lParam):
        return win32gui.DefWindowProc(hWnd, message, wParam, lParam)

class RectWindow:
    def __init__(self):
        #get instance handle

        # the class name
        className = 'Rect'


        # create and initialize window class
        wndClass                = win32gui.WNDCLASS()
        wndClass.lpfnWndProc    = self.wndProc
        wndClass.hInstance      = hInstance
        wndClass.hbrBackground  = win32gui.GetStockObject(win32con.WHITE_BRUSH)
        wndClass.lpszClassName  = className

        # register window class
        self.wndClassAtom = None
        try:
            self.wndClassAtom = win32gui.RegisterClass(wndClass)
        except Exception as e:
            print(e)
            raise e

    def instanciate(self, region, owner=None):
        hWindow = win32gui.CreateWindowEx(
            win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST,
            self.wndClassAtom,                   #it seems message dispatching only works with the atom, not the class name
            '',
            win32con.WS_POPUP,
            *region, owner, 0, hInstance, None)
        win32gui.SetLayeredWindowAttributes(hWindow, 0x00FFFFFF, 0x00, win32con.LWA_COLORKEY)

        # Show & update the window
        win32gui.ShowWindow(hWindow, win32con.SW_SHOWNORMAL)
        win32gui.UpdateWindow(hWindow)
        return hWindow

    def wndProc(self, hWnd, message, wParam, lParam):
        if message == win32con.WM_PAINT:
            rect = win32gui.GetClientRect(hWnd)
            hDC, paintStruct = win32gui.BeginPaint(hWnd)
            pen = win32gui.CreatePen(0,1,0x000000FF)
            win32gui.SelectObject(hDC, win32gui.GetStockObject(win32con.NULL_BRUSH))
            win32gui.SelectObject(hDC, pen)  
            win32gui.Rectangle(hDC, 0, 0, rect[2]-rect[0], rect[3]-rect[1])
            win32gui.EndPaint(hWnd, paintStruct)
            return 0
        else:
            return win32gui.DefWindowProc(hWnd, message, wParam, lParam)

class TextWindow:
    def __init__(self):
        #get instance handle

        # the class name
        className = 'Text'


        # create and initialize window class
        wndClass                = win32gui.WNDCLASS()
        wndClass.lpfnWndProc    = self.wndProc
        wndClass.hInstance      = hInstance
        wndClass.hbrBackground  = win32gui.GetStockObject(win32con.BLACK_BRUSH)
        wndClass.lpszClassName  = className

        # register window class
        self.wndClassAtom = None
        try:
            self.wndClassAtom = win32gui.RegisterClass(wndClass)
        except Exception as e:
            print(e)
            raise e

    def instanciate(self, text, region, owner=None):
        hWindow = win32gui.CreateWindowEx(
            win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST,
            self.wndClassAtom,                   #it seems message dispatching only works with the atom, not the class name
            text,
            win32con.WS_POPUP,
            *region, owner, 0, hInstance, None)
        win32gui.SetLayeredWindowAttributes(hWindow, 0x00000000, 0x00, win32con.LWA_COLORKEY)

        # Show & update the window
        win32gui.ShowWindow(hWindow, win32con.SW_SHOWNORMAL)
        win32gui.UpdateWindow(hWindow)
        return hWindow

    def wndProc(self, hWnd, message, wParam, lParam):
        if message == win32con.WM_PAINT:
            text = win32gui.GetWindowText(hWnd)
            hDC, paintStruct = win32gui.BeginPaint(hWnd)
            win32gui.SetBkMode(hDC, win32con.TRANSPARENT)
            win32gui.SetTextColor(hDC, 0x0000FF00)
            win32gui.ExtTextOut(hDC, 0, 0, 0, None, text)
            win32gui.EndPaint(hWnd, paintStruct)
            return 0
            
        else:
            return win32gui.DefWindowProc(hWnd, message, wParam, lParam)

class BackWindow:
    def __init__(self):
        #get instance handle

        # the class name
        className = 'Back'


        # create and initialize window class
        wndClass                = win32gui.WNDCLASS()
        wndClass.lpfnWndProc    = self.wndProc
        wndClass.hInstance      = hInstance
        wndClass.hbrBackground  = win32gui.GetStockObject(win32con.BLACK_BRUSH)
        wndClass.lpszClassName  = className

        # register window class
        self.wndClassAtom = None
        try:
            self.wndClassAtom = win32gui.RegisterClass(wndClass)
        except Exception as e:
            print(e)
            raise e

    def instanciate(self, region, owner=None):
        hWindow = win32gui.CreateWindowEx(
            win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST,
            self.wndClassAtom,                   #it seems message dispatching only works with the atom, not the class name
            '',
            win32con.WS_POPUP,
            *region, owner, 0, hInstance, None)
        win32gui.SetLayeredWindowAttributes(hWindow, 0x00FFFFFF, 0x00, win32con.LWA_COLORKEY)

        # Show & update the window
        win32gui.ShowWindow(hWindow, win32con.SW_SHOWNORMAL)
        win32gui.UpdateWindow(hWindow)
        return hWindow

    def wndProc(self, hWnd, message, wParam, lParam):
        return win32gui.DefWindowProc(hWnd, message, wParam, lParam)

class Display:
    def __init__(self, q:queue.Queue):
        self.empty = None
        self.rect = None
        self.text = None
        self.back = None
        self.root = None
        self.q = q
        self.hwnd = []
        for _ in range(12):
            self.hwnd.append([None]*4)

    def close(self, hwnd):
        win32gui.SendMessage(hwnd, win32con.WM_CLOSE, None, None)

    def request(self, func, tid, wid, oid, *args):
        self.q.put((func, tid, wid, oid)+args)

    def response(self):
        try:
            func, tid, oid, wid, *args = self.q.get_nowait()
            tid = tid - 1
            if func == "Close":
                self.close(self.root)
                return
            hwnd = self.hwnd[tid][wid]
            owner = None if oid < 0 else self.hwnd[tid][oid]
            if func == "Empty":
                self.hwnd[tid][wid] = self.empty.instanciate(*args, owner=owner)
            elif func == "Rect":
                self.hwnd[tid][wid] = self.rect.instanciate(*args, owner=owner)
            elif func == "Text":
                self.hwnd[tid][wid] = self.text.instanciate(*args, owner=owner)
            elif func == "Back":
                self.hwnd[tid][wid] = self.back.instanciate(*args, owner=owner)
            else: assert False
            if hwnd is not None: self.close(hwnd)
        except queue.Empty:
            return

    def mainloop(self):
        self.empty = EmptyWindow()
        self.rect = RectWindow()
        self.text = TextWindow()
        self.back = BackWindow()
        self.root = self.empty.instanciate()
        while 1:
            win32gui.PumpWaitingMessages()
            self.response()

if __name__ == '__main__':
    com = Display()
    thread = threading.Thread(target=com.mainloop, daemon=True)
    thread.start()
    empty = com.request("Empty")
    back = com.request("Back", 100, 100, 100, 100, owner=empty)
    text1 = com.request("Text", "first", 100, 100, 100, 100, owner=back)
    time.sleep(3)
    text2 = com.request("Text", "second", 100, 100, 100, 100, owner=back)
    win32gui.SendMessage(text1, win32con.WM_CLOSE, None, None)
    time.sleep(3)
    text3 = com.request("Text", "third", 100, 100, 100, 100, owner=back)
    win32gui.SendMessage(text2, win32con.WM_CLOSE, None, None)
    time.sleep(3)
    