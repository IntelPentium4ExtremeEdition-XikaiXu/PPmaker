import tkinter as tk
from tkinter import ttk, messagebox
from serial_controller import SerialManager  # 导入新创建的 SerialManager 类
from ParameterManager import ParameterManager
import pickle  # 用于保存和加载用户参数
from serial_controller import SerialManager

class ApplicationWindow:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Pacing Mode Selection")
        self.root.geometry("900x700")

        self.username = username  # 当前登录的用户名
        self.parameter_manager = ParameterManager()  # 参数管理实例
        self.user_parameters = self.load_user_parameters()  # 加载用户参数

        self.serial_manager = SerialManager()  # 创建 SerialManager 实例

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

        # 字段名称列表
        field_names = [
            "Lower Rate Limit", "Upper Rate Limit", "Atrial Amplitude", "Atrial Pulse Width",
            "Ventricular Amplitude", "Ventricular Pulse Width", "VRP", "ARP", "PVARP",
            "Maximum Sensor Rate", "Fixed AV Delay", "Ventricular Sensitivity",
            "Hysteresis", "Rate Smoothing", "Activity Threshold", "Reaction Time",
            "Response Factor", "Recovery Time"
        ]

        # 每排字段数量
        fields_per_column = (len(field_names) + 1) // 2

        for i, field_name in enumerate(field_names):
            column = i // fields_per_column  # 根据索引计算列号
            row = i % fields_per_column  # 根据索引计算行号

            label = tk.Label(param_frame, text=f"{field_name}:", font=("Arial", 10))
            entry = tk.Entry(param_frame, font=("Arial", 10))

            label.grid(row=row, column=column * 2, sticky=tk.E, padx=10, pady=5)  # label 在偶数列
            entry.grid(row=row, column=column * 2 + 1, sticky=tk.W, padx=10, pady=5)  # entry 在奇数列

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
        """创建连接状态显示区域，并添加串口选择下拉菜单。"""
        status_frame = tk.Frame(self.root)
        status_frame.pack(pady=10)

        # 状态显示标签
        self.status_label = tk.Label(status_frame, text="Device not connected", font=("Arial", 12), fg="red")
        self.status_label.pack(side=tk.LEFT, padx=10)

        # 串口选择下拉菜单
        self.com_var = tk.StringVar()
        self.com_dropdown = ttk.Combobox(status_frame, textvariable=self.com_var, state="readonly")
        self.refresh_com_ports()  # 初始化下拉菜单内容
        self.com_dropdown.pack(side=tk.LEFT, padx=10)

        # 刷新串口按钮
        refresh_button = tk.Button(status_frame, text="Refresh Ports", command=self.refresh_com_ports)
        refresh_button.pack(side=tk.LEFT, padx=10)

        # 连接按钮
        connect_button = tk.Button(status_frame, text="Connect", command=self.connect_to_device)
        connect_button.pack(side=tk.LEFT, padx=10)

    def refresh_com_ports(self):
        """刷新串口列表并更新到下拉菜单。"""
        ports = self.serial_manager.list_available_ports()
        if ports:
            self.com_dropdown['values'] = ports
            self.com_dropdown.current(0)  # 默认选择第一个串口
        else:
            self.com_dropdown['values'] = ["No COM Ports Available"]
            self.com_dropdown.current(0)

    def connect_to_device(self):
        """尝试连接到选定的串口设备并更新连接状态。"""
        selected_port = self.com_var.get()
        if selected_port and selected_port != "No COM Ports Available":
            self.serial_manager.port = selected_port  # 更新 SerialManager 的端口
            if self.serial_manager.connect():
                self.status_label.config(text=f"Connected to {selected_port}", fg="green")
            else:
                self.status_label.config(text=f"Failed to connect to {selected_port}", fg="red")
        else:
            messagebox.showerror("Error", "No valid COM port selected")

    def send_parameters(self):
        """将参数打包并通过串口发送。"""
        field_values = {  # 从输入框中获取字段值
            "Lower Rate Limit": self.fields["Lower Rate Limit"].get(),
            "Upper Rate Limit": self.fields["Upper Rate Limit"].get(),
            "Atrial Amplitude": self.fields["Atrial Amplitude"].get(),
            "Ventricular Amplitude": self.fields["Ventricular Amplitude"].get(),
            # 添加更多字段
        }

        if not self.serial_manager.is_connected():
            messagebox.showerror("Error", "Device not connected")
            return

        # 构建数据包并发送
        data_packet = self.serial_manager.build_data_packet(field_values)
        if data_packet:
            if self.serial_manager.send_data(data_packet):
                messagebox.showinfo("Success", "Parameters sent successfully!")
            else:
                messagebox.showerror("Error", "Failed to send parameters.")
        else:
            messagebox.showerror("Error", "Failed to build data packet.")

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
