# app/ui/cashier_overview.py
"""
Cashier Overview page matching Figma specifications exactly.
From COMPLETE_SYSTEM_ALGORITHM.md section 4.2 and CASHIER_OVERVIEW_ALGORITHM.md
"""

from __future__ import annotations
from typing import List, Dict, Optional
from dataclasses import dataclass

from PySide6.QtCore import Qt, QTimer, Signal, QSize
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QToolButton, QScrollArea, QFrame, QGridLayout
)

from app.ui.components.styles import (
    COLORS, FONT_SIZES, FONT_WEIGHTS, SPACING, DIMENSIONS, RADIUS,
    get_page_stylesheet
)
from .cashier_card import CashierCard
from app.ui.components.toggle_switch import ToggleSwitch
from app.ui.components.icon_utils import set_icon


@dataclass
class CashierData:
    """Cashier data model"""
    id: int
    name: str
    is_online: bool
    battery_percentage: int
    total_bets: float
    cash_in: float
    cash_out: float
    draw_bets: float
    cancel_bets: float
    unclaimed: float
    withdraw: float
    
    @property
    def coh(self) -> float:
        """Calculate Cash on Hand"""
        return self.cash_in - self.cash_out - self.withdraw
    
    def to_dict(self) -> dict:
        """Convert to dictionary for card component"""
        return {
            'id': self.id,
            'name': self.name,
            'is_online': self.is_online,
            'battery_percentage': self.battery_percentage,
            'total_bets': self.total_bets,
            'cash_in': self.cash_in,
            'cash_out': self.cash_out,
            'draw_bets': self.draw_bets,
            'cancel_bets': self.cancel_bets,
            'unclaimed': self.unclaimed,
            'withdraw': self.withdraw,
            'coh': self.coh
        }


