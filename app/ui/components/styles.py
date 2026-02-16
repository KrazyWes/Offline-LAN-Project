# app/ui/components/styles.py
"""
Centralized styling system matching Figma specifications exactly.
All colors, typography, spacing, and dimensions from COMPLETE_SYSTEM_ALGORITHM.md
"""

# =========================================================
# COLOR PALETTE (exact hex values from guide)
# =========================================================

COLORS = {
    # Grayscale
    'gray_50': '#F9FAFB',
    'gray_100': '#F3F4F6',
    'gray_200': '#E5E7EB',
    'gray_300': '#D1D5DB',
    'gray_400': '#9CA3AF',
    'gray_500': '#6B7280',
    'gray_600': '#4B5563',
    'gray_700': '#374151',
    'gray_800': '#1F2937',
    
    # Blue (Primary Action)
    'blue_50': '#EFF6FF',
    'blue_100': '#DBEAFE',
    'blue_200': '#BFDBFE',
    'blue_500': '#3B82F6',
    'blue_600': '#2563EB',
    'blue_700': '#1D4ED8',
    
    # Status Colors
    'green_100': '#D1FAE5',
    'green_500': '#10B981',
    'green_600': '#059669',
    'green_700': '#047857',
    
    'red_100': '#FEE2E2',
    'red_500': '#EF4444',
    'red_600': '#DC2626',
    'red_700': '#B91C1C',
    
    'yellow_600': '#D97706',
    
    # Background
    'white': '#FFFFFF',
    'transparent': 'transparent'
}

# =========================================================
# TYPOGRAPHY
# =========================================================

FONT_SIZES = {
    'xs': 12,    # 0.75rem
    'sm': 14,    # 0.875rem
    'base': 16,  # 1rem (default)
    'lg': 18,    # 1.125rem
    'xl': 20,    # 1.25rem
    '2xl': 24,   # 1.5rem
}

FONT_WEIGHTS = {
    'normal': 400,
    'medium': 500,
    'semibold': 600,
    'bold': 700
}

# =========================================================
# SPACING SYSTEM (base unit = 4px)
# =========================================================

SPACING = {
    '0': 0,
    '1': 4,    # 0.25rem
    '2': 8,    # 0.5rem
    '3': 12,   # 0.75rem
    '4': 16,   # 1rem
    '5': 20,   # 1.25rem
    '6': 24,   # 1.5rem
    '8': 32,   # 2rem
    '10': 40,  # 2.5rem
    '12': 48,  # 3rem
    '16': 64,  # 4rem
    '20': 80   # 5rem
}

# =========================================================
# BORDER RADIUS
# =========================================================

RADIUS = {
    'sm': 4,
    'md': 6,
    'lg': 8,
    'xl': 12,
    'full': 9999  # Circular (badges, status dots)
}

# =========================================================
# DIMENSIONS
# =========================================================

DIMENSIONS = {
    'sidebar_expanded': 256,
    'sidebar_collapsed': 80,
    'header_height': 64,
    'card_min_width': 260,
    'button_height': 40,
    'input_height': 48,
    'icon_sm': 14,
    'icon_md': 18,
    'icon_lg': 20,
    'icon_xl': 22,
}

# =========================================================
# QSS STYLESHEET GENERATORS
# =========================================================

def get_sidebar_stylesheet(is_expanded: bool) -> str:
    """Generate sidebar stylesheet based on expanded state"""
    width = DIMENSIONS['sidebar_expanded'] if is_expanded else DIMENSIONS['sidebar_collapsed']
    
    return f"""
    QFrame#sidebar {{
        background-color: {COLORS['gray_50']};
        border-right: 1px solid {COLORS['gray_200']};
        min-width: {width}px;
        max-width: {width}px;
    }}
    
    QLabel#sidebarTitle {{
        font-size: {FONT_SIZES['lg']}px;
        font-weight: {FONT_WEIGHTS['semibold']};
        color: {COLORS['gray_800']};
    }}
    
    QToolButton.nav-button {{
        border: none;
        padding: {SPACING['3']}px {SPACING['4']}px;
        text-align: left;
        font-size: {FONT_SIZES['sm']}px;
        font-weight: {FONT_WEIGHTS['medium']};
        color: {COLORS['gray_700']};
        background-color: transparent;
        min-width: 100%;
        width: 100%;
    }}
    
    QToolButton.nav-button:hover {{
        background-color: {COLORS['gray_100']};
    }}
    
    QToolButton.nav-button:checked {{
        background-color: {COLORS['blue_600']};
        color: {COLORS['white']};
    }}
    
    QFrame#operatePanel {{
        background-color: transparent;
        border: none;
    }}
    
    QFrame#operatePanel QToolButton {{
        padding-left: {SPACING['4']}px;  /* Same padding as other nav buttons - no indentation */
        background-color: transparent;
        border: none;
    }}
    
    QFrame#operatePanel QToolButton:hover {{
        background-color: {COLORS['gray_100']};
    }}
    
    QFrame#operatePanel QToolButton:checked {{
        background-color: {COLORS['blue_600']};
        color: {COLORS['white']};
    }}
    """

