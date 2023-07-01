# @Author: Xiangxin Kong
# @Date: 2020.5.30
from downloader import *
import tkinter as tk
from tkinter import *


class mainWindow(tk.Tk):
    def __init__(self):
        # initialize the widow
        super().__init__()
        super().title('Manhuagui Downloader')
        super().geometry('400x160')
        baseY = 30
        # initialize the labels
        tk.Label(self, text='Url:', font=('Arial', 16,)).place(x=10, y=baseY)
        tk.Label(self, text='To:', font=('Arial', 16,)).place(x=10, y=baseY + 40)
        # initialize the labels
        self.var_address = tk.StringVar()
        self.var_url = tk.StringVar()
        self.var_address.set('manga/')
        self.var_url.set('https://www.manhuagui.com/comic/24973/')
        tk.Entry(self, textvariable=self.var_url, font=('Arial', 14), width=28).place(x=60, y=baseY)  # url field
        tk.Entry(self, textvariable=self.var_address, font=('Arial', 14), width=28).place(x=60,
                                                                                          y=baseY + 40)  # address field
        # initialize the button
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
    # begin to download
    def __init__(self, s):
        super().__init__()
        super().title('Manhuagui Downloader')
        super().geometry('900x160')
        super().geometry('900x' + str(40 * (s.length // 6) + 260))
        # initialize labels
        self.place_label(s)
        # iniitialie select buttons
        self.place_buttons(s)
        # initialize check all functions
        var = IntVar()

        def checkAll():
            for i in self.buttons:
                if var.get() == 1:
                    i.select()
                elif i.cget("state") == 'normal':
                    i.deselect()

        # check all button
        tk.Checkbutton(self, text='Select All', font=('Arial', 18), variable=var,
                       command=checkAll).place(x=0, y=self.baseY + 80)
        # dowmload buttons
        tk.Button(self, text='Download', font=('Arial', 16),
                  command=lambda: self.downloadChapters(s)).place(x=450, y=self.baseY + 80)
        self.mainloop()

    def place_label(self, s):
        tk.Label(self, text=s.title, font=('Arial', 33,)).place(x=10, y=10)
        tk.Label(self, text="作者: " + s.author, font=('Arial', 12,)).place(x=10, y=70)
        tk.Label(self, text="年代: " + s.year, font=('Arial', 12,)).place(x=160, y=70)
        tk.Label(self, text="地区: " + s.region, font=('Arial', 12,)).place(x=280, y=70)
        tk.Label(self, text="类型: " + s.plot, font=('Arial', 12,)).place(x=400, y=70)
        self.baseY = 120

    def place_buttons(self, s):
        self.buttons = []
        for i in range(len(s.chapters)):
            s.chapters[i][2] = IntVar()
            cha = tk.Checkbutton(self, text=s.chapters[i][0], font=('Arial', 14), variable=s.chapters[i][2])
            cha.place(x=(i % 6) * 150, y=self.baseY + (i // 6) * 40)
            if s.chapters[i][0] in s.existedChapters():
                cha.select()
                cha.config(state='disabled')
            self.buttons.append(cha)
        self.baseY += (s.length // 6) * 40

    def downloadChapters(self, s):
        for i in range(s.length):
            if self.buttons[i].cget("state") == 'normal' and s.chapters[i][2].get():
                s.downloadChapter(s.chapters[i][1])


if __name__ == '__main__':
    mainWindow()
