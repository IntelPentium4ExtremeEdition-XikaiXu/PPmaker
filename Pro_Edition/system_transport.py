import time
import serial
import struct

class SerialConnection:

    def __init__(self, com_port, params):
        self.ser_port = com_port
        self.ser = None
        self.connected = False
        self.status = 0  # 0 = disconnected, 1 = connected
        self.params = params

    def check_connection(self):
        try:
            # 尝试连接并发送 1 byte 数据 10
            self.ser = serial.Serial(port=self.ser_port, baudrate=115200, timeout=1)
            if self.ser.is_open:
                # 发送一个 1 字节数据 10
                self.ser.write(b'\x10')  # 发送 1 字节数据 0x10
                self.connected = True
                self.status = 1
                print("\nConnected and sent data: 10")
            else:
                self.connected = False
                self.status = 0
                print("\nNot Connected")
        except serial.SerialException as e:
            self.connected = False
            self.status = 0
            print(f"Connection failed: {e}")

    def get_connection_status(self):
        return self.status

    def _pack_data(self, data):
        data_binary = b''
        for p in data:
            data_binary += struct.pack('<B', p)  # Little-endian format
        return data_binary

    def receive_data(self):
        print("Receiving data.")
        if self.ser and self.ser.is_open:
            data = self.ser.read(100)
            print(f"Received data: {data}")
            return data
        else:
            print("Error: Serial connection not open.")
            return None

    def close_connection(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("\nConnection closed.")

    def send_and_wait_for_response(self, data, chunk_size=10, timeout=5):
        """
        发送数据并等待串口返回非零数据。
        
        :param data: 要发送的数组
        :param chunk_size: 每次发送的数据块大小
        :param timeout: 等待串口响应的最大时间（秒）
        :return: 返回接收到的数据
        """
        if not self.ser or not self.ser.is_open:
            print("Error: Serial connection is not open.")
            return None

        # 将数据切割成块并发送
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i+chunk_size]
            packed_data = self._pack_data(chunk)
            print(f"Sending chunk: {chunk}")
            self.ser.write(packed_data)

            # 等待响应
            start_time = time.time()
            while time.time() - start_time < timeout:
                received_data = self.receive_data()
                if received_data and received_data != b'\x00':  # 如果收到非零数据
                    print(f"Received valid data: {received_data}")
                    return received_data

            print(f"Timeout reached while waiting for response for chunk: {chunk}")
        return None
