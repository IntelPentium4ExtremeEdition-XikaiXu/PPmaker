import tkinter as tk
from tkinter import messagebox
import bcrypt
import json
import os
import matplotlib
#from system_transport import SerialConnection
from LOL import EgramPlotter
from PIL import Image

base_folder = "storage_system"
user_file = "users.json"

# File for storing parameters
os.makedirs(base_folder, exist_ok=True)


# PARAMLABELS for all modes
PARAMLABELS = [
    "Lower Rate Limit", "Upper Rate Limit", "Atrial Amplitude", "Ventricular Amplitude",
    "Atrial Pulsewidth", "Ventricular Pulsewidth", "Atrial Refractory Period",
    "Ventricular Refractory Period", "Atrium Sense", "Ventricle Sense", "MSR", "Recovery Time",
    "Reaction Time", "Response Factor", "Activity Threshold", "AV Delay", "Additional Parameter"
]

# 加载用户数据
def load_users():
    if os.path.exists(user_file):
        with open(user_file, 'r') as file:
            return json.load(file)
    return {}

# 保存用户数据
def save_users(users):
    with open(user_file, 'w') as file:
        json.dump(users, file, indent=4)

# 初始化用户数据
users = load_users()

# 注册窗口
def open_register_window():
    register_window = tk.Toplevel()
    register_window.title("signed")

    tk.Label(register_window, text="username:").pack(pady=5)
    entry_username = tk.Entry(register_window)
    entry_username.pack(pady=5)

    tk.Label(register_window, text="password:").pack(pady=5)
    entry_password = tk.Entry(register_window, show="*")
    entry_password.pack(pady=5)

    def register():
        username = entry_username.get()
        password = entry_password.get()

        if username in users:
            messagebox.showerror("sorry", "this user is already signed")
            return

        if len(password) < 6:
            messagebox.showerror("sorry", "password must longer than 6")
            return

        # 创建用户文件夹
        user_folder = os.path.join(base_folder, username)
        os.makedirs(user_folder, exist_ok=True)

        # 初始化用户参数文件
        param_file = os.path.join(user_folder, f"{username}_parameters.txt")
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        with open(param_file, 'w') as file:
            file.write(f"password: {hashed_password.decode('utf-8')}\n")
            file.write("aoo: 0\nvoo: 0\naooR: 0\nvooR: 0\n")
            file.write("aii: 0\nvii: 0\naiiR: 0\nviiR: 0\n")

        users[username] = hashed_password.decode('utf-8')
        save_users(users)
        messagebox.showinfo("success", "signed")
        register_window.destroy()

    tk.Button(register_window, text="signed", command=register).pack(pady=10)


# Login functionality
def login():
    username = entry_username.get()
    password = entry_password.get().encode('utf-8')

    if username in users and bcrypt.checkpw(password, users[username].encode('utf-8')):
        messagebox.showinfo("SUCCESS", f"Login successful! User: {username}")
        open_main_window()
    else:
        messagebox.showerror("ERROR", "Incorrect username or password!")

# Main application window
def open_main_window():
    main_window = tk.Tk()
    main_window.title("DCM Main Interface")
    main_window.geometry("540x480")

    menu_bar = tk.Menu(main_window)

    operation_menu = tk.Menu(menu_bar, tearoff=0)
    operation_menu.add_command(label="Device Status", command=show_device_status)
    operation_menu.add_command(label="Refresh Connection", command=refresh_connection_status)
    operation_menu.add_separator()
    operation_menu.add_command(label="Exit", command=main_window.quit)
    menu_bar.add_cascade(label="Operations", menu=operation_menu)

    mode_menu = tk.Menu(menu_bar, tearoff=0)
    mode_menu.add_command(label="Mode Selection", command=open_mode_selection)
    mode_menu.add_command(label="Ready to send?", command=ready_on_serial)
    menu_bar.add_cascade(label="Mode", menu=mode_menu)

    main_window.config(menu=menu_bar)
    main_window.mainloop()

# Device status display
def show_device_status():
    messagebox.showinfo("Device Status", "Device Connected: Yes\nPort: N/A")

# Refresh connection status
def refresh_connection_status():
    messagebox.showinfo("Connection Status", "Connection Refreshed.\nStatus: ", SerialConnection.get_connection_status(), "")

