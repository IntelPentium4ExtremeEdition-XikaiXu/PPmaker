import tkinter as tk
from tkinter import messagebox
import bcrypt
import json
import os
from system_transport import SerialConnection
# File for storing user credentials
user_file = "users.json"

# File for storing parameters
parameters_file = "parameters.json"

# Invite code for registration
invite_code = "123456"

# Load user data
def load_users():
    if os.path.exists(user_file):
        with open(user_file, 'r') as file:
            return json.load(file)
    return {}

# Save user data
def save_users(users):
    with open(user_file, 'w') as file:
        json.dump(users, file, indent=4)

# Load parameters data
def load_parameters():
    if os.path.exists(parameters_file):
        with open(parameters_file, 'r') as file:
            return json.load(file)
    return {"AOO": [], "VOO": [], "AAI": [], "VVI": []}

# Save parameters data
def save_parameters(parameters):
    with open(parameters_file, 'w') as file:
        json.dump(parameters, file, indent=4)

# Initialize global variables
users = load_users()
parameters = load_parameters()

# Registration window
def open_register_window():
    register_window = tk.Toplevel()
    register_window.title("Register")

    tk.Label(register_window, text="Username:").pack(pady=5)
    entry_username = tk.Entry(register_window)
    entry_username.pack(pady=5)

    tk.Label(register_window, text="Password:").pack(pady=5)
    entry_password = tk.Entry(register_window, show="*")
    entry_password.pack(pady=5)

    tk.Label(register_window, text="Invite Code:").pack(pady=5)
    entry_invite_code = tk.Entry(register_window)
    entry_invite_code.pack(pady=5)

    def register():
        username = entry_username.get()
        password = entry_password.get()
        code = entry_invite_code.get()

        if len(users) >= 10:
            messagebox.showerror("ERROR", "User limit reached. Cannot register more users.")
            register_window.destroy()
            return
        if code != invite_code:
            messagebox.showerror("ERROR", "Invalid invite code.")
            return
        if username in users:
            messagebox.showerror("ERROR", "Username already exists.")
            return
        if len(password) < 6:
            messagebox.showerror("ERROR", "Password must be at least 6 characters long.")
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users[username] = hashed_password.decode('utf-8')
        save_users(users)
        messagebox.showinfo("SUCCESS", "Registration successful!")
        register_window.destroy()

    tk.Button(register_window, text="Register", command=register).pack(pady=10)

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
    main_window.geometry("400x300")

    menu_bar = tk.Menu(main_window)

    operation_menu = tk.Menu(menu_bar, tearoff=0)
    operation_menu.add_command(label="Device Status", command=show_device_status)
    operation_menu.add_command(label="Refresh Connection", command=refresh_connection_status)
    operation_menu.add_separator()
    operation_menu.add_command(label="Exit", command=main_window.quit)
    menu_bar.add_cascade(label="Operations", menu=operation_menu)

    mode_menu = tk.Menu(menu_bar, tearoff=0)
    mode_menu.add_command(label="Mode Selection", command=open_mode_selection)
    mode_menu.add_command(label="Ready ti send?", command=ready_on_serial)
    menu_bar.add_cascade(label="Mode", menu=mode_menu)

    main_window.config(menu=menu_bar)
    main_window.mainloop()

# Device status display
def show_device_status():
    messagebox.showinfo("Device Status", "Device Connected: Yes\nPort: N/A\"")

# Refresh connection status
def refresh_connection_status():
    messagebox.showinfo("Connection Status", "Connection Refreshed.\nStatus: ",SerialConnection.get_connection_status(),"")

def ready_on_serial():
    send_window = tk.Toplevel()
    send_window.title("Ready to Send?")
    tk.Button(send_window, text="AOO", command=lambda: SerialConnection.send_data(mode='AOO')).pack(pady=5)
    tk.Button(send_window, text="AAI", command=lambda: SerialConnection.send_data(mode='AAI')).pack(pady=5)
    tk.Button(send_window, text="VOO", command=lambda: SerialConnection.send_data(mode='VOO')).pack(pady=5)
    tk.Button(send_window, text="VVI", command=lambda: SerialConnection.send_data(mode='VVI')).pack(pady=5)

# Mode selection
def open_mode_selection():
    mode_window = tk.Toplevel()
    mode_window.title("Mode Selection")

    tk.Button(mode_window, text="AOO Mode", command=lambda: open_mode("AOO")).pack(pady=5)
    tk.Button(mode_window, text="VOO Mode", command=lambda: open_mode("VOO")).pack(pady=5)
    tk.Button(mode_window, text="AAI Mode", command=lambda: open_mode("AAI")).pack(pady=5)
    tk.Button(mode_window, text="VVI Mode", command=lambda: open_mode("VVI")).pack(pady=5)

# Open specific mode window
def open_mode(mode):
    mode_window = tk.Toplevel()
    mode_window.title(f"{mode} Parameters")

    tk.Label(mode_window, text=f"Enter parameters for {mode} mode").pack(pady=10)

    entry_fields = {}
    labels = ["Lower Rate Limit", "Upper Rate Limit", "Amplitude", "Pulse Width"]
    for label in labels:
        tk.Label(mode_window, text=label).pack(pady=5)
        entry = tk.Entry(mode_window)
        entry.pack(pady=5)
        entry_fields[label] = entry

    def save_mode_parameters():
        try:
            data = {label: round(float(entry_fields[label].get()), 2) for label in labels}
            if validate_input(data["Lower Rate Limit"], data["Upper Rate Limit"], data["Amplitude"], data["Pulse Width"]):
                save_parameters_to_file(mode, data)
                mode_window.destroy()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    tk.Button(mode_window, text="Save Parameters", command=save_mode_parameters).pack(pady=10)

# Save parameters to file
def save_parameters_to_file(mode, data):
    parameters[mode].append(data)
    save_parameters(parameters)
    messagebox.showinfo("Success", f"Parameters for {mode} saved successfully!")

# Input validation
def validate_input(LRL, URL, amplitude, pulse_width):
    if not (30 <= LRL <= 150):
        raise ValueError("Lower Rate Limit must be between 30 and 150.")
    if not (50 <= URL <= 180):
        raise ValueError("Upper Rate Limit must be between 50 and 180.")
    if not (0.5 <= amplitude <= 5.0):
        raise ValueError("Amplitude must be between 0.5V and 5.0V.")
    if not (0.05 <= pulse_width <= 1.9):
        raise ValueError("Pulse Width must be between 0.05ms and 1.9ms.")
    if URL <= LRL:
        raise ValueError("Upper Rate Limit must be greater than Lower Rate Limit.")
    return True



# Program entry point
login_window = tk.Tk()
login_window.title("DCM System Login")

tk.Label(login_window, text="Username:").pack(pady=5)
entry_username = tk.Entry(login_window)
entry_username.pack(pady=5)

tk.Label(login_window, text="Password:").pack(pady=5)
entry_password = tk.Entry(login_window, show="*")
entry_password.pack(pady=5)

tk.Button(login_window, text="Register", command=open_register_window).pack(pady=5)
tk.Button(login_window, text="Login", command=login).pack(pady=5)

login_window.mainloop()
