from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from controler import *
from time import time, localtime, strftime, sleep
from viewMatrix import *
from Latex import *


class MainWindow(Tk):
    WinWidth = 0
    WinHeight = 0
    W_H_ratio = 0
    frame_1 = None
    frame_2 = None
    menutop = None
    model = 2

    def __init__(self):
        super(MainWindow, self).__init__()
        self.WinWidth, self.WinHeight = self.maxsize()
        self.W_H_ratio = self.WinWidth / self.WinHeight
        self.title('多功能可视化函数计算器')
        self.geometry('%dx%d+%d+%d' % (self.WinWidth - 20, self.WinHeight - 104, -9, 0))
        self.state("zoomed")
        self.frame_2 = Frame_2(self)
        self.frame_1 = Frame_1(self)

        self.menutop = MenuTop(self)
        self.config(menu=self.menutop)
        # _thread.start_new_thread(self.frame_1.frame_ctrls.thread_showexpression, ("Thread-1", 2,))


class Frame_1(Frame):
    master = None
    frame_plot = None
    frame_ctrls = None
    plot2d = None
    plot3d = None

    def __init__(self, mainwin):
        super(Frame_1, self).__init__(mainwin)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.config(bg='pink')
        self.master = mainwin
        self.frame_plot = FramePlot(self)
        self.frame_ctrls = FrameCtrls(self)
        self.plot2d = plot2D(self.frame_plot)
        self.plot3d = plot3D(self.frame_plot)
        self.plot2d.switch()
        self.plot2d.paint('')


class FramePlot(Frame):
    master = None
    mainWin = None

    def __init__(self, master):
        super(FramePlot, self).__init__(master)
        self.master = master
        self.mainWin = master.master
        self.place(relx=0, rely=0, relwidth=0.718, relheight=1)


class FrameCtrls(Frame):
    master = None
    mainWin = None
    frame_expression = None
    entry_expression = None
    frame_buttons = None
    latex = None
    fx = None  # 显示f(x)或f(x,y)的frame

    def __init__(self, master):
        super(FrameCtrls, self).__init__(master)
        self.master = master
        self.mainWin = master.master
        self.place(relx=0.718, rely=0, relwidth=1 - 0.718, relheight=1)
        self.config(bg='lightblue')
        self.frame_expression = FrameExpression(self)
        self.inittext()
        self.entry_expression.bind('<KeyRelease>', self.on_entrychange)

        self.latex = stringLatex(self.frame_expression)
        self.frame_buttons = FrameButtons(self)

    def inittext(self):
        self.entry_expression = ttk.Entry(self, font=("Microsoft YaHei UI", 15))
        self.entry_expression.place(relx=0.1 * self.mainWin.W_H_ratio, rely=0.15,
                                    relwidth=1 - 0.1 * self.mainWin.W_H_ratio, relheight=0.05)
        self.fx = ttk.Label(self, text='f(x)=', font=("Microsoft YaHei UI", 15))
        self.fx.place(relx=0, rely=0.15, relwidth=0.1 * self.mainWin.W_H_ratio, relheight=0.05)

    def on_entrychange(self, event):
        self.latex.paint(self.entry_expression.get() + ' ')

    # def thread_showexpression(self, a, b):
    #     while True:
    #         if self.mainWin.model != 4:
    #             # print(self.entry_expression.get())
    #             self.latex.paint('x+1')
    #             sleep(1)


class FrameExpression(Frame):
    master = None
    mainWin = None

    def __init__(self, master):
        super(FrameExpression, self).__init__(master)
        self.master = master
        self.mainWin = master.master.master
        self.place(relx=0, rely=0, relwidth=1, relheight=0.15)
        self.config(bg='gold')


