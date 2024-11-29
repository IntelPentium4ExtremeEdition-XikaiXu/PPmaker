import struct
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from system_transport import FileIO, SerialComm
from time import sleep
import time
import threading
import json

sc = SerialComm()
write = False

f = Figure(figsize=(8, 6), dpi=160)
a = f.add_subplot(111, ylim=(0, 1))

class Run:
    def __init__(self):
        root = tk.Tk()
        cw = ContentWindow(root)
        cw.pack()
        cw.mainloop()

class LoginWindow(tk.Frame):
    WIDTH = 30
    HEIGHT = 1
    FONT = ("TkDefaultFont", 10)
    DEFAULT_USERNAME_TEXT = "Username"  # 默认用户名文本
    DEFAULT_PASSWORD_TEXT = "Password"  # 默认密码文本
    DEFAULT_LOGIN_BUTTON_TEXT = "Login"  # 默认登录按钮文本
    DEFAULT_REGISTER_BUTTON_TEXT = "Register User"  # 默认注册按钮文本
    PADDING = 10  # 边距
    PASSWORDFILE = "password.json"  # 密码文件

    __mainWindow = None  # 主窗口
    __usernameField = None  # 用户名输入框
    __passwordField = None  # 密码输入框
    __loginButton = None  # 登录按钮
    __registerButton = None  # 注册按钮
    __password = None  # 密码
    __username = None  # 用户名
    __buttonFrame = None  # 按钮框架
    __paddingFrame = None  # 填充框架

    def __init__(self, mainWindow):
        """初始化构造函数
        
        参数:
        mainWindow (tk.Tk): 主窗口对象
        """
        tk.Frame.__init__(self, mainWindow, padx=self.PADDING, pady=self.PADDING)
        self.__mainWindow = mainWindow
        # 初始化框架组件
        self.__initializeEntryFields()
        self.__initializeButtons()
        # 初始化框架属性
        self.__paddingFrame = tk.Frame(mainWindow)
        self.__paddingFrame.pack()

    def __initializeEntryFields(self):
        """初始化输入框组件"""
        self.__usernameLabel = tk.Label(self, text=self.DEFAULT_USERNAME_TEXT)  # 用户名标签
        self.__usernameLabel.pack(pady=self.PADDING / 3)
        self.__usernameField = tk.Entry(self, width=self.WIDTH, font=self.FONT)  # 用户名输入框
        self.__usernameField.pack(pady=self.PADDING)
        self.__passwordLabel = tk.Label(self, text=self.DEFAULT_PASSWORD_TEXT)  # 密码标签
        self.__passwordLabel.pack(pady=self.PADDING / 3)
        self.__passwordField = tk.Entry(self, width=self.WIDTH, font=self.FONT, show="*")  # 密码输入框
        self.__passwordField.pack(pady=self.PADDING)

    def __initializeButtons(self):
        """初始化按钮组件"""
        self.__buttonFrame = tk.Frame(self)
        self.__loginButton = tk.Button(self.__buttonFrame, text=self.DEFAULT_LOGIN_BUTTON_TEXT, command=self.checkPass)  # 登录按钮
        self.__loginButton.grid(row=0, column=0, padx=5, pady=10)
        self.__registerButton = tk.Button(self.__buttonFrame, text=self.DEFAULT_REGISTER_BUTTON_TEXT, command=self.registerUser)  # 注册按钮
        self.__registerButton.grid(row=0, column=1, padx=5, pady=10)
        self.__buttonFrame.pack()

    def getText(self):
        """获取用户名和密码输入框中的文本"""
        self.__password = self.__passwordField.get()
        self.__username = self.__usernameField.get()

    def checkPass(self):
        """检查用户名和密码"""
        self.getText()
        alt = FileIO(self.PASSWORDFILE)  # 创建 FileIO 对象来处理密码文件
        f = alt.readText()  # 读取文件中的文本
        if not f:
            alt.writeText("")  # 如果文件为空，写入空文本
            f = ""

        if self.__username == "" or self.__password == "":  # 如果用户名或密码为空
            messagebox.showinfo("Error: No Data Entered", "NO DATA ENTERED")
        elif self.__username in f:  # 如果用户名存在
            if self.__password == f[self.__username]:  # 如果密码匹配
                self.__paddingFrame.pack_forget()  # 隐藏填充框架
                self.__mainWindow.login()  # 调用登录方法
            else:
                messagebox.askretrycancel("User Validation", "Wrong password, try again?")  # 密码错误，提示重试
        else:
            messagebox.showinfo("User Validation", "User not registered, Please Register User")  # 用户未注册，提示注册

    def registerUser(self):
        """注册新用户"""
        alt = FileIO(self.PASSWORDFILE)
        d = alt.get_length()  # 获取当前用户数
        f = alt.readText()  # 读取文件中的用户数据
        self.getText()  # 获取输入的用户名和密码
        text = {self.__username: self.__password}  # 创建包含新用户信息的字典
        if self.__username == "" or self.__password == "":  # 如果用户名或密码为空
            messagebox.showinfo("Error: No Data Entered", "NO DATA ENTERED")
        elif self.__username in f:  # 如果用户名已存在
            messagebox.showinfo("Error: User Exists", "Create another user or login")  # 用户已存在，提示重新创建
        elif d == 10:  # 如果用户数量达到最大限制（10个用户）
            messagebox.showinfo("User Limit", "Maximum 10 users allowed")
        else:
            alt.writeText(text)  # 写入新用户数据
            messagebox.showinfo("User Registered", "User Successfully Registered")  # 显示注册成功消息

    def getUsername(self):
        """返回当前用户名"""
        return self.__username

    def clearVal(self):
        """清除输入框中的文本"""
        self.__usernameField.delete(0, tk.END)  # 清空用户名输入框
        self.__passwordField.delete(0, tk.END)  # 清空密码输入框

    def setPaddingVisible(self):
        """显示填充框架"""
        self.__paddingFrame.pack()


