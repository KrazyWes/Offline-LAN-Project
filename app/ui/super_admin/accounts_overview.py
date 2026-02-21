# app/ui/super_admin/accounts_overview.py
"""
Accounts page - User management. Uses database, excludes super_admin.
Based on ACCOUNTS_PAGE_DOCUMENTATION.md, adapted for Offline-LAN.
"""

from datetime import datetime, time as dt_time
from typing import Optional

from PySide6.QtWidgets import (
    QSizePolicy,
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QDialog, QMessageBox, QFrame, QGraphicsDropShadowEffect, QApplication,
    QToolButton
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QColor, QPixmap

import db
from app.ui.components.styles import COLORS, FONT_SIZES, FONT_WEIGHTS, RADIUS, DIMENSIONS
from app.ui.components.icon_utils import set_icon

# Role mapping: db value -> display name
ROLE_DISPLAY = db.ROLE_DISPLAY
ROLES_FOR_ACCOUNTS = db.ROLES_FOR_ACCOUNTS

# Avatar background colors
_AVATAR_COLORS = ("#FCD34D", "#6EE7B7", "#93C5FD", "#FDE68A", "#D6D3D1", "#C4B5FD", "#F9A8D4")

def _get_initials(name: str) -> str:
    parts = name.strip().split()
    if not parts:
        return "??"
    if len(parts) >= 2:
        return (parts[0][0] + parts[1][0]).upper()
    return (parts[0][:2]).upper()

def _get_avatar_color(name: str) -> str:
    h = hash(name or "x") % len(_AVATAR_COLORS)
    return _AVATAR_COLORS[abs(h)]

def _format_last_active(ts) -> str:
    if ts is None:
        return "Never"
    if isinstance(ts, dt_time):
        return "Just now"
    if isinstance(ts, str):
        try:
            ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except Exception:
            return "Just now"
    now = datetime.now(ts.tzinfo) if getattr(ts, "tzinfo", None) else datetime.now()
    delta = now - ts
    secs = delta.total_seconds()
    if secs < 1:
        return "Just now"
    if secs < 60:
        n = int(secs)
        return f"{n} second{'s' if n != 1 else ''} ago"
    if secs < 3600:
        n = int(secs / 60)
        return f"{n} minute{'s' if n != 1 else ''} ago"
    if secs < 86400:
        n = int(secs / 3600)
        return f"{n} hour{'s' if n != 1 else ''} ago"
    if secs < 604800:
        n = int(secs / 86400)
        return f"{n} day{'s' if n != 1 else ''} ago"
    if secs < 2592000:
        n = int(secs / 604800)
        return f"{n} week{'s' if n != 1 else ''} ago"
    if secs < 31536000:
        n = int(secs / 2592000)
        return f"{n} month{'s' if n != 1 else ''} ago"
    n = int(secs / 31536000)
    return f"{n} year{'s' if n != 1 else ''} ago"

def _get_role_style(role: str) -> str:
    styles = {
        "admin": "background-color: rgba(243, 232, 255, 0.6); color: #7C3AED; border: none;",
        "teller": "background-color: rgba(209, 250, 229, 0.6); color: #047857; border: none;",
        "monitor": "background-color: rgba(219, 234, 254, 0.6); color: #1D4ED8; border: none;",
        "operator_a": "background-color: rgba(219, 234, 254, 0.6); color: #1D4ED8; border: none;",
        "operator_b": "background-color: rgba(254, 243, 199, 0.6); color: #A16207; border: none;",
    }
    return styles.get(role, f"background-color: rgba(243, 244, 246, 0.6); color: {COLORS['gray_700']}; border: none;")

def _get_status_style(is_active: bool) -> str:
    if is_active:
        return "background-color: rgba(209, 250, 229, 0.6); color: #047857; border: none;"
    return f"background-color: rgba(243, 244, 246, 0.6); color: {COLORS['gray_700']}; border: none;"


# Styles matching register_super_admin.py
_INPUT_STYLE = """
    QLineEdit, QComboBox {
        font-size: 15px;
        padding: 10px 12px;
        border: 1px solid #dddfe2;
        border-radius: 8px;
        background-color: white;
    }
    QLineEdit:focus, QComboBox:focus {
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
_BTN_SECONDARY = """
    QPushButton {
        background-color: #f0f2f5;
        color: #1c1e21;
        font-size: 16px;
        font-weight: 600;
        border: none;
        border-radius: 8px;
    }
    QPushButton:hover { background-color: #e4e6eb; }
"""
_BTN_UPDATE = """
    QPushButton {
        background-color: #2563EB;
        color: white;
        font-size: 16px;
        font-weight: 600;
        border: none;
        border-radius: 8px;
    }
    QPushButton:hover { background-color: #1D4ED8; }
    QPushButton:pressed { background-color: #1E40AF; }
"""


class DraggableCardDialog(QDialog):
    """Base for modals styled like register_super_admin card, draggable."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #f3f4f6;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(Qt.darkGray)
        self.setGraphicsEffect(shadow)
        self._drag_pos: Optional[QPoint] = None

    def showEvent(self, event):
        super().showEvent(event)
        parent = self.parentWidget()
        if parent and parent.isVisible():
            geo = self.frameGeometry()
            cen = parent.rect().center()
            cen_global = parent.mapToGlobal(cen)
            geo.moveCenter(cen_global)
            self.move(geo.topLeft())
        else:
            screen = QApplication.primaryScreen()
            if screen:
                geo = self.frameGeometry()
                geo.moveCenter(screen.availableGeometry().center())
                self.move(geo.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_pos is not None:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = None
            event.accept()


class CreateAccountModal(DraggableCardDialog):
    """Modal for creating new account - same style as register_super_admin."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Account")
        self.setFixedWidth(420)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(24, 20, 24, 20)

        _err = "color: #DC2626; font-size: 12px;"
        _err_h = 14

        title = QLabel("Create New Account")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: 600; color: #1c1e21;")
        layout.addWidget(title)
        layout.addSpacing(4)

        # Name field
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Name/Nickname (min. 2 characters)")
        self.name_edit.setFixedHeight(40)
        self.name_edit.setStyleSheet(_INPUT_STYLE)
        self.name_error = QLabel()
        self.name_error.setStyleSheet(_err)
        self.name_error.setFixedHeight(_err_h)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.name_error)

        # Username field
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Username (min. 3 characters)")
        self.username_edit.setFixedHeight(40)
        self.username_edit.setStyleSheet(_INPUT_STYLE)
        self.username_error = QLabel()
        self.username_error.setStyleSheet(_err)
        self.username_error.setFixedHeight(_err_h)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.username_error)

        # Role dropdown
        self.role_combo = QComboBox()
        for r in ROLES_FOR_ACCOUNTS:
            self.role_combo.addItem(ROLE_DISPLAY.get(r, r), r)
        self.role_combo.setCurrentIndex(1)  # Default: Cashier (teller)
        self.role_combo.setFixedHeight(40)
        self.role_combo.setStyleSheet(_INPUT_STYLE)
        _role_spacer = QLabel()
        _role_spacer.setFixedHeight(_err_h)
        layout.addWidget(self.role_combo)
        layout.addWidget(_role_spacer)

        # Password field
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Password (min. 3 characters)")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setFixedHeight(40)
        self.password_edit.setStyleSheet(_INPUT_STYLE)
        self.password_error = QLabel()
        self.password_error.setStyleSheet(_err)
        self.password_error.setFixedHeight(_err_h)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.password_error)

        # Confirm password field
        self.confirm_edit = QLineEdit()
        self.confirm_edit.setPlaceholderText("Confirm password (min. 3 characters)")
        self.confirm_edit.setEchoMode(QLineEdit.Password)
        self.confirm_edit.setFixedHeight(40)
        self.confirm_edit.setStyleSheet(_INPUT_STYLE)
        self.confirm_error = QLabel()
        self.confirm_error.setStyleSheet(_err)
        self.confirm_error.setFixedHeight(_err_h)
        layout.addWidget(self.confirm_edit)
        layout.addWidget(self.confirm_error)

        # Buttons
        layout.addSpacing(4)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(40)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet(_BTN_SECONDARY)
        cancel_btn.clicked.connect(self.reject)
        create_btn = QPushButton("Create Account")
        create_btn.setFixedHeight(40)
        create_btn.setCursor(Qt.PointingHandCursor)
        create_btn.setStyleSheet(_BTN_PRIMARY)
        create_btn.clicked.connect(self._on_create)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(create_btn)
        layout.addLayout(btn_layout)

        # Enter key submits
        self.name_edit.returnPressed.connect(self._on_create)
        self.username_edit.returnPressed.connect(self._on_create)
        self.password_edit.returnPressed.connect(self._on_create)
        self.confirm_edit.returnPressed.connect(self._on_create)

    def _clear_errors(self):
        self.name_error.setText("")
        self.username_error.setText("")
        self.password_error.setText("")
        self.confirm_error.setText("")

    def _validate(self) -> bool:
        self._clear_errors()
        name = self.name_edit.text().strip()
        username = self.username_edit.text().strip()
        pw = self.password_edit.text()
        confirm = self.confirm_edit.text()

        has_error = False
        if not name:
            self.name_error.setText("Name is required")
            has_error = True
        elif len(name) < 2:
            self.name_error.setText("Name must be at least 2 characters")
            has_error = True

        if not username:
            self.username_error.setText("Username is required")
            has_error = True
        elif len(username) < 3:
            self.username_error.setText("Username must be at least 3 characters")
            has_error = True
        elif not all(c.isalnum() or c == "_" for c in username):
            self.username_error.setText("Username can only contain letters, numbers, underscores")
            has_error = True
        elif db.username_exists(username):
            self.username_error.setText("Username already exists")
            has_error = True

        if not pw:
            self.password_error.setText("Password is required")
            has_error = True
        elif len(pw) < 3:
            self.password_error.setText("Password must be at least 3 characters")
            has_error = True

        if not confirm:
            self.confirm_error.setText("Please confirm password")
            has_error = True
        elif pw != confirm:
            self.confirm_error.setText("Passwords do not match")
            has_error = True

        return not has_error

    def _on_create(self):
        if not self._validate():
            return
        name = self.name_edit.text().strip()
        username = self.username_edit.text().strip()
        pw = self.password_edit.text()
        role = self.role_combo.currentData() or "teller"
        role = str(role)

        ok = db.create_user(username, pw, role, name)
        if ok:
            QMessageBox.information(self, "Success", "Account created successfully.")
            self.accept()
        else:
            err = db.get_last_error() or "Unknown error"
            QMessageBox.critical(self, "Error", f"Failed to create account.\n\n{err}")


class EditAccountModal(DraggableCardDialog):
    """Modal for editing account - same style as register_super_admin."""
    def __init__(self, user: dict, parent=None):
        super().__init__(parent)
        self.user = user
        self.setWindowTitle("Edit Account")
        self.setFixedWidth(420)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(24, 20, 24, 20)

        _err = "color: #DC2626; font-size: 12px;"
        _err_h = 14

        title = QLabel("Edit Account")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: 600; color: #1c1e21;")
        layout.addWidget(title)
        layout.addSpacing(4)

        # Name field (pre-filled)
        self.name_edit = QLineEdit()
        self.name_edit.setText(self.user.get("name") or self.user.get("username", ""))
        self.name_edit.setPlaceholderText("Name/Nickname (min. 2 characters)")
        self.name_edit.setFixedHeight(40)
        self.name_edit.setStyleSheet(_INPUT_STYLE)
        self.name_error = QLabel()
        self.name_error.setStyleSheet(_err)
        self.name_error.setFixedHeight(_err_h)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.name_error)

        # Username field (pre-filled)
        self.username_edit = QLineEdit()
        self.username_edit.setText(self.user.get("username", ""))
        self.username_edit.setPlaceholderText("Username (min. 3 characters)")
        self.username_edit.setFixedHeight(40)
        self.username_edit.setStyleSheet(_INPUT_STYLE)
        self.username_error = QLabel()
        self.username_error.setStyleSheet(_err)
        self.username_error.setFixedHeight(_err_h)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.username_error)

        # Role dropdown (pre-selected)
        self.role_combo = QComboBox()
        for r in ROLES_FOR_ACCOUNTS:
            self.role_combo.addItem(ROLE_DISPLAY.get(r, r), r)
        idx = self.role_combo.findData(self.user.get("role", "teller"))
        if idx >= 0:
            self.role_combo.setCurrentIndex(idx)
        self.role_combo.setFixedHeight(40)
        self.role_combo.setStyleSheet(_INPUT_STYLE)
        _role_spacer = QLabel()
        _role_spacer.setFixedHeight(_err_h)
        layout.addWidget(self.role_combo)
        layout.addWidget(_role_spacer)

        # Password field (optional for edit)
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("New password (min. 3 chars, blank to keep)")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setFixedHeight(40)
        self.password_edit.setStyleSheet(_INPUT_STYLE)
        self.password_error = QLabel()
        self.password_error.setStyleSheet(_err)
        self.password_error.setFixedHeight(_err_h)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.password_error)

        # Confirm password field
        self.confirm_edit = QLineEdit()
        self.confirm_edit.setPlaceholderText("Confirm new password (min. 3 characters)")
        self.confirm_edit.setEchoMode(QLineEdit.Password)
        self.confirm_edit.setFixedHeight(40)
        self.confirm_edit.setStyleSheet(_INPUT_STYLE)
        self.confirm_error = QLabel()
        self.confirm_error.setStyleSheet(_err)
        self.confirm_error.setFixedHeight(_err_h)
        layout.addWidget(self.confirm_edit)
        layout.addWidget(self.confirm_error)

        # Connect Enter key on all fields to trigger update
        self.name_edit.returnPressed.connect(self._on_update)
        self.username_edit.returnPressed.connect(self._on_update)
        self.password_edit.returnPressed.connect(self._on_update)
        self.confirm_edit.returnPressed.connect(self._on_update)

        # Buttons
        layout.addSpacing(4)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(40)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet(_BTN_SECONDARY)
        cancel_btn.clicked.connect(self.reject)
        update_btn = QPushButton("Update Account")
        update_btn.setFixedHeight(40)
        update_btn.setCursor(Qt.PointingHandCursor)
        update_btn.setStyleSheet(_BTN_UPDATE)
        update_btn.clicked.connect(self._on_update)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(update_btn)
        layout.addLayout(btn_layout)

    def _clear_errors(self):
        self.name_error.setText("")
        self.username_error.setText("")
        self.password_error.setText("")
        self.confirm_error.setText("")

    def _validate(self) -> bool:
        self._clear_errors()
        name = self.name_edit.text().strip()
        username = self.username_edit.text().strip()
        pw = self.password_edit.text()
        confirm = self.confirm_edit.text()

        has_error = False
        if not name:
            self.name_error.setText("Name is required")
            has_error = True
        elif len(name) < 2:
            self.name_error.setText("Name must be at least 2 characters")
            has_error = True

        if not username:
            self.username_error.setText("Username is required")
            has_error = True
        elif len(username) < 3:
            self.username_error.setText("Username must be at least 3 characters")
            has_error = True
        elif not all(c.isalnum() or c == "_" for c in username):
            self.username_error.setText("Username can only contain letters, numbers, underscores")
            has_error = True
        elif username != self.user.get("username") and db.username_exists(username):
            self.username_error.setText("Username already exists")
            has_error = True

        # Password validation only if password is provided
        if pw or confirm:
            if len(pw) < 3:
                self.password_error.setText("Password must be at least 3 characters")
                has_error = True
            elif pw != confirm:
                self.confirm_error.setText("Passwords do not match")
                has_error = True

        return not has_error

    def _on_update(self):
        print("[DEBUG] Update button clicked")
        if not self._validate():
            print("[DEBUG] Validation failed")
            return
        user_id = self.user["user_id"]
        name = self.name_edit.text().strip()
        username = self.username_edit.text().strip()
        pw = self.password_edit.text() or None
        role = self.role_combo.currentData() or self.user.get("role", "teller")
        role = str(role)

        print(f"[DEBUG] Updating user_id={user_id}, role={role}, password_changed={'Yes' if pw else 'No'}")
        print(f"[DEBUG] DB connection: {db.connection_ok()}")
        
        ok = db.update_user_account(user_id, username, name, role, password_plain=pw)
        print(f"[DEBUG] update_user_account result: {ok}")
        print(f"[DEBUG] Last error: {db.get_last_error()}")
        
        if ok:
            QMessageBox.information(self, "Success", "Account updated successfully.")
            self.accept()
        else:
            err = db.get_last_error() or "Unknown error"
            QMessageBox.critical(self, "Error", f"Failed to update account.\n\n{err}")


class AccountsOverview(QWidget):
    """Accounts management page. Excludes super_admin from list."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("page-container")
        self.users: list = []
        self.search_query = ""
        self.role_filter = "All"
        self.status_filter = "All"
        self._build_ui()
        self._load_users()

    def _build_ui(self):
        GAP = 12
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(GAP)

        # Header with Create button
        header = QHBoxLayout()
        header.setSpacing(GAP)
        title_col = QVBoxLayout()
        title_col.setSpacing(4)
        title = QLabel("Account Management")
        title.setStyleSheet(f"font-size: {FONT_SIZES['2xl']}px; font-weight: {FONT_WEIGHTS['bold']}; color: {COLORS['gray_800']};")
        subtitle = QLabel("Manage user accounts and permissions")
        subtitle.setStyleSheet(f"font-size: {FONT_SIZES['sm']}px; color: {COLORS['gray_500']};")
        title_col.addWidget(title)
        title_col.addWidget(subtitle)
        header.addLayout(title_col)
        header.addStretch()

        create_btn = QPushButton("Create account")
        create_btn.setFixedHeight(40)
        create_btn.setStyleSheet(f"""
            QPushButton {{ background-color: #FBBF24; color: #111827; border-radius: {RADIUS['lg']}px;
            padding: 8px 16px; font-weight: 600; }}
            QPushButton:hover {{ background-color: #F59E0B; }}
        """)
        create_btn.setCursor(Qt.PointingHandCursor)
        create_btn.clicked.connect(self._on_create)
        header.addWidget(create_btn)
        layout.addLayout(header)

        # Search
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search by name, username, or role...")
        self.search_edit.setFixedHeight(44)
        self.search_edit.textChanged.connect(self._on_search_changed)
        self.search_edit.setStyleSheet(f"""
            QLineEdit {{ padding: 10px 14px; border: 1px solid {COLORS['gray_300']};
            border-radius: {RADIUS['lg']}px; font-size: {FONT_SIZES['base']}px; }}
        """)
        layout.addWidget(self.search_edit)

        # Filters
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(GAP)
        filter_label = QLabel("Filter by:")
        filter_label.setStyleSheet(f"font-size: {FONT_SIZES['sm']}px; color: {COLORS['gray_600']};")
        filter_layout.addWidget(filter_label)

        self.role_combo = QComboBox()
        self.role_combo.setFixedHeight(40)
        self.role_combo.addItem("All Roles", "All")
        for r in ROLES_FOR_ACCOUNTS:
            self.role_combo.addItem(ROLE_DISPLAY.get(r, r), r)
        self.role_combo.currentIndexChanged.connect(self._apply_filters)
        filter_layout.addWidget(self.role_combo)

        self.status_combo = QComboBox()
        self.status_combo.setFixedHeight(40)
        self.status_combo.addItem("All Statuses", "All")
        self.status_combo.addItem("Online", "Online")
        self.status_combo.addItem("Offline", "Offline")
        self.status_combo.currentIndexChanged.connect(self._apply_filters)
        filter_layout.addWidget(self.status_combo)

        filter_layout.addStretch()
        self.clear_btn = QPushButton("Clear all filters")
        self.clear_btn.setStyleSheet(f"QPushButton {{ color: {COLORS['gray_600']}; font-size: {FONT_SIZES['sm']}px; }} QPushButton:hover {{ color: {COLORS['gray_800']}; background: {COLORS['gray_100']}; border-radius: {RADIUS['md']}px; }}")
        self.clear_btn.clicked.connect(self._clear_filters)
        filter_layout.addWidget(self.clear_btn)
        layout.addLayout(filter_layout)

        # Stats
        self.stats_label = QLabel("Showing 0 users")
        self.stats_label.setStyleSheet(f"font-size: {FONT_SIZES['sm']}px; color: {COLORS['gray_600']};")
        layout.addWidget(self.stats_label)

        # Database error banner
        self.db_error_banner = QLabel("Database connection unavailable.")
        self.db_error_banner.setStyleSheet(f"""
            padding: 12px 16px; background-color: #FEF2F2; color: #B91C1C;
            border-radius: {RADIUS['md']}px; font-size: {FONT_SIZES['sm']}px;
        """)
        self.db_error_banner.setWordWrap(True)
        self.db_error_banner.setVisible(False)
        layout.addWidget(self.db_error_banner)

        # Table with Actions column
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["User", "Role", "Status", "Last Active", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background: {COLORS['white']};
                border: 1px solid {COLORS['gray_200']};
                border-radius: {RADIUS['lg']}px;
                gridline-color: {COLORS['gray_200']};
            }}
            QHeaderView::section {{
                background: {COLORS['gray_50']};
                padding: 16px;
                font-weight: 600;
                font-size: {FONT_SIZES['xs']}px;
                color: {COLORS['gray_600']};
            }}
            QTableWidget::item {{
                padding: 4px 0;
            }}
        """)
        layout.addWidget(self.table, 1)

        self.setStyleSheet(f"QWidget#page-container {{ background-color: {COLORS['gray_50']}; }}")

    def _load_users(self):
        if not db.connection_ok():
            self.db_error_banner.setVisible(True)
            self.users = []
        else:
            self.db_error_banner.setVisible(False)
            self.users = db.fetch_users_excluding_super_admin()
        self._apply_filters()
        self.table.viewport().update()

    def showEvent(self, event):
        super().showEvent(event)
        self._load_users()

    def _get_filtered_users(self):
        q = self.search_query.lower().strip()
        rf = self.role_filter
        sf = self.status_filter
        filtered = []
        for u in self.users:
            if rf != "All" and u["role"] != rf:
                continue
            if sf != "All":
                status = "Online" if u["is_active"] else "Offline"
                if status != sf:
                    continue
            if q:
                name = (u.get("name") or "").lower()
                username = (u.get("username") or "").lower()
                role = (ROLE_DISPLAY.get(u.get("role", ""), u.get("role", ""))).lower()
                if q not in name and q not in username and q not in role:
                    continue
            filtered.append(u)
        return filtered

    def _on_search_changed(self):
        self.search_query = self.search_edit.text()
        self._apply_filters()

    def _apply_filters(self):
        self.role_filter = self.role_combo.currentData() or "All"
        self.status_filter = self.status_combo.currentData() or "All"
        filtered = self._get_filtered_users()
        self.stats_label.setText(f"Showing {len(filtered)} of {len(self.users)} users")
        self._populate_table(filtered)
        has_filters = self.role_filter != "All" or self.status_filter != "All" or bool(self.search_query.strip())
        self.clear_btn.setVisible(has_filters)

    def _clear_filters(self):
        self.search_edit.clear()
        self.role_combo.setCurrentIndex(0)
        self.status_combo.setCurrentIndex(0)
        self._apply_filters()

    def _populate_table(self, users: list):
        self.table.setRowCount(len(users))
        for i, u in enumerate(users):
            name = u.get("name") or u.get("username", "")
            role_raw = u.get("role", "")
            role_display = ROLE_DISPLAY.get(role_raw, role_raw)
            is_active = u.get("is_active", False)
            status = "Online" if is_active else "Offline"
            last_active = _format_last_active(u.get("last_active"))

            self.table.setCellWidget(i, 0, self._user_cell(name, is_active))
            self.table.setCellWidget(i, 1, self._role_badge(role_display, role_raw))
            self.table.setCellWidget(i, 2, self._status_badge(status, is_active))
            last_item = QTableWidgetItem(last_active)
            last_item.setForeground(QColor(COLORS['gray_800']))
            last_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 3, last_item)
            self.table.setCellWidget(i, 4, self._actions_cell(u))
            self.table.setRowHeight(i, 56)

    def _user_cell(self, name: str, is_active: bool) -> QWidget:
        cell = QWidget()
        layout = QHBoxLayout(cell)
        layout.setContentsMargins(20, 6, 16, 6)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        initials = _get_initials(name)
        color = _get_avatar_color(name)
        avatar_container = QWidget()
        avatar_container.setFixedSize(36, 36)
        avatar_container.setStyleSheet(f"background-color: {color}; border-radius: 18px;")
        avatar_layout = QVBoxLayout(avatar_container)
        avatar_layout.setContentsMargins(0, 0, 0, 0)
        avatar_layout.setAlignment(Qt.AlignCenter)
        init_label = QLabel(initials)
        init_label.setStyleSheet("color: #1F2937; font-weight: 700; font-size: 13px; background: transparent;")
        init_label.setAlignment(Qt.AlignCenter)
        avatar_layout.addWidget(init_label)
        dot = QLabel()
        dot.setFixedSize(14, 14)
        dot.setStyleSheet(f"""
            background-color: {'#10B981' if is_active else COLORS['gray_400']};
            border-radius: 7px;
            border: 2px solid {color};
        """)
        dot.setParent(avatar_container)
        dot.setGeometry(22, 22, 14, 14)
        dot.raise_()
        layout.addWidget(avatar_container)
        name_label = QLabel(name)
        name_label.setStyleSheet(f"font-weight: {FONT_WEIGHTS['medium']}; font-size: {FONT_SIZES['base']}px; color: {COLORS['gray_800']};")
        layout.addWidget(name_label)
        return cell

    def _role_badge(self, text: str, role_raw: str) -> QWidget:
        cell = QWidget()
        cell_layout = QHBoxLayout(cell)
        cell_layout.setContentsMargins(0, 0, 0, 0)
        cell_layout.setAlignment(Qt.AlignCenter)
        badge = QFrame()
        badge.setMaximumWidth(180)
        layout = QHBoxLayout(badge)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignCenter)
        style = _get_role_style(role_raw)
        badge.setStyleSheet(f"""
            QFrame {{ {style} border-radius: 8px; min-height: 16px; max-height: 36px; }}
            QFrame QLabel {{ background: transparent; border: none; }}
        """)
        import os
        from app.ui.components.icon_utils import asset_path
        _ROLE_ICONS = {"teller": "cashier.png", "operator_a": "operator_b.png", "operator_b": "operator_a.png"}
        icon_file = _ROLE_ICONS.get(role_raw, f"{role_raw}.png")
        icon_path = f"icons/role/{icon_file}"
        full_path = asset_path(*icon_path.split("/"))
        if os.path.exists(full_path):
            try:
                sz = 20
                px = QPixmap(full_path)
                if not px.isNull():
                    px = px.scaled(sz, sz, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    icon_lbl = QLabel()
                    icon_lbl.setFixedSize(sz, sz)
                    icon_lbl.setAlignment(Qt.AlignCenter)
                    icon_lbl.setPixmap(px)
                    icon_lbl.setStyleSheet("background: transparent; border: none;")
                    layout.addWidget(icon_lbl)
            except Exception:
                pass
        lbl = QLabel(text)
        lbl.setStyleSheet(f"font-size: {FONT_SIZES['xs']}px; font-weight: {FONT_WEIGHTS['medium']}; background: transparent; border: none;")
        layout.addWidget(lbl, 0, Qt.AlignCenter)
        cell_layout.addWidget(badge)
        return cell

    def _status_badge(self, text: str, is_active: bool) -> QWidget:
        cell = QWidget()
        cell_layout = QHBoxLayout(cell)
        cell_layout.setContentsMargins(0, 0, 0, 0)
        cell_layout.setAlignment(Qt.AlignCenter)
        badge = QFrame()
        layout = QHBoxLayout(badge)
        layout.setContentsMargins(8, 4, 10, 4)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignCenter)
        style = _get_status_style(is_active)
        badge.setStyleSheet(f"""
            QFrame {{ {style} border-radius: 8px; min-height: 12px; max-height: 28px; }}
            QFrame QLabel {{ background: transparent; border: none; }}
        """)
        dot = QFrame()
        dot.setFixedSize(8, 8)
        dot.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        dot.setStyleSheet(f"""
            QFrame {{
                background-color: {'#10B981' if is_active else COLORS['gray_500']};
                border-radius: 4px;
                border: none;
                min-width: 8px; max-width: 8px; min-height: 8px; max-height: 8px;
            }}
        """)
        layout.addWidget(dot)
        lbl = QLabel(text)
        lbl.setStyleSheet(f"font-size: {FONT_SIZES['xs']}px; font-weight: {FONT_WEIGHTS['medium']}; background: transparent;")
        layout.addWidget(lbl)
        cell_layout.addWidget(badge)
        return cell

    def _actions_cell(self, user: dict) -> QWidget:
        """Actions: Edit and Delete icon buttons."""
        cell = QWidget()
        layout = QHBoxLayout(cell)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignCenter)

        # Edit button
        edit_btn = QToolButton()
        edit_btn.setFixedSize(32, 32)
        edit_btn.setCursor(Qt.PointingHandCursor)
        edit_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        edit_btn.setToolTip("Edit")
        edit_btn.setStyleSheet(f"""
            QToolButton {{ background: #EFF6FF; border-radius: {RADIUS['lg']}px; border: none; }}
            QToolButton:hover {{ background: #DBEAFE; }}
        """)
        set_icon(edit_btn, "icons/actions/edit.png", DIMENSIONS['icon_md'])
        edit_btn.clicked.connect(lambda checked, u=user: self._on_edit(u))

        # Delete button
        del_btn = QToolButton()
        del_btn.setFixedSize(32, 32)
        del_btn.setCursor(Qt.PointingHandCursor)
        del_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        del_btn.setToolTip("Delete")
        del_btn.setStyleSheet(f"""
            QToolButton {{ background: #FEF2F2; border-radius: {RADIUS['lg']}px; border: none; }}
            QToolButton:hover {{ background: #FEE2E2; }}
        """)
        set_icon(del_btn, "icons/actions/trash_bin.png", 24)
        del_btn.clicked.connect(lambda checked, u=user: self._on_delete(u))

        layout.addWidget(edit_btn)
        layout.addWidget(del_btn)
        return cell

    def _on_create(self):
        """Open create account modal."""
        dlg = CreateAccountModal(self.window())
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._load_users()

    def _on_edit(self, user: dict):
        """Open edit account modal with user data pre-filled."""
        print(f"[DEBUG] _on_edit called with user_id={user.get('user_id')}, username={user.get('username')}")
        dlg = EditAccountModal(user, self.window())
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._load_users()

    def _on_delete(self, user: dict):
        """Delete user with confirmation dialog."""
        name = user.get("name") or user.get("username", "this user")
        user_id = user.get("user_id")
        parent = self.window()

        if user_id is None:
            QMessageBox.critical(parent, "Error", "Invalid user data (missing user_id).")
            return

        reply = QMessageBox.question(
            parent, "Confirm Delete",
            f'Are you sure you want to delete user "{name}"?\n\nThis action cannot be undone.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            ok = db.delete_user_account(user_id)
            if ok:
                QMessageBox.information(parent, "Success", "User deleted successfully.")
                self._load_users()
            else:
                err = db.get_last_error() or "Unknown error"
                QMessageBox.critical(parent, "Error", f"Failed to delete user.\n\n{err}")
