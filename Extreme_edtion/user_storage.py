import json
import os
import bcrypt

class UserStorage:
    def __init__(self, users_filename='users.json', base_dir='user_data'):
        self.users_filename = users_filename
        self.base_dir = base_dir

        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

    def load_users(self):
        if os.path.exists(self.users_filename):
            with open(self.users_filename, 'r') as file:
                return json.load(file)
        return {}

    def save_users(self, users):
        with open(self.users_filename, 'w') as file:
            json.dump(users, file, indent=4)

    def create_user_directory(self, username):
        user_dir = os.path.join(self.base_dir, username)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        return user_dir

    def create_user_data_file(self, username, password, parameters):
        user_dir = self.create_user_directory(username)
        user_data_file = os.path.join(user_dir, 'data.json')
        user_data = {
            'password': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            'parameters': parameters
        }
        with open(user_data_file, 'w') as file:
            json.dump(user_data, file, indent=4)
        return user_data_file

    def register_user(self, username, password, parameters):
        users = self.load_users()

        if username in users:
            raise ValueError("Username already exists.")

        user_data_file = self.create_user_data_file(username, password, parameters)
        users[username] = user_data_file
        self.save_users(users)
