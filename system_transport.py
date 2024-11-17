import serial
import struct
import param


class SerialConnection:
    """
    Handles serial communication with the Pacemaker device via UART.
    """
    def __init__(self, com_port, params):
        """
        Initializes the connection class.

        :param com_port: The communication port (e.g., COM3 for Windows).
        :param params: The parameter object that contains the pacemaker settings.
        """
        self.ser_port = com_port
        self.ser = None
        self.connected = False
        self.status = 0  # 0 = disconnected, 1 = connected
        self.params = params

    def check_connection(self):
        """
        Establishes a serial connection to the Pacemaker device.

        :return: None
        """
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
        """
        Gets the connection status.

        :return: 1 if connected, 0 if disconnected.
        """
        return self.status

    def _pack_data(self, data):
        """
        Helper function to pack data into binary format for transmission.

        :param data: A list of parameters to be packed.
        :return: Packed binary data.
        """
        data_binary = b''
        for p in data:
            data_binary += struct.pack('<B', p)  # Little-endian format
        return data_binary

    def send_data(self, mode):
        """
        Sends the appropriate mode data to the Pacemaker device.

        :param mode: The mode of the pacemaker (e.g., AOO, VOO, AAI, etc.).
        :return: None
        """
        if mode == 'AOO':
            data = [self.params.get_state(), self.params.get_LowerRateLimit(), self.params.get_UpperRateLimit(),
                    self.params.get_AtrialAmplitude(), self.params.get_AtrialPulseWidth()]
        elif mode == 'VOO':
            data = [self.params.get_state(), self.params.get_LowerRateLimit(), self.params.get_UpperRateLimit(),
                    self.params.get_VentricularAmplitude(), self.params.get_VentricularPulseWidth()]
        elif mode == 'AAI':
            data = [self.params.get_state(), self.params.get_LowerRateLimit(), self.params.get_UpperRateLimit(),
                    self.params.get_AtrialAmplitude(), self.params.get_AtrialPulseWidth(), self.params.get_ARP()]
        elif mode == 'VVI':
            data = [self.params.get_state(), self.params.get_LowerRateLimit(), self.params.get_UpperRateLimit(),
                    self.params.get_VentricularAmplitude(), self.params.get_VentricularPulseWidth(), self.params.get_VRP()]
        elif mode == 'AOOR':
            data = [self.params.get_state(), self.params.get_LowerRateLimit(), self.params.get_UpperRateLimit(),
                    self.params.get_AtrialAmplitude(), self.params.get_AtrialPulseWidth(), self.params.get_MaxSensorRate(),
                    self.params.get_ActivityThreshold(), self.params.get_ReactionTime(), self.params.get_ResponseFactor(),
                    self.params.get_RecoveryTime()]
        elif mode == 'VVOO':
            data = [self.params.get_state(), self.params.get_LowerRateLimit(), self.params.get_UpperRateLimit(),
                    self.params.get_VentricularAmplitude(), self.params.get_VentricularPulseWidth(), self.params.get_MaxSensorRate(),
                    self.params.get_ActivityThreshold(), self.params.get_ReactionTime(), self.params.get_ResponseFactor(),
                    self.params.get_RecoveryTime()]
        else:
            raise ValueError("Unknown mode")
        
        # Pack data and send via UART
        packed_data = self._pack_data(data)
        print(f"Sending data for {mode}: {packed_data}")
        if self.ser and self.ser.is_open:
            self.ser.write(packed_data)
        else:
            print("Error: Serial connection not open.")

    def receive_data(self):
        """
        Receives data from the Pacemaker device.

        :return: None
        """
        print("Receiving data...")
        # Example implementation for receiving data:
        if self.ser and self.ser.is_open:
            data = self.ser.read(100)  # Adjust the number of bytes to read as necessary
            print(f"Received data: {data}")
        else:
            print("Error: Serial connection not open.")

    def close_connection(self):
        """
        Closes the serial connection if open.

        :return: None
        """
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("\nConnection closed.")

