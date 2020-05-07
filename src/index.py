import tkinter as tk
from windows.main import MainWindow
from windows.step_thirth import StepThirdFrame
from redirect import redirect
import sys

sys.stdout = redirect #把print内容重定向到redirec中

def center_window(window, w, h):
    # 获取屏幕 宽、高
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()

    # 计算 x, y 位置
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    window.geometry('%dx%d+%d+%d' % (w, h, x, y))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("批量添加好友")
    root.configure()
    center_window(root, 1000, 700)

    MainWindow(root).place(x=10, y=10, anchor='nw')
    StepThirdFrame(root).place(x=10, y=350, anchor='nw')

    root.mainloop()
