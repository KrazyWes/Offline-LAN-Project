# app/ui/admin_window.py
from PySide6.QtWidgets import QMainWindow, QLabel

class AdminWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        self.setCentralWidget(QLabel(f"Welcome Admin: {user['username']}"))
