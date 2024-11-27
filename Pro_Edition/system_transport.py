import json
import os
import serial

class FileIO:
    """用于存储、写入和读取文件的类
    """
    # 变量声明
    # 常量
    # 私有变量
    __fileName = ""

    def __init__(self, fileName):
        """构造函数

        参数:
            fileName (string): 要存储的文件名
        """
        self.__fileName = fileName

    def writeText(self, text):
        """首先检查文件是否存在，如果不存在则创建一个。
        将字典写入指定的json文件。

        参数:
            text (dictionary): 要写入的字典
        """
        if os.path.isfile(self.__fileName):
            with open(self.__fileName, "r") as f:
                data = self.readText()
                if not data:
                    data = text
                try:
                    data.update(text)
                except Exception:
                    pass
            with open(self.__fileName, "w") as f:
                f.write(json.dumps(data))
        else:
            with open(self.__fileName, "w") as f:
                f.write(json.dumps(text))

    def readText(self):
        """读取json文件并将数据以字典格式返回

        返回:
            [dictionary]: 返回字典格式的数据
        """
        try:
            with open(self.__fileName, "r") as f:
                data = json.load(f)
            return data
        except:
            return None

    # 获取函数
    def getFileName(self):
        """获取当前文件名

        返回:
            [string]: 返回文件名
        """
        return self.__fileName

    def getlength(self):
        """获取字典的长度

        返回:
            [int]: 字典的长度
        """
        data = self.readText()
        return len(data)


class SerialComm:
    __port = None
    __baudrate = 0
    __bytesize = 0
    __parity = serial.PARITY_ODD
    __stopbits = 0
    __timeout = 1
    __xonxoff = 0
    __rtscts = 0
    """构造函数
    """

    def __init__(self):
        super().__init__()
        self.__baudrate = 115200
        self.__bytesize = 8
        self.__parity = serial.PARITY_ODD
        self.__stopbits = serial.STOPBITS_ONE
        self.__timeout = 0
        self.__xonxoff = 0
        self.__rtscts = 0
        self.__ser = serial.Serial(self.__port, self.__baudrate, self.__bytesize, self.__parity, self.__stopbits,
                                   self.__timeout,
                                   self.__xonxoff, self.__rtscts)

    """ 设置当前用于串口通信的端口
    """

    def setPort(self, port):
        if (port[0:3] == "COM"):
            self.__port = port
            self.__ser = serial.Serial(self.__port, self.__baudrate, self.__bytesize, self.__parity, self.__stopbits,
                                       self.__timeout,
                                       self.__xonxoff, self.__rtscts)

    """ 返回所有可用的串口列表
    """

    def getSerialPorts(self):
        ports = []
        result = []
        for i in range(16):
            ports.append('COM' + str(i))
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    """ 尝试向串口通信端口写入数据
    """

    def serialWrite(self, data):
        try:
            try:
                if (type(data) == str):
                    self.__ser.write(data.encode())  # 如果数据是字符串，则编码为字节并写入
                else:
                    self.__ser.write(data)  # 如果数据是字节，则直接写入
            except Exception:
                self.__ser.close()  # 出现异常时关闭串口连接
        except Exception:
            pass

    """ 返回给定字节串的校验位
    """

    def getParityBit(self, data):
        val = []
        if (type(data) == bytes):
            val = "{:0x0A}".format(int(data.hex(), 16))  # 将字节数据转换为十六进制字符串
        else:
            return b'\x00'  # 如果数据不是字节类型，返回默认的校验位
        sum = 0
        for item in val:
            if (item == '1'):
                sum += 1  # 统计字节中 '1' 的个数
        if (sum % 2 == 0):
            return b'\x01'  # 如果 '1' 的个数是偶数，返回校验位 1
        return b'\x00'  # 如果 '1' 的个数是奇数，返回校验位 0

    """ 返回当前存储的串口端口值
    """

    def getCurrentPort(self):
        return self.__port

    """ 尝试从串口通信端口读取数据
    """

    def serialRead(self):
        try:
            val = self.__ser.read(16)  # 读取16个字节的数据
            return val
        except Exception:
            return None  # 如果读取失败，返回 None
