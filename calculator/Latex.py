import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.pyplot import figure


class stringLatex:
    root = 0
    string = " "
    fig = figure(dpi=130)
    ax = fig.add_subplot(111)
    txt = 0
    frame_plot = 0

    def __init__(self, root):
        self.root = root
        self.ax.text(0.5, 0.5, self.string,
                     horizontalalignment='center', fontsize=10)
        self.ax.axis('off')
        self.frame_plot = FigureCanvasTkAgg(self.fig, master=self.root)
        self.frame_plot.draw()
        self.frame_plot.get_tk_widget().pack()

    def find_para(self, string, index):
        """找到反括号"""
        stack = 1
        res = index
        while stack:
            res += 1
            if string[res] == "(":
                stack += 1
            elif string[res] == ")":
                stack -= 1
            if stack == 0:
                return res

    def find_pre_para(self, string, index):
        """找到正括号"""
        stack = 1
        res = index
        while stack:
            res -= 1
            if string[res] == "(":
                stack -= 1
            elif string[res] == ")":
                stack += 1
            if stack == 0:
                return res

    def change_trangle_symbol(self, string):
        res = string
        while res.find(" (") != -1:
            find = res.find(" (")
            start_para = find + 1
            end_para = self.find_para(res, start_para)
            res = res[:start_para] + \
                  "{(" + res[start_para + 1:end_para] + ")}" + res[end_para + 1:]
        return res

    def change_divide_symbol(self, string):
        strings = string.split("/")
        if len(strings) <= 1:
            return string
        res = ""
        res += "\\frac {" + strings[0] + "}{" + strings[1] + "}"
        return res

    def find_fundamental_symbols(self, string, start):
        while True:
            if start == 0:
                return 0
            if string[start] in ['+', '-', '*', '/']:
                return start + 1, string[start]
            start -= 1

    def my_find_division(self, string, index=0):
        i = index
        while i < len(string):
            if string[i] == "(":
                i = self.find_para(string, i)
            elif string[i] == "/":
                return i
            i += 1
        return -1

    def change_fundamental_symbol(self, string):
        # 下面判断是否有指数幂，有则做相应的计算
        if string.find("**") != -1:
            first_para = string.find("(", string.find("**"))
            min_list = list()
            min_list.append(string.find("+", string.find("**")))
            min_list.append(string.find("-", string.find("**")))
            min_list.append(string.find("/", string.find("**")))
            min_list.append(string.find(")", string.find("**")))
            min_list.append(string.find("*", string.find("**") + 2))
            min_list.sort()
            min_index = -1  # 找到四则运算中最小索引，没有则最小索引为-1
            while len(min_list):
                a = min_list.pop(0)
                if a >= 0:
                    min_index = a
                    break
            # 如果是形如“x**(式子)”的形式则可以直接去掉第一个括号写成“x^式子”
            if 0 < first_para < min_index or min_index < 0 < first_para:
                start = string.find("(", string.find("**"))
                if string.find("(", string.find("**")) \
                        == string.find("**") + 2:
                    string = string[:string.find("**") + 2] \
                             + string[string.find("**") + 3:self.find_para(string, start)] \
                             + "}" + string[self.find_para(string, start) + 1:]
                else:
                    string = string[:self.find_para(string, start) + 1] \
                             + "}" + string[self.find_para(string, start) + 1:]
            # 否则正常化简即可
            elif min_index != -1:
                string = string[:min_index] + \
                         "}" + string[min_index:]
            else:
                string = string + "}"
            string = string[:string.find("**")] + \
                     "^{" + string[string.find("**") + 2:]
            string = self.change_fundamental_symbol(string)
        # 直接将乘号去掉
        string = string.replace("*", "")
        # 如果式子里面没有除号就不需要继续转换了，递归
        if self.my_find_division(string) == -1:
            # 下面的代码处理下一级括号中的字符串
            start = -1
            while string.find("(", start + 1) != -1:
                start = string.find("(", start + 1)
                end = self.find_para(string, start)
                string = string[:start + 1] + self.change_fundamental_symbol(
                    string[start + 1:end]) + string[end:]
            return string
        # 下面的while 将除号前面的一部分进行提取分子操作
        index = self.my_find_division(string)
        pointer = index
        pointer -= 1
        while pointer >= 0:
            if string[pointer] == ')':
                pointer = self.find_pre_para(string, pointer)
            if string[pointer] == '+' or string[pointer] == '-' or string[
                pointer] == '{' or string[pointer] == '}' or string[pointer] == ',':
                string = string[:pointer + 1] \
                         + "\\frac {" + string[pointer + 1:]
                break
            # 如果到开头都是分子就直接在开头加入符号
            if pointer == 0:
                string = "\\frac {" + string
            pointer -= 1
        # 下面直到while结束，进行除号后面的提取分母操作
        index = self.my_find_division(string)
        pointer = index + 1
        # 如果形如 “式子/(式子)”则显示后分母就没有括号，显示为"式子/式子"
        if string[pointer] == "(":
            end = self.find_para(string, pointer)
            string = string[:index] + "}{" \
                     + string[index + 2:end] + "}" \
                     + string[end + 1:]
            return string
        # 如果不是上述情况则正常处理
        string = string[:index] + "}{" + string[index + 1:]
        while pointer < len(string):
            if string[pointer] == "(":
                pointer = self.find_para(string, pointer)
            if string[pointer] == '+' or string[pointer] == '-' or string[pointer] == ',' :
                string = string[:pointer] + "}" + string[pointer:]
                break
            if pointer == len(string) - 1:
                string = string + "}"
                break
            pointer += 1
        return self.change_fundamental_symbol(string)

    def simplify_sum(self, string):
        """同时化简summation和函数本身"""
        if string.find("summation") == -1:
            return self.change_fundamental_symbol(string)
        index = string.find("summation") + 9
        end = self.find_para(string, index)
        end_string = string[end + 1:]
        parameters = string[self.find_pre_para(
            string, end - 1) + 1:end - 1].split(",")
        end = self.find_pre_para(string, end - 1) - 1
        function_string = string[index + 1:end]
        string = "\\sum_{" + parameters[0] + "=" + \
                 parameters[1] + "}^{" + parameters[2] + "}"
        return string \
               + "\\left [ " + self.simplify_sum(function_string) \
               + " \\right ]" + \
               self.simplify_sum(end_string)

    def simplify_limit(self, string):
        """在化简summation后执行此函数"""
        if string.find("limit") == -1:
            return string
        start = string.find("limit") + 5
        end = self.find_para(string, start)
        function_string = string[start + 1:end]
        parameters = function_string.split(",")
        return string[:start - 5] \
               + "\\lim_{" + parameters[1] \
               + "\\to " + parameters[2] + "}\\left [ " \
               + self.simplify_limit(parameters[0]) + " \\right ]" \
               + string[end + 1:]

    def simplify_diff(self, string):
        """在化简limit后执行"""
        if string.find("diff") == -1:
            return string
        start = string.find("diff") + 4
        end = self.find_para(string, start)
        function_string = string[start + 1:end]
        parameters = function_string.split(",")
        return string[:start - 4] \
               + "\\frac{\\partial \\left [ " + parameters[0] \
               + " \\right ]}{\\partial " + parameters[1] + "}" \
               + string[end + 1:]

    def simplify_integral(self, string):
        if string.find("integrate") == -1:
            return string
        index = string.find("integrate") + 9
        end = self.find_para(string, index)
        # 定积分
        if string[end - 1] == ")":
            end_string = string[end + 1:]
            parameters = string[self.find_pre_para(
                string, end - 1) + 1:end - 1].split(",")
            end = self.find_pre_para(string, end - 1) - 1
            function_string = string[index + 1:end]
            print(function_string)
            string = "\\int_{" + parameters[1] + "}^{" + parameters[2] + "}"
            if string.find("x") == -1 or string.find("y") == -1:
                return string \
                       + "\\left [ " + self.simplify_integral(function_string) \
                       + " \\right ]" \
                       + "d" + parameters[0] \
                       + self.simplify_integral(end_string)
            else:
                end2 = len(function_string) - 1
                start2 = self.find_pre_para(function_string, end2)
                parameters2 = function_string[start2 + 1:end2].split(",")
                string = "\\int_{" + parameters[1] + "}^{" + parameters[2] + "}" \
                         + "\\int_{" + parameters2[1] + "}^{" + parameters2[2] + "}" \
                         + "\\left [ " + self.simplify_integral(function_string[:start2 - 1]) \
                         + " \\right ]" \
                         + "d" + parameters2[0] \
                         + "d" + parameters[0] \
                         + self.simplify_integral(end_string)
                return string
        # 不定积分
        else:
            start = string.find("integrate") + 9
            end = self.find_para(string, start)
            function_string = string[start + 1:end]
            parameters = function_string.split(",")
            if function_string.find("x") == -1 or function_string.find("y") == -1:
                return string[:start - 9] \
                       + "\\int \\left [ " + parameters[0] \
                       + " \\right ]d" + parameters[1] \
                       + string[end + 1:]
            else:
                return string[:start - 9] \
                       + "\\int " + "\\int \\left [ " + parameters[0] \
                       + " \\right ]d" + parameters[1] \
                       + "d" + parameters[2] \
                       + string[end + 1:]

    def string2latex(self):
        self.string = self.string.replace(" ", "")
        self.string = self.string.replace("/", "/ ")
        self.string = self.simplify_sum(self.string)
        self.string = self.simplify_limit(self.string)
        self.string = self.simplify_diff(self.string)
        self.string = self.simplify_integral(self.string)
        self.string = "$" + self.string + "$"
        self.string = self.string.replace("log", r"\ln ")
        self.string = self.change_trangle_symbol(self.string)
        self.string = self.string.replace(r"\ln 10", r"\log_{10} ")
        self.string = self.change_trangle_symbol(self.string)
        self.string = self.string.replace("gamma", r"\Gamma ")
        self.string = self.change_trangle_symbol(self.string)
        self.string = self.string.replace("sin", r"\sin ")
        self.string = self.change_trangle_symbol(self.string)
        self.string = self.string.replace("tan", r"\tan ")
        self.string = self.change_trangle_symbol(self.string)
        self.string = self.string.replace("cos", r"\cos ")
        self.string = self.change_trangle_symbol(self.string)
        self.string = self.string.replace(r"a\sin ", r"\arcsin ")
        self.string = self.string.replace(r"a\cos ", r"\arccos ")
        self.string = self.string.replace(r"a\tan ", r"\arctan ")
        self.string = self.string.replace(r"\arcsin h", r"arcsinh")
        self.string = self.string.replace(r"\arccos h", r"arccosh")
        self.string = self.string.replace(r"\arctan h", r"arctanh")
        self.string = self.string.replace("oo", "\\infty ")
        self.string = self.string.replace("pi", "\\pi ")
        self.string = self.change_sqrt_symbol(self.string)

    def change_sqrt_symbol(self, string):
        while string.find("sqrt(") != -1:
            start = string.find("sqrt")
            string = string[:start] + "\\sqrt {" \
                     + string[start + 5:self.find_para(string, start + 4)] \
                     + "}" + string[self.find_para(string, start + 4) + 1:]
        return string

    def paint(self, string):
        if string == '':
            self.ax.texts.clear()
            self.frame_plot.draw()
            return
        self.string = string
        self.string2latex()
        self.ax.texts.clear()
        self.ax.text(0.5, 0.5, self.string,
                     horizontalalignment='center', fontsize=10)
        print(self.string)
        self.frame_plot.draw()
