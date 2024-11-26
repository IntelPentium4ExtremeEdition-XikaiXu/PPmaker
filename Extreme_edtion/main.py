import tkinter as tk
from tkinter import messagebox
from user_storage import UserStorage
from data_storage import ParameterReader

# Initialize UserStorage and ParameterReader
user_storage = UserStorage()
parameter_reader = ParameterReader()

# Load parameters from the data file
def load_user_parameters(username):
    try:
        user_data_file = user_storage.load_users()[username]
        with open(user_data_file, 'r') as file:
            user_data = json.load(file)
        return user_data['parameters']
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

# Register user
def register_user(username, password, parameters):
    try:
        user_storage.register_user(username, password, parameters)
        messagebox.showinfo("Success", "User registered successfully!")
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Login functionality
def login(username, password):
    try:
        user_data_file = user_storage.load_users()[username]
        with open(user_data_file, 'r') as file:
            user_data = json.load(file)

        if bcrypt.checkpw(password.encode('utf-8'), user_data['password'].encode('utf-8')):
            messagebox.showinfo("Success", "Login successful!")
            return user_data['parameters']
        else:
            messagebox.showerror("Error", "Incorrect password.")
            return None
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

# Main Function to drive the script
def main():
    # Example to register and login a user
    # This part is simulating a simple registration and login flow
    
    # Register user with username 'test_user', password 'password123', and default parameters
    default_parameters = parameter_reader.get_all_parameters()
    register_user('test_user', 'password123', default_parameters)

    # Login user with username 'test_user' and password 'password123'
    user_params = login('test_user', 'password123')
    if user_params:
        print("User Parameters:", user_params)
    else:
        print("Login failed.")

if __name__ == "__main__":
    main()
