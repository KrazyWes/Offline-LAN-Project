# app/ui/monitor/monitor_window.py
from PySide6.QtWidgets import QMainWindow, QLabel
from PySide6.QtCore import Qt

class MonitorWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("Monitor View (Read-only)")
        self.setMinimumSize(1024, 768)
        self.setWindowState(Qt.WindowMaximized)
        self.setCentralWidget(QLabel("Monitor view (read-only)\n(Monitor dashboard coming soon)"))
