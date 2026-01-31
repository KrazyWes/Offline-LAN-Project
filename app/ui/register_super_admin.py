# app/ui/register_super_admin.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
import db


class RegisterSuperAdminWindow(QWidget):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.setWindowTitle("First-time Setup - Create Super Admin")
        self.setMinimumWidth(360)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("No Super Admin found.\nCreate the first Super Admin account."))

        self.username = QLineEdit()
        self.username.setPlaceholderText("Super Admin username")
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        self.password2 = QLineEdit()
        self.password2.setPlaceholderText("Confirm password")
        self.password2.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password2)

        btn = QPushButton("Create Super Admin")
        btn.clicked.connect(self.create_super_admin)
        layout.addWidget(btn)

        self.setLayout(layout)

    def create_super_admin(self):
        uname = self.username.text().strip()
        pw1 = self.password.text()
        pw2 = self.password2.text()

        if not uname or not pw1:
            QMessageBox.warning(self, "Missing", "Please enter username and password.")
            return
        if pw1 != pw2:
            QMessageBox.warning(self, "Mismatch", "Passwords do not match.")
            return
        if db.username_exists(uname):
            QMessageBox.warning(self, "Taken", "Username already exists.")
            return

        ok = db.create_user(uname, pw1, "super_admin")
        if ok:
            QMessageBox.information(self, "Success", "Super Admin created. You can now log in.")
            self.on_success()
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Failed to create Super Admin. Check DB connection/logs.")
