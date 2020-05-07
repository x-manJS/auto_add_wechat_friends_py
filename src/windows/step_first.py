import tkinter as tk
import xlrd

class StepFirstFrame(tk.Frame):
    def __init__(self, parent, next_frame=None):
        super().__init__(parent)
        self.next_frame = next_frame  # 下一步
        self.set_ui()
        self.pack()

    def set_ui(self):

        tk.Button(self, text="下一步", command=self.to_next).pack()

    def to_next(self):
        self.quit()
        if self.next_frame is not None:
            self.next_frame.grid_propagate(False)


if __name__ == '__main__':
    StepFirstFrame(tk.Tk()).mainloop()
