# @Author: Xiangxin Kong
# @Date: 2020.5.30
import tkinter as tk
from tkinter import *
from tkinter import Canvas
from downloader import *

class mainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        super().title('Manhuagui Downloader')
        super().geometry('400x160')
        baseY = 30
        tk.Label(self, text='Url:', font=('Arial', 16,)).place(x=10, y=baseY)
        tk.Label(self, text='To:', font=('Arial', 16,)).place(x=10, y=baseY + 40)
        self.var_address = tk.StringVar()
        self.var_url = tk.StringVar()
        self.var_address.set('manga/')
        self.var_url.set('https://www.manhuagui.com/comic/24973/')
        tk.Entry(self, textvariable=self.var_url, font=('Arial', 14), width=28).place(x=60, y=baseY)
        tk.Entry(self, textvariable=self.var_address, font=('Arial', 14), width=28).place(x=60, y=baseY + 40)
        tk.Button(self, text='Download', font=('Arial', 12), command=self.download).place(x=290, y=baseY + 80)
        self.mainloop()

    def download(self):
        try:
            s = MangaDownloader(self.var_url.get(), self.var_address.get())
        except:
            print("Manga not Found")
            self.var_url.set("")
            return
        downloadPanel(s)

class downloadPanel(Toplevel):
    def __init__(self, s):
        super().__init__()
        super().title('Manhuagui Downloader')

        super().geometry('1600x600')

        # 创建滚动条
        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # 创建Canvas，并关联滚动条
        self.canvas = Canvas(self, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side='left', fill='both', expand=True)

        self.scroll_frame = Frame(self.canvas)
        self.canvas.create_window(0, 0, window=self.scroll_frame, anchor='nw')
 
        # 设置滚动条的命令为移动Canvas
        self.scrollbar.config(command=self.canvas.yview)

        self.scroll_frame.bind('<Configure>', self.set_scroll_region)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.place_label(s)
        self.place_buttons(s)

        var = IntVar()

        def checkAll():
            for i in self.buttons:
                if var.get() == 1:
                    i.select()
                elif i.cget("state") == 'normal':
                    i.deselect()

        tk.Checkbutton(self.scroll_frame, text='Select All', font=('Arial', 18), variable=var, command=checkAll).grid(row=2, column=0, sticky=W)

        tk.Button(self.scroll_frame, text='Download', font=('Arial', 16), command=lambda: self.downloadChapters(s)).grid(row=2, column=1, sticky=W)

        self.mainloop()
        


    def place_buttons(self, s):
        self.buttons = []
        ROW_OFFSET = 3 # 偏移量
        for i in range(len(s.chapters)):
            s.chapters[i][2] = IntVar()
            cha = tk.Checkbutton(self.scroll_frame, text=s.chapters[i][0], font=('Arial', 14), variable=s.chapters[i][2])
            cha.grid(row=i // 5 + ROW_OFFSET, column=i % 5,sticky=W)
            if s.chapters[i][0] in s.existedChapters():
                cha.select()
                cha.config(state='disabled')
            self.buttons.append(cha)
        self.baseY += (s.length // 5) * 40    

    def set_scroll_region(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def place_label(self, s):
        tk.Label(self.scroll_frame, text=s.title, font=('Arial', 33,)).grid(row=0, column=0, sticky=W)
        tk.Label(self.scroll_frame, text="作者: " + s.author, font=('Arial', 12,)).grid(row=1, column=0, sticky=W)
        tk.Label(self.scroll_frame, text="年代: " + s.year, font=('Arial', 12,)).grid(row=1, column=1, sticky=W)
        tk.Label(self.scroll_frame, text="地区: " + s.region, font=('Arial', 12,)).grid(row=1, column=2, sticky=W)
        tk.Label(self.scroll_frame, text="类型: " + s.plot, font=('Arial', 12,)).grid(row=1, column=3, sticky=W)
        self.baseY = 120
        self.canvas.update_idletasks()

    def downloadChapters(self, s):
        for i in range(s.length):
            if self.buttons[i].cget("state") == 'normal' and s.chapters[i][2].get():
                s.downloadChapter(s.chapters[i][1])
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


if __name__ == '__main__':
    mainWindow()