class FrameButtons(Frame):
    master = None
    mainWin = None
    upframe_d2 = None
    downframe_d2 = None
    upframe_d3 = None
    downframe_d3 = None

    def __init__(self, master):
        super(FrameButtons, self).__init__(master)
        self.master = master
        self.mainWin = master.master.master
        self.config(bg='orange')
        self.place(relx=0, rely=0.2, relwidth=1, relheight=1 - 0.2)
        self.initd2()
        self.initd3()
        self.unshowd3()
    #     为entry_expression 绑定回车响应：
        self.master.entry_expression.bind('<Return>', self.on_pressreturn)

    def initd2(self):
        self.initupframe_d2()
        self.initdownframe_d2()

    def showd2(self):
        self.upframe_d2.place(relx=0, rely=0, relwidth=1, relheight=0.518)
        self.downframe_d2.place(relx=0, rely=0.518, relwidth=1, relheight=1 - 0.518)

    def unshowd2(self):
        # self.upframe_d2.destroy()
        # self.upframe_d2 = None
        # self.downframe_d2.destroy()
        # self.downframe_d2 = None
        self.upframe_d2.place(relwidth=0, relheight=0)
        self.downframe_d2.place(relwidth=0, relheight=0)

    def initupframe_d2(self):
        self.upframe_d2 = SubFrame(self)
        self.upframe_d2.place(relx=0, rely=0, relwidth=1, relheight=0.518)
        btnlist1 = []
        for i in range(30):
            btnlist1.append(ButtonNums(self.upframe_d2, i))
        self.initbutons1_d2(btnlist1)

    def initbutons1_d2(self, btnlist1):
        for i in range(6):
            for j in range(5):
                btnlist1[j + 5 * i].grid(row=i, column=j, ipadx=25, ipady=5,
                                         padx=7, pady=7, sticky='nesw')
        for i in range(5):
            Grid.columnconfigure(self.upframe_d2, i, weight=1)
        for j in range(6):
            Grid.rowconfigure(self.upframe_d2, j, weight=1)
        for i in range(1):
            btnlist1[0].name = '('
            btnlist1[1].name = ')'
            btnlist1[2].name = '-oo'
            btnlist1[3].name = '+oo'
            btnlist1[4].name = 'Del'
            btnlist1[5].name = 'π'
            btnlist1[6].name = '7'
            btnlist1[7].name = '8'
            btnlist1[8].name = '9'
            btnlist1[9].name = '/'
            btnlist1[10].name = '^'
            btnlist1[11].name = '4'
            btnlist1[12].name = '5'
            btnlist1[13].name = '6'
            btnlist1[14].name = '*'
            btnlist1[15].name = '√'
            btnlist1[16].name = '1'
            btnlist1[17].name = '2'
            btnlist1[18].name = '3'
            btnlist1[19].name = '-'
            btnlist1[20].name = '-1'
            btnlist1[21].name = 'E'
            btnlist1[22].name = '0'
            btnlist1[23].name = '.'
            btnlist1[24].name = '+'
            btnlist1[25].name = '!'
            btnlist1[26].name = ','
            btnlist1[27].name = 'C'
            btnlist1[28].name = 'x'
            btnlist1[29].name = 'OK'
        for i in range(30):
            btnlist1[i].config(text=btnlist1[i].name)

    def initdownframe_d2(self):
        self.downframe_d2 = SubFrame(self)
        self.downframe_d2.place(relx=0, rely=0.518, relwidth=1, relheight=1 - 0.518)
        btnlist2 = []
        for i in range(16):
            btnlist2.append(ButtonFunc(self.downframe_d2, i))
        self.initbuttons2_d2(btnlist2)

    def initbuttons2_d2(self, btnlist2):
        for i in range(4):
            for j in range(4):
                btnlist2[j + 4 * i].grid(row=i, column=j, ipadx=25, ipady=5,
                                         padx=7, pady=7, sticky='nesw')
        for i in range(4):
            Grid.columnconfigure(self.downframe_d2, i, weight=1)
        for j in range(4):
            Grid.rowconfigure(self.downframe_d2, j, weight=1)
        for i in range(1):
            btnlist2[0].name = 'sin'
            btnlist2[1].name = 'cos'
            btnlist2[2].name = 'tan'
            btnlist2[3].name = 'log10'
            btnlist2[4].name = 'asin'
            btnlist2[5].name = 'acos'
            btnlist2[6].name = 'atan'
            btnlist2[7].name = 'log'
            btnlist2[8].name = 'sinh'
            btnlist2[9].name = 'cosh'
            btnlist2[10].name = 'tanh'
            btnlist2[11].name = '∑'
            btnlist2[12].name = 'lim'
            btnlist2[13].name = 'diff'
            btnlist2[14].name = '∫'
            btnlist2[15].name = '∫(a,b)'
            ToolTip(btnlist2[11], msg='summation(求和函数,(求和变量,上限,下限))', offset=250)
            ToolTip(btnlist2[12], msg='limit(求极限函数,取极限变量,在某点)', offset=210)
            ToolTip(btnlist2[13], msg='diff(求导函数,自变量)', offset=130)
            ToolTip(btnlist2[14], msg='integrate(求不定积分函数,自变量)', offset=200)
            ToolTip(btnlist2[15], msg='integrate(求定积分函数,(自变量,上限,下限))', offset=250)
        for i in range(16):
            btnlist2[i].config(text=btnlist2[i].name)

    def initd3(self):
        self.initupframe_d3()
        self.initdownframe_d3()

    def showd3(self):
        self.upframe_d3.place(relx=0, rely=0, relwidth=1, relheight=0.518)
        self.downframe_d3.place(relx=0, rely=0.518, relwidth=1, relheight=1 - 0.518)

    def unshowd3(self):
        # self.upframe_d3.destroy()
        # self.upframe_d3 = None
        # self.downframe_d3.destroy()
        # self.downframe_d3 = None
        self.upframe_d3.place(relwidth=0, relheight=0)
        self.downframe_d3.place(relwidth=0, relheight=0)

    def initupframe_d3(self):
        self.upframe_d3 = SubFrame(self)
        self.upframe_d3.place(relx=0, rely=0, relwidth=1, relheight=0.518)
        btnlist1 = []
        for i in range(30):
            btnlist1.append(ButtonNums(self.upframe_d3, i))
        self.initbutons1_d3(btnlist1)

    def initdownframe_d3(self):
        self.downframe_d3 = SubFrame(self)
        self.downframe_d3.place(relx=0, rely=0.518, relwidth=1, relheight=1 - 0.518)
        btnlist2 = []
        for i in range(16):
            btnlist2.append(ButtonFunc(self.downframe_d3, i))
        self.initbuttons2_d3(btnlist2)

    def initbutons1_d3(self, btnlist1):
        for i in range(6):
            for j in range(5):
                btnlist1[j + 5 * i].grid(row=i, column=j, ipadx=25, ipady=5,
                                         padx=7, pady=7, sticky='nesw')
        for i in range(5):
            Grid.columnconfigure(self.upframe_d3, i, weight=1)
        for j in range(6):
            Grid.rowconfigure(self.upframe_d3, j, weight=1)
        for i in range(1):
            btnlist1[0].name = '('
            btnlist1[1].name = ')'
            btnlist1[2].name = '-oo'
            btnlist1[3].name = '+oo'
            btnlist1[4].name = 'Del'
            btnlist1[5].name = 'π'
            btnlist1[6].name = '7'
            btnlist1[7].name = '8'
            btnlist1[8].name = '9'
            btnlist1[9].name = '/'
            btnlist1[10].name = '^'
            btnlist1[11].name = '4'
            btnlist1[12].name = '5'
            btnlist1[13].name = '6'
            btnlist1[14].name = '*'
            btnlist1[15].name = '√'
            btnlist1[16].name = '1'
            btnlist1[17].name = '2'
            btnlist1[18].name = '3'
            btnlist1[19].name = '-'
            btnlist1[20].name = '-1'
            btnlist1[21].name = 'e'
            btnlist1[22].name = '0'
            btnlist1[23].name = '.'
            btnlist1[24].name = '+'
            btnlist1[25].name = 'abs'
            btnlist1[26].name = 'x'
            btnlist1[27].name = 'C'
            btnlist1[28].name = 'y'
            btnlist1[29].name = 'OK'
        for i in range(30):
            btnlist1[i].config(text=btnlist1[i].name)

    def initbuttons2_d3(self, btnlist2):
        for i in range(4):
            for j in range(4):
                btnlist2[j + 4 * i].grid(row=i, column=j, ipadx=25, ipady=5,
                                         padx=7, pady=7, sticky='nesw')
        for i in range(4):
            Grid.columnconfigure(self.downframe_d3, i, weight=1)
        for j in range(4):
            Grid.rowconfigure(self.downframe_d3, j, weight=1)
        for i in range(1):
            btnlist2[0].name = 'sin'
            btnlist2[1].name = 'cos'
            btnlist2[2].name = 'tan'
            btnlist2[3].name = 'log10'
            btnlist2[4].name = 'asin'
            btnlist2[5].name = 'acos'
            btnlist2[6].name = 'atan'
            btnlist2[7].name = 'log'
            btnlist2[8].name = 'sinh'
            btnlist2[9].name = 'cosh'
            btnlist2[10].name = 'tanh'
            btnlist2[11].name = '∑'
            btnlist2[12].name = 'lim'
            btnlist2[13].name = 'diff'
            btnlist2[14].name = '∫'
            btnlist2[15].name = '∫(a,b)'
            ToolTip(btnlist2[11], msg='summation(求和函数,(求和变量,上限,下限))', offset=250)
            ToolTip(btnlist2[12], msg='limit(求极限函数,取极限变量,在某点)', offset=210)
            ToolTip(btnlist2[13], msg='diff(求导函数,自变量)', offset=130)
            ToolTip(btnlist2[14], msg='integrate(求不定积分函数,自变量)', offset=200)
            ToolTip(btnlist2[15], msg='integrate(求定积分函数,(自变量,上限,下限))', offset=250)
        for i in range(16):
            btnlist2[i].config(text=btnlist2[i].name)

    def on_pressreturn(self, event=None):
        errorlog = None
        if self.mainWin.model == 2:
            errorlog = self.mainWin.frame_1.plot2d.paint(
                self.mainWin.frame_1.frame_ctrls.entry_expression.get())
        elif self.mainWin.model == 3:
            errorlog = self.mainWin.frame_1.plot3d.paint(
                self.mainWin.frame_1.frame_ctrls.entry_expression.get())
        if errorlog is not None:
            messagebox.showerror(title='错误！', message=errorlog)
            print(errorlog)
            if self.mainWin.model == 2:
                self.mainWin.frame_1.plot2d.paint('')
            elif self.mainWin.model == 3:
                self.mainWin.frame_1.plot3d.paint('')
        else:
            self.mainWin.frame_1.frame_ctrls.latex.paint(self.mainWin.frame_1.frame_ctrls.entry_expression.get())


