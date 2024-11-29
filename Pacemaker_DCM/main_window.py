import tkinter as tk
from tkinter import ttk, messagebox
from application_window import ApplicationWindow


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome Window")
        self.root.geometry("800x600")

        # Welcome Label
        welcome_msg = tk.Label(root, text="Hello, Welcome to Pacemaker Control System", font=("Arial", 14))
        welcome_msg.pack(pady=20)

        # Username input
        self.username_input = tk.Entry(root, font=("Arial", 12))
        self.username_input.insert(0, "Enter your username")
        self.username_input.pack(pady=10)

        # Password input
        self.password_input = tk.Entry(root, font=("Arial", 12), show="*")
        self.password_input.insert(0, "Enter your password")
        self.password_input.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        register_btn = tk.Button(btn_frame, text="Register", command=self.register_user, width=15)
        register_btn.grid(row=0, column=0, padx=5)

        login_btn = tk.Button(btn_frame, text="Log In", command=self.login_user, width=15)
        login_btn.grid(row=0, column=1, padx=5)

        delete_btn = tk.Button(btn_frame, text="Delete User", command=self.delete_user, width=15)
        delete_btn.grid(row=0, column=2, padx=5)

        exit_btn = tk.Button(root, text="Exit", command=self.root.quit, width=15)
        exit_btn.pack(pady=10)

        # Success message
        self.success_msg = tk.Label(root, text="", font=("Arial", 12), fg="green")
        self.success_msg.pack(pady=10)

    def register_user(self):
        username = self.username_input.get()
        password = self.password_input.get()

        if username and password:
            try:
                with open('users.txt', 'r') as file:
                    users = file.readlines()

                if len(users) >= 10:
                    messagebox.showwarning("Error", "Maximum number of users reached (10 users).")
                    return
            except FileNotFoundError:
                pass

            with open('users.txt', 'a') as file:
                file.write(f"{username},{password}\n")

            self.success_msg.config(text="User registered successfully!")
            self.username_input.delete(0, tk.END)
            self.password_input.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Please fill in both fields.")

    def login_user(self):
        username = self.username_input.get()
        password = self.password_input.get()

        if username and password:
            try:
                with open('users.txt', 'r') as file:
                    users = file.readlines()

                for user in users:
                    stored_username, stored_password = user.strip().split(',')
                    if stored_username == username and stored_password == password:
                        self.success_msg.config(text="Login successful!")
                        self.open_application_window(username)
                        return

                messagebox.showwarning("Error", "Invalid username or password.")
            except FileNotFoundError:
                messagebox.showwarning("Error", "No users registered yet.")
        else:
            messagebox.showwarning("Error", "Please fill in both fields.")

    def delete_user(self):
        username = self.username_input.get()
        password = self.password_input.get()

        if username and password:
            try:
                with open('users.txt', 'r') as file:
                    users = file.readlines()

                with open('users.txt', 'w') as file:
                    user_found = False
                    for user in users:
                        stored_username, stored_password = user.strip().split(',')
                        if stored_username == username and stored_password == password:
                            user_found = True
                        else:
                            file.write(user)

                    if user_found:
                        self.success_msg.config(text="User deleted successfully!")
                    else:
                        messagebox.showwarning("Error", "User not found.")
            except FileNotFoundError:
                messagebox.showwarning("Error", "No users registered yet.")
        else:
            messagebox.showwarning("Error", "Please fill in both fields.")

    def open_application_window(self, username):
        app_window = tk.Toplevel(self.root)
        ApplicationWindow(app_window, username)


def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
