# app/ui/login.py
from pathlib import Path

from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QCheckBox,
    QFrame,
    QApplication,
    QGraphicsDropShadowEffect,
)

import db

# Path to background image relative to app/ui
_BG_PATH = Path(__file__).resolve().parent.parent / "assets" / "backgrounds" / "rooster_squad_1.png"
_BG_WIDTH = 1920
_BG_HEIGHT = 1080
_SETTINGS_KEY_REMEMBER = "login/remember_username"
_SETTINGS_KEY_USERNAME = "login/username"


def save_remembered_username(username: str) -> None:
    """Save username when user logs out, so it is pre-filled on next login."""
    settings = QSettings()
    settings.setValue(_SETTINGS_KEY_REMEMBER, True)
    settings.setValue(_SETTINGS_KEY_USERNAME, username or "")
    settings.sync()


class LoginWindow(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.setWindowTitle("Login")

        # Standard window with title bar (close, minimize, maximize buttons)
        self.setWindowFlags(Qt.Window)

        # Size: maximize to full available screen
        screen = QApplication.primaryScreen()
        if screen:
            geom = screen.availableGeometry()
            w = geom.width()
            h = geom.height()
        else:
            w, h = _BG_WIDTH, _BG_HEIGHT
        self.resize(w, h)
        self.setObjectName("loginWindow")

        # Center on screen
        if screen:
            cx = geom.x()
            cy = geom.y()
            self.move(cx, cy)

        # Background label (load from bytes to avoid Qt file path / pixmap creation errors)
        self._bg_label = QLabel(self)
        self._bg_label.setScaledContents(True)
        self._bg_label.setGeometry(0, 0, w, h)
        self._bg_label.lower()
        _load_background_pixmap(self._bg_label, w, h)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignCenter)

        # Login card overlay (Facebook-style)
        card = QFrame()
        card.setObjectName("loginCard")
        card.setFixedWidth(364)
        card.setStyleSheet("""
            QFrame#loginCard {
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

        title = QLabel("Sign In")
        title.setStyleSheet("font-size: 22px; font-weight: 600; color: #1c1e21;")
        form.addWidget(title)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
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

        self.remember_check = QCheckBox("Remember username")
        self.remember_check.setChecked(True)
        self.remember_check.setStyleSheet("font-size: 14px; color: #1c1e21;")
        form.addWidget(self.remember_check)

        btn = QPushButton("Log In")
        btn.setFixedHeight(48)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #1877f2;
                color: white;
                font-size: 18px;
                font-weight: 600;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #166fe5;
            }
            QPushButton:pressed {
                background-color: #145dbf;
            }
        """)
        btn.clicked.connect(self.handle_login)
        self.username.returnPressed.connect(self.handle_login)
        self.password.returnPressed.connect(self.handle_login)
        form.addWidget(btn)

        main_layout.addWidget(card, alignment=Qt.AlignCenter)
        self._bg_label.lower()  # Ensure background stays behind card

        # Load remembered username
        self._load_remembered_username()

    def showEvent(self, event):
        super().showEvent(event)
        self.showMaximized()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        s = self.size()
        self._bg_label.setGeometry(0, 0, s.width(), s.height())
        _load_background_pixmap(self._bg_label, s.width(), s.height())

    def _load_remembered_username(self):
        settings = QSettings()
        remember = settings.value(_SETTINGS_KEY_REMEMBER, True)
        if remember in (True, "true", 1, "1"):
            uname = settings.value(_SETTINGS_KEY_USERNAME, "")
            if uname:
                self.username.setText(str(uname))

    def _save_remembered_username(self):
        settings = QSettings()
        if self.remember_check.isChecked():
            settings.setValue(_SETTINGS_KEY_REMEMBER, True)
            settings.setValue(_SETTINGS_KEY_USERNAME, self.username.text().strip())
        else:
            settings.setValue(_SETTINGS_KEY_REMEMBER, False)
            settings.remove(_SETTINGS_KEY_USERNAME)

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

        db.update_last_active(user["user_id"])
        self._save_remembered_username()
        self.on_login_success(user)
        self.close()


def _load_background_pixmap(label: QLabel, w: int, h: int) -> None:
    """Load background image from bytes into label (same approach as test.py)."""
    path = _BG_PATH
    if not path.exists():
        return
    with open(path, "rb") as f:
        data = f.read()
    img = QImage()
    img.loadFromData(data)
    if img.isNull():
        try:
            from PIL import Image
            import io
            pil_img = Image.open(io.BytesIO(data)).convert("RGBA")
            img = QImage(pil_img.tobytes(), pil_img.width, pil_img.height, QImage.Format.Format_RGBA8888)
        except (ImportError, ValueError, OSError, RuntimeError):
            return
    pix = QPixmap.fromImage(img)
    if not pix.isNull():
        # Same as test.py: set full pixmap, setScaledContents handles scaling
        label.setPixmap(pix)