class SubFrame(Frame):
    master = None
    mainWin = None

    def __init__(self, master):
        super(SubFrame, self).__init__(master)
        self.master = master
        self.mainWin = master.mainWin


class ButtonNums(ttk.Button):
    master = None
    mainWin = None
    name = "0"
    entry_expression = None

    def __init__(self, master, name):
        super(ButtonNums, self).__init__(master, text=name, command=self.on_command, width=2)
        self.master = master
        self.mainWin = master.mainWin
        self.name = name
        self.entry_expression = self.master.master.master.entry_expression

    def on_command(self):
        if self.name == 'C':
            self.mainWin.frame_1.frame_ctrls.latex.paint('')
            self.entry_expression.delete(0, END)
            if self.mainWin.model == 2:
                self.mainWin.frame_1.plot2d.paint('')
            elif self.mainWin.model == 3:
                self.mainWin.frame_1.plot3d.paint('')
        elif self.name == 'OK':
            errorlog = None
            if self.mainWin.model == 2:
                errorlog = self.mainWin.frame_1.plot2d.paint(
                    self.mainWin.frame_1.frame_ctrls.entry_expression.get())
            elif self.mainWin.model == 3:
                errorlog = self.mainWin.frame_1.plot3d.paint(
                    self.mainWin.frame_1.frame_ctrls.entry_expression.get())

            if errorlog is not None:
                messagebox.showerror(title='错误！', message=errorlog)
                print(errorlog)
                if self.mainWin.model == 2:
                    self.mainWin.frame_1.plot2d.paint('')
                elif self.mainWin.model == 3:
                    self.mainWin.frame_1.plot3d.paint('')
            else:
                self.mainWin.frame_1.frame_ctrls.latex.paint(self.mainWin.frame_1.frame_ctrls.entry_expression.get())
        elif self.name == 'Del':
            self.entry_expression.delete(self.entry_expression.index("insert") - 1)
        elif self.name == '√':
            self.entry_expression.insert('insert', 'sqrt()')
            self.entry_expression.icursor(self.entry_expression.index("insert") - 1)
        elif self.name == 'abs':
            self.entry_expression.insert('insert', 'abs()')
            self.entry_expression.icursor(self.entry_expression.index("insert") - 1)
        elif self.name == '!':
            self.entry_expression.insert('insert', 'factorial()')
            self.entry_expression.icursor(self.entry_expression.index("insert") - 1)
        elif self.name == '-1':
            self.entry_expression.insert('insert', '^-1')
        elif self.name == 'π':
            self.entry_expression.insert('insert', 'pi')
        else:
            self.entry_expression.insert('insert', self.name)
        self.mainWin.frame_1.frame_ctrls.latex.paint(self.mainWin.frame_1.frame_ctrls.entry_expression.get())