class CashierOverview(QWidget):
    """Cashier Overview main page"""
    
    refresh_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("page-container")
        
        # State management
        self.cashiers: List[CashierData] = []
        self.global_view_all: bool = True
        self.individual_views: Dict[int, bool] = {}
        self.show_unclaimed: bool = True
        self.search_query: str = ""
        self.sort_option: str = "name-asc"
        self.show_tooltip: bool = False
        
        # Debounce timer for search
        self.search_timer: Optional[QTimer] = None
        
        # Load mock data (will be replaced with DB data later)
        self._load_mock_data()
        
        self._build_ui()
        self._render_cards()
    
    def _load_mock_data(self):
        """Load mock cashier data (from CASHIER_OVERVIEW_ALGORITHM.md)"""
        import random
        
        names = [
            "John Smith", "Maria Garcia", "David Lee", "Emily Davis",
            "James Wilson", "Jennifer Moore", "Jessica Martinez", "Amanda Martin",
            "Joseph Harris", "Karen Robinson", "Lisa Anderson", "Charles Clark",
            "Michael Brown", "Michelle White", "Nancy Lewis", "Richard Jackson",
            "Robert Taylor", "Sarah Johnson", "Thomas Thompson", "William Thomas"
        ]
        
        self.cashiers = []
        for i in range(20):
            cash_in = random.uniform(20000, 100000)
            cash_out = random.uniform(5000, 45000)
            withdraw = random.uniform(5000, 35000)
            
            cashier = CashierData(
                id=i + 1,
                name=names[i],
                is_online=random.random() > 0.3,  # 70% online
                battery_percentage=random.randint(0, 100),
                total_bets=random.uniform(10000, 60000),
                cash_in=cash_in,
                cash_out=cash_out,
                draw_bets=0.0,
                cancel_bets=0.0,
                unclaimed=0.0,
                withdraw=withdraw
            )
            self.cashiers.append(cashier)
            self.individual_views[cashier.id] = True
    
    def _build_ui(self):
        """Build the UI layout"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING['8'], SPACING['8'], SPACING['8'], SPACING['8'])
        layout.setSpacing(SPACING['6'])
        
        # Header Section
        header = self._build_header()
        layout.addLayout(header)
        
        # Filters Section
        filters = self._build_filters()
        layout.addLayout(filters)
        
        # Cards Grid (scrollable)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {COLORS['gray_50']};
                border: none;
            }}
        """)
        
        self.cards_container = QWidget()
        self.cards_layout = QGridLayout(self.cards_container)
        self.cards_layout.setSpacing(SPACING['4'])
        self.cards_layout.setAlignment(Qt.AlignTop)
        
        scroll_area.setWidget(self.cards_container)
        layout.addWidget(scroll_area)
        
        # Apply page stylesheet
        self.setStyleSheet(get_page_stylesheet())
    
    def _build_header(self) -> QHBoxLayout:
        """Build header section with title and controls"""
        header = QHBoxLayout()
        header.setSpacing(SPACING['3'])
        
        # Left: Title & Subtitle
        title_container = QVBoxLayout()
        title_container.setSpacing(SPACING['1'])
        
        title = QLabel("Cashier Overview")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: {FONT_SIZES['2xl']}px;
                font-weight: {FONT_WEIGHTS['bold']};
                color: {COLORS['gray_800']};
            }}
        """)
        title_container.addWidget(title)
        
        subtitle = QLabel("Monitor all cashier transactions and statuses")
        subtitle.setStyleSheet(f"""
            QLabel {{
                font-size: {FONT_SIZES['sm']}px;
                font-weight: {FONT_WEIGHTS['normal']};
                color: {COLORS['gray_500']};
            }}
        """)
        title_container.addWidget(subtitle)
        
        header.addLayout(title_container)
        header.addStretch()
        
        # Right: Controls
        controls = QHBoxLayout()
        controls.setSpacing(SPACING['3'])
        
        # Refresh button
        btn_refresh = QToolButton()
        btn_refresh.setFixedSize(40, 40)
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_refresh.setStyleSheet(f"""
            QToolButton {{
                background-color: {COLORS['gray_100']};
                border-radius: {RADIUS['lg']}px;
                border: none;
            }}
            QToolButton:hover {{
                background-color: {COLORS['gray_200']};
            }}
        """)
        # Load refresh icon from assets
        from PySide6.QtGui import QPixmap, QIcon
        import os
        refresh_path = os.path.join("app", "assets", "icons", "topbar", "refresh.png")
        if os.path.exists(refresh_path):
            refresh_pixmap = QPixmap(refresh_path)
            if not refresh_pixmap.isNull():
                scaled_pixmap = refresh_pixmap.scaled(
                    DIMENSIONS['icon_lg'], 
                    DIMENSIONS['icon_lg'],
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                btn_refresh.setIcon(QIcon(scaled_pixmap))
                btn_refresh.setIconSize(QSize(DIMENSIONS['icon_lg'], DIMENSIONS['icon_lg']))
        else:
            # Fallback to icon_utils if file doesn't exist
            set_icon(btn_refresh, "icons/topbar/refresh.png", DIMENSIONS['icon_lg'])
        btn_refresh.setToolTip("Refresh page")
        btn_refresh.clicked.connect(self._on_refresh)
        controls.addWidget(btn_refresh)
        
        # Unclaimed toggle switch
        toggle_container = QHBoxLayout()
        toggle_container.setSpacing(SPACING['2'])
        
        self.unclaimed_toggle = ToggleSwitch()
        self.unclaimed_toggle.setChecked(self.show_unclaimed)
        self.unclaimed_toggle.toggled.connect(self._on_unclaimed_toggle)
        toggle_container.addWidget(self.unclaimed_toggle)
        
        # Info button with tooltip
        btn_info = QToolButton()
        btn_info.setFixedSize(20, 20)
        btn_info.setCursor(Qt.PointingHandCursor)
        btn_info.setStyleSheet(f"""
            QToolButton {{
                background-color: {COLORS['gray_200']};
                border-radius: 10px;
                border: none;
            }}
            QToolButton:hover {{
                background-color: {COLORS['gray_300']};
            }}
        """)
        set_icon(btn_info, "icons/topbar/help.png", DIMENSIONS['icon_sm'])
        btn_info.setToolTip("Toggle to show/hide unclaimed amounts in all cashier cards")
        toggle_container.addWidget(btn_info)
        
        controls.addLayout(toggle_container)
        
        # View All / Hide All button
        self.btn_global_toggle = QPushButton("Hide All")
        self.btn_global_toggle.setCursor(Qt.PointingHandCursor)
        self.btn_global_toggle.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['blue_600']};
                color: {COLORS['white']};
                border: none;
                border-radius: {RADIUS['lg']}px;
                padding: {SPACING['2']}px {SPACING['4']}px;
                font-size: {FONT_SIZES['sm']}px;
                font-weight: {FONT_WEIGHTS['medium']};
            }}
            QPushButton:hover {{
                background-color: {COLORS['blue_700']};
            }}
        """)
        set_icon(self.btn_global_toggle, "icons/topbar/eye-off.png", DIMENSIONS['icon_md'])
        self.btn_global_toggle.clicked.connect(self._on_global_toggle)
        controls.addWidget(self.btn_global_toggle)
        
        header.addLayout(controls)
        
        return header
    
    def _build_filters(self) -> QHBoxLayout:
        """Build filters section with search and sort"""
        filters = QHBoxLayout()
        filters.setSpacing(SPACING['4'])
        
        # Search input container with icon
        search_container = QFrame()
        search_container.setObjectName("searchContainer")
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(SPACING['3'], 0, SPACING['3'], 0)
        search_layout.setSpacing(SPACING['2'])
        
        # Style the container to look like an input field
        search_container.setStyleSheet(f"""
            QFrame#searchContainer {{
                background-color: {COLORS['white']};
                border: 1px solid {COLORS['gray_200']};
                border-radius: {RADIUS['lg']}px;
                min-height: {DIMENSIONS['input_height']}px;
            }}
        """)
        
        # Search icon
        search_icon_label = QLabel()
        search_icon_label.setFixedSize(20, 20)
        search_icon_label.setScaledContents(True)
        from PySide6.QtGui import QPixmap
        import os
        search_icon_path = os.path.join("app", "assets", "icons", "topbar", "search.png")
        if os.path.exists(search_icon_path):
            search_pixmap = QPixmap(search_icon_path)
            if not search_pixmap.isNull():
                search_icon_label.setPixmap(search_pixmap.scaled(
                    20, 20,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ))
        search_layout.addWidget(search_icon_label)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search cashier by name...")
        self.search_input.setMinimumHeight(DIMENSIONS['input_height'])
        self.search_input.textChanged.connect(self._on_search_changed)
        # Remove border and background to blend with container
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                border: none;
                background-color: transparent;
                padding: 0px;
            }}
        """)
        search_layout.addWidget(self.search_input)
        
        filters.addWidget(search_container, 1)  # Stretch factor
        
        # Sort dropdown
        self.sort_dropdown = QComboBox()
        self.sort_dropdown.setMinimumHeight(DIMENSIONS['input_height'])
        self.sort_dropdown.setMinimumWidth(256)
        self.sort_dropdown.addItem("Name: A to Z", "name-asc")
        self.sort_dropdown.addItem("Name: Z to A", "name-desc")
        self.sort_dropdown.addItem("Status: Online First", "online")
        self.sort_dropdown.addItem("Status: Offline First", "offline")
        self.sort_dropdown.addItem("COH: Highest to Lowest", "coh-high")
        self.sort_dropdown.addItem("COH: Lowest to Highest", "coh-low")
        self.sort_dropdown.addItem("Total Bets: Highest to Lowest", "bets-high")
        self.sort_dropdown.addItem("Total Bets: Lowest to Highest", "bets-low")
        self.sort_dropdown.currentIndexChanged.connect(self._on_sort_changed)
        filters.addWidget(self.sort_dropdown)
        
        return filters
    
    def _on_refresh(self):
        """Handle refresh button click"""
        self.refresh_requested.emit()
        # TODO: Reload data from database
    
    def _on_unclaimed_toggle(self, checked: bool):
        """Handle unclaimed toggle switch"""
        self.show_unclaimed = checked
        self._render_cards()
    
    def _on_global_toggle(self):
        """Handle View All / Hide All button"""
        self.global_view_all = not self.global_view_all
        
        # Update all individual views
        for cashier_id in self.individual_views.keys():
            self.individual_views[cashier_id] = self.global_view_all
        
        # Update button text and icon
        if self.global_view_all:
            self.btn_global_toggle.setText("Hide All")
            set_icon(self.btn_global_toggle, "icons/topbar/eye-off.png", DIMENSIONS['icon_md'])
        else:
            self.btn_global_toggle.setText("View All")
            set_icon(self.btn_global_toggle, "icons/topbar/eye.png", DIMENSIONS['icon_md'])
        
        self._render_cards()
    
    def _on_search_changed(self, text: str):
        """Handle search input change (with debounce)"""
        if self.search_timer:
            self.search_timer.stop()
        
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(lambda: self._apply_search(text))
        self.search_timer.start(300)  # 300ms debounce
    
    def _apply_search(self, text: str):
        """Apply search filter"""
        self.search_query = text.lower()
        self._render_cards()
    
    def _on_sort_changed(self):
        """Handle sort dropdown change"""
        self.sort_option = self.sort_dropdown.currentData()
        self._render_cards()
    
    def _on_individual_toggle(self, cashier_id: int):
        """Handle individual card toggle"""
        self.individual_views[cashier_id] = not self.individual_views[cashier_id]
        self._render_cards()
    
    def _get_filtered_sorted_cashiers(self) -> List[CashierData]:
        """Apply filters and sorting to cashier data"""
        # Filter by search
        filtered = self.cashiers
        if self.search_query:
            filtered = [
                c for c in filtered
                if self.search_query in c.name.lower()
            ]
        
        # Sort
        if self.sort_option == "name-asc":
            filtered.sort(key=lambda c: c.name)
        elif self.sort_option == "name-desc":
            filtered.sort(key=lambda c: c.name, reverse=True)
        elif self.sort_option == "online":
            filtered.sort(key=lambda c: (not c.is_online, c.name))
        elif self.sort_option == "offline":
            filtered.sort(key=lambda c: (c.is_online, c.name))
        elif self.sort_option == "coh-high":
            filtered.sort(key=lambda c: c.coh, reverse=True)
        elif self.sort_option == "coh-low":
            filtered.sort(key=lambda c: c.coh)
        elif self.sort_option == "bets-high":
            filtered.sort(key=lambda c: c.total_bets, reverse=True)
        elif self.sort_option == "bets-low":
            filtered.sort(key=lambda c: c.total_bets)
        
        return filtered
    
    def _render_cards(self):
        """Render cashier cards in grid"""
        # Clear existing cards
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Get filtered and sorted cashiers
        cashiers = self._get_filtered_sorted_cashiers()
        
        if not cashiers:
            # Empty state
            empty_label = QLabel(f'No cashiers found matching "{self.search_query}"')
            empty_label.setStyleSheet(f"""
                QLabel {{
                    font-size: {FONT_SIZES['lg']}px;
                    color: {COLORS['gray_500']};
                    padding: {SPACING['12']}px;
                }}
            """)
            empty_label.setAlignment(Qt.AlignCenter)
            self.cards_layout.addWidget(empty_label, 0, 0, 1, 4)
            return
        
        # Render cards in responsive grid (4 columns max); equal width per column
        cols = 4
        for c in range(cols):
            self.cards_layout.setColumnStretch(c, 1)
        
        row = col = 0
        for cashier in cashiers:
            is_expanded = self.individual_views.get(cashier.id, self.global_view_all)
            
            card = CashierCard(
                cashier.to_dict(),
                is_expanded,
                self.show_unclaimed,
                self._on_individual_toggle
            )
            # Align cards to top so collapsed cards stay small and don't stretch with row
            self.cards_layout.addWidget(card, row, col, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            
            col += 1
            if col >= cols:
                col = 0
                row += 1
    
    def update_cashiers(self, cashiers: List[CashierData]):
        """Update cashier data from database"""
        self.cashiers = cashiers
        # Initialize individual views
        self.individual_views = {c.id: True for c in cashiers}
        self._render_cards()
