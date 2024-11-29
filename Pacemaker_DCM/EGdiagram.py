import time

# 线程函数，用于在DCM窗口上绘制ECG图
class rander:
    def __init__(self):
        self.__displayGraph
        self.__annotations__
        
    def __displayGraph(self):
        """
        线程函数，用于绘制ECG图
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