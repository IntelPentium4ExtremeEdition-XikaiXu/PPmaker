import tkinter as tk
from tkinter import messagebox

# Preset account (default account)
users = {
    "zhant88": "password123"  # default password
}

# New user sign up
def register():
    username = entry_username.get()
    password = entry_password.get()
    
    if username in users:
        messagebox.showerror("ERROR", "Username already exist.")
    else:
        users[username] = password
        messagebox.showinfo("SUCCESS", "You have registered！")
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)

# Login for existing user
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if username in users and users[username] == password:
        messagebox.showinfo("SUCCESS", "Login successfully!")
        open_main_window()
    else:
        messagebox.showerror("ERROR", "Incorrect username or password!")

# Main interface
def open_main_window():
    login_window.destroy()  # Close the login window
    main_window = tk.Tk()
    main_window.title("DCM Main Interface")
    
    label_welcome = tk.Label(main_window, text="                                                    Welcome to the DCM system.                                                    ")
    label_welcome.pack(pady=20)
    
    # Mode selection buttons
    label_mode = tk.Label(main_window, text="Select mode for the pacemaker:")
    label_mode.pack(pady=10)
    
    btn_AOO = tk.Button(main_window, text="AOO Mode", command=lambda: select_mode("AOO"))
    btn_AOO.pack(pady=5)
    
    btn_VOO = tk.Button(main_window, text="VOO Mode", command=lambda: select_mode("VOO"))
    btn_VOO.pack(pady=5)
    
    btn_AAI = tk.Button(main_window, text="AAI Mode", command=lambda: select_mode("AAI"))
    btn_AAI.pack(pady=5)
    
    btn_VVI = tk.Button(main_window, text="VVI Mode", command=lambda: select_mode("VVI"))
    btn_VVI.pack(pady=5)
    
    main_window.mainloop()

# Feedback after mode selection
def select_mode(mode):
    messagebox.showinfo("Mode selection", f"You chose {mode} Mode")

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
