import serial
import struct
import time
from tkinter import messagebox
from serial.tools import list_ports  # 用于列出可用的串口

class SerialManager:
    def __init__(self, port="COM3", baudrate=115200, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_port = None

    def list_available_ports(self):
        """列出所有可用的串口"""
        ports = list_ports.comports()  # 获取所有可用串口
        available_ports = [port.device for port in ports]
        return available_ports

    def connect(self):
        """连接到串口设备"""
        try:
            self.serial_port = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            if self.serial_port.is_open:
                return True
        except serial.SerialException as e:
            print(f"无法连接到 {self.port}: {e}")
            return False

    def disconnect(self):
        """断开串口连接"""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()

    def is_connected(self):
        """检查串口是否连接"""
        return self.serial_port and self.serial_port.is_open

    def send_data(self, data):
        """发送数据到串口设备"""
        if self.is_connected():
            try:
                self.serial_port.write(data)
                return True
            except Exception as e:
                print(f"发送数据时出错: {e}")
                return False
        else:
            print("设备未连接")
            return False

    def build_data_packet(self, field_values):
        """根据字段值构建数据包"""
        try:
            header = struct.pack(0x16, 0x55)  # 示例头部
            data_format = '<4B2f2B2f3Hf2B1H'  # 示例数据格式
            data = struct.pack(
                data_format,
                int(field_values["Lower Rate Limit"]),
                int(field_values["Upper Rate Limit"]),
                float(field_values["Atrial Amplitude"]),
                float(field_values["Ventricular Amplitude"]),
                # 其他字段
            )
            return header + data
        except Exception as e:
            print(f"构建数据包时出错: {e}")
            return None