def ready_on_serial():
    send_window = tk.Toplevel()
    send_window.title("Ready to Send?")
    tk.Button(send_window, text="AOO", command=lambda: SerialConnection.send_data(mode='AOO')).pack(pady=5)
    tk.Button(send_window, text="AAI", command=lambda: SerialConnection.send_data(mode='AAI')).pack(pady=5)
    tk.Button(send_window, text="VOO", command=lambda: SerialConnection.send_data(mode='VOO')).pack(pady=5)
    tk.Button(send_window, text="VVI", command=lambda: SerialConnection.send_data(mode='VVI')).pack(pady=5)
    tk.Button(send_window, text="AOOR", command=lambda: SerialConnection.send_data(mode='AOOR')).pack(pady=5)
    tk.Button(send_window, text="AAIR", command=lambda: SerialConnection.send_data(mode='AAIR')).pack(pady=5)
    tk.Button(send_window, text="VOOR", command=lambda: SerialConnection.send_data(mode='VOOR')).pack(pady=5)
    tk.Button(send_window, text="VVIR", command=lambda: SerialConnection.send_data(mode='VVIR')).pack(pady=5)

# Mode selection
def open_mode_selection():
    mode_window = tk.Toplevel()
    mode_window.title("Mode Selection")

    for mode in ["AOO", "VOO", "AAI", "VVI", "AOOR", "VOOR", "AAIR", "VVIR"]:
        tk.Button(mode_window, text=f"{mode} Mode", command=lambda m=mode: open_mode(m)).pack(pady=5)

# Open specific mode window
def open_mode(mode):
    mode_window = tk.Toplevel()
    mode_window.title(f"{mode} Parameters")
    
    tk.Label(mode_window, text=f"Enter parameters for {mode} mode").pack(pady=10)

    entry_fields = {}
    for label in PARAMLABELS:
        tk.Label(mode_window, text=label).pack(pady=5)
        entry = tk.Entry(mode_window)
        entry.pack(pady=5)
        entry_fields[label] = entry

    def save_mode_parameters():
        try:
            data = {label: round(float(entry_fields[label].get()), 2) for label in PARAMLABELS}
            # Validate input
            if validate_input(data["Lower Rate Limit"], data["Upper Rate Limit"], data["Atrial Amplitude"], data["Ventricular Amplitude"]):
                save_parameters_to_file(mode, data)
                mode_window.destroy()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    tk.Button(mode_window, text="Save Parameters", command=save_mode_parameters).pack(pady=10)

# Save parameters to file
def save_parameters_to_file(mode, data):
    parameters = load_parameters()  # Implement the load_parameters function to load parameters from a file
    if mode not in parameters:
        parameters[mode] = []
    parameters[mode].append(data)
    save_parameters(parameters)
    messagebox.showinfo("Success", f"Parameters for {mode} saved successfully!")

# Input validation
def validate_input(data):
    validation_rules = {
        "Lower Rate Limit": (30, 150),  # 下限速率
        "Upper Rate Limit": (50, 180),  # 上限速率
        "Atrial Amplitude": (0.5, 5.0),  # 心房振幅
        "Ventricular Amplitude": (0.5, 5.0),  # 心室振幅
        "Atrial Pulsewidth": (1, 2),  # 心房脉冲宽度
        "Ventricular Pulsewidth": (1, 2),  # 心室脉冲宽度
        "Atrial Refractory Period": (1, 2),  # 心房不应期
        "Ventricular Refractory Period": (1, 2),  # 心室不应期
        "Atrium Sense": (1, 2),  # 心房感应
        "Ventricle Sense": (1, 2),  # 心室感应
        "MSR": (1, 2),  # 最大感应速率
        "Recovery Time": (1, 2),  # 恢复时间
        "Reaction Time": (1, 2),  # 反应时间
        "Response Factor": (1, 2),  # 响应因子
        "Activity Threshold": (1, 2),  # 活动阈值
        "AV Delay": (1, 2),  # 房室延迟
        "Additional Parameter": (1, 2),  # 其他参数
    }
    for param, value in data.items():
        if param in validation_rules:
            min_val, max_val = validation_rules[param]
            if not (min_val <= value <= max_val):
                raise ValueError(f"{param} must between {min_val} and {max_val}.")
        else:
            raise ValueError(f"wrong：{param}")
    return True


# Loading and saving parameters from/to a file
def load_parameters():
    if os.path.exists("parameters.json"):
        with open("parameters.json", "r") as file:
            return json.load(file)
    return {}

def save_parameters(parameters):
    with open("parameters.json", "w") as file:
        json.dump(parameters, file, indent=4)

def show_egram_graph():
    plotter = EgramPlotter(root)
    plotter.start() 


if __name__ == "__main__":
    root = tk.Tk()
    root.title("User Login")
    root.geometry("300x280")
    
    # 定义其他 UI 组件
    tk.Label(root, text="Username:").pack(pady=10)
    entry_username = tk.Entry(root)
    entry_username.pack(pady=5)
    tk.Label(root, text="Password:").pack(pady=10)
    entry_password = tk.Entry(root, show="*")
    entry_password.pack(pady=5)
    tk.Button(root, text="Login", command=login).pack(pady=10)
    tk.Button(root, text="Register", command=open_register_window).pack(pady=5)
    
    root.mainloop()



