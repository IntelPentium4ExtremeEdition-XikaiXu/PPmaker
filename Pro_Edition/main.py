import struct
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from IOStream import FileIO, SerialComm
from time import sleep
import time
import threading

sc = SerialComm()
write = False

f = Figure(figsize=(8, 6), dpi=160)
a = f.add_subplot(111, ylim=(0, 1))

class Run:
    def __init__(self):
        root = tk.Tk()
        # The login window object is created
        cw = ContentWindow(root)
        cw.pack()
        cw.mainloop()

class LoginWindow(tk.Frame):
    # Variable Declaration
    # Constants
    WIDTH = 30
    HEIGHT = 1
    FONT = ("Arial", 12)
    DEFAULT_USERNAME_TEXT = "Username"
    DEFAULT_PASSWORD_TEXT = "Password"
    DEFAULT_LOGIN_BUTTON_TEXT = "Login"
    DEFAULT_REGISTER_BUTTON_TEXT = "Register User"
    PADDING = 10
    BACKGROUND_COLOR = "#ADD8E6"
    FOREGROUND_COLOR = "#C0C0C0"
    PASSWORDFILE = "password.json"

    # Private Variables
    __mainWindow = None
    __usernameField = None
    __passwordField = None
    __loginButton = None
    __registerButton = None
    __password = None
    __username = None
    __buttonFrame = None
    __paddingFrame = None

    # Public Variables

    def __init__(self, mainWindow):
        tk.Frame.__init__(self, mainWindow, bg=self.FOREGROUND_COLOR, width=200, height=200, padx=self.PADDING,
                          pady=self.PADDING, relief=tk.RIDGE, borderwidth=3)
        self.__mainWindow = mainWindow
        # Initialize components of frame
        self.__initializeEntryFields()
        self.__initializeButtons()
        # Initialize frame properties
        self.__paddingFrame = Frame(mainWindow, bg=self.BACKGROUND_COLOR, width=300, height=150)
        self.__paddingFrame.pack()


    def __initializeEntryFields(self):
        self.__usernameField = Entry(self, width=self.WIDTH, font=self.FONT)
        self.__usernameLabel = Label(self, text=self.DEFAULT_USERNAME_TEXT, bg=self.FOREGROUND_COLOR)
        self.__passwordLabel = Label(self, text=self.DEFAULT_PASSWORD_TEXT, bg=self.FOREGROUND_COLOR)
        self.__usernameLabel.pack(pady=self.PADDING / 3)
        self.__usernameField.pack(pady=self.PADDING)
        self.__passwordLabel.pack(pady=self.PADDING / 3)
        self.__passwordField = Entry(self, width=self.WIDTH, font=self.FONT, show="*")
        self.__passwordField.pack(pady=self.PADDING)

    def __initializeButtons(self):
        self.__buttonFrame = Frame(self, bg=self.FOREGROUND_COLOR)
        self.__loginButton = Button(self.__buttonFrame, text=self.DEFAULT_LOGIN_BUTTON_TEXT, command=self.checkPass,
                                    relief="flat")

        self.__loginButton.grid(row=0, column=0, padx=5, pady=10)

        self.__registerButton = Button(self.__buttonFrame, text=self.DEFAULT_REGISTER_BUTTON_TEXT,
                                       command=self.registerUser, relief="flat")
        self.__registerButton.grid(row=0, column=1, padx=5, pady=10)

        self.__buttonFrame.pack()

    def getText(self):
        self.__password = self.__passwordField.get()
        self.__username = self.__usernameField.get()

    def checkPass(self):
        self.getText()
        alt = FileIO(self.PASSWORDFILE)
        f = alt.readText()
        if not f:
            alt.writeText("")
            f = ""

        if self.__username == "" or self.__password == "":
            messagebox.showinfo("Error: No Data Entered", "NO DATA ENTERED")
        elif self.__username in f:
            if self.__password == f[self.__username]:
                self.__paddingFrame.pack_forget()
                self.__mainWindow.login()
            else:
                messagebox.askretrycancel("User Validation", "Wrong password,try again?")
        else:
            messagebox.showinfo("User Validation", "User not registered, Please Register User")

    def registerUser(self):
        """Registers a new user and checks whether a user already exists
        """
        alt = FileIO(self.PASSWORDFILE)
        d = alt.getlength()
        f = alt.readText()
        self.getText()
        text = {self.__username: self.__password}
        if self.__username == "" or self.__password == "":
            messagebox.showinfo("Error: No Data Entered", "NO DATA ENTERED")
        elif self.__username in f:
            messagebox.showinfo("Error: User Exists", "Create another user or login")
        elif d == 10:
            messagebox.showinfo("User Limit", "Maximum 10 users allowed")
        else:
            alt.writeText(text)
            messagebox.showinfo("User Registered", "User Successfully Registered")

    def getUsername(self):
        return self.__username

    def clearVal(self):
        """Clears the entry fields in LoginWindow
        """
        self.__usernameField.delete(0, END)
        self.__usernameField.pack()
        self.__passwordField.delete(0, END)
        self.__passwordField.pack()

    def setPaddingVisible(self):
        """ Helper function for formatting
        """
        self.__paddingFrame.pack()


