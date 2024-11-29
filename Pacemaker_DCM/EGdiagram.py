import time
import threading
import struct
import tkinter as tk
from tkinter import Canvas
import serial  # 需要安装 pyserial 库：pip install pyserial

class ECGRenderer(threading.Thread):
    def __init__(self, canvas, serial_port):
        super().__init__()
        self.canvas = canvas  # 用来绘制心电图的 Canvas
        self.serial_port = serial_port  # 串口对象
        self.running = True  # 线程运行标志
        self.voltageA = []  # 存储 ECG A 电压数据
        self.talist = []  # 存储时间戳
        self.voltageV = []  # 存储额外电压数据
        self.tvlist = []  # 存储额外电压数据的时间戳

    def run(self):
        """
        主线程函数：读取串口数据，并实时更新心电图。
        """
        t = time.time()  # 获取初始时间戳
        lasttime = t  # 上次更新时间戳

        if not self.serial_port.is_open:
            print("Error:串口未打开!")
            return  # 如果串口未打开，直接退出线程

        while self.running:
            if self.serial_port.is_open:
                # 向串口发送请求数据的命令
                self.serial_port.write(b'\x15\x00\x22')
                time.sleep(0.1)  # 延时，确保数据准备好

                try:
                    # 读取串口数据，假设一次读取16个字节
                    temp = self.serial_port.read(16)

                    try:
                        # 解包前8个字节获取电压 A
                        val, = struct.unpack('d', temp[0:8])
                        if 0.4 < val < 3.5:  # 如果数据在有效范围内
                            self.voltageA.append(val * 3.3)  # 转换为电压值
                            self.talist.append(time.time() - t)  # 记录时间戳
                    except Exception:
                        self.voltageA.append(0.5 * 3.3)  # 解包失败时使用默认值
                        self.talist.append(time.time() - t)

                    try:
                        # 解包后8个字节获取电压 V
                        val, = struct.unpack('d', temp[8:16])
                        if 0.4 < val < 5.0:  # 如果数据在有效范围内
                            self.voltageV.append(val * 3.3)  # 转换为电压值
                            self.tvlist.append(time.time() - t)  # 记录时间戳
                    except Exception:
                        self.voltageV.append(0.5 * 3.3)  # 解包失败时使用默认值
                        self.tvlist.append(time.time() - t)

                    # 限制电压数据的长度，超过350个数据点则移除最旧的
                    if len(self.voltageA) > 350:
                        self.voltageA.pop(0)
                        self.talist.pop(0)

                    if len(self.voltageV) > 450:
                        self.voltageV.pop(0)
                        self.tvlist.pop(0)

                    # 每0.025秒更新一次图表
                    if time.time() - lasttime > 0.025:
                        lasttime = time.time()
                        self.update_plot()

                except Exception as e:
                    print(f"串口读取错误: {e}")
                    break  # 如果读取串口时出现问题，退出循环

    def update_plot(self):
        """
        更新心电图的绘制
        """
        self.canvas.delete("all")  # 清空画布

        # 确保数据不为空，否则设置默认值
        if not self.talist or not self.tvlist or not self.voltageA or not self.voltageV:
            return  # 如果没有数据，则不进行绘制

        max_x = max(max(self.talist, default=1), max(self.tvlist, default=1))  # 获取最大X轴值
        max_y = max(max(self.voltageA, default=0), max(self.voltageV, default=0))  # 获取最大Y轴值

        # 避免除零错误，给 max_y 和 max_x 设置最小值
        if max_x == 0:
            max_x = 1
        if max_y == 0:
            max_y = 1

        # 将数据缩放到画布的大小
        scale_x = self.canvas.winfo_width() / max_x
        scale_y = self.canvas.winfo_height() / max_y

        # 绘制电压 A 的心电图，红色线条
        for i in range(1, len(self.talist)):
            self.canvas.create_line(
                self.talist[i - 1] * scale_x, self.voltageA[i - 1] * scale_y,
                self.talist[i] * scale_x, self.voltageA[i] * scale_y,
                fill="red", width=2
            )

        # 绘制电压 V 的数据，绿色线条
        for i in range(1, len(self.tvlist)):
            self.canvas.create_line(
                self.tvlist[i - 1] * scale_x, self.voltageV[i - 1] * scale_y,
                self.tvlist[i] * scale_x, self.voltageV[i] * scale_y,
                fill="green", width=2
            )

        # 更新画布显示
        self.canvas.update()

    def stop(self):
        """
        停止 ECG 渲染线程
        """
        self.running = False


class ECGApp:
    def __init__(self, root, serial_port):
        self.root = root  # Tkinter 主窗口
        self.serial_port = serial_port  # 串口对象

        # 创建一个 Canvas 用于绘制心电图
        self.canvas = Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()

        # 初始化 ECGRenderer 线程
        self.renderer = ECGRenderer(self.canvas, self.serial_port)
        self.renderer.start()

    def stop(self):
        """
        停止 ECG 渲染线程
        """
        self.renderer.stop()


# 初始化 Tkinter 窗口
root = tk.Tk()
root.title("心电图监控")

# 初始化串口通信（请根据实际串口端口进行修改）
serial_port = serial.Serial('COM3', 9600, timeout=1)  # 将 'COM3' 替换为你的串口端口

# 检查串口是否成功打开
if not serial_port.is_open:
    print("Error: 串口无法打开!")
else:
    # 初始化 ECG 应用
    app = ECGApp(root, serial_port)

    # 启动 Tkinter 主循环
    root.mainloop()

# 程序结束后关闭串口
serial_port.close()
