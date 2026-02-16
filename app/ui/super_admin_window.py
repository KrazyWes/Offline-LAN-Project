# app/ui/super_admin_window.py
"""
Super Admin Window - Main dashboard for super admin role.
Matches Figma specifications from COMPLETE_SYSTEM_ALGORITHM.md
"""

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QLabel
from PySide6.QtCore import Qt

from app.ui.sidebar import Sidebar
from app.ui.cashier_overview import CashierOverview
from app.ui.styles import COLORS


class SuperAdminWindow(QMainWindow):
    """Super Admin Dashboard Window"""
    
    def __init__(self, user: dict):
        super().__init__()
        self.user = user
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
        
        # Logout page (placeholder - should show login window)
        self.logout_page = QLabel("Logging out...")
        self.logout_page.setAlignment(Qt.AlignCenter)
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
        """Handle logout action"""
        from PySide6.QtWidgets import QMessageBox
        
        reply = QMessageBox.question(
            self,
            'Confirm Logout',
            'Are you sure you want to logout?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # TODO: Close database connections, clear session
            # For now, just close the window
            self.close()
