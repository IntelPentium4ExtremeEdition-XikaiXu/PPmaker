import tkinter as tk
from tkinter import messagebox
import bcrypt
#import json

# v0.2 Note 10/21/2024 3:45PM - Security overhaul: enhanced security by adding password hashing, 
# admin key, and minimal password length. In addition to hashing, the passwords also involves 
# 'salt', which adds random strings for cyphering. 
# Admin key function is removed for easier demo/grading.

# v0.21 Note 10/22/2024 added: show username when login

# v0.22 Note 10/23/2024 added: maximum local user count set to 10
# Added user input parameters such as lower rate limit, upper rate limit, etc... for each mode.
# Outputs the user input after data is input

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

# Preset account (default account)
users = {
    "zhant88": bcrypt.hashpw(b"password123", bcrypt.gensalt())  # default password
}

def validate_input(LRL, URL, amplitude, pulse_width):
    try:
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
        if (URL <= LRL):
            raise ValueError("Warning: Lower Rate cannot exceed Upper Rate.")
        return True

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
        return False

def save_parameters_to_file(mode, parameters):
    filename = f"{mode}_parameters.txt"
    with open(filename, 'w') as file:
        # Record parameters in plain text 
        for key, value in parameters.items():
            file.write(f"{key}: {value}\n")
    messagebox.showinfo("SUCCESS", f"Parameters saved to {filename}")

# New user sign up
def register():
    username = entry_username.get()
    password = entry_password.get()
    
    if len(password) < 6:
        messagebox.showerror("ERROR", "Password must be at least 6 characters long.")
        return
    if len(users) > 10:
        messagebox.showerror("ERROR", "Maximum of 10 users reached.")
    else:
        if username in users:
            messagebox.showerror("ERROR", "Username already exists.")
        else:
            # Hash the password before storing it
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            users[username] = hashed_password
            messagebox.showinfo("SUCCESS", "You have registered!")
            entry_username.delete(0, tk.END)
            entry_password.delete(0, tk.END)

# Login for existing user
def login():
    username = entry_username.get()
    password = entry_password.get()

    if username in users and bcrypt.checkpw(password.encode('utf-8'), users[username]):
        messagebox.showinfo("SUCCESS", f"Login successful!\nUser: {username}")
        open_main_window()
    else:
        messagebox.showerror("ERROR", "Incorrect username or password!")

# Main interface
def open_main_window():
    login_window.destroy()  # Close the login window
    main_window = tk.Tk()
    main_window.title("DCM Main Interface")
    
    label_welcome = tk.Label(main_window, text="                                                    Welcome to the DCM system.                                                    \nPacemaker Status: Connected\nPort:N/A")
    label_welcome.pack(pady=20)
    
    # Mode selection buttons
    label_mode = tk.Label(main_window, text="Select mode for the pacemaker:")
    label_mode.pack(pady=10)
    
    btn_AOO = tk.Button(main_window, text="AOO Mode", command=lambda: open_AOO())
    btn_AOO.pack(pady=5)
    
    btn_VOO = tk.Button(main_window, text="VOO Mode", command=lambda: open_VOO())
    btn_VOO.pack(pady=5)
    
    btn_AAI = tk.Button(main_window, text="AAI Mode", command=lambda: open_AAI())
    btn_AAI.pack(pady=5)
    
    btn_VVI = tk.Button(main_window, text="VVI Mode", command=lambda: open_VVI())
    btn_VVI.pack(pady=5)
    
    main_window.mainloop()

# Feedback after mode selection
def select_mode(mode):
    messagebox.showinfo("Mode selection", f"{mode} Mode has been selected.")

# AOO Parameters
def open_AOO():
    AOO_window = tk.Tk()
    AOO_window.title("AOO Parameters")
    label_AOO = tk.Label(AOO_window, text="                                                    Choose your AOO parameters.                                                    ")
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

    # Displays the results after enter button is clicked
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

    btn_AOO = tk.Button(AOO_window, text="Enter", command=AOO_results).pack(pady=5)
    

# VOO Parameters
def open_VOO():
    VOO_window = tk.Tk()
    VOO_window.title("VOO Parameters")
    label_VOO = tk.Label(VOO_window, text="                                                    Choose your VOO parameters.                                                    ")
    label_VOO.pack(pady=20)

    label_LRL = tk.Label(VOO_window, text="Lower Rate Limit").pack(pady=5)
    entry_LRL = tk.Entry(VOO_window)
    entry_LRL.pack(pady=5)

    label_URL = tk.Label(VOO_window, text="Upper Rate Limit").pack(pady=5)
    entry_URL = tk.Entry(VOO_window)
    entry_URL.pack(pady=5)

    label_VA = tk.Label(VOO_window, text="Ventricular Amplitude").pack(pady=5)
    entry_VA = tk.Entry(VOO_window)
    entry_VA.pack(pady=5)

    label_VPW = tk.Label(VOO_window, text="Ventricular Pulse Width").pack(pady=5)
    entry_VPW = tk.Entry(VOO_window)
    entry_VPW.pack(pady=5)

    # Displays the results after enter button is clicked
    def VOO_results():
        LRL = entry_LRL.get()
        URL = entry_URL.get()
        amplitude = entry_VA.get()
        pulse_width = entry_VPW.get()

        if validate_input(LRL, URL, amplitude, pulse_width):
            parameters = {
                "Lower Rate Limit": LRL,
                "Upper Rate Limit": URL,
                "Ventricular Amplitude": amplitude,
                "Ventricular Pulse Width": pulse_width
            }
            save_parameters_to_file("VOO", parameters)

    btn_VOO = tk.Button(VOO_window, text="Enter", command=VOO_results).pack(pady=5)
    
