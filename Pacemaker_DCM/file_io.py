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
    
    def write_parameter(self, values, username, mode):
        """
        将参数值写入与用户名关联的文件中，且仅覆盖当前模式的值。
        参数 'values' 期望是一个字段名称及其对应值的字典。
        """
        user_file_path = os.path.join(self.db_folder, f"{username}.txt")

        # 如果用户文件不存在，返回 False（无法写入）
        if not os.path.exists(user_file_path):
            return False

        # 先读取文件中的内容，保存原有的密码和模式部分
        with open(user_file_path, 'r') as file:
            lines = file.readlines()

        password = None
        existing_parameters = {}
        mode_section = None
        # 提取密码和已有的模式参数部分
        for i, line in enumerate(lines):
            if line.startswith("Password:"):
                password = line.strip()
            elif line.strip() == "Parameters:":
                # 从 "Parameters:" 之后开始查找参数
                parameter_section = True
                continue
            elif parameter_section:
                if line.strip():  # 如果当前行有内容
                    if line.startswith("Mode:"):
                        mode_section = line.strip().split(":")[1].strip()  # 获取当前存储的模式
                    else:
                        key, value = line.split(":", 1)  # 按 ": " 分割
                        existing_parameters[key.strip()] = value.strip()

        # 如果当前文件中有该模式的参数，更新该模式的参数
        if mode_section and mode == mode_section:
            # 只更新与当前模式相关的参数
            existing_parameters.update(values)
        else:
            # 没有该模式，或者模式不同，保持原模式值
            existing_parameters["Mode"] = mode
            existing_parameters.update(values)

        # 重写文件，确保不覆盖密码，更新参数
        with open(user_file_path, 'w') as file:
            if password:
                file.write(f"{password}\n")

            file.write("\nParameters:\n")
            file.write(f"Mode: {mode}\n")
            for key, value in existing_parameters.items():
                if key != "Mode":
                    file.write(f"{key}: {value}\n")

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
        mode = None
        for line in lines:
            # 发现 "Parameters" 字段后，开始读取参数
            if line.strip() == "Parameters:":
                parameter_section = True
                continue  # Skip the "Parameters:" line
            if parameter_section:
                if line.startswith("Mode:"):
                    mode = line.split(":")[1].strip()  # 获取存储的模式
                elif line.strip():  # 如果当前行有内容
                    key, value = line.split(":", 1)  # 按 ": " 分割
                    parameters[key.strip()] = value.strip()

        if mode:
            parameters["Mode"] = mode

        return parameters