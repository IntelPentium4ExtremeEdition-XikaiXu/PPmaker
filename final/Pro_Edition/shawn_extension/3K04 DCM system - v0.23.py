import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import bcrypt
import json
import os
import PPmaker.Pro_Edition.system_transport as st
# v0.2 Note 10/21/2024 3:45PM - Security overhaul: enhanced security by adding password hashing, 
# admin key, and minimal password length. In addition to hashing, the passwords also involves 
# 'salt', which adds random strings for cyphering. 
# Admin key function is removed for easier demo/grading.

# v0.21 Note 10/22/2024 added: show username when login

# v0.22 Note 10/23/2024 added: maximum local user count set to 10
# Added user input parameters such as lower rate limit, upper rate limit, etc... for each mode.
# Outputs the user input after data is input

#v0.3 Note 10/25/2024 

#Implemented an invite code requirement for registration for added security. The invite code is currently set to "123456".
#Stored registered user credentials in an external JSON file ("users.json") to persist data across sessions.

# Check if bcrypt is installed for hashing 
try:
    import bcrypt #checking bcrypt situation 

except ImportError:

    # Notify the user that bcrypt is missing
    def notify_missing_bcrypt():
        messagebox.showerror(
            "Security Module Not Found", 
            "The Python Library 'bcrypt' is not detected.\nPlease install 'bcrypt' to run this program.\n\n\nFor Windows system, use the command in the Windows PowerShell:\n\npip install bcrypt"
        )

    # GUI execution 
    notify_missing_bcrypt() 
    # Backup SystemExit
    raise SystemExit("bcrypt is required to run this program. Please install it using 'pip install bcrypt' for windows system.")

# Initial data and settings
users = {}
user_file = "users.json"
invite_code = "123456"


# Load user data file
def load_users():
    global users
    if os.path.exists(user_file):
        with open(user_file, 'r') as file:
            users = json.load(file)
    else:
        users = {}

# Save user data
def save_users():
    with open(user_file, 'w') as file:
        json.dump(users, file)

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

    # Registration functionality
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
        save_users()
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

# Main window and functionality
def open_main_window():
    global main_window  # Declare main_window as a global variable
    main_window = tk.Tk()
    main_window.title("DCM Main Interface")
    main_window.geometry("400x300")

    # Add menu bar
    menu_bar = tk.Menu(main_window)

    # Operations menu
    operation_menu = tk.Menu(menu_bar, tearoff=0)
    operation_menu.add_command(label="Device Status", command=show_device_status)
    operation_menu.add_command(label="Refresh Connection", command=refresh_connection_status)
    operation_menu.add_separator()
    operation_menu.add_command(label="Exit", command=main_window.quit)
    menu_bar.add_cascade(label="Operations", menu=operation_menu)

    # Mode menu
    mode_menu = tk.Menu(menu_bar, tearoff=0)
    mode_menu.add_command(label="Mode Selection", command=open_mode_selection)
    menu_bar.add_cascade(label="Mode", menu=mode_menu)

    # Data menu
    data_menu = tk.Menu(menu_bar, tearoff=0)
    data_menu.add_command(label="Show ECG", command=show_ecg_graph)
    menu_bar.add_cascade(label="Data", menu=data_menu)

    main_window.config(menu=menu_bar)
    main_window.mainloop()

# Device status display
def show_device_status():
    messagebox.showinfo("Device Status", "Device Connected: Yes\nPort: N/A\nBattery: 75%")

# Refresh connection status
def refresh_connection_status():
    messagebox.showinfo("Connection Status", "Connection Refreshed.\nStatus: Connected")

# ECG display
def show_ecg_graph():
    ecg_window = tk.Toplevel(main_window)
    ecg_window.title("ECG Display")
    label = tk.Label(ecg_window, text="ECG Graph will be displayed here.")
    label.pack(pady=20)