class DCMWindow(tk.Frame):
    """ Extends tk.Frame
        The DCMWindow is a subclass of tk.Frame that stores all the components of the DCM Window.
    """
    # Constants
    #PARAMLABELS = ["Lower Rate Limit", "Upper Rate Limit", "Atrial Amplitude", "Ventricular Amplitude",
     #              "Atrial Pulsewidth", "Ventricular Pulsewidth", "Atrial Refractory Period",
      #             "Ventricular Refractory Period", "Atrium Sense", "Ventricle Sense", "MSR", "Recovery Time",
       #            "Reaction Time", "Response Factor", "Activity Threshold", "AV Delay", ""]
    
    PARAMLABELS = ["AMP", "LRL", "PulseWidth", "thresold",
                   "ARP", "VRP", "Upper_rate",
                   "MSR", "Action_threshood", "response_factor", "reaction_time", "recovery_time"]
    
    LRL = [30, 35, 40, 45, 50]
    URL = []
    ATRAMP = ["Off"]
    VENTAMP = ["Off"]
    ATRWIDTH = []
    VENTWIDTH = []
    ATRREFRAC = []
    VENTREFRAC = []
    ASENSE = [0]
    VSENSE = [0]
    MSR = []
    RECOVERYTIME = []
    REACTIONTIME = []
    RESPONSEFACTOR = []
    ACTIVITYTHRESHOLD = ["V-Low", "Low", "Med-Low", "Med", "Med-High", "High", "V-High"]
    AVDELAY = []
    PROGRAMABLEPARAMETERS = [LRL, URL, ATRAMP, VENTAMP, ATRWIDTH, VENTWIDTH, ATRREFRAC, VENTREFRAC, ASENSE, VSENSE, MSR,
                             RECOVERYTIME, REACTIONTIME, RESPONSEFACTOR, ACTIVITYTHRESHOLD, AVDELAY]
    PARAMETERFILE = "parameters.json"

    TYPELIST = ["1", "1", "1", "1", "2", "2", "2", "2", "1", "1", "1", "1", "8", "8", "f", "16"]

    #TYPELIST = ["8", "8", "f", "f", "8", "8", "16", "16", "f", "f", "8", "8", "8", "8", "f", "16"]
    
    NUMBEROFPARAMETERS = len(PROGRAMABLEPARAMETERS)

    MODELABELS = ["AOO", "VOO", "AAI", "VVI", "AOOR", "VOOR", "AAIR", "VVIR"]
    # The following variable is a placeholder before serial communication is implemented
    BACKGROUND_COLOR = "#ADD8E6"
    SERIALCOMMODE = SerialComm().getSerialPorts()
    ACTIVITYTHRESHOLDDICT = {"V-Low": 1.1, "Low": 1.3, "Med-Low": 1.5, "Med": 1.7, "Med-High": 1.9, "High": 2.1,
                             "V-High": 2.3}

    # Private Variables
    __mainWindow = None
    __labelArr = []
    __entryArr = []
    __buttonArr = []
    __modeList = None
    __currentMode = None
    __currentPort = None
    __saveButton = None
    __comMode = None
    __usernameLabel = None
    __logoutButton = None
    __comButton = None
    __consoleLog = None
    __buttonSend = None
    __username = None
    __showState = ["readonly", "readonly", "readonly", "readonly", "readonly", "readonly", "readonly", "readonly"]
    __graphWindowButton = None

    def __init__(self, mainWindow, username):
        tk.Frame.__init__(self, mainWindow, bg=self.BACKGROUND_COLOR, width=1280, height=600)
        self.__username = username
        self.__initalizeConstants()
        self.__mainWindow = mainWindow
        self.__mainWindow.focus_set()
        self.__currentMode = ""
        self.__currentPort = StringVar(self)
        self.__initalizeTopFrame(username)
        self.__centerFrame = Frame(self, bg=self.BACKGROUND_COLOR, width=1280, height=550)
        self.__centerFrame.pack()
        self.__initalizeRightFrame()
        self.__initalizeBottomFrame()
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        #self.__modeSelect()

    def __initalizeTopFrame(self, username):
        # 创建标题标签，显示项目名称 "Pacemaker Project"
        title_label = tk.Label(self, text="Pacemaker Project", bg=self.BACKGROUND_COLOR)
        title_label.pack(pady=20)  # 将标题标签放入窗口并设置上下间距

        # 创建一个顶部框架，设置背景颜色和大小
        self.__topFrame = Frame(self, bg=self.BACKGROUND_COLOR, width=1280, height=30)
        
        # 创建一个用户名标签，显示当前用户的用户名
        self.__usernameLabel = Label(self.__topFrame, text="User: " + username, bg=self.BACKGROUND_COLOR)
        self.__usernameLabel.grid(row=0, column=0, padx=110)  # 设置用户名标签的位置，添加水平间距

        # 创建一个串口模式选择框，用户可以选择不同的串口通信模式
        self.__comMode = ttk.Combobox(self.__topFrame, values=self.SERIALCOMMODE, state="readonly")
        self.__comMode.grid(row=0, column=1, padx=5)  # 设置选择框的位置，并添加水平间距

        # 创建一个连接按钮，点击后调用 __checkPort 方法来检查串口连接
        self.__comButton = Button(self.__topFrame, text="Connect", bg="lightgreen", command=self.__checkPort, relief="flat",
                                padx=20)
        self.__comButton.grid(row=0, column=2, padx=5)  # 设置连接按钮的位置，并添加水平间距

        # 创建一个登出按钮，点击后调用 logout 方法登出
