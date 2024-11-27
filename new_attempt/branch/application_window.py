import tkinter as tk
from tkinter import ttk, messagebox
import pickle
from PPmaker.new_attempt.branch.ParameterManager import ParameterManager


class ApplicationWindow:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Pacing Mode Selection")
        self.root.geometry("1000x700")

        # User-related information and parameter management
        self.username = username
        self.parameter_manager = ParameterManager()
        self.user_parameters = self.load_user_parameters()

        # Layout creation
        self.create_header()
        self.create_mode_selection()
        self.create_parameter_fields()
        self.create_apply_button()
        self.create_status_display()

    def create_header(self):
        """Create the header area with username display and exit button."""
        header_frame = tk.Frame(self.root)
        header_frame.pack(pady=10, fill=tk.X)

        user_label = tk.Label(header_frame, text=f"Logged in as: {self.username}", font=("Arial", 12))
        user_label.pack(side=tk.LEFT, padx=10)

        exit_button = tk.Button(header_frame, text="Exit", command=self.root.quit)
        exit_button.pack(side=tk.RIGHT, padx=10)

    def create_mode_selection(self):
        """Create a dropdown menu for selecting pacing mode."""
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
        """Create fields for parameters."""
        self.fields = {}
        param_frame = tk.Frame(self.root)
        param_frame.pack(pady=20)

        field_names = [
            "Lower Rate Limit", "Upper Rate Limit", "Atrial Amplitude", "Atrial Pulse Width",
            "Ventricular Amplitude", "Ventricular Pulse Width", "VRP", "ARP", "PVARP",
            "Maximum Sensor Rate", "Fixed AV Delay", "Ventricular Sensitivity",
            "Hysteresis", "Rate Smoothing", "Activity Threshold", "Reaction Time",
            "Response Factor", "Recovery Time"
        ]

        for i, field_name in enumerate(field_names):
            label = tk.Label(param_frame, text=f"{field_name}:", font=("Arial", 10))
            entry = tk.Entry(param_frame, font=("Arial", 10))
            label.grid(row=i, column=0, sticky=tk.E, padx=10, pady=5)
            entry.grid(row=i, column=1, sticky=tk.W, padx=10, pady=5)
            self.fields[field_name] = entry

    def create_apply_button(self):
        """Create a button to apply parameters."""
        apply_button = tk.Button(self.root, text="Apply", command=self.apply_parameters)
        apply_button.pack(pady=10)

    def create_status_display(self):
        """Create a display to show connection status."""
        self.status_label = tk.Label(self.root, text="Device not connected", font=("Arial", 12), fg="red")
        self.status_label.pack(pady=10)

    def update_parameters(self, event=None):
        """Update the visibility of parameter fields based on selected mode."""
        mode = self.pacing_mode_var.get()
        relevant_fields = self.get_relevant_parameters_for_mode(mode)
        for field_name, entry in self.fields.items():
            entry.config(state=tk.NORMAL if field_name in relevant_fields else tk.DISABLED)

    def apply_parameters(self):
        """Apply parameters to the ParameterManager."""
        try:
            for field_name, entry in self.fields.items():
                value = entry.get()
                if value:
                    setattr(self.parameter_manager, f"set{field_name.replace(' ', '')}", value)
            messagebox.showinfo("Success", "Parameters applied successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_relevant_parameters_for_mode(self, mode):
        """Retrieve relevant parameters for the selected mode."""
        relevant_params = {
            "AOO": ["Lower Rate Limit", "Upper Rate Limit", "Atrial Amplitude", "Atrial Pulse Width"],
            "AAI": ["Lower Rate Limit", "Upper Rate Limit", "Atrial Amplitude", "Atrial Pulse Width", "ARP"],
            # Add more modes as per the actual protocol
        }
        return relevant_params.get(mode, [])

    def load_user_parameters(self):
        """Load user parameters."""
        try:
            with open("users.dat", "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return {}

    def save_user_parameters(self):
        """Save user parameters."""
        self.user_parameters[self.username] = self.parameter_manager
        with open("users.dat", "wb") as file:
            pickle.dump(self.user_parameters, file)


if __name__ == "__main__":
    root = tk.Tk()
    app = ApplicationWindow(root, username="test_user")
    root.mainloop()
