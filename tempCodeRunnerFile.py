
from time import sleep
import time
import threading

# Global variables
# sc is the static serial communication variable
sc = SerialComm()
# write is used to detect whether the serial port is reading or writing so it does not interfere with each mode
write = False

#Figures for the ECG
f = Figure(figsize=(8, 6), dpi=160)
a = f.add_subplot(111, ylim=(0, 1))


class Run: