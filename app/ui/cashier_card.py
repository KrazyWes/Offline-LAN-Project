# app/ui/cashier_card.py
"""
Cashier Card component - enhanced layout and styling from reference design.
Clean card with header actions, status badge, transaction details, COH, and View Records.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QToolButton,
    QGridLayout, QSizePolicy, QGraphicsDropShadowEffect
)
from PySide6.QtGui import QColor
from app.ui.styles import (
    COLORS, FONT_SIZES, FONT_WEIGHTS, SPACING, RADIUS, DIMENSIONS,
    get_card_stylesheet
)
from app.ui.icon_utils import set_icon


def format_currency(amount: float) -> str:
    """Format amount as Philippine Peso"""
    return f"₱{amount:,.2f}"


def get_battery_icon_path(battery_percentage: int) -> str:
    """Get battery icon path based on percentage"""
    if battery_percentage >= 80:
        return "icons/battery/full_battery.png"
    elif battery_percentage >= 20:
        return "icons/battery/half_battery.png"
    else:
        return "icons/battery/low_battery.png"


def _muted_label(text: str) -> QLabel:
    """Small muted label for metric names"""
    w = QLabel(text)
    w.setObjectName("muted")
    return w


def _value_label(text: str) -> QLabel:
    """Value label for metrics"""
    w = QLabel(text)
    w.setObjectName("value")
    return w


class CashierCard(QFrame):
    """Cashier card with collapsed/expanded views"""
    
    def __init__(self, cashier_data: dict, is_expanded: bool, show_unclaimed: bool, 
                 toggle_callback=None, parent=None):
        super().__init__(parent)
        self.cashier_data = cashier_data
        self.is_expanded = is_expanded
        self.show_unclaimed = show_unclaimed
        self.toggle_callback = toggle_callback
        
        self.setObjectName("cashier-card")
        self.setStyleSheet(get_card_stylesheet())
        
        # Subtle shadow for card lift (reference design)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 38))
        self.setGraphicsEffect(shadow)
        
        # Same width for all cards (small and big)
        self.setMinimumWidth(DIMENSIONS['card_min_width'])
        
        # Collapsed cards must not stretch: keep small height. Expanded cards can grow.
        self._update_card_size_policy()
        
        self.layout = QVBoxLayout(self)
        pad = SPACING['3'] if not is_expanded else SPACING['4']
        self.layout.setContentsMargins(pad, pad, pad, pad)
        self.layout.setSpacing(SPACING['3'])
        
        self._render()
    
    def _update_card_size_policy(self):
        """Keep collapsed cards small; expanded cards can use full height."""
        if self.is_expanded:
            self.setMaximumHeight(16777215)  # QWidget default
            self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        else:
            self.setMaximumHeight(52)
            self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
    
    def _render(self):
        """Render card based on expanded state"""
        self._update_card_size_policy()
        # Clear existing widgets
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if self.is_expanded:
            self._render_expanded()
        else:
            self._render_collapsed()
    
    def _render_collapsed(self):
        """Render collapsed view (name only)"""
        row = QHBoxLayout()
        row.setSpacing(SPACING['2'])
        
        # Status indicator dot
        dot = QLabel()
        dot.setFixedSize(8, 8)
        dot.setStyleSheet(f"""
            QLabel {{
                background-color: {COLORS['green_500'] if self.cashier_data['is_online'] else COLORS['red_500']};
                border-radius: 4px;
            }}
        """)
        row.addWidget(dot)
        
        # Cashier name
        name_label = QLabel(self.cashier_data['name'])
        name_label.setStyleSheet(f"""
            QLabel {{
                font-size: {FONT_SIZES['base']}px;
                font-weight: {FONT_WEIGHTS['medium']};
                color: {COLORS['gray_800']};
            }}
        """)
        row.addWidget(name_label)
        
        row.addStretch()
        
        # Expand button
        btn_expand = QToolButton()
        btn_expand.setCursor(Qt.PointingHandCursor)
        btn_expand.setStyleSheet("QToolButton { background: transparent; border: none; }")
        set_icon(btn_expand, "icons/topbar/eye.png", DIMENSIONS['icon_md'])
        if self.toggle_callback:
            btn_expand.clicked.connect(lambda: self.toggle_callback(self.cashier_data['id']))
        row.addWidget(btn_expand)
        
        self.layout.addLayout(row)
    
    def _render_expanded(self):
        """Render expanded view (full details) - reference: clean two-column metrics, COH highlight, full-width CTA"""
        # ---- Header: action icons (left), status badge (center), visibility (right) ----
        header = QHBoxLayout()
        header.setSpacing(SPACING['3'])
        
        # Left: square action buttons (printer = blue, battery = light gray)
        icons_group = QHBoxLayout()
        icons_group.setSpacing(SPACING['2'])
        
        btn_print = QToolButton()
        btn_print.setFixedSize(40, 40)
        btn_print.setCursor(Qt.PointingHandCursor)
        btn_print.setStyleSheet(f"""
            QToolButton {{
                background-color: {COLORS['blue_100']};
                border-radius: {RADIUS['lg']}px;
                border: none;
            }}
            QToolButton:hover {{
                background-color: {COLORS['blue_200']};
            }}
        """)
        set_icon(btn_print, "icons/card/printer.png", DIMENSIONS['icon_lg'])
        btn_print.setToolTip("Print transaction card")
        icons_group.addWidget(btn_print)
        
        btn_battery = QToolButton()
        btn_battery.setFixedSize(40, 40)
        btn_battery.setCursor(Qt.PointingHandCursor)
        btn_battery.setStyleSheet(f"""
            QToolButton {{
                background-color: {COLORS['gray_100']};
                border-radius: {RADIUS['lg']}px;
                border: none;
            }}
            QToolButton:hover {{
                background-color: {COLORS['gray_200']};
            }}
        """)
        battery_path = get_battery_icon_path(self.cashier_data['battery_percentage'])
        set_icon(btn_battery, battery_path, DIMENSIONS['icon_lg'])
        btn_battery.setToolTip(f"Battery: {self.cashier_data['battery_percentage']}%")
        icons_group.addWidget(btn_battery)
        
        header.addLayout(icons_group)
        
        # Center: Online/Offline pill badge
        badge = QLabel("Online" if self.cashier_data['is_online'] else "Offline")
        badge.setObjectName("badge-online" if self.cashier_data['is_online'] else "badge-offline")
        header.addWidget(badge)
        header.addStretch()
        
        # Right: visibility (hide) icon
        btn_collapse = QToolButton()
        btn_collapse.setFixedSize(36, 36)
        btn_collapse.setCursor(Qt.PointingHandCursor)
        btn_collapse.setStyleSheet(f"""
            QToolButton {{
                background-color: transparent;
                border: none;
                border-radius: {RADIUS['md']}px;
            }}
            QToolButton:hover {{
                background-color: {COLORS['gray_100']};
            }}
        """)
        set_icon(btn_collapse, "icons/topbar/eye-off.png", DIMENSIONS['icon_md'])
        if self.toggle_callback:
            btn_collapse.clicked.connect(lambda: self.toggle_callback(self.cashier_data['id']))
        btn_collapse.setToolTip("Hide details")
        header.addWidget(btn_collapse)
        
        self.layout.addLayout(header)
        
        # Cashier: (muted) + name (bold)
        name_row = QHBoxLayout()
        name_row.setSpacing(SPACING['1'])
        prefix_label = QLabel("Cashier:")
        prefix_label.setObjectName("card-prefix")
        name_row.addWidget(prefix_label)
        name_label = QLabel(self.cashier_data['name'])
        name_label.setObjectName("card-title")
        name_row.addWidget(name_label)
        name_row.addStretch()
        self.layout.addSpacing(SPACING['2'])
        self.layout.addLayout(name_row)
        self.layout.addSpacing(SPACING['2'])
        
        # Transaction details: two-column layout, label (muted) + value per cell
        grid = QGridLayout()
        grid.setVerticalSpacing(SPACING['2'])
        grid.setHorizontalSpacing(SPACING['4'])
        
        def add_row(r, left_label, left_val, right_label, right_val):
            grid.addWidget(_muted_label(left_label), r, 0)
            grid.addWidget(_value_label(left_val), r, 1)
            grid.addWidget(_muted_label(right_label), r, 2)
            grid.addWidget(_value_label(right_val), r, 3)
        
        add_row(0, "Total Bets", format_currency(self.cashier_data['total_bets']),
                "Cash In", format_currency(self.cashier_data['cash_in']))
        add_row(1, "Cash Out", format_currency(self.cashier_data['cash_out']),
                "Draw Bets", format_currency(self.cashier_data['draw_bets']))
        if self.show_unclaimed:
            add_row(2, "Cancel Bets", format_currency(self.cashier_data['cancel_bets']),
                    "Unclaimed", format_currency(self.cashier_data['unclaimed']))
            add_row(3, "Withdraw", format_currency(self.cashier_data['withdraw']), "", "")
        else:
            add_row(2, "Cancel Bets", format_currency(self.cashier_data['cancel_bets']),
                    "Withdraw", format_currency(self.cashier_data['withdraw']))
        
        # Ensure columns 2 and 3 have min width so values align
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)
        
        self.layout.addLayout(grid)
        
        # Horizontal separator above COH
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"QFrame {{ border-top: 1px solid {COLORS['gray_200']}; background: transparent; }}")
        self.layout.addSpacing(SPACING['4'])
        self.layout.addWidget(line)
        self.layout.addSpacing(SPACING['3'])
        
        # Cash on Hand (COH) - prominent blue value, centered
        coh_label = QLabel("Cash on Hand (COH)")
        coh_label.setObjectName("muted")
        self.layout.addWidget(coh_label)
        coh_value = QLabel(format_currency(self.cashier_data['coh']))
        coh_value.setObjectName("coh-value")
        coh_value.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        coh_row = QHBoxLayout()
        coh_row.addStretch()
        coh_row.addWidget(coh_value)
        coh_row.addStretch()
        self.layout.addLayout(coh_row)
        
        # View Records - full-width button, reduced height
        self.layout.addSpacing(SPACING['3'])
        btn_records = QPushButton("View Records")
        btn_records.setObjectName("primary-btn")
        btn_records.setCursor(Qt.PointingHandCursor)
        btn_records.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout.addWidget(btn_records)
    
    def update_state(self, is_expanded: bool, show_unclaimed: bool):
        """Update card state (used when reusing widget; normally overview recreates cards)."""
        if self.is_expanded != is_expanded or self.show_unclaimed != show_unclaimed:
            self.is_expanded = is_expanded
            self.show_unclaimed = show_unclaimed
            self._render()
