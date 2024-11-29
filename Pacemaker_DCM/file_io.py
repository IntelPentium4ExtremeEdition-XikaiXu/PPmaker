import os

class FileIO:
    def __init__(self, base_path):
        self.base_path = base_path
        self.db_folder = os.path.join(self.base_path, "database")

        # 如果数据库文件夹不存在，则创建
        if not os.path.exists(self.db_folder):
            os.makedirs(self.db_folder)

    def save_user(self, username, password):
        """
        保存用户名和密码到文件
        """
        user_file_path = os.path.join(self.db_folder, f"{username}.txt")

        if os.path.exists(user_file_path):
            return False  # 用户名已存在

        with open(user_file_path, 'w') as file:
            file.write(f"Password: {password}\n")
        return True

    def load_user(self, username):
        """
        从文件加载用户信息
        """
        user_file_path = os.path.join(self.db_folder, f"{username}.txt")

        if not os.path.exists(user_file_path):
            return None  # 用户名不存在

        with open(user_file_path, 'r') as file:
            lines = file.readlines()

        user_data = {}
        for line in lines:
            if line.startswith("Password:"):
                user_data['password'] = line.split(":")[1].strip()

        return user_data
