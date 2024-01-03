from tkinter import *
from tkinter import ttk
from LatexMatrix import *
from math import *


class Frame_2(Frame):
    master = None
    frame_matrix = None
    frame_ctrls_m = None
    latexmatrix = None

    def __init__(self, mainwin):
        super(Frame_2, self).__init__(mainwin)
        self.master = mainwin
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.master = mainwin
        self.frame_matrix = FrameMatrix(self)
        self.frame_ctrls_m = FrameCtrlsM(self)
        self.latexmatrix = LatexMatrix(self.frame_matrix)
        self.latexmatrix.switch()
        # self.latexmatrix.paint(num=0)


class FrameMatrix(Frame):
    master = None
    mainWin = None

    def __init__(self, master):
        super(FrameMatrix, self).__init__(master)
        self.master = master
        self.mainWin = master.master
        self.config(bg='lightblue')
        self.place(relx=0, rely=0, relwidth=1, relheight=0.45)


class FrameCtrlsM(Frame):
    master = None
    mainWin = None
    entry_matrix = None
    entry_num = None
    num = 0
    frame_buttons = None
    fm = None  # 显示在此输入矩阵的frame
    btnOK = None

    def __init__(self, master):
        super(FrameCtrlsM, self).__init__(master)
        self.master = master
        self.mainWin = master.master
        self.place(rely=0.45, relwidth=1, relheight=1 - 0.45)
        # self.config(bg='pink')
        self.fm = ttk.Label(self, text='在此输入列表:')
        self.fm.place(relwidth=0.06, relheight=0.08)
        self.entry_matrix = ttk.Entry(self)
        self.entry_matrix.place(relx=0.06, relwidth=0.7, relheight=0.08)
        self.entry_matrix.bind('<Return>', self.on_commandOK)
        ttk.Label(self, text=' 未知数个数：').place(relx=0.76, relwidth=0.06, relheight=0.08)
        self.entry_num = ttk.Entry(self)
        self.entry_num.place(relx=0.82, relwidth=0.05, relheight=0.08)
        self.entry_num.bind('<Return>', self.on_commandOK)
        self.btnC = ttk.Button(self, text='C', command=self.on_commandC)
        self.btnC.place(relx=0.87, relwidth=0.06, relheight=0.08)
        self.btnOK = ttk.Button(self, text='OK', command=self.on_commandOK)
        self.btnOK.place(relx=0.93, relwidth=0.07, relheight=0.08)
        self.frame_buttons = FrameButtons(self)

    def on_commandOK(self, event=None):
        from tkinter import messagebox
        if len(self.entry_num.get()) != 0:
            try:
                num = int(self.entry_num.get())
                if num != 0:
                    # matlist = self.entry2list(self.entry_matrix.get())
                    print(num)
                    self.num = num
                    self.master.latexmatrix.paint(num=num)
                else:
                    messagebox.showerror(title='错误！', message='未知数个数应大于0！')
                self.entry_num.delete(0, END)
            except BaseException as e:
                messagebox.showerror(title='错误！', message='请输入正确的未知数个数！')
                self.entry_num.delete(0, END)
            self.entry_matrix.delete(0, END)
        else:
            if self.num != 0:
                try:
                    matlist = self.entry2list(self.entry_matrix.get())
                    if len(matlist) == self.num + 1:
                        self.master.latexmatrix.paint(list=matlist)
                    else:
                        messagebox.showerror(title='错误！', message='列表与未知数个数不对应！')
                except BaseException as e:
                    if str(e) == "没有唯一解！":
                        messagebox.showerror(title='错误！', message=e)
                    else:
                        messagebox.showerror(title='错误！', message='参数和解列表错误！')
            self.entry_matrix.delete(0, END)

    def on_commandC(self):
        self.entry_matrix.delete(0, END)
        self.entry_num.delete(0, END)
        self.num = 0
        self.master.latexmatrix.switch()

    def entry2list(self, string):
        string = string.replace('^', '**')
        strlist = string.split(',')
        matlist = []
        for i in range(len(strlist)):
            matlist.append(eval(strlist[i]))
        print(matlist)
        return matlist


class FrameButtons(Frame):
    master = None
    mainWin = None

    def __init__(self, master):
        super(FrameButtons, self).__init__(master)
        self.master = master
        self.mainWin = master.master.master
        self.place(relx=0.2, rely=0.08, relwidth=1 - 0.2 * 2, relheight=0.92)
        btnlist1 = []
        for i in range(25):
            btnlist1.append(ButtonMatrix(self, i))
        for i in range(5):
            for j in range(5):
                btnlist1[j + 5 * i].grid(row=i, column=j, ipadx=25, ipady=5,
                                         padx=7, pady=7, sticky='nesw')
        for i in range(5):
            Grid.columnconfigure(self, i, weight=1)
        for j in range(5):
            Grid.rowconfigure(self, j, weight=1)
        for i in range(1):
            btnlist1[0].name = '^'
            btnlist1[1].name = 'sin'
            btnlist1[2].name = 'cos'
            btnlist1[3].name = 'tan'
            btnlist1[4].name = 'Del'
            btnlist1[5].name = 'pi'
            btnlist1[6].name = '7'
            btnlist1[7].name = '8'
            btnlist1[8].name = '9'
            btnlist1[9].name = '/'
            btnlist1[10].name = 'e'
            btnlist1[11].name = '4'
            btnlist1[12].name = '5'
            btnlist1[13].name = '6'
            btnlist1[14].name = '*'
            btnlist1[15].name = 'log'
            btnlist1[16].name = '1'
            btnlist1[17].name = '2'
            btnlist1[18].name = '3'
            btnlist1[19].name = '-'
            btnlist1[20].name = 'log10'
            btnlist1[21].name = ','
            btnlist1[22].name = '0'
            btnlist1[23].name = '.'
            btnlist1[24].name = '+'

        for i in range(25):
            btnlist1[i].config(text=btnlist1[i].name)


class ButtonMatrix(ttk.Button):
    master = None
    mainWin = None
    name = '0'
    entry_matrix = None
    entry_num = None

    def __init__(self, master, name):
        super(ButtonMatrix, self).__init__(master, text=name, command=self.on_command, width=2)
        self.master = master
        self.mainWin = master.mainWin
        self.name = name
        self.entry_matrix = master.master.entry_matrix
        self.entry_num = master.master.entry_num

    def on_command(self):
        if self.name == 'Del':
            self.entry_matrix.delete(self.entry_matrix.index("insert") - 1)
        elif len(self.name) > 2:
            self.entry_matrix.insert('insert', self.name + '()')
            self.entry_matrix.icursor(self.entry_matrix.index("insert") - 1)
        else:
            self.entry_matrix.insert('insert', self.name)
