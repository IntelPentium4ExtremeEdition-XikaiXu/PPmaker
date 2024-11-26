import bcrypt
import json
import os


class UserManager:
    data_root = "data/"
    invite_code = "123456"
    def __init__(self):
        if not os.path.exists(self.data_root):
            os.makedirs(self.data_root)
    def _get_user_directory(self, username):
        return os.path.join(self.data_root, username)
    def _get_user_data_file(self, username):
        return os.path.join(self._get_user_directory(username), "user_data.json")
    
    def register_user(self, username, password, invite_code):
        if invite_code != self.invite_code:
            return False, "Wrong invite Code LOL."
        user_dir = self._get_user_directory(username)
        if os.path.exists(user_dir):
            return False, "Username already exists."
        if len(password) < 6:
            return False, "Password must be at least 6 characters long."
        os.makedirs(user_dir)
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user_data = {
            "password": hashed_password.decode("utf-8"),
            "parameters": {
                "AOO": [],
                "VOO": [],
                "AAI": [],
                "VVI": [],
            },
        }
        
        with open(self._get_user_data_file(username), "w") as file:
            json.dump(user_data, file, indent=4)

        return True, "Registration successful!"

    def authenticate_user(self, username, password):
        user_data_file = self._get_user_data_file(username)
        if not os.path.exists(user_data_file):
            return False, "User does not exist."

        with open(user_data_file, "r") as file:
            user_data = json.load(file)

        if bcrypt.checkpw(password.encode("utf-8"), user_data["password"].encode("utf-8")):
            return True, f"Login successful! User: {username}"
        return False, "Incorrect username or password!"


class ParameterManager:
    def __init__(self, username):
        self.user_dir = os.path.join("data", username)
        self.user_data_file = os.path.join(self.user_dir, "user_data.json")
        if not os.path.exists(self.user_data_file):
            raise FileNotFoundError(f"No data found for user {username}.")
    def load_parameters(self):
        with open(self.user_data_file, "r") as file:
            user_data = json.load(file)
        return user_data.get("parameters", {})
    def save_parameters(self, mode, data):
        with open(self.user_data_file, "r") as file:
            user_data = json.load(file)
        if "parameters" not in user_data:
            user_data["parameters"] = {}
        if mode not in user_data["parameters"]:
            user_data["parameters"][mode] = []
        user_data["parameters"][mode].append(data)
        with open(self.user_data_file, "w") as file:
            json.dump(user_data, file, indent=4)