def get_card_stylesheet() -> str:
    """Generate cashier card stylesheet (reference: clean card with shadow, rounded corners)"""
    return f"""
    QFrame#cashier-card {{
        background-color: {COLORS['white']};
        border: 1px solid {COLORS['gray_200']};
        border-radius: {RADIUS['xl']}px;
    }}
    
    QLabel#card-prefix {{
        font-size: {FONT_SIZES['sm']}px;
        font-weight: {FONT_WEIGHTS['normal']};
        color: {COLORS['gray_500']};
    }}
    
    QLabel#card-title {{
        font-size: {FONT_SIZES['xl']}px;
        font-weight: {FONT_WEIGHTS['bold']};
        color: {COLORS['gray_800']};
    }}
    
    QLabel.muted {{
        font-size: {FONT_SIZES['xs']}px;
        font-weight: {FONT_WEIGHTS['normal']};
        color: {COLORS['gray_500']};
    }}
    
    QLabel.value {{
        font-size: {FONT_SIZES['sm']}px;
        font-weight: {FONT_WEIGHTS['bold']};
        color: {COLORS['gray_800']};
    }}
    
    QLabel#coh-value {{
        font-size: {FONT_SIZES['xl']}px;
        font-weight: {FONT_WEIGHTS['bold']};
        color: {COLORS['blue_600']};
    }}
    
    QPushButton#primary-btn {{
        background-color: {COLORS['blue_600']};
        color: {COLORS['white']};
        border: none;
        border-radius: {RADIUS['lg']}px;
        padding: {SPACING['2']}px {SPACING['4']}px;
        font-size: {FONT_SIZES['sm']}px;
        font-weight: {FONT_WEIGHTS['medium']};
        min-height: 28px;
    }}
    
    QPushButton#primary-btn:hover {{
        background-color: {COLORS['blue_700']};
    }}
    
    QLabel#badge-online {{
        background-color: {COLORS['green_100']};
        color: {COLORS['green_600']};
        border-radius: {RADIUS['xl']}px;
        padding: {SPACING['2']}px {SPACING['4']}px;
        font-size: {FONT_SIZES['xs']}px;
        font-weight: {FONT_WEIGHTS['medium']};
    }}
    
    QLabel#badge-offline {{
        background-color: {COLORS['red_100']};
        color: {COLORS['red_600']};
        border-radius: {RADIUS['xl']}px;
        padding: {SPACING['2']}px {SPACING['4']}px;
        font-size: {FONT_SIZES['xs']}px;
        font-weight: {FONT_WEIGHTS['medium']};
    }}
    """

def get_page_stylesheet() -> str:
    """Generate page container stylesheet"""
    return f"""
    QWidget#page-container {{
        background-color: {COLORS['gray_50']};
    }}
    
    QLineEdit {{
        border: 1px solid {COLORS['gray_300']};
        border-radius: {RADIUS['lg']}px;
        padding: {SPACING['3']}px {SPACING['4']}px;
        font-size: {FONT_SIZES['base']}px;
        background-color: {COLORS['white']};
    }}
    
    QLineEdit:focus {{
        border: none;
        outline: 2px solid {COLORS['blue_500']};
    }}
    
    QComboBox {{
        border: 1px solid {COLORS['gray_300']};
        border-radius: {RADIUS['lg']}px;
        padding: {SPACING['3']}px {SPACING['4']}px;
        font-size: {FONT_SIZES['base']}px;
        background-color: {COLORS['white']};
        min-width: 256px;
    }}
    
    QComboBox:focus {{
        border: none;
        outline: 2px solid {COLORS['blue_500']};
    }}
    """
