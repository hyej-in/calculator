import numpy as np
from numpy import inf, nan, e, abs
# 在eval函数中使用到math所以勿删math
# from sympy import exp, symbols, integrate, oo, sin, cos, log, tan, pi, factorial, E, erfi
# from sympy import asin, acos, atan, sinh, cosh, tanh, summation, diff, limit, Integral, Abs, AccumBounds
import sympy
from sympy import *
# 对话框所需的库

# 创建画布需要的库
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# 创建工具栏需要的库
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
# 快捷键需要的库
from matplotlib.backend_bases import key_press_handler
# 导入画图常用的库
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class ZoomPan:
    """
    放大或缩小函数图像
    移动函数图像
    """

    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None

    def zoom_factory(self, string1, x, y, string, ax, base_scale=2.):
        def zoom(event):
            nonlocal x, y, string, string1
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata  # get event x location
            ydata = event.ydata  # get event y location

            if event.button == 'up':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'down':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1 - relx),
                         xdata + new_width * relx])
            ax.set_ylim([ydata - new_height * (1 - rely),
                         ydata + new_height * rely])

            if string != "":
                if string.find('log') != -1 or string.find('sqrt') != - \
                        1 or string.find('!') != -1:
                    x = np.linspace(0.0001, ax.get_xlim()[1], 100)
                elif string.find('asin') != -1 or string.find('acos') != -1 or string.find('atan') != -1:
                    x = np.linspace(-1, 1, 100)
                else:
                    x = np.linspace(ax.get_xlim()[0], ax.get_xlim()[1], 100)
                y = [eval(string) for i in x]
            else:
                x = []
                y = []
            # while len(ax.lines) != 0:
            #     ax.lines.pop(0)
            ax.lines = []
            handle = ax.plot(x, y)
            ax.grid(True)
            ax.legend(handles=handle, labels=string1)
            ax.figure.canvas.draw()

        fig = ax.get_figure()  # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_factory(self, string1, x, y, string, ax):
        def on_press(event):
            if event.inaxes != ax:
                return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press

        def on_release(event):
            nonlocal x, y, string, string1
            self.press = None
            if string != "":
                if string.find('log') != -1 or string.find('sqrt') != - \
                        1 or string.find('!') != -1:
                    x = np.linspace(0.0001, ax.get_xlim()[1], 100)
                elif string.find('asin') != -1 or string.find('acos') != -1 or string.find('atan') != -1:
                    x = np.linspace(-1, 1, 100)
                else:
                    x = np.linspace(ax.get_xlim()[0], ax.get_xlim()[1], 100)
                y = [eval(string) for i in x]
            else:
                x = []
                y = []
            ax.lines = []
            handle = ax.plot(x, y)
            ax.grid(True)
            ax.legend(handles=handle, labels=string1)
            ax.figure.canvas.draw()

        def on_motion(event):
            nonlocal x, y, string, string1
            if self.press is None:
                return
            if event.inaxes != ax:
                return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)
            if string != "":
                if string.find('log') != -1 or string.find('sqrt') != - \
                        1 or string.find('!') != -1:
                    x = np.linspace(0.0001, ax.get_xlim()[1], 100)
                elif string.find('asin') != -1 or string.find('acos') != -1 or string.find('atan') != -1:
                    x = np.linspace(-1, 1, 100)
                else:
                    x = np.linspace(ax.get_xlim()[0], ax.get_xlim()[1], 100)
                y = [eval(string) for i in x]
            else:
                x = []
                y = []
            ax.lines = []
            handle = ax.plot(x, y)
            ax.grid(True)
            ax.legend(handles=handle, labels=string1)
            ax.figure.canvas.draw()

        fig = ax.get_figure()  # get the figure of interest
        # attach the call back
        fig.canvas.mpl_connect('button_press_event', on_press)
        fig.canvas.mpl_connect('button_release_event', on_release)
        fig.canvas.mpl_connect('motion_notify_event', on_motion)
        return on_motion