# Mode selection window
def open_mode_selection():
    mode_window = tk.Toplevel(main_window)
    mode_window.title("Mode Selection")

    btn_AOO = tk.Button(mode_window, text="AOO Mode", command=lambda: open_AOO())
    btn_AOO.pack(pady=5)
    btn_VOO = tk.Button(mode_window, text="VOO Mode", command=lambda: open_VOO())
    btn_VOO.pack(pady=5)
    btn_AAI = tk.Button(mode_window, text="AAI Mode", command=lambda: open_AAI())
    btn_AAI.pack(pady=5)
    btn_VVI = tk.Button(mode_window, text="VVI Mode", command=lambda: open_VVI())
    btn_VVI.pack(pady=5)

# AOO mode window
def open_AOO():
    AOO_window = tk.Toplevel(main_window)
    AOO_window.title("AOO Parameters")
    label_AOO = tk.Label(AOO_window, text="Choose your AOO parameters.")
    label_AOO.pack(pady=20)

    label_LRL = tk.Label(AOO_window, text="Lower Rate Limit").pack(pady=5)
    entry_LRL = tk.Entry(AOO_window)
    entry_LRL.pack(pady=5)

    label_URL = tk.Label(AOO_window, text="Upper Rate Limit").pack(pady=5)
    entry_URL = tk.Entry(AOO_window)
    entry_URL.pack(pady=5)

    label_AA = tk.Label(AOO_window, text="Atrial Amplitude").pack(pady=5)
    entry_AA = tk.Entry(AOO_window)
    entry_AA.pack(pady=5)

    label_APW = tk.Label(AOO_window, text="Atrial Pulse Width").pack(pady=5)
    entry_APW = tk.Entry(AOO_window)
    entry_APW.pack(pady=5)

    def AOO_results():
        LRL = entry_LRL.get()
        URL = entry_URL.get()
        amplitude = entry_AA.get()
        pulse_width = entry_APW.get()

        if validate_input(LRL, URL, amplitude, pulse_width):
            parameters = {
                "Lower Rate Limit": LRL,
                "Upper Rate Limit": URL,
                "Atrial Amplitude": amplitude,
                "Atrial Pulse Width": pulse_width
            }
            save_parameters_to_file("AOO", parameters)
            AOO_window.destroy()

    tk.Button(AOO_window, text="Enter", command=AOO_results).pack(pady=5)

# Input validation
def validate_input(LRL, URL, amplitude, pulse_width):
    try:
        if not LRL.replace('.', '', 1).isdigit() or not URL.replace('.', '', 1).isdigit() or \
           not amplitude.replace('.', '', 1).isdigit() or not pulse_width.replace('.', '', 1).isdigit():
            raise ValueError("All inputs must be numeric.")
        
        LRL = round(float(LRL), 5)
        URL = round(float(URL), 5)
        amplitude = round(float(amplitude), 5)
        pulse_width = round(float(pulse_width), 5)

        if not (30 <= LRL <= 150):
            raise ValueError("Lower Rate Limit must be between 30 and 150.")
        if not (50 <= URL <= 180):
            raise ValueError("Upper Rate Limit must be between 50 and 180.")
        if not (0.5 <= amplitude <= 5.0):
            raise ValueError("Amplitude must be between 0.5V and 5.0V.")
        if not (0.05 <= pulse_width <= 1.9):
            raise ValueError("Pulse Width must be between 0.05ms and 1.9ms.")
        if URL <= LRL:
            raise ValueError("Warning: Lower Rate cannot exceed Upper Rate.")
        return True

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
        return False

# Save parameters to file
def save_parameters_to_file(mode, parameters):
    filename = f"{mode}_parameters.txt"
    with open(filename, 'w') as file:
        for key, value in parameters.items():
            file.write(f"{key}: {value}\n")
    messagebox.showinfo("SUCCESS", f"Parameters saved to {filename}")

# Program entry point
load_users()
login_window = tk.Tk()
login_window.title("DCM System Login")

label_username = tk.Label(login_window, text="Username:")
label_username.pack(pady=5)
entry_username = tk.Entry(login_window)
entry_username.pack(pady=5)

label_password = tk.Label(login_window, text="Password:")
label_password.pack(pady=5)
entry_password = tk.Entry(login_window, show="*")
entry_password.pack(pady=5)

btn_register = tk.Button(login_window, text="Register", command=open_register_window)
btn_register.pack(pady=5)

btn_login = tk.Button(login_window, text="Login", command=login)
btn_login.pack(pady=5)

login_window.mainloop()
