import tkinter as tk
from tkinter import messagebox
from application_window import ApplicationWindow
import os

class MainWindow:
    def __init__(self, root):
        # 设置主窗口
        self.root = root
        self.root.title("This is a Eemergency SOFTWARE")
        self.root.geometry("600x360")

        # 欢迎信息
        mainline = tk.Label(root, text="Quartz Extreme PPmaker")
        mainline.pack(pady=20)

        # 用户名输入框
        self.usrname = tk.Entry(root)
        self.usrname.insert(0, "Username")
        self.usrname.pack(pady=10)

        # 密码输入框
        self.password_input = tk.Entry(root)
        self.password_input.insert(0, "Password")
        self.password_input.pack(pady=10)

        # 按钮区域
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=15)

        # 注册按钮
        register_btn = tk.Button(btn_frame, text="注册", command=self.register_user, width=15)
        register_btn.pack(side=tk.LEFT, padx=5)

        # 登录按钮
        login_btn = tk.Button(btn_frame, text="登录", command=self.login_user, width=15)
        login_btn.pack(side=tk.LEFT, padx=5)

        # 退出按钮
        exit_btn = tk.Button(root, text="退出", command=self.root.quit, width=5)
        exit_btn.pack(side=tk.RIGHT, padx=20)

        # 成功信息标签
        self.success_msg = tk.Label(root, text="")
        self.success_msg.pack(pady=20)
        
        # 获取脚本目录路径
        self.base_path = os.path.dirname(os.path.abspath(__file__))  

    def register_user(self):
        """
        注册用户的函数
        """
        username = self.usrname.get().strip()  # 获取用户名并去掉多余空格
        password = self.password_input.get().strip()  # 获取密码并去掉多余空格

        if username and password:  # 检查用户名和密码是否为空
            # 检查或创建 database 文件夹
            db_folder = os.path.join(self.base_path, "database")  # 确保 database 文件夹位于脚本目录
            if not os.path.exists(db_folder):
                os.makedirs(db_folder)  # 如果文件夹不存在，创建文件夹

            # 构建用户文件路径
            user_file_path = os.path.join(db_folder, f"{username}.txt")

            if os.path.exists(user_file_path):  # 检查用户文件是否已存在
                messagebox.showwarning("错误", "用户名已存在！")
                return  # 用户名重复，直接返回

            # 创建以用户名命名的文件，并写入密码
            with open(user_file_path, 'w') as file:
                file.write(f"Password: {password}\n")  # 写入密码，未来可增加其他参数

            self.success_msg.config(text="注册成功！")  # 更新成功提示信息
            self.usrname.delete(0, tk.END)  # 清空用户名输入框
            self.password_input.delete(0, tk.END)  # 清空密码输入框
        else:
            messagebox.showwarning("错误", "请填写用户名和密码。")  # 用户名或密码为空，提示错误

    def login_user(self):
        """
        用户登录的函数
        """
        username = self.usrname.get().strip()  # 获取用户名并去掉多余空格
        password = self.password_input.get().strip()  # 获取密码并去掉多余空格

        if username and password:  # 检查用户名和密码是否为空
            # 构建用户文件路径
            db_folder = os.path.join(self.base_path, "database")
            user_file_path = os.path.join(db_folder, f"{username}.txt")

            if not os.path.exists(user_file_path):  # 检查用户文件是否存在
                messagebox.showwarning("错误", "用户名不存在。")  # 用户名不存在，提示错误
                return

            # 读取用户文件并验证密码
            with open(user_file_path, 'r') as file:
                lines = file.readlines()  # 读取文件的所有行

            stored_password = None
            for line in lines:
                if line.startswith("Password:"):  # 查找存储的密码行
                    stored_password = line.split(":")[1].strip()  # 提取密码

            if stored_password == password:  # 验证密码
                self.success_msg.config(text="登录成功！")  # 更新成功提示信息
                self.open_application_window(username)  # 打开应用窗口
            else:
                messagebox.showwarning("错误", "密码错误。")  # 密码错误，提示错误
        else:
            messagebox.showwarning("错误", "请填写用户名和密码。")  # 用户名或密码为空，提示错误
            

    def open_application_window(self, username):
        """
        打开应用程序窗口
        """
        app_window = tk.Toplevel(self.root)
        ApplicationWindow(app_window, username)
        self.root.withdraw()


def main():
    """
    主程序入口
    """
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
