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
    
    def write_parameter(self, values, username):
        """
        将参数值写入与用户名关联的文件中。
        参数 'values' 期望是一个字段名称及其对应值的字典。
        """
        user_file_path = os.path.join(self.db_folder, f"{username}.txt")

        # 如果用户文件不存在，返回 False（无法写入）
        if not os.path.exists(user_file_path):
            return False

        # 先读取文件中的内容，保存原有的密码部分
        with open(user_file_path, 'r') as file:
            lines = file.readlines()

        password = None
        # 提取密码部分
        for line in lines:
            if line.startswith("Password:"):
                password = line.strip()
                break

        # 如果密码部分存在，将其保留下来，写入新的参数部分
        with open(user_file_path, 'w') as file:
            # 如果密码部分存在，先写入密码
            if password:
                file.write(f"{password}\n")
            
            # 然后将参数值写入文件
            file.write("\nParameters:\n")
            for key, value in values.items():
                file.write(f"{key}: {value}\n")
                print(value)
        return True

    def load_parameter(self, username):
        """
        从文件中加载并返回与用户名关联的参数值。
        返回的是一个字典，包含所有的参数字段和值。
        """
        user_file_path = os.path.join(self.db_folder, f"{username}.txt")

        # 如果文件不存在，返回 None
        if not os.path.exists(user_file_path):
            return None

        parameters = {}

        with open(user_file_path, 'r') as file:
            lines = file.readlines()

        # 查找 "Parameters" 之后的字段和值
        parameter_section = False
        for line in lines:
            # 发现 "Parameters" 字段后，开始读取参数
            if line.strip() == "Parameters:":
                parameter_section = True
                continue  # Skip the "Parameters:" line
            if parameter_section:
                if line.strip():  # 如果当前行有内容
                    key, value = line.split(":", 1)  # 按 ": " 分割
                    parameters[key.strip()] = value.strip()

        return parameters