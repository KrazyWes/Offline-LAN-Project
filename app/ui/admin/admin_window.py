# app/ui/admin/admin_window.py
from PySide6.QtWidgets import QMainWindow, QLabel
from PySide6.QtCore import Qt

class AdminWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("Admin Dashboard")
        self.setMinimumSize(1024, 768)
        self.setWindowState(Qt.WindowMaximized)
        self.setCentralWidget(QLabel(f"Welcome Admin: {user['username']}\n(Admin dashboard coming soon)"))