def log10(num):
    return log(num) / log(10)


def sqrt(num):
    return num * 0.5


class plot2D:
    fig = figure(dpi=130)
    ax = fig.add_subplot(111)
    frame = 0
    x = 0
    y = 0
    i = 0

    def __init__(self, root):
        self.frame = root

    def switch(self):
        self.i += 1
        self.fig.tight_layout()
        self.fig.subplots_adjust(right=1, top=0.95, hspace=0.1, wspace=0.1)
        frame_plot = FigureCanvasTkAgg(self.fig, master=self.frame)
        if self.i == 1:
            toolbar = NavigationToolbar2Tk(frame_plot, self.frame)

            def on_key_press(event):
                key_press_handler(event, frame_plot, toolbar)

            frame_plot.mpl_connect("key_press_event", on_key_press)
        frame_plot.draw()
        # 显示画布
        frame_plot.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=0.95)

    def paint(self, string):
        self.fig.clf()
        self.ax = self.fig.add_subplot(111)
        list_expr = string.split(",")
        string1 = []
        for sub_expr in list_expr:
            string1.append(sub_expr)
        # print(string)
        if string != '':
            if string.find('log') != -1 or string.find('sqrt') != - \
                    1 or string.find('!') != -1:
                self.x = np.linspace(0.0001, self.ax.get_xlim()[1], 100)
            elif string.find('asin') != -1 or string.find('acos') != -1 or string.find('atan') != -1:
                self.x = np.linspace(-1, 1, 100)

            else:
                self.x = np.linspace(
                    self.ax.get_xlim()[0], self.ax.get_xlim()[1], 1000)
            try:
                string = self.string_process(string)
            except BaseException as e:
                return e
            try:
                self.y = [eval(string) for i in self.x]
            except BaseException as e:
                return e
        else:
            self.x = []
            self.y = []
        try:
            handle = self.ax.plot(self.x, self.y)
        except BaseException as e:
            return e
        self.ax.grid(True)
        self.ax.legend(labels=string1, handles=handle)
        self.ax.figure.canvas.draw()
        zp = ZoomPan()
        scale = 1.1
        figZoom = zp.zoom_factory(
            string1, self.x, self.y, string, self.ax, base_scale=scale)
        figPan = zp.pan_factory(string1, self.x, self.y, string, self.ax)
        return None

    def string_process(self, string):
        # string = string.replace("pi", "3.141592653589793")
        string = '0.0+' + string
        string = string.replace("^", "**")
        # string = string.replace('e', 'exp(1)')
        # string = string.replace('intexp(1)gratexp(1)', 'integrate')
        try:
            string = self.deep_process(string)
        except BaseException as e:
            raise e
        # string = string.replace('(factorial', '(float)(factorial')
        # string = string.replace('sin', 'np.sin')
        # string = string.replace('cos', 'np.cos')
        # string = string.replace('tan', 'np.tan')
        # string = string.replace('anp.sin', 'np.arcsin')
        # string = string.replace('anp.cos', 'np.arccos')
        # string = string.replace('anp.tan', 'np.arctan')
        # string = string.replace('log', 'np.log')
        string = string.replace('x', 'i')
        string = string.replace('eip', 'exp')
        print(string)
        return string

    # 对表达式里求和，求极限，积分，求导进行处理，输出算术式
    def deep_process(self, string):
        x = sympy.Symbol('x')
        # y = sympy.Symbol("y", integer=True)
        try:
            res = eval(string)
        except BaseException as e:
            raise e
        return str(res)

    def my_integrate(self, f, b, a):
        sum = 0
        n = 1000
        h = (b - a) / n
        for i in range(1, n + 1):
            xi, xj, xk = a + (i - 1) * h, a + (i - 0.5) * h, a + i * h
            sum = sum + f(xi) + 4 * f(xj) + f(xk)
        for i in range(1, n):
            xi = a + i * h
            sum = sum + 2 * f(xi)
            h, sum = (b - a) / n, 0
            for i in range(1, n + 1):
                xi = a + i * h
                sum = sum + f(xi) * h
        h = (b - a) / n
        for i in range(1, n + 1):
            xi, xj, xk = a + (i - 1) * h, a + (i - 0.5) * h, a + i * h
            sum = sum + f(xi) + 4 * f(xj) + f(xk)