class ButtonFunc(ttk.Button):
    master = None
    mainWin = None
    name = "0"
    entry_expression = None

    def __init__(self, master, name):
        super(ButtonFunc, self).__init__(master, text=name, command=self.on_command, width=2)
        self.master = master
        self.mainWin = master.mainWin
        self.name = name
        self.entry_expression = self.master.master.master.entry_expression

    def on_command(self):
        if self.name == '∑':
            self.entry_expression.insert('insert', 'summation(,(x,,))')
            self.entry_expression.icursor(self.entry_expression.index("insert") - 7)
        elif self.name == 'lim':
            self.entry_expression.insert('insert', 'limit(,x,)')
            self.entry_expression.icursor(self.entry_expression.index("insert") - 4)
        elif self.name == 'diff':
            if self.mainWin.model == 2:
                self.entry_expression.insert('insert', 'diff(,x)')
                self.entry_expression.icursor(self.entry_expression.index("insert") - 3)
            elif self.mainWin.model == 3:
                self.entry_expression.insert('insert', 'diff(,)')
                self.entry_expression.icursor(self.entry_expression.index("insert") - 2)
        elif self.name == '∫':
            if self.mainWin.model == 2:
                self.entry_expression.insert('insert', 'integrate(,x)')
                self.entry_expression.icursor(self.entry_expression.index("insert") - 3)
            elif self.mainWin.model == 3:
                self.entry_expression.insert('insert', 'integrate(,x,y)')
                self.entry_expression.icursor(self.entry_expression.index("insert") - 5)
        elif self.name == '∫(a,b)':
            if self.mainWin.model == 2:
                self.entry_expression.insert('insert', 'integrate(,(x,,))')
                self.entry_expression.icursor(self.entry_expression.index("insert") - 7)
            elif self.mainWin.model == 3:
                self.entry_expression.insert('insert', 'integrate(,(x,,),(y,,))')
                self.entry_expression.icursor(self.entry_expression.index("insert") - 13)
        else:
            self.entry_expression.insert('insert', self.name + '()')
            self.entry_expression.icursor(self.entry_expression.index("insert") - 1)
        self.mainWin.frame_1.frame_ctrls.latex.paint(self.mainWin.frame_1.frame_ctrls.entry_expression.get())


