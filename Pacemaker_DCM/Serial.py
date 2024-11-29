import serial
from serial.tools import list_ports
class SerialComm:
    """Class for managing serial communication."""

    def __init__(self):
        """Initialize default settings for serial communication."""
        self.__port = None
        self.__baudrate = 115200
        self.__bytesize = serial.EIGHTBITS
        self.__parity = serial.PARITY_NONE
        self.__stopbits = serial.STOPBITS_ONE
        self.__timeout = 1
        self.__ser = None

    def setPort(self, port):
        """Set the current serial port and configure it."""
        try:
            self.__port = port
            self.__ser = serial.Serial(
                port=self.__port,
                baudrate=self.__baudrate,
                bytesize=self.__bytesize,
                parity=self.__parity,
                stopbits=self.__stopbits,
                timeout=self.__timeout,
            )
            print(f"Connected to {self.__port} at {self.__baudrate} baud.")
        except serial.SerialException as e:
            print(f"Error: Unable to open serial port {self.__port}: {e}")

    def getSerialPorts(self):
        """Return a list of available serial ports."""
        return [port.device for port in list_ports.comports()]

    def serialWrite(self, data):
        """Write data to the serial port."""
        if self.__ser and self.__ser.is_open:
            try:
                if isinstance(data, str):
                    self.__ser.write(data.encode())
                else:
                    self.__ser.write(data)
                print(f"Data written to {self.__port}: {data}")
            except serial.SerialException as e:
                print(f"Error writing to {self.__port}: {e}")
        else:
            print("Error: Serial port is not open.")

    def serialRead(self, num_bytes=16):
        """Read a specified number of bytes from the serial port."""
        if self.__ser and self.__ser.is_open:
            try:
                data = self.__ser.read(num_bytes)
                print(f"Data read from {self.__port}: {data}")
                return data
            except serial.SerialException as e:
                print(f"Error reading from {self.__port}: {e}")
                return None
        else:
            print("Error: Serial port is not open.")
            return None

    def closePort(self):
        """Close the serial port if it is open."""
        if self.__ser and self.__ser.is_open:
            self.__ser.close()
            print(f"Serial port {self.__port} closed.")

    def getCurrentPort(self):
        """Return the current serial port."""
        return self.__port

