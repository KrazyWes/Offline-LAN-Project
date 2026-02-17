# app/ui/super_admin/super_admin_window.py
"""
Super Admin Window - Main dashboard for super admin role.
Matches Figma specifications from COMPLETE_SYSTEM_ALGORITHM.md
"""

from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel,
    QPushButton, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QImage, QPixmap, QResizeEvent
from PySide6.QtWidgets import QGraphicsDropShadowEffect

from app.ui.components.styles import COLORS, FONT_SIZES, FONT_WEIGHTS, SPACING, RADIUS
from .sidebar import Sidebar
from .cashier_overview import CashierOverview

_LOGOUT_BG_PATH = Path(__file__).resolve().parent.parent.parent / "assets" / "backgrounds" / "rooster.png"


def _load_logout_background_pixmap(label: QLabel, w: int, h: int) -> None:
    """Load rooster.png background (same approach as login page / test.py)."""
    path = _LOGOUT_BG_PATH
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
        label.setPixmap(pix)


class LogoutPage(QWidget):
    """Full-page logout confirmation with background image (same style as login page)."""

    confirmed = Signal()
    cancelled = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("logoutPage")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignCenter)

        # Background label (positioned via setGeometry, same as login)
        self._bg_label = QLabel(self)
        self._bg_label.setScaledContents(True)
        self._bg_label.lower()

        # Card overlay (same style as login)
        card = QFrame()
        card.setObjectName("logoutCard")
        card.setFixedWidth(440)
        card.setStyleSheet("""
            QFrame#logoutCard {
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
        form.setSpacing(SPACING['4'])
        form.setContentsMargins(SPACING['6'], SPACING['6'], SPACING['6'], SPACING['6'])

        msg = QLabel("Are you sure you want to logout?")
        msg.setWordWrap(True)
        msg.setAlignment(Qt.AlignCenter)
        msg.setStyleSheet(f"font-size: {FONT_SIZES['lg']}px; color: {COLORS['gray_800']};")
        form.addWidget(msg, 1)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(SPACING['3'])
        btn_layout.addStretch()
        btn_yes = QPushButton("Yes")
        btn_yes.setObjectName("yesBtn")
        btn_yes.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_yes.setStyleSheet(f"""
            QPushButton#yesBtn {{
                background-color: {COLORS['blue_600']};
                color: {COLORS['white']};
                border: none;
                border-radius: {RADIUS['lg']}px;
                min-width: 100px;
                min-height: 36px;
            }}
            QPushButton#yesBtn:hover {{ background-color: {COLORS['blue_700']}; }}
        """)
        btn_yes.clicked.connect(self.confirmed.emit)
        btn_layout.addWidget(btn_yes)
        btn_no = QPushButton("No")
        btn_no.setObjectName("noBtn")
        btn_no.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_no.setStyleSheet(f"""
            QPushButton#noBtn {{
                background-color: {COLORS['gray_100']};
                color: {COLORS['gray_800']};
                border: none;
                border-radius: {RADIUS['lg']}px;
                min-width: 100px;
                min-height: 36px;
            }}
            QPushButton#noBtn:hover {{ background-color: {COLORS['gray_200']}; }}
        """)
        btn_no.clicked.connect(self.cancelled.emit)
        btn_layout.addWidget(btn_no)
        btn_layout.addStretch()
        form.addLayout(btn_layout)
        main_layout.addWidget(card, alignment=Qt.AlignCenter)
        self._bg_label.lower()

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        s = self.size()
        self._bg_label.setGeometry(0, 0, s.width(), s.height())
        _load_logout_background_pixmap(self._bg_label, s.width(), s.height())

    def showEvent(self, event):
        super().showEvent(event)
        s = self.size()
        self._bg_label.setGeometry(0, 0, s.width(), s.height())
        _load_logout_background_pixmap(self._bg_label, s.width(), s.height())


class SuperAdminWindow(QMainWindow):
    """Super Admin Dashboard Window"""
    
    def __init__(self, user: dict, on_logout=None):
        super().__init__()
        self.user = user
        self.on_logout = on_logout  # callback to show login again (e.g. start_login)
        self.setWindowTitle("Super Admin Dashboard")
        self.setMinimumSize(1024, 768)
        self.resize(1920, 1080)
        
        # Set window to maximized state
        self.setWindowState(Qt.WindowMaximized)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main horizontal layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.menu_changed.connect(self._on_menu_changed)
        main_layout.addWidget(self.sidebar)
        
        # Content area (right side)
        self.content_area = QWidget()
        content_layout = QHBoxLayout(self.content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet(f"""
            QStackedWidget {{
                background-color: {COLORS['gray_50']};
            }}
        """)
        content_layout.addWidget(self.stacked_widget)
        
        main_layout.addWidget(self.content_area, 1)  # Stretch factor
        
        # Initialize pages
        self._setup_pages()
        
        # Set default page
        self.sidebar.set_active_item('cashier-overview')
    
    def _setup_pages(self):
        """Setup all dashboard pages"""
        # Cashier Overview (main page)
        self.cashier_overview = CashierOverview()
        self.cashier_overview.refresh_requested.connect(self._on_refresh_requested)
        self.stacked_widget.addWidget(self.cashier_overview)
        
        # Placeholder pages (to be implemented later)
        self.event_overview = QLabel("Event Overview\n(Coming soon)")
        self.event_overview.setAlignment(Qt.AlignCenter)
        self.event_overview.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                color: {COLORS['gray_500']};
            }}
        """)
        self.stacked_widget.addWidget(self.event_overview)
        
        self.accounts_page = QLabel("Accounts\n(Coming soon)")
        self.accounts_page.setAlignment(Qt.AlignCenter)
        self.accounts_page.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                color: {COLORS['gray_500']};
            }}
        """)
        self.stacked_widget.addWidget(self.accounts_page)
        
        self.reports_page = QLabel("Reports and Database\n(Coming soon)")
        self.reports_page.setAlignment(Qt.AlignCenter)
        self.reports_page.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                color: {COLORS['gray_500']};
            }}
        """)
        self.stacked_widget.addWidget(self.reports_page)
        
        self.operator_a_page = QLabel("Operator A\n(Coming soon)")
        self.operator_a_page.setAlignment(Qt.AlignCenter)
        self.operator_a_page.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                color: {COLORS['gray_500']};
            }}
        """)
        self.stacked_widget.addWidget(self.operator_a_page)
        
        self.operator_b_page = QLabel("Operator B\n(Coming soon)")
        self.operator_b_page.setAlignment(Qt.AlignCenter)
        self.operator_b_page.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                color: {COLORS['gray_500']};
            }}
        """)
        self.stacked_widget.addWidget(self.operator_b_page)
        
        self.settings_page = QLabel("Settings\n(Coming soon)")
        self.settings_page.setAlignment(Qt.AlignCenter)
        self.settings_page.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                color: {COLORS['gray_500']};
            }}
        """)
        self.stacked_widget.addWidget(self.settings_page)
        
        self.utility_page = QLabel("Utility\n(Coming soon)")
        self.utility_page.setAlignment(Qt.AlignCenter)
        self.utility_page.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                color: {COLORS['gray_500']};
            }}
        """)
        self.stacked_widget.addWidget(self.utility_page)
        
        # Logout page (full-page with rooster.png background, same style as login)
        self.logout_page = LogoutPage(self)
        self.logout_page.confirmed.connect(self._do_logout)
        self.logout_page.cancelled.connect(self._on_logout_cancelled)
        self.stacked_widget.addWidget(self.logout_page)
    
    def _on_menu_changed(self, menu_id: str):
        """Handle sidebar menu item selection"""
        page_map = {
            'cashier-overview': 0,
            'event-overview': 1,
            'accounts': 2,
            'reports': 3,
            'operator-a': 4,
            'operator-b': 5,
            'settings': 6,
            'utility': 7,
            'logout': 8,
        }
        
        if menu_id in page_map:
            self.stacked_widget.setCurrentIndex(page_map[menu_id])
            
            # Handle logout
            if menu_id == 'logout':
                self._handle_logout()
    
    def _on_refresh_requested(self):
        """Handle refresh request from cashier overview"""
        # TODO: Reload data from database
        print("Refresh requested - reloading cashier data from database")
    
    def _handle_logout(self):
        """Handle logout menu: switch to logout page (background + confirmation card)."""
        self.stacked_widget.setCurrentWidget(self.logout_page)

    def _do_logout(self):
        """Perform logout: close window and call on_logout callback."""
        self.close()
        if callable(self.on_logout):
            self.on_logout()

    def _on_logout_cancelled(self):
        """User clicked No on logout page: return to cashier overview."""
        self.stacked_widget.setCurrentIndex(0)
        self.sidebar.set_active_item('cashier-overview')
