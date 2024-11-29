import tkinter as tk
from tkinter import ttk, messagebox
import pickle
import serial
import struct
from ParameterManager import ParameterManager


class ApplicationWindow:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Pacing Mode Selection")
        self.root.geometry("1000x700")

        # 用户相关信息和参数管理
        self.username = username
        self.parameter_manager = ParameterManager()
        self.user_parameters = self.load_user_parameters()

        # 串口对象初始化
        self.serial_port = None

        # 布局创建
        self.create_header()
        self.create_mode_selection()
        self.create_parameter_fields()
        self.create_buttons()
        self.create_status_display()

    def create_header(self):
        """创建头部区域，显示用户名和退出按钮。"""
        header_frame = tk.Frame(self.root)
        header_frame.pack(pady=10, fill=tk.X)

        user_label = tk.Label(header_frame, text=f"Logged in as: {self.username}", font=("Arial", 12))
        user_label.pack(side=tk.LEFT, padx=10)

        exit_button = tk.Button(header_frame, text="Exit", command=self.root.quit)
        exit_button.pack(side=tk.RIGHT, padx=10)

    def create_mode_selection(self):
        """创建下拉菜单以选择起搏模式。"""
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(pady=10)

        mode_label = tk.Label(mode_frame, text="Select Pacing Mode:", font=("Arial", 12))
        mode_label.pack(side=tk.LEFT, padx=10)

        self.pacing_mode_var = tk.StringVar(value="None")
        self.pacing_mode_dropdown = ttk.Combobox(mode_frame, textvariable=self.pacing_mode_var)
        self.pacing_mode_dropdown["values"] = [
            "None", "AOO", "VOO", "AAI", "VVI", "AOOR", "AAIR", "VOOR", "VVIR", "DDD", "DDDR"
        ]
        self.pacing_mode_dropdown.pack(side=tk.LEFT, padx=10)
        self.pacing_mode_dropdown.bind("<<ComboboxSelected>>", self.update_parameters)

    def create_parameter_fields(self):
        """创建参数输入字段。"""
        self.fields = {}
        param_frame = tk.Frame(self.root)
        param_frame.pack(pady=20)

        field_names = [
            "Lower Rate Limit", "Upper Rate Limit", "Atrial Amplitude", "Atrial Pulse Width",
            "Ventricular Amplitude", "Ventricular Pulse Width", "VRP", "ARP", "PVARP",
            "Maximum Sensor Rate", "Fixed AV Delay", "Ventricular Sensitivity",
            "Hysteresis", "Rate Smoothing", "Activity Threshold", "Reaction Time",
            "Response Factor", "Recovery Time"
        ]

        for i, field_name in enumerate(field_names):
            label = tk.Label(param_frame, text=f"{field_name}:", font=("Arial", 10))
            entry = tk.Entry(param_frame, font=("Arial", 10))
            label.grid(row=i, column=0, sticky=tk.E, padx=10, pady=5)
            entry.grid(row=i, column=1, sticky=tk.W, padx=10, pady=5)
            self.fields[field_name] = entry

    def create_buttons(self):
        """创建“应用”和“发送数据”按钮。"""
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        apply_button = tk.Button(button_frame, text="Apply", command=self.apply_parameters)
        apply_button.pack(side=tk.LEFT, padx=20)

        send_button = tk.Button(button_frame, text="Send Data", command=self.send_parameters)
        send_button.pack(side=tk.LEFT, padx=20)

    def create_status_display(self):
        """创建连接状态显示区域。"""
        self.status_label = tk.Label(self.root, text="Device not connected", font=("Arial", 12), fg="red")
        self.status_label.pack(pady=10)

        connect_button = tk.Button(self.root, text="Connect", command=self.connect_to_device)
        connect_button.pack(pady=5)

    def connect_to_device(self):
        """尝试连接到 pacemaker 设备并更新连接状态。"""
        try:
            self.serial_port = serial.Serial(port="COM3", baudrate=115200, timeout=1)
            self.status_label.config(text="Device connected", fg="green")
        except serial.SerialException:
            self.status_label.config(text="Device not connected", fg="red")

    def send_parameters(self):
        """将参数打包并通过串口发送。"""
        if not self.serial_port:
            messagebox.showerror("Error", "Device not connected")
            return

        try:
            header = struct.pack('<2B', 0x16, 0x55)  # 示例头部
            data_format = '<4B2f2B2f3Hf2B1H'  # 示例数据格式
            data = struct.pack(
                data_format,
                int(self.fields["Lower Rate Limit"].get()),
                int(self.fields["Upper Rate Limit"].get()),
                float(self.fields["Atrial Amplitude"].get()),
                float(self.fields["Ventricular Amplitude"].get()),
                # 添加更多参数
            )
            self.serial_port.write(header + data)
            messagebox.showinfo("Success", "Parameters sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send parameters: {str(e)}")

    def apply_parameters(self):
        """应用参数并验证输入的有效性。"""
        try:
            for field_name, entry in self.fields.items():
                value = entry.get()
                if value:
                    setattr(self.parameter_manager, f"set{field_name.replace(' ', '')}", value)
            messagebox.showinfo("Success", "Parameters applied successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_parameters(self, event=None):
        """更新可见的参数字段。"""
        mode = self.pacing_mode_var.get()
        relevant_fields = self.get_relevant_parameters_for_mode(mode)
        for field_name, entry in self.fields.items():
            entry.config(state=tk.NORMAL if field_name in relevant_fields else tk.DISABLED)

    def get_relevant_parameters_for_mode(self, mode):
        """根据模式获取相关参数字段。"""
        relevant_params = {
            "AOO": ["Lower Rate Limit", "Upper Rate Limit", "Atrial Amplitude", "Atrial Pulse Width"],
            "AAI": ["Lower Rate Limit", "Upper Rate Limit", "Atrial Amplitude", "Atrial Pulse Width", "ARP"],
            # 添加更多模式及其相关参数
        }
        return relevant_params.get(mode, [])

    def load_user_parameters(self):
        """加载用户参数。"""
        try:
            with open("users.dat", "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return {}

    def save_user_parameters(self):
        """保存用户参数。"""
        self.user_parameters[self.username] = self.parameter_manager
        with open("users.dat", "wb") as file:
            pickle.dump(self.user_parameters, file)


if __name__ == "__main__":
    root = tk.Tk()
    app = ApplicationWindow(root, username="test_user")
    root.mainloop()
