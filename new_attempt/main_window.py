import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from application_window import ApplicationWindow  

# Main Class to customize pacemaker's welcome window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
    
        # Set the window title
        self.setWindowTitle("Welcom Window")

        # Set the dimensions of the main window
        self.setFixedSize(QSize(800, 600))

        # Load images and set size
        mac_img = QPixmap("mac.png").scaled(600, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        fireball_img = QPixmap("fireball.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        # Create QLabel for welcome msg
        msg = QLabel('Hello, Welcome to Pacemaker Control System')
        msg.setFont(QFont('Arial', 14))

        # Create QLabel widgets to display the images
        mac_label = QLabel()
        mac_label.setPixmap(mac_img if not mac_img.isNull() else QPixmap())

        fireball_label = QLabel()
        fireball_label.setPixmap(fireball_img if not fireball_img.isNull() else QPixmap())

        # Create user registration, login, and delete existing user input line
        self.username_input = QLineEdit()
        self.username_input.setFixedSize(400, 40)
        self.username_input.setPlaceholderText("Enter your username")

        self.password_input = QLineEdit()
        self.password_input.setFixedSize(400, 40)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Create buttons:
        # registration
        self.register = QPushButton("Register")
        self.register.setFixedSize(100, 40)
        self.register.clicked.connect(self.register_user)
        # login
        self.login = QPushButton("Log In")
        self.login.setFixedSize(100, 40)
        self.login.clicked.connect(self.login_user)
        # Delete users
        self.delete = QPushButton("Delete User")
        self.delete.setFixedSize(100, 40)
        self.delete.clicked.connect(self.delete_user)
        # Exit button
        self.exit = QPushButton("Exit")
        self.exit.setFixedSize(100, 40)
        self.exit.clicked.connect(self.exit_program)

        # Connect the Enter key to log in button
        shortcut = QShortcut(QKeySequence(Qt.Key.Key_Return), self)  # Key_Return refers to enter key
        shortcut.activated.connect(self.login.click)

        # Create a layout and add the widgets
        main_layout = QVBoxLayout()  # Vertical layout

        # Create a top and horizontal layout to hold images
        img_layout = QHBoxLayout()
        img_layout.addWidget(mac_label, alignment=Qt.AlignmentFlag.AlignLeft)
        img_layout.addWidget(fireball_label, alignment=Qt.AlignmentFlag.AlignRight)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.register, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        button_layout.addWidget(self.login, alignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignTop)
        button_layout.addWidget(self.delete, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Success message QLabel
        self.success_msg = QLabel("")
        self.success_msg.setFont(QFont('Arial', 12))
        self.success_msg.setStyleSheet("color: green;")  # Set the color to green for success messages

        # Arrange layout vertical order and combine them together
        main_layout.addLayout(img_layout)
        main_layout.addWidget(msg, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        main_layout.addWidget(self.username_input, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        main_layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.success_msg, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(self.exit, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        # Set the layout for the central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def register_user(self):
        # Get username and password
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            # Check if the maximum number of users has been reached
            try:
                with open('users.txt', 'r') as file:
                    lines = file.readlines()

                if len(lines) >= 10:
                    QMessageBox.warning(self, "Error", "Maximum number of users reached (10 users).")
                    return
            except FileNotFoundError:
                # File doesn't exist yet, so no users are registered
                pass

            # Store the credentials in a text file
            with open('users.txt', 'a') as file:
                file.write(f"{username},{password}\n")

            # Display success message
            self.success_msg.setText("User registered successfully!")

            # Clear input fields
            self.username_input.clear()
            self.password_input.clear()
        else:
            # Display error message if fields are not filled
            QMessageBox.warning(self, "Error", "Please fill in both fields.")

    def delete_user(self):
        # Get username and password
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            # Read the existing users from the file
            try:
                with open('users.txt', 'r') as file:
                    lines = file.readlines()

                # Write back all users except the one to be deleted
                with open('users.txt', 'w') as file:
                    user_found = False
                    for line in lines:
                        stored_username, stored_password = line.strip().split(',')
                        if stored_username == username and stored_password == password:
                            user_found = True
                            continue  # Skip writing this user to the file
                        file.write(line)

                if user_found:
                    self.success_msg.setText("User deleted successfully!")
                else:
                    QMessageBox.warning(self, "Error", "User not found.")
            except FileNotFoundError:
                QMessageBox.warning(self, "Error", "No users registered yet.")
        else:
            # Display error message if fields are not filled
            QMessageBox.warning(self, "Error", "Please fill in both fields.")

    def login_user(self):
        # Get username and password
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            try:
                with open('users.txt', 'r') as file:
                    lines = file.readlines()

                # Check if user credentials match any registered user
                for line in lines:
                    stored_username, stored_password = line.strip().split(',')
                    if stored_username == username and stored_password == password:
                        self.success_msg.setText("Login successful!")
                        self.open_application_window(username)
                        return

                QMessageBox.warning(self, "Error", "Invalid username or password.")
            except FileNotFoundError:
                QMessageBox.warning(self, "Error", "No users registered yet.")
        else:
            QMessageBox.warning(self, "Error", "Please fill in both fields.")

    def open_application_window(self, username):
        # Don't hide the log in window so more user can be logged in
        # Open the main application window and pass the username
        self.app_window = ApplicationWindow(username)
        self.app_window.show()

    def exit_program(self):
        QApplication.quit()

# Main function to run the application
def main():
    app = QApplication(sys.argv) # Create an instance of QApplication
    window = MainWindow()
    window.show()  # Show the main window
    sys.exit(app.exec()) # Start the application's event loop

if __name__ == "__main__":
    main()