class plot3D:
    fig = figure(dpi=130)
    ax = fig.add_subplot(111)
    frame = 0
    x = 0
    z = 0

    def __init__(self, root):
        self.frame = root

    def switch(self):
        self.fig.tight_layout()
        self.fig.subplots_adjust(right=1, top=0.95, hspace=0.1, wspace=0.1)
        frame_plot = FigureCanvasTkAgg(self.fig, master=self.frame)
        frame_plot.draw()
        # 显示画布
        frame_plot.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=0.95)
        # toolbar = NavigationToolbar2Tk(frame_plot,self.frame)
        # def on_key_press(event):
        #     key_press_handler(event, frame_plot, toolbar)
        #
        # frame_plot.mpl_connect("key_press_event", on_key_press)

    def paint(self, string):
        self.fig.clf()
        self.ax = self.fig.add_subplot(111, projection='3d')
        list_expr = string.split(",")
        string1 = []
        for sub_expr in list_expr:
            string1.append(sub_expr)

        if string != "":
            if string.find('log') != -1 or string.find('sqrt') != - \
                    1 or string.find('!') != -1:
                self.x = np.linspace(0.0001, 5, 50)
                self.y = np.linspace(0.0001, 5, 50)
            elif string.find('asin') != -1 or string.find('acos') != -1 or string.find('atan') != -1:
                self.x = np.linspace(-1, 1, 50)
                self.y = np.linspace(-1, 1, 50)
            else:
                self.x = np.linspace(-5, 5, 50)
                self.y = np.linspace(-5, 5, 50)

            try:
                string = self.string_process(string)
            except BaseException as e:
                return e
            self.x, self.y = np.meshgrid(self.x, self.y)
            try:
                self.z = eval(string)
            except BaseException as e:
                return e
        else:
            self.x = np.linspace(0, 0, 0)
            self.y = np.linspace(0, 0, 0)
            self.x, self.y = np.meshgrid(self.x, self.y)
            self.z = 0 * self.x + 0 * self.y

        self.ax.plot_surface(
            self.x,
            self.y,
            self.z,
            rstride=1,
            cstride=1,
            cmap='rainbow')
        self.ax.grid(True)
        self.ax.figure.canvas.draw()
        return None

    def string_process(self, string):
        # string = string.replace("pi", "3.141592653589793")
        string = string.replace('pi', 'np.pi')
        string += "+0*x+0*y"
        string = string.replace("^", "**")
        # string = string.replace('e', 'exp(1)')
        # string = string.replace('intexp(1)gratexp(1)', 'integrate')
        try:
            string = self.deep_process(string)
        except BaseException as e:
            raise e
        string += "+0*x+0*y"
        string = '0.0+' + string.replace('x', 'self.x')
        string = string.replace('y', 'self.y')
        string = string.replace('Abs', 'np.abs')
        string = string.replace('sin', 'np.sin')
        string = string.replace('cos', 'np.cos')
        string = string.replace('tan', 'np.tan')
        string = string.replace('anp.sin', 'np.arcsin')
        string = string.replace('anp.cos', 'np.arccos')
        string = string.replace('anp.tan', 'np.arctan')
        string = string.replace('log', 'np.log')
        string = string.replace("sexp(1)lf", "self")
        return string

    # 对表达式里求和，求极限，积分，求导进行处理，输出算术式
    def deep_process(self, string):
        x = sympy.Symbol('x')
        y = sympy.Symbol('y')
        res = eval(string)
        return str(res)
