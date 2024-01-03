import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import figure


class LatexMatrix:
    def __init__(self, root):
        self.num = 0
        self.A = 0
        self.b = 0
        self.index = 0
        self.fig = figure(dpi=130)
        self.ax = self.fig.add_subplot(111)
        self.root = root
        self.ax.axis('off')
        self.frame_plot = FigureCanvasTkAgg(self.fig, master=self.root)
        self.frame_plot.draw()
        self.frame_plot.get_tk_widget().pack()

    def switch(self):
        self.fig.clf()
        self.fig.tight_layout()
        self.fig.subplots_adjust(right=1, top=0.95, hspace=0, wspace=0)
        self.frame_plot = FigureCanvasTkAgg(self.fig, master=self.root)
        self.frame_plot.draw()
        self.frame_plot.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)

    def paint(self, num=0, list=[]):
        """接收参数或绘制图像"""
        self.fig.clf()
        self.ax = self.fig.add_subplot(111)
        self.ax.axis("off")
        self.ax.texts.clear()
        if num != 0:
            self.num = num
            self.A = np.zeros((self.num, self.num))
            self.b = np.zeros((self.num, 1))
            self.index = 0
            for i in range(self.num):
                string = "$"
                for j in range(self.num):
                    string += "\\quad x_{" + str(j) + "}+"
                string = string[:-1] + "=  $"
                self.ax.text(0.2, 1 - (1 + i) / self.num + 1 / 2 / self.num, string, horizontalalignment='center',
                             fontsize=10)
            self.frame_plot.draw()
        else:
            for i in range(self.num):
                self.A[self.index][i] = list[i]
                print(self.A)
            self.b[self.index][0] = list[self.num]
            for i in range(self.num):
                string = "$"
                for j in range(self.num):
                    if i > self.index:
                        string += "\\quad x_{" + str(j) + "}+"
                    else:
                        string += str(self.A[i][j]) + "x_{" + str(j) + "}+"
                if i > self.index:
                    string = string[:-1] + "=\\quad $"
                else:
                    string = string[:-1] + "=" + str(self.b[i][0]) + "$"
                self.ax.text(0.2, 1 - (1 + i) / self.num + 1 / 2 / self.num, string, horizontalalignment='center',
                             fontsize=10)
            self.frame_plot.draw()
            self.index += 1
        if self.index == self.num and self.num > 0:
            # self.X = np.linalg.solve(self.A, self.b)
            try:
                self.X = np.linalg.solve(self.A, self.b)
            except np.linalg.LinAlgError:
                self.index = 0
                raise Exception("没有唯一解！")
            for i in range(self.num):
                string = "$x_{" + str(i) + "}=" + str(self.X[i][0]) + "$"
                self.ax.text(
                    0.8,
                    1 - (1 + i) / self.num + 1 / 2 / self.num,
                    string,
                    horizontalalignment='center',
                    fontsize=10)
                self.frame_plot.draw()
            self.index = 0
