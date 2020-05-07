from main import Main
from run import run
import tkinter as tk
from tkinter import filedialog, ttk
import xlrd
import xlwt
import sys
import os
import threading
from tkinter import StringVar, messagebox
from redirect import redirect

sys.path.append('../')



class StepThirdFrame(tk.Frame):
    def __init__(self, parent, next_frame=None):
        super().__init__(parent)

        columns = ("phone", "msg", "remark", 'status')
        self.tree = ttk.Treeview(self, columns=columns)  # 表格

        # 设置表格文字居中
        self.tree.column("phone", anchor="center", width=100)
        self.tree.column("msg", anchor="center")
        self.tree.column("remark", anchor="center")
        self.tree.column("status", anchor="center")

        # 设置表格头部标题
        self.tree.heading("phone", text="微信号/手机号")
        self.tree.heading("msg", text="验证信息")
        self.tree.heading("remark", text="备注")
        self.tree.heading("status", text="状态")

        self.list_box = tk.Listbox(self)
        self.next_frame = next_frame  # 下一步

        # 添加控件
        self.tree.pack()
        tk.Button(self, text="选择批量添加名单（excel文件）",
                  command=self.read_xls_file_thread).pack(side='left')
        tk.Button(self, text="开始执行添加",
                  command=self.to_run_thread).pack(side='left')
        tk.Button(self, text="导出excel",
                  command=self.export_excel_thread).pack(side='left')

        self.messages_label= tk.Label(self, text= "消息窗口")
        self.messages_label.pack()
        self.update_messages()

        self.pack()
        self.data = []
        self._worker = Main()

    def update_messages(self):
        self.messages_label['text']= redirect.content
        timer = threading.Timer(0.5, self.update_messages)
        timer.start()

    def read_xls_file_thread(self):
        th = threading.Thread(target=self.read_xls_file)
        th.setDaemon(True)
        th.start()

    def read_xls_file(self):
        filename = filedialog.askopenfilename()

        data = xlrd.open_workbook(filename)
        table = data.sheets()[0]
        nrows = table.nrows

        result = []
        for i in range(1, nrows):
            rows = table.row_values(i)
            item = {'phone': rows[0], 'msg': rows[1],
                    'remark': rows[2], 'status': rows[3]}
            result.append(item)
        self.fill_to_listbox(result)

    def fill_to_listbox(self, data):
        # 清空树里的数据
        self.del_items(self.tree)

        for index, item in enumerate(data):
            self.tree.insert("", index, text=index + 1, values=(
                item['phone'], item['msg'], item['remark'], item['status']))  # 插入数据，

        self.data = data

        self.tree.pack()

    def del_items(self, tree):
        x = tree.get_children()
        for item in x:
            tree.delete(item)

    def to_run_thread(self):
        thread = threading.Thread(target=self._worker.main, args=(
            self.data, self.add_friends_finished_callback,))
        thread.start()

    def add_friends_finished_callback(self, data):
        self.fill_to_listbox(data)

    def export_excel_thread(self):
        th = threading.Thread(target=self.export_excel)
        th.setDaemon(True)
        th.start()

    def export_excel(self):
        filename = filedialog.asksaveasfilename(
            filetypes=[('excel', '.xlsx')], defaultextension=".xlsx")

        f = xlwt.Workbook()  # 创建工作簿

        #  创建第一个sheet
        sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
        row0 = [u'微信号/手机号', u'验证信息', u'备注', u'状态']

        # 生成第一行
        for i in range(0, len(row0)):
            sheet1.write(0, i, row0[i])

        # 生成数据
        for rowIndex in range(0, len(self.data)):
            item = self.data[rowIndex]
            sheet1.write(rowIndex, 0, item['phone'])
            sheet1.write(rowIndex, 1, item['msg'])
            sheet1.write(rowIndex, 2, item['remark'])
            sheet1.write(rowIndex, 3, item['status'])

        f.save(filename)  # 保存文件
        messagebox.showinfo("保存成功", "已保存至：{}".format(filename))


if __name__ == '__main__':
    StepThirdFrame(tk.Tk()).mainloop()
