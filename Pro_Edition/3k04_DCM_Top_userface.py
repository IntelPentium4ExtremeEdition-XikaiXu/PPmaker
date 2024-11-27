import tkinter as tk
from tkinter import messagebox
import bcrypt
import json
import os
#from system_transport import SerialConnection
from LOL import EgramPlotter


#def show_egram_graph():
#   messagebox.showinfo("Electrogram", "Displaying electrogram...")



# File for storing user credentials
base_folder = "storage_system"
user_file = "users.json"

# File for storing parameters
os.makedirs(base_folder, exist_ok=True)

# Invite code for registration
invite_code = "114514"

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

    tk.Button(register_window, text="注册", command=register).pack(pady=10)


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
    main_window.geometry("800x480")

    menu_bar = tk.Menu(main_window)

    # Add an image
    image = Image.open("example.jpg").resize((400, 300))  # Resize to 400x300
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(main_window, image=photo)
    label.image = image  # Keep a reference to avoid garbage collection
    label.pack(pady=20)
    
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
def validate_input(LRL, URL, atrial_amplitude, ventricular_amplitude):
    if not (30 <= LRL <= 150):
        raise ValueError("Lower Rate Limit must be between 30 and 150.")
    if not (50 <= URL <= 180):
        raise ValueError("Upper Rate Limit must be between 50 and 180.")
    if not (0.5 <= atrial_amplitude <= 5.0):
        raise ValueError("Atrial Amplitude must be between 0.5V and 5.0V.")
    if not (0.5 <= ventricular_amplitude <= 5.0):
        raise ValueError("Ventricular Amplitude must be between 0.5V and 5.0V.")
    # Add more validation logic as needed for other parameters
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
    plotter = EgramPlotter(root)  # 使用 root 窗口作为父窗口
    plotter.start()  # 开始加载 CSV 和绘图流程


if __name__ == "__main__":
    root = tk.Tk()
    root.title("User Login")
    root.geometry("300x200")
    
    # 定义其他 UI 组件
    tk.Label(root, text="Username:").pack(pady=10)
    entry_username = tk.Entry(root)
    entry_username.pack(pady=5)
    tk.Label(root, text="Password:").pack(pady=10)
    entry_password = tk.Entry(root, show="*")
    entry_password.pack(pady=5)
    tk.Button(root, text="Login", command=login).pack(pady=10)
    tk.Button(root, text="Register", command=open_register_window).pack(pady=5)
    
    # 定义 egram_button
    #egram_button = tk.Button(root, text="Show Electrogram", command=show_egram_graph)
    #egram_button.pack(pady=20)

    root.mainloop()



