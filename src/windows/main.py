from adb import Adb
import tkinter as tk
import sys
import threading
import os
from tkinter import filedialog, messagebox
from shutil import copyfile

sys.path.append('../')


class MainWindow(tk.Frame):
    def __init__(self, parent, next_frame=None):
        super().__init__(parent)
        self.next_frame = next_frame  # 下一步
        self.set_ui()
        self.pack()
        self._adb = Adb()

        self.base_path = getattr(sys, 'frozen', False) and sys._MEIPASS or os.path.dirname(os.path.dirname(
            os.path.dirname(__file__)))

    def set_ui(self):
        tk.Label(self, text="""
        在批量导入用户之前，你需要准备以下内容：\n
        1.用数据线把手机连接好电脑，并在手机上打开调试功能，以华为手机为例：设置-系统-开发人员选项-USB调试 \n
        2.安装ADBKeyboard输入法，下方的按钮可以帮你安装这个输入法。\n
        3.导出excel模板，按格式填写你需要添加的微信好友信息。
        4.点击导入名单按钮，选择你填好的名单excel
        5.打开微信-切换到通讯录界面
        6.点击导入按钮，程序开始为你批量添加好友，添加完成后，可以导出excel查看导出情况。

        ps: 如果安装ADBKeyboard输入法后，手机没切换成ADBKeyboard输入法，请手动切换。
        """, justify="left",).pack()

        tk.Button(self, text="验证手机是否授权",
                  command=self.check_is_authorize).pack(side='left')
        tk.Button(self, text="安装ADBKeyboard输入法",
                  command=self.install_input_method).pack(side='left')
        tk.Button(self, text="卸载ADBKeyboard输入法",
                  command=self.uninstall_input_method).pack(side='left')
        tk.Button(self, text="切换到ADBKeyboard输入法",
                  command=self.change_to_adb_input_method).pack(side='left')

        tk.Button(self, text="下载模板", command=self.download_excel_template_thread).pack(
            side='left')

    def check_is_authorize(self):
        self._adb.check_devices()

    def install_input_method(self):
        th= threading.Thread(target= self._adb.install_input_method)
        th.setDaemon(True)
        th.start();

    def uninstall_input_method(self):
        th= threading.Thread(target= self._adb.uninstall_input_method)
        th.setDaemon(True)
        th.start();

    def change_to_adb_input_method(self):
        th= threading.Thread(target= self._adb.change_to_adb_input_method)
        th.setDaemon(True)
        th.start();

    def download_excel_template_thread(self):
        download_thread = threading.Thread(target=self.download_excel_template)
        download_thread.setDaemon(True)
        download_thread.start()

    def download_excel_template(self):
        file_name = filedialog.asksaveasfilename(title= "选择下载模板保存地址", 
            filetypes= [('模板','.xlsx')], defaultextension=".xlsx")
        if file_name:
            copyfile("{}/data/name.xlsx".format(self.base_path), file_name)
            messagebox.showinfo("提示", "下载成功")


if __name__ == '__main__':
    StepSecondFrame(tk.Tk()).mainloop()