class MenuTop(Menu):
    master = None
    mainWin = None
    menu1 = None

    def __init__(self, master):
        super(MenuTop, self).__init__(master, tearoff=False, font=("黑体", 15, "bold"))
        self.master = master
        self.mainWin = master
        self.add_command(label='二维绘图', command=self.drawd2)
        self.add_command(label='三维绘图', command=self.drawd3)
        self.add_command(label='解方程组', command=self.matrixcal)

    def drawd2(self):
        if self.mainWin.model == 3:
            self.mainWin.model = 2
            self.mainWin.frame_1.frame_ctrls.latex.paint('')
            self.mainWin.frame_1.place(relwidth=1, relheight=1)
            self.mainWin.frame_1.frame_ctrls.entry_expression.delete(0, END)
            self.mainWin.frame_1.frame_ctrls.frame_buttons.unshowd3()
            self.mainWin.frame_1.frame_ctrls.fx.config(text='f(x)=')
            self.mainWin.frame_1.frame_ctrls.frame_buttons.showd2()
            self.mainWin.frame_1.plot2d.switch()
            self.mainWin.frame_1.plot2d.paint('')
        elif self.mainWin.model == 4:
            self.mainWin.model = 2
            self.mainWin.frame_1.frame_ctrls.latex.paint('')
            self.mainWin.frame_1.plot2d.switch()
            self.mainWin.frame_1.plot2d.paint('')
            self.mainWin.frame_1.frame_ctrls.frame_buttons.unshowd3()
            self.mainWin.frame_1.frame_ctrls.fx.config(text='f(x)=')
            self.mainWin.frame_1.frame_ctrls.frame_buttons.showd2()
            self.mainWin.frame_1.frame_ctrls.entry_expression.delete(0, END)
            self.mainWin.frame_1.place(relwidth=1, relheight=1)
            self.mainWin.frame_2.place(relwidth=0, relheight=0)

    def drawd3(self):
        if self.mainWin.model == 2:
            self.mainWin.model = 3
            self.mainWin.frame_1.frame_ctrls.latex.paint('')
            self.mainWin.frame_1.place(relwidth=1, relheight=1)
            self.mainWin.frame_1.frame_ctrls.entry_expression.delete(0, END)
            self.mainWin.frame_1.frame_ctrls.frame_buttons.unshowd2()
            self.mainWin.frame_1.frame_ctrls.fx.config(text='f(x,y)=')
            self.mainWin.frame_1.frame_ctrls.frame_buttons.showd3()
            self.mainWin.frame_1.plot3d.switch()
            self.mainWin.frame_1.plot3d.paint('')
        elif self.mainWin.model == 4:
            self.mainWin.model = 3
            self.mainWin.frame_1.frame_ctrls.latex.paint('')
            self.mainWin.frame_1.plot3d.switch()
            self.mainWin.frame_1.plot3d.paint('')
            self.mainWin.frame_1.frame_ctrls.frame_buttons.unshowd2()
            self.mainWin.frame_1.frame_ctrls.fx.config(text='f(x,y)=')
            self.mainWin.frame_1.frame_ctrls.frame_buttons.showd3()
            self.mainWin.frame_1.frame_ctrls.entry_expression.delete(0, END)
            self.mainWin.frame_1.place(relwidth=1, relheight=1)
            self.mainWin.frame_2.place(relwidth=0, relheight=0)

    def matrixcal(self):
        if self.mainWin.model != 4:
            self.mainWin.model = 4
            self.mainWin.frame_1.place(relwidth=0, relheight=0)
            self.mainWin.frame_2.place(relwidth=1, relheight=1)
            self.mainWin.frame_2.latexmatrix.switch()


