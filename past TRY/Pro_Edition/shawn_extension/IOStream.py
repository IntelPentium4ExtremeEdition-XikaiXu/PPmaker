import json
import os
import serial
from serial.tools import list_ports

class FileIO:
    """Class for handling file operations such as reading and writing JSON files."""

    def __init__(self, fileName):
        """Initialize with a file name."""
        self.__fileName = fileName

    def writeText(self, text):
        """Write a dictionary to a JSON file. Create the file if it doesn't exist."""
        data = self.readText() or {}
        data.update(text)
        with open(self.__fileName, "w") as f:
            json.dump(data, f)

    def readText(self):
        """Read and return the contents of a JSON file as a dictionary."""
        if os.path.isfile(self.__fileName):
            try:
                with open(self.__fileName, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error: Could not decode JSON from {self.__fileName}.")
        return None

    def getFileName(self):
        """Return the file name."""
        return self.__fileName

    def getlength(self):
        """Return the number of keys in the JSON file."""
        data = self.readText()
        return len(data) if data else 0


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

