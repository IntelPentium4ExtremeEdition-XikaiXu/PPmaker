import serial
import struct
import param
from fileio import ParameterReader

class SerialConnection:

    def __init__(self, com_port, params):
        self.ser_port = com_port
        self.ser = None
        self.connected = False
        self.status = 0  # 0 = disconnected, 1 = connected
        self.params = params

    def check_connection(self):
        try:
            self.ser = serial.Serial(port=self.ser_port, baudrate=115200, timeout=1)
            if self.ser.is_open:
                self.connected = True
                self.status = 1
                print("\nConnected")
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

    def send_data(self, mode):
        if mode == 'AOO':
            data = [ParameterReader.get_aoo_parameters()]
        elif mode == 'VOO':
            data = [ParameterReader.get_voo_parameters()]
        elif mode == 'AAI':
            data = [ParameterReader.get_aai_parameters()]
        elif mode == 'VVI':
            data = [ParameterReader.get_vvi_parameters()]
        else:
            raise ValueError("Unknown mode")
        packed_data = self._pack_data(data)
        print(f"Sending data for {mode}: {packed_data}")
        if self.ser and self.ser.is_open:
            self.ser.write(packed_data)
        else:
            print("Error: Serial connection not open.")
    def receive_data(self):
        print("Receiving dat.")
        if self.ser and self.ser.is_open:
            data = self.ser.read(100)  
            print(f"Received data: {data}")
        else:
            print("Error: Serial connection not open.")

    def close_connection(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("\nConnection closed.")

