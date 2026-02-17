# app/ui/register_super_admin.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFrame,
    QApplication,
    QGraphicsDropShadowEffect,
)

import db


class RegisterSuperAdminWindow(QWidget):
    """Same layout/style as login page, but no background image."""

    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.setWindowTitle("First-time Setup - Create Super Admin")
        self.setWindowFlags(Qt.Window)

        # Size: maximize to full available screen (same as login)
        screen = QApplication.primaryScreen()
        if screen:
            geom = screen.availableGeometry()
            w = geom.width()
            h = geom.height()
        else:
            w, h = 1920, 1080
        self.resize(w, h)
        if screen:
            self.move(geom.x(), geom.y())

        # Main layout (plain background, no image)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: #f0f2f5;")

        # Card overlay (same style as login)
        card = QFrame()
        card.setObjectName("registerCard")
        card.setFixedWidth(364)
        card.setStyleSheet("""
            QFrame#registerCard {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 12px;
                border: 1px solid rgba(0, 0, 0, 0.08);
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(Qt.darkGray)
        card.setGraphicsEffect(shadow)

        form = QVBoxLayout(card)
        form.setSpacing(16)
        form.setContentsMargins(32, 28, 32, 28)

        title = QLabel("Create Super Admin")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: 700; color: #1c1e21; selection-background-color: transparent;")
        form.addWidget(title)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name/Nickname")
        self.name.setFixedHeight(48)
        self.name.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 12px 14px;
                border: 1px solid #dddfe2;
                border-radius: 8px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1877f2;
                outline: none;
            }
        """)
        form.addWidget(self.name)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Super Admin username")
        self.username.setFixedHeight(48)
        self.username.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 12px 14px;
                border: 1px solid #dddfe2;
                border-radius: 8px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1877f2;
                outline: none;
            }
        """)
        form.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFixedHeight(48)
        self.password.setStyleSheet(self.username.styleSheet())
        form.addWidget(self.password)

        self.password2 = QLineEdit()
        self.password2.setPlaceholderText("Confirm password")
        self.password2.setEchoMode(QLineEdit.Password)
        self.password2.setFixedHeight(48)
        self.password2.setStyleSheet(self.username.styleSheet())
        form.addWidget(self.password2)

        btn = QPushButton("Create Super Admin")
        btn.setFixedHeight(48)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #1877f2;
                color: white;
                font-size: 18px;
                font-weight: 700;
                border: none;
                border-radius: 8px;
                selection-background-color: transparent;
            }
            QPushButton:hover {
                background-color: #166fe5;
            }
            QPushButton:pressed {
                background-color: #145dbf;
            }
        """)
        btn.clicked.connect(self.create_super_admin)
        self.name.returnPressed.connect(self.create_super_admin)
        self.username.returnPressed.connect(self.create_super_admin)
        self.password.returnPressed.connect(self.create_super_admin)
        self.password2.returnPressed.connect(self.create_super_admin)
        form.addWidget(btn)

        main_layout.addWidget(card, alignment=Qt.AlignCenter)

    def showEvent(self, event):
        super().showEvent(event)
        self.showMaximized()

    def create_super_admin(self):
        name = self.name.text().strip()
        uname = self.username.text().strip()
        pw1 = self.password.text()
        pw2 = self.password2.text()

        if not name:
            QMessageBox.warning(self, "Missing", "Please enter name.")
            return
        if not uname or not pw1:
            QMessageBox.warning(self, "Missing", "Please enter username and password.")
            return
        if pw1 != pw2:
            QMessageBox.warning(self, "Mismatch", "Passwords do not match.")
            return
        if db.username_exists(uname):
            QMessageBox.warning(self, "Taken", "Username already exists.")
            return

        ok = db.create_user(uname, pw1, "super_admin", name=name)
        if ok:
            QMessageBox.information(self, "Success", "Super Admin created. You can now log in.")
            self.on_success()
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Failed to create Super Admin. Check DB connection/logs.")
