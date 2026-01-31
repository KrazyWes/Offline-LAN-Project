# app/ui/teller_window.py
from PySide6.QtWidgets import QMainWindow, QLabel

class TellerWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("Teller Dashboard")
        self.setCentralWidget(QLabel(f"Welcome Teller: {user['username']}"))
