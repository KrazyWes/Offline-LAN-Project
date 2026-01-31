from PySide6.QtWidgets import QMainWindow, QLabel

class MonitorWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("Monitor View (Read-only)")
        self.setCentralWidget(QLabel("Monitor view (read-only)"))
