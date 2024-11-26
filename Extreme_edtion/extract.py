import serial
import struct
import time

class PacemakerDCM:
    def __init__(self, port, baud_rate=115200):
        self.serial_conn = serial.Serial(port, baud_rate, timeout=1)
        self.parameters = {
            "pulse_amplitude": 5.0,  # 默认 5.0V
            "pulse_width": 1,       # 默认 1 ms
            "sensitivity": 2.5      # 默认灵敏度 2.5V
        }

    def set_parameter(self, param_name, value):
        if param_name not in self.parameters:
            raise ValueError(f"Invalid parameter: {param_name}")
        self.parameters[param_name] = value

    def send_parameters(self):

        frame = struct.pack(
            ">fIf",
            self.parameters["pulse_amplitude"],
            self.parameters["pulse_width"],
            self.parameters["sensitivity"]
        )
        self.serial_conn.write(frame)
        print("Parameters sent:", self.parameters)

    def verify_parameters(self):

        self.serial_conn.write(b'READ_PARAMS')
        response = self.serial_conn.read(12)  # 每个参数4字节
        if len(response) == 12:
            amp, width, sens = struct.unpack(">fIf", response)
            verification = (
                amp == self.parameters["pulse_amplitude"] and
                width == self.parameters["pulse_width"] and
                sens == self.parameters["sensitivity"]
            )
            if verification:
                print("Parameters verified successfully.")
            else:
                print("Parameter mismatch:", {"amp": amp, "width": width, "sens": sens})
        else:
            print("Failed to receive parameter data.")

    def receive_egram(self):

        self.serial_conn.write(b'REQUEST_EGRAM')
        egram_data = self.serial_conn.read(1024)  # 假设最多接收1024字节
        if egram_data:
            print("Received egram data:", egram_data.hex())
        else:
            print("No egram data received.")

    def interactive_mode(self):

        print("Interactive Mode: Enter commands")
        print("1: Set Parameters")
        print("2: Send Parameters")
        print("3: Verify Parameters")
        print("4: Receive egram")
        print("q: Quit")
        while True:
            command = input("Enter command: ").strip()
            if command == '1':
                try:
                    amp = float(input("Pulse Amplitude (0.1-5.0V): "))
                    width = int(input("Pulse Width (1-30ms): "))
                    sens = float(input("Sensitivity (0-5V): "))
                    self.set_parameter("pulse_amplitude", amp)
                    self.set_parameter("pulse_width", width)
                    self.set_parameter("sensitivity", sens)
                except ValueError as e:
                    print("Invalid input:", e)
            elif command == '2':
                self.send_parameters()
            elif command == '3':
                self.verify_parameters()
            elif command == '4':
                self.receive_egram()
            elif command.lower() == 'q':
                print("Exiting Interactive Mode.")
                break
            else:
                print("Invalid command.")

if __name__ == "__main__": 
    try:
        pacemaker_dcm = PacemakerDCM(port="COM3")  
        pacemaker_dcm.interactive_mode()
    except serial.SerialException as e:
        print("Serial connection error:", e)
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")

