# app/ui/super_admin_window.py
from PySide6.QtWidgets import QMainWindow, QLabel

class SuperAdminWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("Super Admin Dashboard")
        self.setCentralWidget(QLabel(f"Welcome Super Admin: {user['username']}"))