#        self.__logoutButton = Button(self.__topFrame, text="Logout", bg="red", command=self.logout, relief="flat", padx=20)
#        self.__logoutButton.grid(row=0, column=3, padx=230)  # 设置登出按钮的位置，添加较大的水平间距

        # 将顶部框架添加到主窗口中
        self.__topFrame.pack()


    def __initalizeRightFrame(self):
        self.__rightFrame = Frame(self.__centerFrame, bg=self.BACKGROUND_COLOR, width=640, height=550)
        self.__rightFrame.grid(row=0, column=1)
        topRight = Frame(self.__rightFrame, bg=self.BACKGROUND_COLOR, width=640, height=275)
        bottomRight = Frame(self.__rightFrame, bg=self.BACKGROUND_COLOR, width=640, height=275)
        topRight.pack()
        bottomRight.pack()
        #self.__saveButton = Button(topRight, text="Select Mode", command=self.__modeSelect, relief="flat", padx=20)
        #self.__saveButton.grid(row=0, column=1, padx=20, pady=20)
        self.__modeList = ttk.Combobox(topRight, values=self.MODELABELS, state="readonly")
        self.__modeList.grid(row=0, column=0, padx=20, pady=20)
        self.__modeList.current(0)
        self.__initalizeParameterList(bottomRight)

    def __initalizeBottomFrame(self):
        self.__bottomFrame = Frame(self, bg=self.BACKGROUND_COLOR, width=1280, height=10)
        self.__bottomFrame.pack()
        self.__buttonSend = Button(self.__bottomFrame, text="Send", command=self.__saveParameters, relief="flat",
                                   padx=20)
        self.__buttonSend.grid(row=0, column=1, padx=20, pady=5)
        self.__graphWindowButton = Button(self.__bottomFrame, text="Plot Data", command=self.__graphButtonClicked,
                                          relief="flat", padx=10)
        self.__graphWindowButton.grid(row=0, column=3, padx=20, pady=5)

    def __graphButtonClicked(self):
        t1_gw = threading.Thread(target=self.__displayGraph)
        t1_gw.start()

    def __displayGraph(self):
        global write
        t = time.time()
        tvlist = []
        talist = []
        voltageV = []
        voltageA = []
        lasttime = t
        write = False
        print(write)
        while not write:
            if not (sc.getCurrentPort() is None):
                if not write:
                    sc.serialWrite(
                        b'\x10\x22\00\x3C\x78\x00\x00\xA0\x40\x00\x00\xA0\x40\x02\x02\xFA\x00\xFA\x00\x00\x00\x80\x40'
                        b'\x00\x00\x80\x40\x64\x02\x0A\x10\xCD\xCC\x8C\x3F\x64\x00')
                    temp = sc.serialRead()
                    try:
                        val, = struct.unpack('d', temp[0:8])
                        if (val > 0.4) and (val < 3.5):
                            voltageA.append(val * 3.3)
                            talist.append(time.time() - t)
                    except Exception:
                        voltageA.append(0.5 * 3.3)
                        talist.append(time.time() - t)
                    try:
                        val, = struct.unpack('d', temp[8:len(temp)])
                        if (val > 0.4) and (val < 5):
                            voltageV.append(val * 3.3)
                            tvlist.append(time.time() - t)
                    except Exception:
                        voltageV.append(0.5 * 3.3)
                        tvlist.append(time.time() - t)
                else:
                    sleep(2)

                if len(voltageA) > 500:
                    voltageA.pop(0)
                    talist.pop(0)

                if len(voltageV) > 600:
                    voltageV.pop(0)
                    tvlist.pop(0)
                if time.time() - lasttime > 0.25:
                    lasttime = time.time()
                    a.clear()
                    a.plot(talist, voltageA, color='red')
                    a.plot(tvlist, voltageV, color='green')
                    self.canvas.draw()

    def __saveParameters(self):
        messagebox.showinfo("Success.","Successfully sent parameters!")
        Data_stack = [] #init the
        print(self.__entryArr[10]["state"])
        if (self.__entryArr[0].get()) > (self.__entryArr[1].get()):
            print(self.__entryArr[0].get())
            print(self.__entryArr[1].get())
            messagebox.showinfo("Error:Invalid inputs",
                                "The lower rate limit has to be lower than the higher rate limit")
            for i in range(2):
                self.__entryArr[i].set("")
        elif (self.__entryArr[10]["state"] == "readonly") and (
                (self.__entryArr[10].get()) < (self.__entryArr[0].get())):
            print(self.__entryArr[10].get())
            print(self.__entryArr[0].get())
            messagebox.showinfo("Error:Invalid inputs", "The Maximum sensing rate has to be between URL and LRL")
            self.__entryArr[10].set("")
        elif (self.__entryArr[10]["state"] == "readonly") and (
                (self.__entryArr[10].get()) > (self.__entryArr[1].get())):
            print(self.__entryArr[10].get())
            print(self.__entryArr[1].get())
            messagebox.showinfo("Error:Invalid inputs", "The Maximum sensing rate has to be between URL and LRL")
            self.__entryArr[10].set("")
        else:
            global write
            write = True
            alt = FileIO(self.__username + self.__currentMode + self.PARAMETERFILE)
            f = alt.readText()
            if not f:
                alt.writeText("")
                f = ""
            for i in range(self.NUMBEROFPARAMETERS):
                alt.writeText({self.PARAMLABELS[i]: ""})
            alt.writeText({"Mode": self.__currentMode})
            for i in range(self.NUMBEROFPARAMETERS):
                print(self.__entryArr[i]["state"])
                if self.__entryArr[i]["state"] == "readonly":
                    text = {self.PARAMLABELS[i]: self.__entryArr[i].get()}
                    alt.writeText(text)
                    print(text)
            alt1 = FileIO("Usernamemode")
            f = alt1.readText()
            if not f:
                alt1.writeText("")
                f = ""
            alt1.writeText({self.__username: self.__currentMode})
            print(self.__entryArr[0].get())
            print(self.__entryArr[10].get())
            print(self.__entryArr[1].get())
            Data_stack.append((self.MODELABELS.index(self.__currentMode)).to_bytes(1, byteorder='little')) #mod selection 
        for i in range(self.NUMBEROFPARAMETERS):
            try:
                if self.TYPELIST[i] == "1": #sram detection
                    Data_stack.append(int(self.__entryArr[i].get()).to_bytes(1, byteorder='little'))
                elif self.TYPELIST[i] == "f":
                    temparr = (bytearray(struct.pack('f', float(self.__entryArr[i].get()))))
                    for item in temparr:
                        val = int(item)
                        Data_stack.append(val.to_bytes(1, byteorder='little'))
                else:
                    val = int(self.__entryArr[i].get()).to_bytes(2, byteorder='little')
                    Data_stack.append(val)

            except ValueError:
                if str(self.__entryArr[i].get()) in self.ACTIVITYTHRESHOLD:
                    val = self.ACTIVITYTHRESHOLDDICT[str(self.__entryArr[i].get())]
                    temparr = bytearray(struct.pack('f', val))
                    for item in temparr:
                        val = int(item)
                        Data_stack.append(val.to_bytes(1, byteorder='little'))
                else:
                    if self.TYPELIST[i] == "1": #register
                        Data_stack.append(b'\x00')
                    elif self.TYPELIST[i] == "f":
                        Data_stack.append(b'\x00')
                        Data_stack.append(b'\x00')
                        Data_stack.append(b'\x00')
                        Data_stack.append(b'\x00')
                    else:
                        Data_stack.append(b'\x00')
                        Data_stack.append(b'\x00')

                if self.__entryArr[i]["state"] == "readonly":
                    text = {self.PARAMLABELS[i]: self.__entryArr[i].get()}
                    alt.writeText(text)

        print(Data_stack)

        val = b'\x16\x55'
        for item in Data_stack:
            val = val + item
        print(self.__currentPort)
        t1_sc = threading.Thread(target=self.serialCommWrite, args=(val,))
        t1_sc.start()

    def serialCommWrite(self, val):
        global write
        print(type(val))
        sc.serialWrite(val)
        print(val)
        write = False

    def resetMode(self):
        alt = FileIO("Usernamemode")
        data = alt.readText()
        if not (data):
            alt.writeText("")
            data = ""
        if (len(data) == 0):
            self.__modeList.set("VOO")

        elif self.__username not in data:
            self.__modeList.set("VOO")
            for item in self.__entryArr:
                item.set("")
        else:
            self.__modeList.set(data[self.__username])
            alt = FileIO(self.__username + data[self.__username] + self.PARAMETERFILE)
            f = alt.readText()
            for item in self.__entryArr:
                item.set("")
            for i in range(16):
                if list(f.values())[i] == "":
                    self.__entryArr[i].config(state="disabled")
                else:
                    self.__entryArr[i].config(state="readonly")
                    self.__entryArr[i].set(list(f.values())[i])

    def __checkPort(self):
        messagebox.showinfo("Success:Valid Connection","Connected!")
        self.__currentPort = self.__comMode.get()
        sc.setPort(self.__currentPort)
        t2_sc = threading.Thread(target=self.__runPort)
        t2_sc.daemon = True
        t2_sc.start()

    def __runPort(self):
        self.__comMode["values"] = SerialComm().getSerialPorts()

    def logout(self):
        self.__mainWindow.logout()

    def setUsername(self, username):
        self.__usernameLabel.config(text="User: " + username)
        self.__username = username

    def __initalizeParameterList(self, higherFrame):
        # for i in range(0, self.NUMBEROFPARAMETERS, 4):
        for i in range(0, self.NUMBEROFPARAMETERS, 4):
            for j in range(4):
                label = Label(higherFrame, text=self.PARAMLABELS[4], bg=self.BACKGROUND_COLOR)
                entry = ttk.Combobox(higherFrame, values=self.PROGRAMABLEPARAMETERS[i + j], state="disabled")
                self.__labelArr.append(label)
                label.grid(row=i, column=j, padx=60, pady=2)
                self.__entryArr.append(entry)
                entry.grid(row=i + 1, column=j, padx=60, pady=2)
                self.__buttonArr.append(entry)

    def __initalizeConstants(self):
        for i in range(40):
            self.LRL.append(51 + i)
        for i in range(17):
            self.LRL.append(95 + 5 * i)

        for i in range(26):
            self.URL.append(50 + i * 5)
            self.MSR.append(50 + i * 5)

        for i in range(50):
            self.ATRAMP.append(round(0.1 + 0.1 * i, 1))
            self.VENTAMP.append(round(0.1 + 0.1 * i, 1))
            self.ASENSE.append(round(0.1 + 0.1 * i, 1))
            self.VSENSE.append(round(0.1 + 0.1 * i, 1))
        for i in range(30):
            self.ATRWIDTH.append(1 + i)
            self.VENTWIDTH.append(1 + i)
        for i in range(36):
            self.ATRREFRAC.append(150 + 10 * i)
            self.VENTREFRAC.append(150 + 10 * i)
        for i in range(2, 17, 1):
            self.RECOVERYTIME.append(i)
        for i in range(10, 51, 10):
            self.REACTIONTIME.append(i)
        for i in range(1, 17):
            self.RESPONSEFACTOR.append(i)
        for i in range(70, 301, 10):
            self.AVDELAY.append(i)


class ContentWindow(tk.Frame):
    __loginWindow = None
    __parent = None
    __DCM = None

    username = ""

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.__parent = parent
        parent.title("DCM")
        parent.geometry("1200x700")
        parent.resizable(True, True)
        parent.config(bg="LightBlue")
        self.__loginWindow = LoginWindow(self)
        self.__DCM = DCMWindow(self, self.username)
        self.__loginWindow.pack()

    def login(self):
        self.__loginWindow.pack_forget()
        self.username = self.__loginWindow.getUsername()
        self.__DCM.setUsername(self.username)
        self.__DCM.resetMode()
        self.__DCM.pack()

# Main script
if __name__ == "__main__":
    run = Run()