class DCMWindow(tk.Frame):
    """继承自tk.Frame
        DCMWindow是tk.Frame的子类，存储了DCM窗口的所有组件。
    """
    # 常量
    PARAMLABELS = ["Ampitute","LRL",
                   "Pulsewidth", "Threshold" , "ARP",
                   "VRP", "URL", "MSR", "Activity_Threshold",
                    "Response_Factor", "Reaction_time", "Recovery_time", ""]
    Ampitute = []
    LRL = [30, 35, 40, 45, 50]  # 下限速率
    Pulsewidth = []
    ARP = []
    VRP = []
    URL = []
    Response_Factor = []
    Threshold = []
    MSR = []  # 最大速度响应
    Activity_Threshold = ["V-Low", "Low", "Med-Low", "Med", "Med-High", "High", "V-High"]  # 活动阈值
    Recovery_time = []
    Reaction_time = []
    PROGRAMABLEPARAMETERS = [Ampitute,LRL,
                   Pulsewidth, Threshold , ARP,
                   VRP, URL, MSR, Activity_Threshold,
                    Response_Factor, Reaction_time, Recovery_time]  # 可编程参数
    
    PARAMETERFILE = "parameters.json"  # 参数文件
    TYPELIST = ["16", "16", "f", "16", "f", "f", "16", "16", "f", "16", "16", "16"]  # 类型列表
    NUMBEROFPARAMETERS = len(PROGRAMABLEPARAMETERS)  # 参数数量
    MODELABELS = ["AOO", "VOO", "AAI", "VVI", "AOOR", "VOOR", "AAIR", "VVIR"]  # 模式标签
    BACKGROUND_COLOR = "#FFFFFF"  # 背景颜色
    SERIALCOMMODE = SerialComm().getSerialPorts()  # 获取串口通信模式
    ACTIVITYTHRESHOLDDICT = {"V-Low": 1.1, "Low": 1.3, "Med-Low": 1.5, "Med": 1.7, "Med-High": 1.9, "High": 2.1,
                             "V-High": 2.3}  # 活动阈值字典

    # 私有变量
    __mainWindow = None  # 主窗口
    __labelArr = []  # 标签数组
    __entryArr = []  # 输入框数组
    __buttonArr = []  # 按钮数组
    __modeList = None  # 模式列表
    __currentMode = None  # 当前模式
    __currentPort = None  # 当前串口
    __saveButton = None  # 保存按钮
    __comMode = None  # 通信模式
    __usernameLabel = None  # 用户名标签
    __comButton = None  # 串口按钮
    __consoleLog = None  # 控制台日志
    __buttonSend = None  # 发送按钮
    __username = None  # 用户名
    __showState = ["readonly", "readonly", "readonly", "readonly", "readonly", "readonly", "readonly", "readonly"]  # 显示状态
    __graphWindowButton = None  # 图形窗口按钮

    def __init__(self, mainWindow, username):
        """构造函数
        
        参数:
            mainWindow (ContentWindow): 存储DCMWindow的上级框架
            username (string): 存储用户名
        """
        tk.Frame.__init__(self, mainWindow, bg=self.BACKGROUND_COLOR, width=1280, height=600)
        self.__username = username  # 设置用户名
        self.__initalizeConstants()  # 初始化常量
        self.__mainWindow = mainWindow  # 设置主窗口
        self.__mainWindow.focus_set()  # 设置焦点
        self.__currentMode = ""  # 初始化当前模式为空
        self.__currentPort = StringVar(self)  # 设置当前串口
        self.__initalizeTopFrame(username)  # 初始化顶部框架
        self.__centerFrame = tk.Frame(self, bg=self.BACKGROUND_COLOR, width=1280, height=550)  # 创建中心框架
        self.__centerFrame.pack()  # 显示中心框架
        self.__initalizeRightFrame()  # 初始化右侧框架
        self.__initalizeBottomFrame()  # 初始化底部框架
        self.canvas = FigureCanvasTkAgg(f, self)  # 创建画布
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)  # 显示画布
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)  # 创建工具栏
        self.toolbar.update()  # 更新工具栏
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)  # 显示工具栏

    def __initalizeTopFrame(self, username):
        """初始化DCM窗口的顶部框架

        参数:
            username (string): 存储用户名
        """
        
        # 创建标题标签
        title_label = tk.Label(self, text="Pacemaker Project")
        title_label.pack(pady=20)

        # 创建顶部框架
        self.__topFrame = Frame(self, bg=self.BACKGROUND_COLOR, width=1280, height=30)
        
        # 显示用户名标签
        self.__usernameLabel = Label(self.__topFrame, text="User: " + username)
        self.__usernameLabel.grid(row=0, column=0, padx=110)
        
        # 串口通信模式选择框
        self.__comMode = ttk.Combobox(self.__topFrame, values=self.SERIALCOMMODE, state="readonly")
        self.__comMode.grid(row=0, column=1, padx=5)
        
        # 连接按钮
        self.__comButton = Button(self.__topFrame, text="Connect", bg="lightgreen", command=self.__checkPort, relief="flat", padx=20)
        self.__comButton.grid(row=0, column=2, padx=5)
        
        
        # 显示顶部框架
        self.__topFrame.pack()

    # 初始化右侧框架
    def __initalizeRightFrame(self):
        """初始化DCM窗口的右侧框架
        """
        self.__rightFrame = Frame(self.__centerFrame, bg=self.BACKGROUND_COLOR, width=640, height=550)
        self.__rightFrame.grid(row=0, column=1)
        
        # 创建右侧框架的上半部分
        topRight = Frame(self.__rightFrame, bg=self.BACKGROUND_COLOR, width=640, height=275)
        # 创建右侧框架的下半部分
        bottomRight = Frame(self.__rightFrame, bg=self.BACKGROUND_COLOR, width=640, height=275)
        
        # 显示右侧框架的上下部分
        topRight.pack()
        bottomRight.pack()
        
        # 创建“选择模式”按钮
        self.__saveButton = Button(topRight, text="Select Mode",  relief="flat", padx=20)
        self.__saveButton.grid(row=0, column=5, padx=20, pady=20)
     
        # 创建模式选择框
        self.__modeList = ttk.Combobox(topRight, values=self.MODELABELS, state="readonly")
        self.__modeList.grid(row=0, column=0, padx=20, pady=20)
        self.__modeList.current(0)
        
        # 初始化参数列表
        self.__initalizeParameterList(bottomRight)

    # 初始化底部框架
    def __initalizeBottomFrame(self):
        """初始化DCM窗口的底部框架
        """
        self.__bottomFrame = Frame(self, bg=self.BACKGROUND_COLOR, width=1280, height=10)
        self.__bottomFrame.pack()
        
        # 创建发送按钮
        self.__buttonSend = Button(self.__bottomFrame, text="Send", command=self.__saveParameters, relief="flat", padx=20)
        self.__buttonSend.grid(row=0, column=1, padx=20, pady=5)
        
        # 创建“绘制数据”按钮
        self.__graphWindowButton = Button(self.__bottomFrame, text="Plot Data", command=self.__graphButtonClicked, relief="flat", padx=10)
        self.__graphWindowButton.grid(row=0, column=3, padx=20, pady=5)

    # 按钮点击事件，触发绘制数据
    def __graphButtonClicked(self):
        """检测“绘制数据”按钮是否被点击
        """
        t1_gw = threading.Thread(target=self.__displayGraph)
        t1_gw.start()

    # 线程函数，用于在DCM窗口上绘制ECG图
    def __displayGraph(self):
        """线程函数，用于绘制ECG图
        """
        global write
        t = time.time()  # 记录当前时间
        tvlist = []  # 存储心电图的时间戳
        talist = []  # 存储心电图的幅度
        voltageV = []  # 存储电压V数据
        voltageA = []  # 存储电压A数据
        lasttime = t  # 最后更新时间

        write = True  # 初始为未写入状态
        print(write)
        print(sc.getCurrentPort())
        print(sc.serialWrite(b'\x16\x00\x22'))
        while not write:
            # 判断串口是否打开
            if not (sc.getCurrentPort() is None):
                if not write:
                    # 发送数据到串口
                    sc.serialWrite(b'\x16\x00\x22')
                    print(sc.serialWrite(b'\x16\x00\x22'))
                    temp = sc.serial_read()  # 读取串口数据
                    temp = 0  # 临时值
                    try:
                        # 解包读取第一个值
                        val, = struct.unpack('d', temp[0:8])
                        # 如果值在有效范围内，保存数据
                        if (val > 0.4) and (val < 3.5):
                            voltageA.append(val * 3.3)
                            talist.append(time.time() - t)
                    except Exception:
                        # 如果读取失败，设置默认值
                        voltageA.append(0.5 * 3.3)
                        talist.append(time.time() - t)

                    try:
                        # 解包读取第二个值
                        val, = struct.unpack('d', temp[8:len(temp)])
                        # 如果值在有效范围内，保存数据
                        if (val > 0.4) and (val < 5):
                            voltageV.append(val * 3.3)
                            tvlist.append(time.time() - t)
                    except Exception:
                        # 如果读取失败，设置默认值
                        voltageV.append(0.5 * 3.3)
                        tvlist.append(time.time() - t)
                else:
                    sleep(0.5)

                # 如果电压数据超过500个，删除最旧的数据
                if len(voltageA) > 350:
                    voltageA.pop(0)
                    talist.pop(0)

                # 如果电压数据超过600个，删除最旧的数据
                if len(voltageV) > 450:
                    voltageV.pop(0)
                    tvlist.pop(0)
                
                # 每隔0.25秒更新一次图表
                if time.time() - lasttime > 0.025:
                    lasttime = time.time()
                    a.clear()  # 清空画布
                    # 绘制心电图数据
                    a.plot(talist, voltageA, color='red')
                    a.plot(tvlist, voltageV, color='green')
                    self.canvas.draw()  # 更新画布


    def __saveParameters(self):
        global write

        """保存 PROGRAMABLEPARAMETERS 到外部 JSON 文件并发送参数"""
        try:
            parameters = {}
            arr = []

            if self.__entryArr[10]["state"] == "readonly":
                if (self.__entryArr[10].get() < self.__entryArr[0].get()) or (
                    self.__entryArr[10].get() > self.__entryArr[1].get()):
                    messagebox.showinfo("Error: Invalid inputs",
                                        "The Maximum Sensing Rate must be between URL and LRL.")
                    self.__entryArr[10].delete(0, tk.END)
                    return

            # 保存参数到文件
            alt = FileIO(self.__username + self.__currentMode + self.PARAMETERFILE)
            alt.writeText({"Mode": self.__currentMode})

            for i in range(self.NUMBEROFPARAMETERS):
                if self.__entryArr[i]["state"] == "readonly":
                    alt.writeText({self.PARAMLABELS[i], self.__entryArr[i].get()})


            # 构建字节数组
            arr.append((self.MODELABELS.index(self.__currentMode)).to_bytes(1, byteorder='little'))
            for i in range(self.NUMBEROFPARAMETERS):
                try:
                    if self.TYPELIST[i] == "8":
                        arr.append(int(self.__entryArr[i].get()).to_bytes(1, byteorder='little'))
                    elif self.TYPELIST[i] == "f":
                        temparr = bytearray(struct.pack('f', float(self.__entryArr[i].get())))
                        arr.extend(temparr)
                    else:
                        arr.append(int(self.__entryArr[i].get()).to_bytes(2, byteorder='little'))
                except ValueError:
                    default_val = b'\x00\x00' if self.TYPELIST[i] == "16" else b'\x00'
                    arr.extend(default_val)

            # 设置 write = True
                write = True  # 所有验证通过后设置 write 为 True

            # 发送串口数据
            val = b'\x16\00\x55' + b''.join(arr)
            t1_sc = threading.Thread(target=self.serialCommWrite, args=(val,))
            t1_sc.start()

            # 显示成功消息
            messagebox.showinfo("Success", "Parameters sent and saved successfully!")

        except Exception as e:
            write = False  # 出现异常时将 write 设置为 False
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")


    def serialCommWrite(self, val):
        global write
        print(type(val))
        sc.serialWrite(val)  # 通过串口发送数据
        print(val)
        write = False  # 写入完成后将标志设为False

    def resetMode(self):
        """ 将状态重置为 VOO 模式
        """
        alt = FileIO("Usernamemode")
        data = alt.readText()  # 读取用户名和模式数据
        if not data:
            alt.writeText("")  # 如果没有数据，则创建新文件
            data = ""

        # 如果没有保存的模式数据或用户名不匹配，设置为默认模式 "VOO"
        if len(data) == 0 or self.__username not in data:
            self.__modeList.set("VOO")
        else:
            self.__modeList.set(data[self.__username])  # 设置为保存的模式
            alt = FileIO(self.__username + data[self.__username] + self.PARAMETERFILE)
            f = alt.readText()  # 读取保存的参数文件

            # 重置参数值


    def __checkPort(self):
        """ 检查选择了哪个串口
        连接成功后，显示一个弹出框，表示成功连接。
        然后，获取当前选中的串口并设置它，接着启动一个线程来检查串口。
        """
        messagebox.showinfo("Success: Valid Connection", "Connected!")  # 弹出连接成功的提示框
        self.__currentPort = self.__comMode.get()  # 获取当前选中的串口
        sc.setPort(self.__currentPort)  # 设置串口
        t2_sc = threading.Thread(target=self.__runPort)  # 启动一个线程来运行串口检查函数
        t2_sc.daemon = True  # 设置线程为守护线程，主程序结束时该线程也会结束
        t2_sc.start()  # 启动线程

    def __runPort(self):
        """ 独立线程函数，用于检查串口
        该函数将在一个独立线程中运行，更新可用的串口列表。
        """
        self.__comMode["values"] = SerialComm().getSerialPorts()  # 获取串口列表并更新

    def setUsername(self, username):
        """ 显示当前用户的用户名在DCM窗口的左上角

        Args:
            username (string): 用户名
        """
        self.__usernameLabel.config(text="User: " + username)  # 更新界面上的用户名标签
        self.__username = username  # 保存用户名

    def __initalizeParameterList(self, higherFrame):
        """ 创建一个包含参数值输入的标签和文本输入框的网格

        Args:
            higherFrame (tk.Frame): 高级框架，用于存放组件
        """
        row_index = 0  # 初始化行索引
        column_index = 0  # 初始化列索引
        for i in range(0, self.NUMBEROFPARAMETERS, 2):
            for j in range(2):
                label = Label(higherFrame, text=self.PARAMLABELS[i + j], bg=self.BACKGROUND_COLOR)  # 创建标签
                entry = Entry(higherFrame, state="normal")  # 创建文本输入框
                self.__labelArr.append(label)  # 将标签添加到标签数组
                label.grid(row=row_index, column=column_index, padx=60, pady=2)  # 设置标签的网格位置，第一列或第二列
                self.__entryArr.append(entry)  # 将输入框添加到输入数组
                entry.grid(row=row_index + 1, column=column_index, padx=60, pady=2)  # 设置输入框的网格位置，第一列或第二列
                self.__buttonArr.append(entry)  # 将输入框添加到按钮数组
                
                # 每处理完一组标签和输入框后，切换到另一列
                column_index += 1
                if column_index == 2:  # 如果到了第二列，重置列索引并增加行索引
                    column_index = 0
                    row_index += 2  # 每个标签和输入框占用两行，增加行索引



    def __initalizeConstants(self):
        """ 
        初始化不同参数设置的值。
        此函数为不同的心脏起搏器设置（如 LRL、URL、MSR 等）生成一系列的预设值。
        """
        # 初始化 LRL（最小心率）列表，范围从 51 到 135，每个值递增 1。
        for i in range(40):
            self.LRL.append(51 + i)
        # 为 LRL 添加额外的值，范围从 95 开始，每个值递增 5。
        for i in range(17):
            self.LRL.append(95 + 5 * i)

        # 初始化 URL（最大心率）和 MSR（最大感应率）列表，值从 50 开始，每个值递增 5。
        for i in range(26):
            self.URL.append(50 + i * 5)
            self.MSR.append(50 + i * 5)

        # 初始化 REACTIONTIME（反应时间）列表，值从 10 到 50，递增 10。
        for i in range(10, 51, 10):
            self.Reaction_time.append(i)

        # 初始化 RESPONSEFACTOR（反应因子）列表，值从 1 到 16，递增 1。
        for i in range(1, 17):
            self.Response_Factor.append(i)

        # 初始化 RECOVERYTIME（恢复时间）列表，值从 2 到 16，递增 1。
        for i in range(2, 17, 1):
            self.Recovery_time.append(i)


