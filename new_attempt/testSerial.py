import serial
import struct

# Define the data to be sent
SYNC = 0x16
FN_CODE = 0x55  # or 0x22 depending on the function
RED_ENABLE = 1  # example value
GREEN_ENABLE = 0  # example value
BLUE_ENABLE = 0  # example value
OFF_TIME = struct.pack('f', 0.2)  # example value, 4 bytes
SWITCH_TIME = struct.pack('H', 100)  # example value, 2 bytes

# Combine all parts into a single byte array
data = struct.pack('B B B B B 4s 2s', SYNC, FN_CODE, RED_ENABLE, GREEN_ENABLE, BLUE_ENABLE, OFF_TIME, SWITCH_TIME)

# Open the serial port
s = serial.Serial(
    port='COM5',  # Change to open serial port
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# Write the data to the serial port
s.write(data)

# Close the serial connection
s.close()