class ToolTip(Toplevel):
    """
    Provides a ToolTip widget for Tkinter.
    To apply a ToolTip to any Tkinter widget, simply pass the widget to the
    ToolTip constructor
    """
    offset = 0

    def __init__(self, wdgt, msg=None, msgFunc=None, delay=0, follow=True, offset=100):
        """
        Initialize the ToolTip

        Arguments:
          wdgt: The widget this ToolTip is assigned to
          msg:  A static string message assigned to the ToolTip
          msgFunc: A function that retrieves a string to use as the ToolTip text
          delay:   The delay in seconds before the ToolTip appears(may be float)
          follow:  If True, the ToolTip follows motion, otherwise hides
        """

        self.wdgt = wdgt
        self.parent = self.wdgt.master  # The parent of the ToolTip is the parent of the ToolTips widget
        Toplevel.__init__(self, self.parent, bg='black', padx=1, pady=1)  # Initalise the Toplevel
        self.withdraw()  # Hide initially
        self.overrideredirect(True)  # The ToolTip Toplevel should have no frame or title bar
        self.offset = offset
        self.msgVar = StringVar()  # The msgVar will contain the text displayed by the ToolTip
        if msg == None:
            self.msgVar.set('No message provided')
        else:
            self.msgVar.set(msg)
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        Message(self, textvariable=self.msgVar, bg='#FFFFDD',
                aspect=1000).grid()  # The test of the ToolTip is displayed in a Message widget
        self.wdgt.bind('<Enter>', self.spawn,
                       '+')  # Add bindings to the widget.  This will NOT override bindings that the widget already has
        self.wdgt.bind('<Leave>', self.hide, '+')
        self.wdgt.bind('<Motion>', self.move, '+')

    def spawn(self, event=None):
        """
        Spawn the ToolTip.  This simply makes the ToolTip eligible for display.
        Usually this is caused by entering the widget

        Arguments:
          event: The event that called this funciton
        """
        self.visible = 1
        self.after(int(self.delay * 1000), self.show)  # The after function takes a time argument in miliseconds

    def show(self):
        """
        Displays the ToolTip if the time delay has been long enough
        """
        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()

    def move(self, event):
        """
        Processes motion within the widget.

        Arguments:
          event: The event that called this function
        """
        self.lastMotion = time()
        if self.follow == False:  # If the follow flag is not set, motion within the widget will make the ToolTip dissapear
            self.withdraw()
            self.visible = 1
        self.geometry('+%i+%i' % (
            event.x_root - self.offset, event.y_root - 30))  # Offset the ToolTip 10x10 pixes southwest of the pointer
        try:
            self.msgVar.set(
                self.msgFunc())  # Try to call the message function.  Will not change the message if the message function is None or the message function fails
        except:
            pass
        self.after(int(self.delay * 1000), self.show)

    def hide(self, event=None):
        """
        Hides the ToolTip.  Usually this is caused by leaving the widget

        Arguments:
          event: The event that called this function
        """
        self.visible = 0
        self.withdraw()
