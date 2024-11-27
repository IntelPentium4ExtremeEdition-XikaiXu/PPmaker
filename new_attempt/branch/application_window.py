import tkinter as tk
from tkinter import ttk, messagebox
from PPmaker.new_attempt.branch.ParameterManager import ParameterManager


class ApplicationWindow:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Pacing Mode Selection")
        self.root.geometry("1000x700")

        # User-specific parameter manager
        self.username = username
        self.parameter_manager = ParameterManager()

        # Header
        header_frame = tk.Frame(root)
        header_frame.pack(pady=10, fill=tk.X)

        user_label = tk.Label(header_frame, text=f"Logged in as: {username}", font=("Arial", 12))
        user_label.pack(side=tk.LEFT, padx=10)

        exit_button = tk.Button(header_frame, text="Exit", command=root.quit)
        exit_button.pack(side=tk.RIGHT, padx=10)

        # Pacing Mode Selection
        mode_frame = tk.Frame(root)
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

        # Parameter Fields
        self.fields = {}
        param_frame = tk.Frame(root)
        param_frame.pack(pady=20)

        for i, field_name in enumerate([
            "Lower Rate Limit", "Upper Rate Limit", "Atrial Amplitude", "Atrial Pulse Width",
            "Ventricular Amplitude", "Ventricular Pulse Width", "VRP", "ARP", "PVARP",
            "Maximum Sensor Rate", "Fixed AV Delay", "Ventricular Sensitivity",
            "Hysteresis", "Rate Smoothing", "Activity Threshold", "Reaction Time",
            "Response Factor", "Recovery Time"
        ]):
            label = tk.Label(param_frame, text=f"{field_name}:", font=("Arial", 10))
            entry = tk.Entry(param_frame, font=("Arial", 10))
            label.grid(row=i, column=0, sticky=tk.E, padx=10, pady=5)
            entry.grid(row=i, column=1, sticky=tk.W, padx=10, pady=5)
            self.fields[field_name] = entry

        # Apply Button
        apply_button = tk.Button(root, text="Apply", command=self.apply_parameters)
        apply_button.pack(pady=10)

        # Connection Status
        self.status_label = tk.Label(root, text="Device not connected", font=("Arial", 12), fg="red")
        self.status_label.pack(pady=10)

    def update_parameters(self, event=None):
        mode = self.pacing_mode_var.get()
        # Add visibility logic if needed

    def apply_parameters(self):
        try:
            for field_name, entry in self.fields.items():
                value = entry.get()
                print(f"{field_name}: {value}")
            messagebox.showinfo("Success", "Parameters applied successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
