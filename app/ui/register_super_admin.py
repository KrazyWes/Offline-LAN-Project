# app/ui/register_super_admin.py
"""Same UI concept as Create/Edit Account modals - compact, centered card (not draggable)."""

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

# Same styling as Create/Edit Account modals in accounts_overview
_INPUT_STYLE = """
    QLineEdit {
        font-size: 15px;
        padding: 10px 12px;
        border: 1px solid #dddfe2;
        border-radius: 8px;
        background-color: white;
    }
    QLineEdit:focus {
        border-color: #1877f2;
        outline: none;
    }
"""
_BTN_PRIMARY = """
    QPushButton {
        background-color: #1877f2;
        color: white;
        font-size: 16px;
        font-weight: 600;
        border: none;
        border-radius: 8px;
    }
    QPushButton:hover { background-color: #166fe5; }
    QPushButton:pressed { background-color: #145dbf; }
"""


class RegisterSuperAdminWindow(QWidget):
    """Same UI concept as Create/Edit Account modals - centered card, not draggable."""

    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.setWindowTitle("First-time Setup - Create Super Admin")
        self.setWindowFlags(Qt.Window)

        screen = QApplication.primaryScreen()
        if screen:
            geom = screen.availableGeometry()
            w, h = geom.width(), geom.height()
        else:
            w, h = 1920, 1080
        self.resize(w, h)
        if screen:
            self.move(geom.x(), geom.y())

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: #f0f2f5;")

        # Card (same style as Create/Edit modals - centered, not draggable)
        card = QFrame()
        card.setObjectName("registerCard")
        card.setFixedWidth(420)
        card.setStyleSheet("""
            QFrame#registerCard {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #f3f4f6;
            }
            QFrame#registerCard QLabel {
                background-color: transparent;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(Qt.darkGray)
        card.setGraphicsEffect(shadow)

        form = QVBoxLayout(card)
        form.setSpacing(6)
        form.setContentsMargins(24, 20, 24, 20)

        _err = "color: #DC2626; font-size: 12px;"
        _err_h = 14

        title = QLabel("Create Super Admin")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: 600; color: #1c1e21; background-color: transparent;")
        form.addWidget(title)
        form.addSpacing(4)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name/Nickname")
        self.name.setFixedHeight(40)
        self.name.setStyleSheet(_INPUT_STYLE)
        self.name_error = QLabel()
        self.name_error.setStyleSheet(_err)
        self.name_error.setFixedHeight(_err_h)
        form.addWidget(self.name)
        form.addWidget(self.name_error)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Super Admin username")
        self.username.setFixedHeight(40)
        self.username.setStyleSheet(_INPUT_STYLE)
        self.username_error = QLabel()
        self.username_error.setStyleSheet(_err)
        self.username_error.setFixedHeight(_err_h)
        form.addWidget(self.username)
        form.addWidget(self.username_error)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFixedHeight(40)
        self.password.setStyleSheet(_INPUT_STYLE)
        self.password_error = QLabel()
        self.password_error.setStyleSheet(_err)
        self.password_error.setFixedHeight(_err_h)
        form.addWidget(self.password)
        form.addWidget(self.password_error)

        self.password2 = QLineEdit()
        self.password2.setPlaceholderText("Confirm password")
        self.password2.setEchoMode(QLineEdit.Password)
        self.password2.setFixedHeight(40)
        self.password2.setStyleSheet(_INPUT_STYLE)
        self.password2_error = QLabel()
        self.password2_error.setStyleSheet(_err)
        self.password2_error.setFixedHeight(_err_h)
        form.addWidget(self.password2)
        form.addWidget(self.password2_error)

        form.addSpacing(4)
        btn = QPushButton("Create Super Admin")
        btn.setFixedHeight(40)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(_BTN_PRIMARY)
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

    def _clear_errors(self):
        self.name_error.setText("")
        self.username_error.setText("")
        self.password_error.setText("")
        self.password2_error.setText("")

    def create_super_admin(self):
        self._clear_errors()
        name = self.name.text().strip()
        uname = self.username.text().strip()
        pw1 = self.password.text()
        pw2 = self.password2.text()

        has_error = False
        if not name:
            self.name_error.setText("Name is required")
            has_error = True
        elif len(name) < 2:
            self.name_error.setText("Name must be at least 2 characters")
            has_error = True

        if not uname:
            self.username_error.setText("Username is required")
            has_error = True
        elif len(uname) < 3:
            self.username_error.setText("Username must be at least 3 characters")
            has_error = True
        elif db.username_exists(uname):
            self.username_error.setText("Username already exists")
            has_error = True

        if not pw1:
            self.password_error.setText("Password is required")
            has_error = True
        elif len(pw1) < 3:
            self.password_error.setText("Password must be at least 3 characters")
            has_error = True

        if pw1 != pw2:
            self.password2_error.setText("Passwords do not match")
            has_error = True

        if has_error:
            return

        ok = db.create_user(uname, pw1, "super_admin", name=name)
        if ok:
            QMessageBox.information(self, "Success", "Super Admin created. You can now log in.")
            self.on_success()
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Failed to create Super Admin. Check DB connection/logs.")
