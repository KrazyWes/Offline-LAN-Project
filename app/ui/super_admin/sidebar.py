# app/ui/sidebar.py
"""
Sidebar navigation component matching Figma specifications exactly.
From COMPLETE_SYSTEM_ALGORITHM.md section 3
"""

from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QToolButton,
    QSizePolicy
)
from app.ui.components.styles import (
    COLORS, FONT_SIZES, FONT_WEIGHTS, SPACING, DIMENSIONS,
    get_sidebar_stylesheet
)


class NavButton(QToolButton):
    """Navigation button with active state"""
    
    # Icon size: 0.4 inch = 0.4 * 96 DPI = 38.4 pixels ≈ 38 pixels
    ICON_SIZE = 38
    
    def __init__(self, key: str, text: str, icon_path: str = None, parent=None):
        super().__init__(parent)
        self.key = key
        self.setText(text)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(True)
        self.setAutoExclusive(False)  # We'll handle exclusivity manually
        self.setObjectName("nav-button")
        
        # Make button expand to fill available width
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        if icon_path:
            self._set_icon(icon_path)
    
    def _set_icon(self, icon_path: str):
        """Set icon with proper size (0.4 inch minimum)"""
        from PySide6.QtGui import QPixmap, QIcon
        from PySide6.QtCore import QSize
        import os
        
        icon_file = os.path.join("app", "assets", *icon_path.split("/"))
        if os.path.exists(icon_file):
            pixmap = QPixmap(icon_file)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.ICON_SIZE,
                    self.ICON_SIZE,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.setIcon(QIcon(scaled_pixmap))
                self.setIconSize(QSize(self.ICON_SIZE, self.ICON_SIZE))
        else:
            # Fallback to icon_utils
            from app.ui.components.icon_utils import set_icon
            set_icon(self, icon_path, self.ICON_SIZE)