# AAI Parameters
def open_AAI():
    AAI_window = tk.Tk()
    AAI_window.title("AAI Parameters") 
    label_AAI = tk.Label(AAI_window, text="                                                    Choose your AAI parameters.                                                    ")
    label_AAI.pack(pady=20)
    label_LRL = tk.Label(AAI_window, text="Lower Rate Limit").pack(pady=5)
    entry_LRL = tk.Entry(AAI_window)
    entry_LRL.pack(pady=5)
    label_URL = tk.Label(AAI_window, text="Upper Rate Limit").pack(pady=5)
    entry_URL = tk.Entry(AAI_window)
    entry_URL.pack(pady=5)
    label_AA = tk.Label(AAI_window, text="Atrial Amplitude").pack(pady=5)
    entry_AA = tk.Entry(AAI_window)
    entry_AA.pack(pady=5)
    label_APW = tk.Label(AAI_window, text="Atrial Pulse Width").pack(pady=5)
    entry_APW = tk.Entry(AAI_window)
    entry_APW.pack(pady=5)
    label_ARP = tk.Label(AAI_window, text="ARP").pack(pady=5)
    entry_ARP = tk.Entry(AAI_window)
    entry_ARP.pack(pady=5)
    

    # Displays the results after enter button is clicked
    def AAI_results():
        LRL = entry_LRL.get()
        URL = entry_URL.get()
        amplitude = entry_AA.get()
        pulse_width = entry_APW.get()
        ARP = entry_ARP.get()

        if validate_input(LRL, URL, amplitude, pulse_width):
            parameters = {
                "Lower Rate Limit": LRL,
                "Upper Rate Limit": URL,
                "Atrial Amplitude": amplitude,
                "Atrial Pulse Width": pulse_width,
                "ARP": ARP
            }
            save_parameters_to_file("AAI", parameters)

    btn_AAI = tk.Button(AAI_window, text="Enter", command=AAI_results).pack(pady=5)

# VVI Parameters
def open_VVI():
    VVI_window = tk.Tk()
    VVI_window.title("VVI Parameters") 
    label_VVI = tk.Label(VVI_window, text="                                                    Choose your VVI parameters.                                                    ")
    label_VVI.pack(pady=20)
    label_LRL = tk.Label(VVI_window, text="Lower Rate Limit").pack(pady=5)
    entry_LRL = tk.Entry(VVI_window)
    entry_LRL.pack(pady=5)
    label_URL = tk.Label(VVI_window, text="Upper Rate Limit").pack(pady=5)
    entry_URL = tk.Entry(VVI_window)
    entry_URL.pack(pady=5)
    label_VA = tk.Label(VVI_window, text="Ventricular Amplitude").pack(pady=5)
    entry_VA = tk.Entry(VVI_window)
    entry_VA.pack(pady=5)
    label_VPW = tk.Label(VVI_window, text="Ventricular Pulse Width").pack(pady=5)
    entry_VPW = tk.Entry(VVI_window)
    entry_VPW.pack(pady=5)
    label_VRP = tk.Label(VVI_window, text="VRP").pack(pady=5)
    entry_VRP = tk.Entry(VVI_window)
    entry_VRP.pack(pady=5)
    

    # Displays the results after enter button is clicked
    def VVI_results():
        LRL = entry_LRL.get()
        URL = entry_URL.get()
        amplitude = entry_VA.get()
        pulse_width = entry_VPW.get()
        VRP = entry_VRP.get()

        if validate_input(LRL, URL, amplitude, pulse_width):
            parameters = {
                "Lower Rate Limit": LRL,
                "Upper Rate Limit": URL,
                "Ventricular Amplitude": amplitude,
                "Ventricular Pulse Width": pulse_width,
                "VRP": VRP
            }
            save_parameters_to_file("VVI", parameters)

    btn_VVI = tk.Button(VVI_window, text="Enter", command=VVI_results).pack(pady=5)


# Create login window
login_window = tk.Tk()
login_window.title("DCM System Login")

# Username and password input
label_username = tk.Label(login_window, text="                                                    Username:                                                    ")
label_username.pack(pady=5)
entry_username = tk.Entry(login_window)
entry_username.pack(pady=5)

label_password = tk.Label(login_window, text="Password:")
label_password.pack(pady=5)
entry_password = tk.Entry(login_window, show="*")
entry_password.pack(pady=5)

# login and register window
btn_register = tk.Button(login_window, text="Register", command=register)
btn_register.pack(pady=5)

btn_login = tk.Button(login_window, text="Login", command=login)
btn_login.pack(pady=5)

login_window.mainloop()
