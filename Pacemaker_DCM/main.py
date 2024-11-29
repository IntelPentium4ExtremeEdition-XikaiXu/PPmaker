import tkinter as tk
from tkinter import ttk, messagebox
from serial_controller import SerialManager  # 导入新创建的 SerialManager 类
from ParamENUM import ParamEnum
from serial_controller import SerialManager
from file_io import FileIO
import os
class ApplicationWindow:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Pacing Mode Selection")
        self.root.geometry("900x500")

        self.username = username  # 当前登录的用户名
        self.parameter_manager = ParamEnum()  # 参数管理实例
        self.user_parameters = self.load_user_parameters()  # 加载用户参数
        self.serial_manager = SerialManager()  # 创建 SerialManager 实例
        # 默认从存储中加载模式，如果有的话
        self.selected_mode = self.user_parameters.get("mode", "None")  # 默认模式为 "None"
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

        user_label = tk.Label(header_frame, text=f"Logged in as: {self.username}")
        user_label.pack(side=tk.LEFT, padx=10)

        exit_button = tk.Button(header_frame, text="Exit", command=self.root.quit)
        exit_button.pack(side=tk.RIGHT, padx=10)

    def create_mode_selection(self):
        """创建下拉菜单以选择起搏模式。"""
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(pady=10)

        mode_label = tk.Label(mode_frame, text="Select Mode:")
        mode_label.pack(side=tk.LEFT, padx=10)

        self.pacing_mode_var = tk.StringVar(value=self.selected_mode)  # 使用选中的模式值初始化
        self.pacing_mode_dropdown = ttk.Combobox(mode_frame, textvariable=self.pacing_mode_var)
        self.pacing_mode_dropdown["values"] = [
            "None", "AOO", "VOO", "AAI", "VVI", "AOOR", "AAIR", "VOOR", "VVIR"]
        self.pacing_mode_dropdown.pack(side=tk.LEFT, padx=10)
        self.pacing_mode_dropdown.bind("<<ComboboxSelected>>", self.update_parameters)

    def create_parameter_fields(self):
        """创建参数输入字段。"""
        self.fields = {}
        param_frame = tk.Frame(self.root)
        param_frame.pack(pady=20)

        # 字段名称列表
        field_names = [
            "Ampitute","LRL",
            "Pulsewidth", "Threshold" , "ARP",
            "VRP", "URL", "MSR", "Activity_Threshold",
            "Response_Factor", "Reaction_time", "Recovery_time"
        ]

        # 每排字段数量
        fields_per_column = (len(field_names) + 1) // 2

        for i, field_name in enumerate(field_names):
            column = i // fields_per_column  # 根据索引计算列号
            row = i % fields_per_column  # 根据索引计算行号

            label = tk.Label(param_frame, text=f"{field_name}:")
            entry = tk.Entry(param_frame)

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
        
        save_button = tk.Button(button_frame, text="Save Data", command=self.save_user_parameters)
        save_button.pack(side=tk.LEFT, padx=20)
        
        egdiagrom_button = tk.Button(button_frame, text="Display EGDIAGRAM", command=self.send_parameters)
        egdiagrom_button.pack(side=tk.LEFT, padx=20)

    def create_status_display(self):
        """创建连接状态显示区域，并添加串口选择下拉菜单。"""
        status_frame = tk.Frame(self.root)
        status_frame.pack(pady=10)

        # 状态显示标签
        self.status_label = tk.Label(status_frame, text="Device not connected")
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
                self.status_label.config(text=f"Connected to {selected_port}")
            else:
                self.status_label.config(text=f"Failed to connect to {selected_port}")
        else:
            messagebox.showerror("Error", "No valid COM port selected")

    def send_parameters(self):
        """将参数打包并通过串口发送。"""
        
        field_values = {  # 从输入框中获取字段值
            "Ampitute": self.fields["Ampitute"].get(),
            "LRL": self.fields["LRL"].get(),
            "Pulsewidth": self.fields["Pulsewidth"].get(),
            "Threshold": self.fields["Threshold"].get(),
            "ARP": self.fields["ARP"].get(),
            "VRP": self.fields["VRP"].get(),
            "URL": self.fields["URL"].get(),
            "MSR": self.fields["MSR"].get(),
            "Activity_Threshold": self.fields["Activity_Threshold"].get(),
            "Response_Factor": self.fields["Response_Factor"].get(),
            "Reaction_time": self.fields["Reaction_time"].get(),
            "Recovery_time": self.fields["Recovery_time"].get(),
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
                print(value)
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
            "AOO": ["LRL", "URL", "Pulsewidth","Ampitute"],
            "AAI": ["LRL", "URL", "Amplitude", "Pulsewidth", "ARP"],
            "VOO": ["LRL", "URL", "Pulsewidth","Ampitute"],
            "VVI": ["LRL", "URL", "Amplitude", "Pulsewidth", "VRP"],
            "AOOR": ["LRL", "URL","MSR", "Pulsewidth","Amplitude","Reaction_time","Response_Factor","Activity_Threshold"],
            "AAIR": ["LRL", "URL", "Amplitude", "Pulsewidth", "ARP","Response_Factor", "Reaction_time", "Recovery_time","Activity_Threshold"],
            "VOOR": ["LRL", "URL", "Amplitude", "Pulsewidth", "ARP","Response_Factor", "Reaction_time", "Recovery_time","Activity_Threshold"],
            "VVIR": ["LRL", "URL", "Amplitude", "Pulsewidth", "MSR","ARP","Response_Factor", "Reaction_time", "Recovery_time"],
        }
        return relevant_params.get(mode, [])

    def load_user_parameters(self):
        """加载用户参数，包括模式。"""
        try:
            user_params = FileIO.load_parameter(self.username)  # 从文件加载参数
            return user_params if user_params else {}
        except Exception as e:
            print(f"Error loading user parameters: {e}")
            return {}

    def save_user_parameters(self):
        """保存用户参数"""
        try:
            # 从输入框中获取字段值，确保文本是数字，若为空则默认使用0
            field_values = {
                "Amplitude": self.get_float_value("Amplitude", 100),  # 默认初始值 100
                "LRL": self.get_float_value("LRL", 60),                # 默认初始值 60
                "Pulsewidth": self.get_float_value("Pulsewidth", 0.4),  # 默认初始值 0.4
                "Threshold": self.get_float_value("Threshold", 66),    # 默认初始值 66
                "ARP": self.get_float_value("ARP", 320),               # 默认初始值 320
                "VRP": self.get_float_value("VRP", 320),               # 默认初始值 320
                "URL": self.get_float_value("URL", 120),               # 默认初始值 120
                "MSR": self.get_float_value("MSR", 120),               # 默认初始值 120
                "Activity_Threshold": self.get_float_value("Activity_Threshold", 1.1),  # 默认初始值 1.1
                "Response_Factor": self.get_float_value("Response_Factor", 8),          # 默认初始值 8
                "Reaction_time": self.get_float_value("Reaction_time", 10),            # 默认初始值 10
                "Recovery_time": self.get_float_value("Recovery_time", 30),            # 默认初始值 30
            }

            # 获取当前模式（例如："AOO", "VOO", "VVI" 等）
            mode = self.pacing_mode_var.get()

            # 打印当前的 Amplitude 和字段值字典，用于调试
            print(f"Amplitude from parameter manager: {self.parameter_manager.getAmplitude()}")
            print(f"Field Values: {field_values}")
            
            # 使用绝对路径创建 FileIO 实例
            file_io = FileIO(os.path.dirname(os.path.abspath(__file__)))
            
            # 写入参数到文件
            success = file_io.write_parameter(field_values, username=self.username, mode=mode)
            
            # 输出成功或失败信息
            if success:
                print("Parameters saved successfully.")
            else:
                print("Failed to save parameters.")
        
        except Exception as e:
            print(f"Error while saving parameters: {e}")


    def get_float_value(self, field_name, default_value=0):
        """安全地从输入框获取字段值并转换为浮动值"""
        value = self.fields.get(field_name)  # 获取 Entry 对象
        print(value)
        if value is not None:
            text_value = value.get()  # 获取文本内容
            print(text_value)
            try:
                # 尝试转换为 float 类型
                return float(text_value) if text_value else default_value
            except ValueError:
                print(f"Invalid input for {field_name}, using default value {default_value}")
                return default_value  # 如果转换失败，返回默认值
        return default_value  # 如果字段不存在，返回默认值


if __name__ == "__main__":
    root = tk.Tk()
    app = ApplicationWindow(root, username="becnch")
    root.mainloop()
