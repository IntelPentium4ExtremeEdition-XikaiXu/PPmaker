import tkinter as tk
from tkinter import messagebox
from data_storage import DataStorage

class UserInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DCM System Login")
        self.root.geometry("300x200")
        self.data_storage = DataStorage()

    def open_login_window(self):
        tk.Label(self.root, text="Username:").pack(pady=5)
        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack(pady=5)

        tk.Button(self.root, text="Register", command=self.open_register_window).pack(pady=5)
        tk.Button(self.root, text="Login", command=self.login).pack(pady=5)

        self.root.mainloop()

    def open_register_window(self):
        self.root.withdraw()
        register_window = tk.Toplevel(self.root)
        register_window.title("Register")
        register_window.geometry("300x250")

        tk.Label(register_window, text="Username:").pack(pady=5)
        entry_username = tk.Entry(register_window)
        entry_username.pack(pady=5)

        tk.Label(register_window, text="Password:").pack(pady=5)
        entry_password = tk.Entry(register_window, show="*")
        entry_password.pack(pady=5)

        def register():
            username = entry_username.get()
            password = entry_password.get()
            if len(password) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters.")
                return
            if self.data_storage.register_user(username, password):
                messagebox.showinfo("Success", "Registration successful!")
                register_window.destroy()
                self.root.deiconify()
            else:
                messagebox.showerror("Error", "User already exists!")

        tk.Button(register_window, text="Register", command=register).pack(pady=10)

        def on_close():
            register_window.destroy()
            self.root.deiconify()

        register_window.protocol("WM_DELETE_WINDOW", on_close)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if self.data_storage.authenticate_user(username, password):
            messagebox.showinfo("Success", f"Welcome, {username}!")
            self.root.destroy()
            self.open_main_interface(username)
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def open_main_interface(self, username):
        main_window = tk.Tk()
        main_window.title(f"DCM Main Interface - {username}")
        main_window.geometry("400x400")

        tk.Label(main_window, text=f"Welcome, {username}!", font=("Arial", 16)).pack(pady=10)

        menu_bar = tk.Menu(main_window)
        operation_menu = tk.Menu(menu_bar, tearoff=0)
        operation_menu.add_command(label="Device Status", command=self.show_device_status)
        operation_menu.add_separator()
        operation_menu.add_command(label="Exit", command=main_window.quit)
        operation_menu.add_command(lable="Ready for srial?",command=self.open_Serial_Conection)
        menu_bar.add_cascade(label="Operations", menu=operation_menu)

        tk.Label(main_window, text="Enter Parameters", font=("Arial", 14)).pack(pady=10)
        mode_frame = tk.Frame(main_window)
        mode_frame.pack(pady=10)

        tk.Label(mode_frame, text="Mode:").grid(row=0, column=0, padx=5)
        mode_var = tk.StringVar(value="AOO")
        mode_dropdown = tk.OptionMenu(mode_frame, mode_var, "AOO", "VOO", "AAI", "VVI")
        mode_dropdown.grid(row=0, column=1, padx=5)

        tk.Label(main_window, text="Lower Rate Limit:").pack()
        entry_lrl = tk.Entry(main_window)
        entry_lrl.pack()

        tk.Label(main_window, text="Upper Rate Limit:").pack()
        entry_url = tk.Entry(main_window)
        entry_url.pack()

        tk.Label(main_window, text="Amplitude:").pack()
        entry_amplitude = tk.Entry(main_window)
        entry_amplitude.pack()

        tk.Label(main_window, text="Pulse Width:").pack()
        entry_pulse_width = tk.Entry(main_window)
        entry_pulse_width.pack()

        def save_parameters():
            try:
                mode = mode_var.get()
                lrl = float(entry_lrl.get())
                url = float(entry_url.get())
                amplitude = float(entry_amplitude.get())
                pulse_width = float(entry_pulse_width.get())

                if not (30 <= lrl <= 150):
                    raise ValueError("Lower Rate Limit must be between 30 and 150.")
                if not (50 <= url <= 180):
                    raise ValueError("Upper Rate Limit must be between 50 and 180.")
                if not (0.5 <= amplitude <= 5.0):
                    raise ValueError("Amplitude must be between 0.5V and 5.0V.")
                if not (0.05 <= pulse_width <= 1.9):
                    raise ValueError("Pulse Width must be between 0.05ms and 1.9ms.")
                if url <= lrl:
                    raise ValueError("Upper Rate Limit must be greater than Lower Rate Limit.")
                parameters = {
                    "Lower Rate Limit": lrl,
                    "Upper Rate Limit": url,
                    "Amplitude": amplitude,
                    "Pulse Width": pulse_width
                }
                self.data_storage.save_parameters(username, mode, parameters)
                messagebox.showinfo("Success", f"Parameters for {mode} saved successfully!")
            except ValueError as e:
                messagebox.showerror("Input Error", str(e))

        tk.Button(main_window, text="Save Parameters", command=save_parameters).pack(pady=10)
        main_window.config(menu=menu_bar)
        main_window.mainloop()

    def show_device_status(self):
        messagebox.showinfo("Device Status", "Device Connected: UNKNOWN\nPort: N/A")
    
    def open_Serial_Conection(self):
        tk.Label(self.root, text="button for connection detection").pack(pady=5)