class ContentWindow(tk.Frame):
    """ 
    扩展 tk.Frame
    ContentWindow 是 tk.Frame 的子类，存储所有内容窗口的组件。
    ContentWindow 用于管理 DCM 中其他框架的交互。
    """
    # 私有变量
    __loginWindow = None  # 登录窗口
    __parent = None  # 父窗口
    __DCM = None  # DCM 窗口

    # 公共变量
    username = ""  # 用户名
    def __init__(self, parent):
        """对象构造函数

        参数:
        parent (tk.Tk): 顶级框架，持有 ContentWindow 的父窗口。通常parent 应为 tk.Tk()，因为 ContentWindow 是一个顶级窗口管理器
        """
        tk.Frame.__init__(self, parent)
        self.__parent = parent
        parent.title("PPMaker Extreme Edition")  # 设置窗口标题
        parent.geometry("700x850")  # 设置窗口大小
        parent.resizable(True, True)  # 允许窗口调整大小

        self.__loginWindow = LoginWindow(self)  # 创建登录窗口

        self.__DCM = DCMWindow(self, self.username)  # 创建 DCM 窗口
        
        self.__loginWindow.pack()  # 显示登录窗口

    def login(self):
        """ 该方法禁用登录窗口界面并启用 DCM 界面，同时进行格式化
        """
        self.__loginWindow.pack_forget()  # 隐藏登录窗口
        self.username = self.__loginWindow.getUsername()  # 获取用户名
        self.__DCM.setUsername(self.username)  # 设置 DCM 窗口的用户名
        self.__DCM.resetMode()  # 重置 DCM 窗口模式
        self.__DCM.pack()  # 显示 DCM 窗口

# Main script
if __name__ == "__main__":
    run = Run()
