import signal
import threading
import keyboard
import time
import sys
import ctypes
import pygetwindow as gw

user32 = ctypes.WinDLL('user32', use_last_error=True)

class m_MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]
    
class m_INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("mi", m_MOUSEINPUT)]

class Application:
    Playing = False
    
    def __init__(self):
        self.running = True
        self.prepare()

    def prepare(self):
        signal.signal(signal.SIGINT, self.exit_handler)

        keyboard.add_hotkey("F5", self.ChangeState)
        keyboard.add_hotkey("F4", lambda : self.exit_handler(None, None))

        self.threadChenKenh = threading.Thread(target=self.chenKenh)
        print('============================ CHEN KÊNH ============================')
        print('                             **--.--**')
        print('Phím tắt:')
        print('F4: Thoát chương trình')
        print('F5: Bật/tắt chen kênh')
        print('Chọn kênh cần vào rồi bấm F5 để chen, F5 lần nữa để tắt')
        print('                             **--.--**')
    def exit_handler(self, sig, frame):
        self.running = False
        sys.exit()

    def run(self):
        self.threadChenKenh.start()
        while self.running:
            time.sleep(0.05)
    
    def Click(self, x, y):
        ctypes.windll.user32.SetCursorPos(x, y)
        time.sleep(0.01)
        inp = m_INPUT()
        inp.type = 0
        inp.mi = m_MOUSEINPUT(x, y, 0, 0x0002, 0, None)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(inp), ctypes.sizeof(m_INPUT))
        time.sleep(0.01)
        inp.mi = m_MOUSEINPUT(x, y, 0, 0x0004, 0, None)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(inp), ctypes.sizeof(m_INPUT))

    def fixSize(self, w, h):
        x = 0
        y = 0
        if w >= 1920:
            x = (w - 1920) / 2
            w = 1920
        elif w >= 1440:
            x = (w - 1440) / 2
            w = 1440
        elif w >= 1280:
            x = (w - 1280) / 2
            w = 1280
        elif w >= 1024:
            x = (w - 1024) / 2
            w = 1024

        if h >= 1080:
            y = h - 1080
            h = 1080
        elif h >= 960:
            y = h - 960
            h = 960
        elif h >= 768:
            y = h - 768
            h = 768
        return [x, y, w, h]

    def findAudition(self):
        wlist = gw.getWindowsWithTitle("Audition")
        class_ = ctypes.create_unicode_buffer(256)
        for window in wlist:
            ctypes.windll.user32.GetClassNameW(window._hWnd, class_, 256)
            if class_.value == 'DLightClass':
                return window
        raise ValueError('Không tìm thấy cửa sổ game Audition!')

    def ChangeState(self):
        try:
            if not self.Playing:
                window = self.findAudition()
                x, y, w, h = self.fixSize(window.right - window.left, window.bottom - window.top)
                if window.isMinimized:
                    raise ValueError(f"Cửa sổ Audition đang bị thu nhỏ, không thể chen kênh!")
                ratio_w = w / 1024.0
                ratio_h = h / 768.0
                self.ClickPos = [
                    [window.left + x + 445.0 * ratio_w, window.top + y + 695.0 * ratio_h],
                    [window.left + x + 600.0 * ratio_w, window.top + y + 405.0 * ratio_h]]
                self.Playing = True
            else:
            
                self.Playing = False
            
        except Exception as e:
            print(e)
            pass

    def chenKenh(self):
        while(self.running):
            if(self.Playing):
                for pos in self.ClickPos:
                    self.Click(int(pos[0]), int(pos[1]))
            else:
                time.sleep(0.1)