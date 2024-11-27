import serial
import struct

header_byte_1 = 0x16
header_byte_2 = 0x55 #PACEMAKER recive is 55    PACEMAKER send is 22
red_enable = 1
green_enable = 2
blue_enable = 3
off_time = 5.0
switch_time = 120

# < little-endian,
# B 8-bit unsigned int
# f float (4 bytes)
# H 16-bit unsigned int
struct_format = '<2B3BfH'

# Pack the data into a binary format
data_packet = struct.pack(struct_format,
                          header_byte_1,
                          header_byte_2,
                          red_enable,
                          green_enable,
                          blue_enable,
                          off_time,
                          switch_time)

try:
    with serial.Serial(port="COM5", baudrate=115200, timeout=1) as pacemaker:
        # Write
        pacemaker.write(data_packet)
        print(f"Data sent: header_byte_1={header_byte_1}, header_byte_2={header_byte_2}, "
              f"red_enable={red_enable}, green_enable={green_enable}, blue_enable={blue_enable}, "
              f"off_time={off_time}, switch_time={switch_time}")

        # Read
        expected_data_format = '<3BfH' # red green blue off_time switch_time
        expected_data_length = struct.calcsize(expected_data_format) 
        received_data = pacemaker.read(expected_data_length)

        # Unpack
        if len(received_data) == expected_data_length:
            unpacked_data = struct.unpack(expected_data_format, received_data)
            print(f"Data received: red_enable={unpacked_data[0]}, green_enable={unpacked_data[1]}, "
                  f"blue_enable={unpacked_data[2]}, off_time={unpacked_data[3]}, switch_time={unpacked_data[4]}")
        else:
            print("Received data is incomplete or incorrect length.")

except serial.SerialException as e:
    print(f"Error opening or using COM5: {e}")