class Sidebar(QWidget):
    """Collapsible sidebar navigation matching Figma specs"""
    
    menu_changed = Signal(str)  # Emits menu item ID
    toggle_requested = Signal()  # Emits when toggle button clicked
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self._is_expanded = True
        self._operate_open = False
        self._active_item = 'cashier-overview'
        
        self._setup_ui()
        self._setup_animation()
        self._update_ui_state()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header Section (64px height)
        header = QFrame()
        header.setFixedHeight(DIMENSIONS['header_height'])
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['gray_50']};
                border-bottom: 1px solid {COLORS['gray_200']};
            }}
        """)
        
        header_layout = QHBoxLayout(header)
        # Match padding to align with navigation items below
        header_layout.setContentsMargins(SPACING['4'], 0, SPACING['4'], 0)
        header_layout.setSpacing(SPACING['2'])
        
        # Dashboard icon (only when expanded) - 0.6 inch by 0.6 inch
        # 0.6 inch = 0.6 * 96 DPI = 57.6 pixels ≈ 58 pixels
        dashboard_icon_size = 58
        self.dashboard_icon = QLabel()
        self.dashboard_icon.setFixedSize(dashboard_icon_size, dashboard_icon_size)
        self.dashboard_icon.setScaledContents(True)
        from PySide6.QtGui import QPixmap
        import os
        dashboard_path = os.path.join("app", "assets", "icons", "sidebar", "dashboard.png")
        if os.path.exists(dashboard_path):
            dashboard_pixmap = QPixmap(dashboard_path)
            if not dashboard_pixmap.isNull():
                self.dashboard_icon.setPixmap(dashboard_pixmap.scaled(
                    dashboard_icon_size, 
                    dashboard_icon_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ))
        header_layout.addWidget(self.dashboard_icon)
        
        # Dashboard text (only when expanded)
        self.dashboard_text = QLabel("Dashboard")
        self.dashboard_text.setObjectName("sidebarTitle")
        header_layout.addWidget(self.dashboard_text)
        
        header_layout.addStretch()
        
        # Toggle button - Use 0.4 inch icon size
        self.toggle_btn = QToolButton()
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.setObjectName("toggle-button")
        self.toggle_btn.clicked.connect(self._on_toggle_clicked)
        # Set icon with 0.4 inch size (38px)
        from PySide6.QtGui import QPixmap, QIcon
        from PySide6.QtCore import QSize
        import os
        toggle_icon_size = 38  # 0.4 inch
        chevron_path = os.path.join("app", "assets", "icons", "sidebar", "chevron_left.png")
        if os.path.exists(chevron_path):
            pixmap = QPixmap(chevron_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(toggle_icon_size, toggle_icon_size, 
                                      Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
                self.toggle_btn.setIcon(QIcon(scaled))
                self.toggle_btn.setIconSize(QSize(toggle_icon_size, toggle_icon_size))
        else:
            from app.ui.components.icon_utils import set_icon
            set_icon(self.toggle_btn, "icons/sidebar/chevron_left.png", toggle_icon_size)
        header_layout.addWidget(self.toggle_btn)
        
        layout.addWidget(header)
        
        # Navigation Section (scrollable)
        nav_container = QFrame()
        nav_container.setStyleSheet(f"""
            QFrame {{
                background-color: transparent;
            }}
        """)
        nav_layout = QVBoxLayout(nav_container)
        # Match horizontal margins with header exactly (dashboard icon to chevron alignment)
        # Left margin matches where dashboard icon starts, right margin matches where chevron ends
        nav_layout.setContentsMargins(SPACING['4'], 0, SPACING['4'], 0)
        nav_layout.setSpacing(0)
        
        # Main menu items
        self.btn_cashier = NavButton("cashier-overview", "Cashier overview", "icons/sidebar/cashier_overview.png")
        self.btn_event = NavButton("event-overview", "Event overview", "icons/sidebar/event_overview.png")
        self.btn_accounts = NavButton("accounts", "Accounts", "icons/sidebar/accounts.png")
        self.btn_reports = NavButton("reports", "Reports and database", "icons/sidebar/reports_db.png")
        
        for btn in [self.btn_cashier, self.btn_event, self.btn_accounts, self.btn_reports]:
            btn.clicked.connect(lambda checked, b=btn: self._on_nav_clicked(b.key))
            nav_layout.addWidget(btn)
        
        # Operate (with submenu) - Use NavButton for consistency
        self.btn_operate = NavButton("operate", "Operate", "icons/sidebar/operate.png")
        self.btn_operate.clicked.connect(self._on_operate_clicked)
        nav_layout.addWidget(self.btn_operate)
        
        # Operate submenu panel - No indentation, align with other nav items
        self.operate_panel = QFrame()
        self.operate_panel.setObjectName("operatePanel")
        operate_layout = QVBoxLayout(self.operate_panel)
        # Same margins as other nav items - no indentation for cleaner look
        operate_layout.setContentsMargins(0, SPACING['2'], 0, SPACING['2'])
        operate_layout.setSpacing(SPACING['2'])
        
        self.btn_op_a = NavButton("operator-a", "Operator A", "icons/sidebar/operate.png")
        self.btn_op_b = NavButton("operator-b", "Operator B", "icons/sidebar/operate.png")
        
        for btn in [self.btn_op_a, self.btn_op_b]:
            btn.clicked.connect(lambda checked, b=btn: self._on_nav_clicked(b.key))
            operate_layout.addWidget(btn)
        
        self.operate_panel.setVisible(False)
        nav_layout.addWidget(self.operate_panel)
        
        # Spacer to push bottom items down
        nav_layout.addStretch()
        
        # Add top spacing before bottom section
        nav_layout.addSpacing(SPACING['4'])
        
        # Bottom section separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(f"QFrame {{ border-top: 1px solid {COLORS['gray_200']}; background-color: transparent; }}")
        nav_layout.addWidget(separator)
        
        # Bottom menu items
        self.btn_settings = NavButton("settings", "Settings", "icons/sidebar/settings.png")
        self.btn_utility = NavButton("utility", "Utility", "icons/sidebar/wrench.png")
        self.btn_logout = NavButton("logout", "Logout", "icons/sidebar/logout.png")
        
        for btn in [self.btn_settings, self.btn_utility, self.btn_logout]:
            btn.clicked.connect(lambda checked, b=btn: self._on_nav_clicked(b.key))
            nav_layout.addWidget(btn)
        
        # Add bottom spacing after bottom section
        nav_layout.addSpacing(SPACING['4'])
        
        layout.addWidget(nav_container)
        
        # Set initial active state
        self.btn_cashier.setChecked(True)
    
    def _setup_animation(self):
        """Setup width animation for collapse/expand"""
        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
    
    def _on_toggle_clicked(self):
        """Handle sidebar toggle button click"""
        self._is_expanded = not self._is_expanded
        
        # Close submenu if collapsing
        if not self._is_expanded:
            self._operate_open = False
            self.operate_panel.setVisible(False)
            self.btn_operate.setChecked(False)
        
        self._update_ui_state()
        self.toggle_requested.emit()
    
    def _on_operate_clicked(self):
        """Handle Operate menu click"""
        if not self._is_expanded:
            return  # Don't toggle if collapsed
        
        self._operate_open = not self._operate_open
        self.operate_panel.setVisible(self._operate_open)
        
        # Update chevron icon (TODO: rotate chevron)
    
    def _on_nav_clicked(self, key: str):
        """Handle navigation item click"""
        # Update active state
        self._active_item = key
        
        # Uncheck all buttons
        for btn in [
            self.btn_cashier, self.btn_event, self.btn_accounts, self.btn_reports,
            self.btn_op_a, self.btn_op_b, self.btn_settings, self.btn_utility, self.btn_logout
        ]:
            btn.setChecked(False)
        
        # Check clicked button
        button_map = {
            'cashier-overview': self.btn_cashier,
            'event-overview': self.btn_event,
            'accounts': self.btn_accounts,
            'reports': self.btn_reports,
            'operator-a': self.btn_op_a,
            'operator-b': self.btn_op_b,
            'settings': self.btn_settings,
            'utility': self.btn_utility,
            'logout': self.btn_logout,
        }
        
        if key in button_map:
            button_map[key].setChecked(True)
        
        # Emit signal
        self.menu_changed.emit(key)
    
    def _update_ui_state(self):
        """Update UI based on expanded/collapsed state"""
        target_width = DIMENSIONS['sidebar_expanded'] if self._is_expanded else DIMENSIONS['sidebar_collapsed']
        
        # Animate width
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(target_width)
        self.animation.start()
        
        # Show/hide text and icon
        self.dashboard_text.setVisible(self._is_expanded)
        self.dashboard_icon.setVisible(self._is_expanded)
        
        # Update button styles
        button_style = Qt.ToolButtonTextBesideIcon if self._is_expanded else Qt.ToolButtonIconOnly
        
        for btn in [
            self.btn_cashier, self.btn_event, self.btn_accounts, self.btn_reports,
            self.btn_operate, self.btn_op_a, self.btn_op_b,
            self.btn_settings, self.btn_utility, self.btn_logout
        ]:
            btn.setToolButtonStyle(button_style)
        
        # Update toggle button icon with proper size (0.4 inch)
        from PySide6.QtGui import QPixmap, QIcon
        from PySide6.QtCore import QSize
        import os
        toggle_icon_size = 38  # 0.4 inch
        chevron_file = "chevron_left.png" if self._is_expanded else "chevron_right.png"
        chevron_path = os.path.join("app", "assets", "icons", "sidebar", chevron_file)
        if os.path.exists(chevron_path):
            pixmap = QPixmap(chevron_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(toggle_icon_size, toggle_icon_size,
                                      Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
                self.toggle_btn.setIcon(QIcon(scaled))
                self.toggle_btn.setIconSize(QSize(toggle_icon_size, toggle_icon_size))
        else:
            from app.ui.components.icon_utils import set_icon
            set_icon(self.toggle_btn, f"icons/sidebar/{chevron_file}", toggle_icon_size)
        
        # Update stylesheet
        self.setStyleSheet(get_sidebar_stylesheet(self._is_expanded))
    
    def set_active_item(self, key: str):
        """Set active navigation item programmatically"""
        self._on_nav_clicked(key)
    
    def is_expanded(self) -> bool:
        return self._is_expanded
