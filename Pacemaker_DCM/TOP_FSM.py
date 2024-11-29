import tkinter as tk
from tkinter import messagebox
import os
from file_io import FileIO
from main import ApplicationWindow

class MainWindow:
    def __init__(self, root):
        # 设置主窗口
        self.root = root
        self.root.title("This is a Eemergency SOFTWARE")
        self.root.geometry("600x360")

        # 初始化 FileIO
        self.file_io = FileIO(os.path.dirname(os.path.abspath(__file__)))

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
        register_btn = tk.Button(btn_frame, text="signed", command=self.register_user, width=15)
        register_btn.pack(side=tk.LEFT, padx=5)

        # 登录按钮
        login_btn = tk.Button(btn_frame, text="login", command=self.login_user, width=15)
        login_btn.pack(side=tk.LEFT, padx=5)

        # 退出按钮
        exit_btn = tk.Button(root, text="quit", command=self.root.quit, width=5)
        exit_btn.pack(side=tk.RIGHT, padx=20)

        # 成功信息标签
        self.success_msg = tk.Label(root, text="ACT")
        self.success_msg.pack(pady=20)

    def register_user(self):
        """
        注册用户的函数
        """
        username = self.usrname.get().strip()
        password = self.password_input.get().strip()

        if username and password:
            success = self.file_io.save_user(username, password)
            if success:
                self.success_msg.config(text="sign success")
                self.usrname.delete(0, tk.END)
                self.password_input.delete(0, tk.END)
            else:
                messagebox.showwarning("error, user has already in the database")
        else:
            messagebox.showwarning("error please input username or password")

    def login_user(self):
        """
        用户登录的函数
        """
        username = self.usrname.get().strip()
        password = self.password_input.get().strip()

        if username and password:
            user_data = self.file_io.load_user(username)
            if not user_data:
                messagebox.showwarning("error", "no user account")
                return

            if user_data.get('password') == password:
                self.success_msg.config(text="login in success")
                self.open_application_window(username)
            else:
                messagebox.showwarning("error no passwordW")
        else:
            messagebox.showwarning("error", "please input password")
            
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
