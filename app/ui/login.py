# app/ui/login.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
import db


class LoginWindow(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.setWindowTitle("Login")
        self.setMinimumWidth(320)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Enter your credentials"))

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        btn = QPushButton("Login")
        btn.clicked.connect(self.handle_login)
        layout.addWidget(btn)

        self.setLayout(layout)

    def handle_login(self):
        uname = self.username.text().strip()
        pw = self.password.text()

        if not uname or not pw:
            QMessageBox.warning(self, "Missing", "Please enter username and password.")
            return

        user = db.verify_login(uname, pw)
        if not user:
            QMessageBox.critical(self, "Login failed", "Invalid credentials or inactive account.")
            return

        self.on_login_success(user)
        self.close()
