# PySide6 + PostgreSQL Migration Guide
## Complete Dashboard Application - Technical Specification

**Document Version:** 1.0  
**Date:** February 14, 2026  
**Target Framework:** PySide6 (Qt for Python)  
**Database:** PostgreSQL  
**Original Stack:** React + TypeScript + Tailwind CSS

---

## TABLE OF CONTENTS

1. [Application Architecture](#1-application-architecture)
2. [Database Schema](#2-database-schema)
3. [Visual Design Specifications](#3-visual-design-specifications)
4. [Component Breakdown](#4-component-breakdown)
5. [State Management](#5-state-management)
6. [User Interactions & Event Handling](#6-user-interactions--event-handling)
7. [Data Flow & Business Logic](#7-data-flow--business-logic)
8. [PySide6 Implementation Guide](#8-pyside6-implementation-guide)
9. [PostgreSQL Integration](#9-postgresql-integration)
10. [Responsive Design & Layouts](#10-responsive-design--layouts)
11. [Icons & Assets](#11-icons--assets)
12. [Testing Checklist](#12-testing-checklist)

---

## 1. APPLICATION ARCHITECTURE

### 1.1 Application Structure

```
Dashboard Application
│
├── Main Window (QMainWindow)
│   ├── Sidebar (QWidget) - Left side, collapsible
│   └── Content Area (QWidget) - Right side, scrollable
│       └── Dynamic Content (QStackedWidget)
│           ├── Cashier Overview Page
│           ├── Event Overview Page (placeholder)
│           ├── Accounts Page (placeholder)
│           ├── Reports & Database Page (placeholder)
│           ├── Operator A Page (placeholder)
│           ├── Operator B Page (placeholder)
│           ├── Settings Page (placeholder)
│           └── Utility Page (placeholder)
```

### 1.2 Main Window Layout

**Window Properties:**
- **Default Size:** 1920x1080 (Full HD)
- **Minimum Size:** 1024x768
- **Background Color:** #F9FAFB (gray-50)
- **Layout:** Horizontal Box Layout (QHBoxLayout)
  - Left: Sidebar widget
  - Right: Content area widget (with stretch factor)

**Layout Code Structure (PySide6):**
```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard - Cashier Overview")
        self.setMinimumSize(1024, 768)
        self.resize(1920, 1080)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main horizontal layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar (left)
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Content area (right) - with scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { background-color: #F9FAFB; border: none; }")
        
        self.content_widget = QWidget()
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(32, 32, 32, 32)  # 8 * 4 = 32px padding
        
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget)
        
        scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(scroll_area, 1)  # Stretch factor = 1
        
        # Connect sidebar signals
        self.sidebar.menu_changed.connect(self.switch_content)
```

### 1.3 Application Flow

1. **Startup:**
   - Initialize database connection
   - Load user preferences (sidebar state, last viewed page)
   - Fetch initial cashier data
   - Display Cashier Overview by default

2. **Runtime:**
   - User navigates via sidebar
   - Content area updates based on selection
   - Data refreshes on user action or timer
   - Real-time updates for cashier status changes

3. **Shutdown:**
   - Save user preferences
   - Close database connections
   - Clean up resources

---

## 2. DATABASE SCHEMA

### 2.1 PostgreSQL Database: `dashboard_db`

**Connection Details:**
```python
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'dashboard_db',
    'user': 'dashboard_user',
    'password': 'your_secure_password'
}
```

### 2.2 Table: `cashiers`

**Purpose:** Store cashier information and device details

```sql
CREATE TABLE cashiers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100),
    phone VARCHAR(20),
    device_id VARCHAR(50) UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_cashiers_name ON cashiers(name);
CREATE INDEX idx_cashiers_device_id ON cashiers(device_id);
CREATE INDEX idx_cashiers_is_active ON cashiers(is_active);
```

**Sample Data:**
```sql
INSERT INTO cashiers (name, email, device_id) VALUES
('John Smith', 'john.smith@example.com', 'DEV001'),
('Maria Garcia', 'maria.garcia@example.com', 'DEV002'),
('David Lee', 'david.lee@example.com', 'DEV003'),
-- ... (total 20 cashiers)
('Nancy Lewis', 'nancy.lewis@example.com', 'DEV020');
```

### 2.3 Table: `cashier_status`

**Purpose:** Track real-time cashier device status

```sql
CREATE TABLE cashier_status (
    id SERIAL PRIMARY KEY,
    cashier_id INTEGER REFERENCES cashiers(id) ON DELETE CASCADE,
    is_online BOOLEAN DEFAULT FALSE,
    battery_percentage INTEGER CHECK (battery_percentage >= 0 AND battery_percentage <= 100),
    last_heartbeat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(cashier_id)
);

-- Indexes
CREATE INDEX idx_cashier_status_cashier_id ON cashier_status(cashier_id);
CREATE INDEX idx_cashier_status_is_online ON cashier_status(is_online);
```

**Sample Data:**
```sql
INSERT INTO cashier_status (cashier_id, is_online, battery_percentage) VALUES
(1, TRUE, 85),
(2, TRUE, 92),
(3, FALSE, 45),
-- ... (one entry per cashier)
(20, TRUE, 78);
```

### 2.4 Table: `transactions`

**Purpose:** Store all cashier transactions

```sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    cashier_id INTEGER REFERENCES cashiers(id) ON DELETE CASCADE,
    transaction_type VARCHAR(20) NOT NULL, -- 'bet', 'cashin', 'cashout', 'draw', 'cancel', 'unclaimed', 'withdraw'
    amount DECIMAL(15, 2) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reference_number VARCHAR(50) UNIQUE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_transactions_cashier_id ON transactions(cashier_id);
CREATE INDEX idx_transactions_type ON transactions(transaction_type);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_reference ON transactions(reference_number);
```

**Transaction Types:**
- `bet` - Total bets placed
- `cashin` - Cash received
- `cashout` - Cash paid out
- `draw` - Draw bets
- `cancel` - Cancelled bets
- `unclaimed` - Unclaimed winnings
- `withdraw` - Cash withdrawals

### 2.5 Table: `transaction_summary`

**Purpose:** Materialized view for quick cashier overview data (updated periodically)

```sql
CREATE TABLE transaction_summary (
    id SERIAL PRIMARY KEY,
    cashier_id INTEGER REFERENCES cashiers(id) ON DELETE CASCADE,
    total_bets DECIMAL(15, 2) DEFAULT 0,
    cash_in DECIMAL(15, 2) DEFAULT 0,
    cash_out DECIMAL(15, 2) DEFAULT 0,
    draw_bets DECIMAL(15, 2) DEFAULT 0,
    cancel_bets DECIMAL(15, 2) DEFAULT 0,
    unclaimed DECIMAL(15, 2) DEFAULT 0,
    withdraw DECIMAL(15, 2) DEFAULT 0,
    coh DECIMAL(15, 2) DEFAULT 0, -- Cash on Hand (calculated)
    summary_date DATE DEFAULT CURRENT_DATE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(cashier_id, summary_date)
);

-- Indexes
CREATE INDEX idx_transaction_summary_cashier_id ON transaction_summary(cashier_id);
CREATE INDEX idx_transaction_summary_date ON transaction_summary(summary_date);
```

**COH Calculation Formula:**
```
COH = cash_in - cash_out - withdraw
```

### 2.6 Stored Procedures

**2.6.1 Update Transaction Summary**

```sql
CREATE OR REPLACE FUNCTION update_transaction_summary(p_cashier_id INTEGER, p_date DATE)
RETURNS VOID AS $$
DECLARE
    v_total_bets DECIMAL(15, 2);
    v_cash_in DECIMAL(15, 2);
    v_cash_out DECIMAL(15, 2);
    v_draw_bets DECIMAL(15, 2);
    v_cancel_bets DECIMAL(15, 2);
    v_unclaimed DECIMAL(15, 2);
    v_withdraw DECIMAL(15, 2);
    v_coh DECIMAL(15, 2);
BEGIN
    -- Calculate totals for the given cashier and date
    SELECT
        COALESCE(SUM(CASE WHEN transaction_type = 'bet' THEN amount ELSE 0 END), 0),
        COALESCE(SUM(CASE WHEN transaction_type = 'cashin' THEN amount ELSE 0 END), 0),
        COALESCE(SUM(CASE WHEN transaction_type = 'cashout' THEN amount ELSE 0 END), 0),
        COALESCE(SUM(CASE WHEN transaction_type = 'draw' THEN amount ELSE 0 END), 0),
        COALESCE(SUM(CASE WHEN transaction_type = 'cancel' THEN amount ELSE 0 END), 0),
        COALESCE(SUM(CASE WHEN transaction_type = 'unclaimed' THEN amount ELSE 0 END), 0),
        COALESCE(SUM(CASE WHEN transaction_type = 'withdraw' THEN amount ELSE 0 END), 0)
    INTO
        v_total_bets, v_cash_in, v_cash_out, v_draw_bets, 
        v_cancel_bets, v_unclaimed, v_withdraw
    FROM transactions
    WHERE cashier_id = p_cashier_id 
      AND DATE(transaction_date) = p_date;
    
    -- Calculate COH
    v_coh := v_cash_in - v_cash_out - v_withdraw;
    
    -- Insert or update summary
    INSERT INTO transaction_summary (
        cashier_id, total_bets, cash_in, cash_out, draw_bets, 
        cancel_bets, unclaimed, withdraw, coh, summary_date, updated_at
    ) VALUES (
        p_cashier_id, v_total_bets, v_cash_in, v_cash_out, v_draw_bets,
        v_cancel_bets, v_unclaimed, v_withdraw, v_coh, p_date, CURRENT_TIMESTAMP
    )
    ON CONFLICT (cashier_id, summary_date) 
    DO UPDATE SET
        total_bets = EXCLUDED.total_bets,
        cash_in = EXCLUDED.cash_in,
        cash_out = EXCLUDED.cash_out,
        draw_bets = EXCLUDED.draw_bets,
        cancel_bets = EXCLUDED.cancel_bets,
        unclaimed = EXCLUDED.unclaimed,
        withdraw = EXCLUDED.withdraw,
        coh = EXCLUDED.coh,
        updated_at = CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;
```

**2.6.2 Get Cashier Overview Data**

```sql
CREATE OR REPLACE FUNCTION get_cashier_overview(p_date DATE DEFAULT CURRENT_DATE)
RETURNS TABLE (
    cashier_id INTEGER,
    cashier_name VARCHAR(100),
    is_online BOOLEAN,
    battery_percentage INTEGER,
    total_bets DECIMAL(15, 2),
    cash_in DECIMAL(15, 2),
    cash_out DECIMAL(15, 2),
    draw_bets DECIMAL(15, 2),
    cancel_bets DECIMAL(15, 2),
    unclaimed DECIMAL(15, 2),
    withdraw DECIMAL(15, 2),
    coh DECIMAL(15, 2)
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id AS cashier_id,
        c.name AS cashier_name,
        COALESCE(cs.is_online, FALSE) AS is_online,
        COALESCE(cs.battery_percentage, 0) AS battery_percentage,
        COALESCE(ts.total_bets, 0) AS total_bets,
        COALESCE(ts.cash_in, 0) AS cash_in,
        COALESCE(ts.cash_out, 0) AS cash_out,
        COALESCE(ts.draw_bets, 0) AS draw_bets,
        COALESCE(ts.cancel_bets, 0) AS cancel_bets,
        COALESCE(ts.unclaimed, 0) AS unclaimed,
        COALESCE(ts.withdraw, 0) AS withdraw,
        COALESCE(ts.coh, 0) AS coh
    FROM cashiers c
    LEFT JOIN cashier_status cs ON c.id = cs.cashier_id
    LEFT JOIN transaction_summary ts ON c.id = ts.cashier_id AND ts.summary_date = p_date
    WHERE c.is_active = TRUE
    ORDER BY c.name;
END;
$$ LANGUAGE plpgsql;
```

### 2.7 Database Triggers

**Auto-update transaction summary on transaction insert:**

```sql
CREATE OR REPLACE FUNCTION trigger_update_summary()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM update_transaction_summary(NEW.cashier_id, DATE(NEW.transaction_date));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_summary_on_transaction
AFTER INSERT OR UPDATE ON transactions
FOR EACH ROW
EXECUTE FUNCTION trigger_update_summary();
```

### 2.8 User Preferences Table

**Purpose:** Store user UI preferences

```sql
CREATE TABLE user_preferences (
    id SERIAL PRIMARY KEY,
    preference_key VARCHAR(50) UNIQUE NOT NULL,
    preference_value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample preferences
INSERT INTO user_preferences (preference_key, preference_value) VALUES
('sidebar_expanded', 'true'),
('last_active_page', 'cashier-overview'),
('show_unclaimed_field', 'true'),
('cashier_cards_view_all', 'true');
```

---

## 3. VISUAL DESIGN SPECIFICATIONS

### 3.1 Color Palette

**Primary Colors:**
```python
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
```

### 3.2 Typography

**Font Family:**
```python
FONTS = {
    'family': 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    'fallback': 'Arial, sans-serif'
}
```

**Font Sizes:**
```python
FONT_SIZES = {
    'xs': 12,    # 0.75rem
    'sm': 14,    # 0.875rem
    'base': 16,  # 1rem (default)
    'lg': 18,    # 1.125rem
    'xl': 20,    # 1.25rem
    '2xl': 24,   # 1.5rem
}
```

**Font Weights:**
```python
FONT_WEIGHTS = {
    'normal': 400,
    'medium': 500,
    'semibold': 600,
    'bold': 700
}
```

### 3.3 Spacing System

**All spacing values in pixels (base unit = 4px):**
```python
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
```

### 3.4 Border Radius

```python
RADIUS = {
    'sm': 4,    # Small elements
    'md': 6,    # Medium elements
    'lg': 8,    # Large elements (buttons, cards)
    'xl': 12,   # Extra large
    'full': 9999  # Circular (badges, status dots)
}
```

### 3.5 Shadows

```python
SHADOWS = {
    'sm': 'QGraphicsDropShadowEffect: blurRadius=2, xOffset=0, yOffset=1, color=rgba(0,0,0,0.05)',
    'md': 'QGraphicsDropShadowEffect: blurRadius=6, xOffset=0, yOffset=4, color=rgba(0,0,0,0.1)',
    'lg': 'QGraphicsDropShadowEffect: blurRadius=15, xOffset=0, yOffset=10, color=rgba(0,0,0,0.1)'
}
```

### 3.6 Transitions

**All transitions should be smooth with 300ms duration:**
```python
TRANSITIONS = {
    'default': 300,  # milliseconds
    'fast': 150,
    'slow': 500
}
```

---

## 4. COMPONENT BREAKDOWN

### 4.1 Sidebar Component

**Class Name:** `Sidebar` (inherits QWidget)

**Dimensions:**
- Expanded Width: 256px (64 * 4)
- Collapsed Width: 80px (20 * 4)
- Height: 100% of window
- Transition Duration: 300ms

**Structure:**

```
Sidebar (QWidget)
├── Header Section (QWidget)
│   ├── Dashboard Icon (QLabel) - only when expanded
│   ├── Dashboard Text (QLabel) - only when expanded
│   └── Toggle Button (QPushButton) - chevron icon
│
├── Navigation Section (QScrollArea)
│   ├── Main Menu Items (QVBoxLayout)
│   │   ├── Cashier Overview (NavButton)
│   │   ├── Event Overview (NavButton)
│   │   ├── Accounts (NavButton)
│   │   ├── Reports and Database (NavButton)
│   │   └── Operate (NavButton with submenu)
│   │       ├── Operator A (SubNavButton)
│   │       └── Operator B (SubNavButton)
│   │
│   └── Bottom Menu Items (QVBoxLayout)
│       ├── Settings (NavButton)
│       ├── Utility (NavButton)
│       └── Logout (NavButton)
```

**Visual Specifications:**

**Header:**
- Height: 64px
- Background: white (#FFFFFF)
- Border Bottom: 1px solid #E5E7EB
- Padding: 16px
- Layout: Horizontal flex (space-between)

**Dashboard Icon:**
- Icon: LayoutDashboard (from lucide icons)
- Size: 22x22px
- Color: #2563EB (blue-600)
- Margin Right: 8px

**Dashboard Text:**
- Text: "Dashboard"
- Font Size: 18px (lg)
- Font Weight: 600 (semibold)
- Color: #1F2937 (gray-800)

**Toggle Button:**
- Size: 40x40px
- Padding: 8px
- Border Radius: 8px
- Background: transparent
- Hover Background: #F3F4F6 (gray-100)
- Icon Size: 20x20px
- Icon Color: #4B5563 (gray-600)
- Icon: ChevronLeft (expanded) / ChevronRight (collapsed)

**Navigation Item (NavButton):**
- Full Width
- Height: 48px (12px padding top/bottom)
- Padding: 12px 16px
- Font Size: 14px (sm)
- Font Weight: 500 (medium)
- Border Radius: 0px
- Gap between icon and text: 12px

**States:**
```python
# Default state
{
    'background': 'transparent',
    'color': '#374151',  # gray-700
}

# Hover state
{
    'background': '#F3F4F6',  # gray-100
    'color': '#374151',
}

# Active state
{
    'background': '#DBEAFE',  # blue-100
    'color': '#2563EB',  # blue-600
}
```

**Icon Specifications:**
- Size: 20x20px
- Color: Inherits from parent text color

**Sub-Navigation Item (SubNavButton):**
- Same as NavButton but:
- Padding Left: 56px (14 * 4) - indented
- Background on hover: #F9FAFB (gray-50)
- Background active: #EFF6FF (blue-50)
- Parent Background (Operate submenu container): #F9FAFB

**Collapse/Expand Behavior:**

When collapsed:
- Show only icons (centered)
- Hide all text
- Hide submenu chevron
- Submenu doesn't open
- Show tooltip on hover with full menu name

When expanded:
- Show icons + text
- Show submenu chevron for "Operate"
- Submenu can toggle open/close
- No tooltips needed

**Icon Mapping:**
```python
MENU_ICONS = {
    'cashier-overview': 'LayoutDashboard',
    'event-overview': 'Calendar',
    'accounts': 'Users',
    'reports': 'FileText',
    'operate': 'Wrench',
    'settings': 'Settings',
    'utility': 'Wrench',
    'logout': 'LogOut',
}
```

**Submenu Toggle:**
- Icon Size: 16x16px
- Chevron Down (closed) / Chevron Up (open)
- Position: Right aligned in button

**Signal Emitted:**
```python
menu_changed = Signal(str)  # Emits menu item ID
```

### 4.2 Cashier Overview Component

**Class Name:** `CashierOverview` (inherits QWidget)

**Structure:**

```
CashierOverview (QWidget)
├── Header Section (QWidget)
│   ├── Left: Title & Subtitle
│   └── Right: Controls
│       ├── Refresh Button
│       ├── Unclaimed Toggle Switch
│       ├── Unclaimed Info Button (with tooltip)
│       └── View All / Hide All Button
│
├── Filters Section (QWidget)
│   ├── Search Input (QLineEdit)
│   └── Sort Dropdown (QComboBox)
│
└── Cards Grid (QWidget with FlowLayout or Grid)
    └── Cashier Cards (20 cards, dynamic)
```

**Header Section:**

**Container:**
- Layout: Horizontal (space-between)
- Padding Bottom: 24px

**Title Area (Left):**
```python
{
    'title': 'Cashier Overview',
    'title_font_size': 24,  # 2xl
    'title_font_weight': 700,  # bold
    'title_color': '#1F2937',  # gray-800
    
    'subtitle': 'Monitor all cashier transactions and statuses',
    'subtitle_font_size': 14,  # sm
    'subtitle_font_weight': 400,  # normal
    'subtitle_color': '#6B7280',  # gray-500
    'subtitle_margin_top': 4,
}
```

**Controls Area (Right):**
- Layout: Horizontal
- Gap: 12px
- Alignment: Center vertically

**1. Refresh Button:**
```python
{
    'size': (40, 40),  # width, height
    'padding': 8,
    'border_radius': 8,
    'background': '#F3F4F6',  # gray-100
    'background_hover': '#E5E7EB',  # gray-200
    'icon': 'RefreshCw',
    'icon_size': 20,
    'icon_color': '#374151',  # gray-700
    'tooltip': 'Refresh page',
    'action': 'Reload data from database',
}
```

**2. Unclaimed Toggle Switch (iOS-style):**
```python
# Container
{
    'layout': 'horizontal',
    'gap': 8,
}

# Switch
{
    'width': 44,  # 11 * 4
    'height': 24,  # 6 * 4
    'border_radius': 12,  # full (half of height)
    'transition_duration': 300,
    
    # OFF state
    'background_off': '#D1D5DB',  # gray-300
    
    # ON state
    'background_on': '#2563EB',  # blue-600
    
    # Toggle circle (slider)
    'circle_size': 16,  # 4 * 4
    'circle_color': '#FFFFFF',
    'circle_position_off': 4,  # translate-x-1
    'circle_position_on': 24,  # translate-x-6
    
    # Focus ring
    'focus_ring': '2px solid #3B82F6',
    'focus_ring_offset': 2,
}
```

**3. Info Button (Unclaimed tooltip):**
```python
{
    'size': (20, 20),
    'border_radius': 10,  # full
    'background': '#E5E7EB',  # gray-200
    'background_hover': '#D1D5DB',  # gray-300
    'icon': 'HelpCircle',
    'icon_size': 14,
    'icon_color': '#4B5563',  # gray-600
}

# Tooltip
{
    'position': 'below button',
    'offset_top': 8,
    'width': 192,  # 48 * 4
    'padding': 8,
    'background': '#1F2937',  # gray-800
    'color': '#FFFFFF',
    'font_size': 12,  # xs
    'border_radius': 8,
    'shadow': 'lg',
    'text': 'Toggle to show/hide unclaimed amounts in all cashier cards',
    
    # Arrow pointer (8x8px diamond rotated 45deg)
    'arrow_size': 8,
    'arrow_position': 'top-left with 8px offset',
    'arrow_color': '#1F2937',
}
```

**4. View All / Hide All Button:**
```python
{
    'padding': (16, 8),  # horizontal, vertical
    'border_radius': 8,
    'background': '#2563EB',  # blue-600
    'background_hover': '#1D4ED8',  # blue-700
    'color': '#FFFFFF',
    'font_size': 14,  # sm
    'font_weight': 500,
    'gap_icon_text': 8,
    
    # Icon
    'icon_size': 18,
    'icon_view': 'Eye',  # when hidden
    'icon_hide': 'EyeOff',  # when showing
    
    # Text
    'text_view': 'View All',
    'text_hide': 'Hide All',
}
```

**Filters Section:**

**Container:**
- Layout: Horizontal (responsive - vertical on small screens)
- Gap: 16px
- Padding Bottom: 24px

**1. Search Input:**
```python
{
    'flex': 1,  # takes remaining space
    'height': 48,  # 12 * 4
    'padding_left': 40,  # space for icon
    'padding_right': 16,
    'border': '1px solid #D1D5DB',  # gray-300
    'border_radius': 8,
    'font_size': 16,
    'font_weight': 400,
    'placeholder': 'Search cashier by name...',
    'placeholder_color': '#9CA3AF',  # gray-400
    
    # Focus state
    'border_focus': 'none',
    'outline_focus': '2px solid #3B82F6',  # blue-500
    'outline_offset': 0,
    
    # Icon (Search)
    'icon_position': 'absolute left 12px, vertical center',
    'icon_size': 20,
    'icon_color': '#9CA3AF',  # gray-400
}
```

**2. Sort Dropdown:**
```python
{
    'width': 256,  # 64 * 4 (md breakpoint and up)
    'height': 48,
    'padding_left': 40,
    'padding_right': 16,
    'border': '1px solid #D1D5DB',
    'border_radius': 8,
    'background': '#FFFFFF',
    'font_size': 16,
    'font_weight': 400,
    'cursor': 'pointer',
    
    # Focus state
    'border_focus': 'none',
    'outline_focus': '2px solid #3B82F6',
    
    # Icon (ArrowUpDown)
    'icon_position': 'absolute left 12px, vertical center',
    'icon_size': 20,
    'icon_color': '#9CA3AF',
    
    # Options
    'options': [
        ('name-asc', 'Name: A to Z'),
        ('name-desc', 'Name: Z to A'),
        ('online', 'Status: Online First'),
        ('offline', 'Status: Offline First'),
        ('coh-high', 'COH: Highest to Lowest'),
        ('coh-low', 'COH: Lowest to Highest'),
        ('bets-high', 'Total Bets: Highest to Lowest'),
        ('bets-low', 'Total Bets: Lowest to Highest'),
    ]
}
```

**Cards Grid:**

```python
{
    'layout': 'CSS Grid with auto-fill',
    'grid_template': 'repeat(auto-fill, minmax(280px, 1fr))',
    'gap': 16,
    'items_align': 'start',
    
    # Responsive behavior
    # Grid automatically adjusts columns based on available space
    # Minimum card width: 280px
    # Cards grow to fill space evenly
}
```

**Empty State:**
```python
{
    'display': 'When search returns no results',
    'colspan': 'full',
    'text_align': 'center',
    'padding_vertical': 48,
    'text': 'No cashiers found matching "{search_query}"',
    'text_color': '#6B7280',  # gray-500
    'font_size': 18,  # lg
}
```

### 4.3 Cashier Card Component

**Class Name:** `CashierCard` (inherits QWidget)

**Two View States:**
1. Collapsed View (name-only)
2. Expanded View (full details)

**Collapsed View:**

```python
{
    'container': {
        'background': '#FFFFFF',
        'border': '1px solid #E5E7EB',  # gray-200
        'border_radius': 8,
        'padding': 16,
        'shadow': 'sm',
        'shadow_hover': 'md',
        'transition': 'shadow 300ms',
    },
    
    'layout': 'horizontal space-between',
    
    # Left side
    'status_indicator': {
        'type': 'circle',
        'size': 8,  # 2 * 4
        'border_radius': 4,  # full
        'color_online': '#10B981',  # green-500
        'color_offline': '#EF4444',  # red-500
        'margin_right': 8,
    },
    
    'name': {
        'font_size': 16,
        'font_weight': 500,
        'color': '#1F2937',  # gray-800
    },
    
    # Right side
    'toggle_button': {
        'size': (36, 36),
        'padding': 8,
        'border_radius': 8,
        'background': 'transparent',
        'background_hover': '#F3F4F6',  # gray-100
        'icon': 'Eye',
        'icon_size': 18,
        'icon_color': '#4B5563',  # gray-600
        'tooltip': 'View details',
    },
}
```

**Expanded View:**

```python
{
    'container': {
        'background': '#FFFFFF',
        'border': '1px solid #E5E7EB',
        'border_radius': 8,
        'padding': 20,  # 5 * 4
        'shadow': 'sm',
        'shadow_hover': 'md',
        'transition': 'shadow 300ms',
    },
    
    # Header section
    'header': {
        'layout': 'horizontal space-between',
        'margin_bottom': 16,
        
        # Left icons group
        'icons_group': {
            'layout': 'horizontal',
            'gap': 12,
            
            # Printer button
            'printer_button': {
                'size': (40, 40),
                'padding': 8,
                'border_radius': 8,
                'background': '#DBEAFE',  # blue-100
                'background_hover': '#BFDBFE',  # blue-200
                'icon': 'Printer',
                'icon_size': 20,
                'icon_color': '#2563EB',  # blue-600
                'tooltip': 'Print transaction card',
            },
            
            # Battery indicator
            'battery_indicator': {
                'size': (40, 40),
                'padding': 8,
                'border_radius': 8,
                'background': '#F3F4F6',  # gray-100
                'icon_size': 20,
                'tooltip': 'Battery: {percentage}%',
                
                # Battery icon selection
                'icon_full': {  # >= 80%
                    'icon': 'BatteryFull',
                    'color': '#059669',  # green-600
                },
                'icon_medium': {  # 20-79%
                    'icon': 'Battery',
                    'color': '#D97706',  # yellow-600
                },
                'icon_low': {  # < 20%
                    'icon': 'BatteryLow',
                    'color': '#DC2626',  # red-600
                },
            },
            
            # Online/Offline badge
            'status_badge': {
                'padding': (12, 4),  # horizontal, vertical
                'border_radius': 9999,  # full pill shape
                'font_size': 12,  # xs
                'font_weight': 500,
                
                'online': {
                    'background': '#D1FAE5',  # green-100
                    'color': '#047857',  # green-700
                    'text': 'Online',
                },
                'offline': {
                    'background': '#FEE2E2',  # red-100
                    'color': '#B91C1C',  # red-700
                    'text': 'Offline',
                },
            },
        },
        
        # Right toggle button
        'toggle_button': {
            'size': (36, 36),
            'padding': 8,
            'border_radius': 8,
            'background': 'transparent',
            'background_hover': '#F3F4F6',
            'icon': 'EyeOff',
            'icon_size': 18,
            'icon_color': '#4B5563',
            'tooltip': 'Hide details',
        },
    },
    
    # Cashier name
    'cashier_name': {
        'text': 'Cashier: {name}',
        'font_size': 18,  # lg
        'font_weight': 600,
        'color': '#1F2937',
        'margin_bottom': 16,
    },
    
    # Transaction details grid
    'details_grid': {
        'layout': 'grid 2 columns',
        'gap': 16,
        
        # Each field
        'field': {
            'layout': 'vertical',
            'gap': 4,
            
            'label': {
                'font_size': 12,  # xs
                'font_weight': 400,
                'color': '#6B7280',  # gray-500
            },
            
            'value': {
                'font_size': 16,
                'font_weight': 600,
                'color': '#1F2937',
                'format': '₱{amount:,.2f}',  # Philippine Peso
            },
        },
        
        # Fields order
        'fields': [
            'Total Bets',
            'Cash In',
            'Cash Out',
            'Draw Bets',
            'Cancel Bets',
            'Unclaimed',  # Only if showUnclaimed is True
            'Withdraw',
        ],
    },
    
    # COH section (spans 2 columns)
    'coh_section': {
        'colspan': 2,
        'margin_top': 8,
        'padding_top': 16,
        'border_top': '1px solid #E5E7EB',
        
        'label': {
            'text': 'Cash on Hand (COH)',
            'font_size': 12,
            'font_weight': 400,
            'color': '#6B7280',
            'margin_bottom': 4,
        },
        
        'value': {
            'font_size': 20,  # xl
            'font_weight': 700,
            'color': '#2563EB',  # blue-600
            'format': '₱{coh:,.2f}',
            'margin_bottom': 16,
        },
        
        # View Records button
        'view_records_button': {
            'width': '100%',
            'height': 40,
            'padding': (16, 8),
            'border_radius': 8,
            'background': '#2563EB',
            'background_hover': '#1D4ED8',
            'color': '#FFFFFF',
            'font_size': 14,
            'font_weight': 500,
            'text': 'View Records',
        },
    },
}
```

**Currency Formatting:**
```python
def format_currency(amount: float) -> str:
    """
    Format amount as Philippine Peso
    Examples:
    - 1234.56 -> ₱1,234.56
    - 1000000 -> ₱1,000,000.00
    - 0 -> ₱0.00
    """
    return f"₱{amount:,.2f}"
```

**Conditional Rendering:**
- **Unclaimed field:** Only displayed when `showUnclaimed` global toggle is True
- When hidden, grid adjusts to maintain 2-column layout

---

## 5. STATE MANAGEMENT

### 5.1 Application-Level State

**Class:** `AppState` (Singleton pattern)

```python
class AppState(QObject):
    # Signals
    active_page_changed = Signal(str)
    cashier_data_updated = Signal(list)
    preferences_changed = Signal(dict)
    
    def __init__(self):
        super().__init__()
        self._active_page = 'cashier-overview'
        self._sidebar_expanded = True
        self._cashier_data = []
        self._preferences = {}
        
    # Properties
    @property
    def active_page(self) -> str:
        return self._active_page
    
    @active_page.setter
    def active_page(self, value: str):
        if self._active_page != value:
            self._active_page = value
            self.active_page_changed.emit(value)
            self.save_preference('last_active_page', value)
    
    @property
    def sidebar_expanded(self) -> bool:
        return self._sidebar_expanded
    
    @sidebar_expanded.setter
    def sidebar_expanded(self, value: bool):
        if self._sidebar_expanded != value:
            self._sidebar_expanded = value
            self.save_preference('sidebar_expanded', str(value))
    
    # Methods
    def load_preferences(self):
        """Load preferences from database"""
        pass
    
    def save_preference(self, key: str, value: str):
        """Save single preference to database"""
        pass
```

### 5.2 Cashier Overview State

**Class:** `CashierOverviewState`

```python
class CashierOverviewState:
    def __init__(self):
        # Data
        self.cashiers: List[CashierData] = []
        
        # View state
        self.global_view_all: bool = True
        self.individual_views: Dict[int, bool] = {}  # {cashier_id: is_expanded}
        self.show_unclaimed: bool = True
        
        # Filters
        self.search_query: str = ''
        self.sort_option: str = 'name-asc'
        
        # UI state
        self.show_tooltip: bool = False
    
    def initialize_individual_views(self):
        """Set all cashiers to expanded view initially"""
        self.individual_views = {
            cashier['id']: True 
            for cashier in self.cashiers
        }
    
    def toggle_global_view(self):
        """Toggle all cards between expanded/collapsed"""
        self.global_view_all = not self.global_view_all
        for cashier_id in self.individual_views.keys():
            self.individual_views[cashier_id] = self.global_view_all
    
    def toggle_individual_view(self, cashier_id: int):
        """Toggle single card view"""
        self.individual_views[cashier_id] = not self.individual_views[cashier_id]
    
    def get_filtered_sorted_cashiers(self) -> List[dict]:
        """Apply filters and sorting to cashier data"""
        # Filter by search query
        filtered = [
            c for c in self.cashiers
            if self.search_query.lower() in c['name'].lower()
        ]
        
        # Sort
        if self.sort_option == 'name-asc':
            filtered.sort(key=lambda c: c['name'])
        elif self.sort_option == 'name-desc':
            filtered.sort(key=lambda c: c['name'], reverse=True)
        elif self.sort_option == 'online':
            filtered.sort(key=lambda c: c['is_online'], reverse=True)
        elif self.sort_option == 'offline':
            filtered.sort(key=lambda c: c['is_online'])
        elif self.sort_option == 'coh-high':
            filtered.sort(key=lambda c: c['coh'], reverse=True)
        elif self.sort_option == 'coh-low':
            filtered.sort(key=lambda c: c['coh'])
        elif self.sort_option == 'bets-high':
            filtered.sort(key=lambda c: c['total_bets'], reverse=True)
        elif self.sort_option == 'bets-low':
            filtered.sort(key=lambda c: c['total_bets'])
        
        return filtered
```

### 5.3 Data Models

**Cashier Data Model:**

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class CashierData:
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
    coh: float
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'CashierData':
        """Create instance from database query result"""
        return cls(
            id=row[0],
            name=row[1],
            is_online=row[2],
            battery_percentage=row[3],
            total_bets=float(row[4]),
            cash_in=float(row[5]),
            cash_out=float(row[6]),
            draw_bets=float(row[7]),
            cancel_bets=float(row[8]),
            unclaimed=float(row[9]),
            withdraw=float(row[10]),
            coh=float(row[11])
        )
    
    def to_dict(self) -> dict:
        """Convert to dictionary for easier handling"""
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
            'coh': self.coh,
        }
```

---

## 6. USER INTERACTIONS & EVENT HANDLING

### 6.1 Sidebar Interactions

**6.1.1 Toggle Sidebar (Expand/Collapse)**

**Trigger:** Click toggle button (chevron icon)

**Behavior:**
1. Toggle `sidebar_expanded` state
2. Animate width change (300ms transition)
   - From 256px → 80px (collapse)
   - From 80px → 256px (expand)
3. Show/hide text labels
4. If collapsing: Close any open submenus
5. Save preference to database

**Code Flow:**
```python
def on_toggle_clicked(self):
    self.state.sidebar_expanded = not self.state.sidebar_expanded
    
    # Start animation
    self.animation = QPropertyAnimation(self, b"minimumWidth")
    self.animation.setDuration(300)
    self.animation.setStartValue(self.width())
    self.animation.setEndValue(256 if self.state.sidebar_expanded else 80)
    self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
    self.animation.start()
    
    # Update UI
    self.update_sidebar_ui()
    
    # Close submenu if collapsing
    if not self.state.sidebar_expanded:
        self.close_submenu()
```

**6.1.2 Navigate to Menu Item**

**Trigger:** Click on navigation button (e.g., "Cashier Overview")

**Behavior:**
1. Update active menu item state
2. Emit `menu_changed` signal with menu ID
3. Update visual styling (active state)
4. Switch content area to corresponding page

**Code Flow:**
```python
def on_menu_clicked(self, menu_id: str):
    # Update active state
    self.active_menu = menu_id
    
    # Emit signal
    self.menu_changed.emit(menu_id)
    
    # Update button styles
    self.update_active_button()
```

**6.1.3 Toggle Submenu (Operate)**

**Trigger:** Click "Operate" menu item

**Behavior:**
1. Only works when sidebar is expanded
2. Toggle submenu visibility
3. Animate height change (300ms)
4. Rotate chevron icon (down ↔ up)
5. Don't change active page (stays on current page)

**Code Flow:**
```python
def on_operate_clicked(self):
    if not self.sidebar_expanded:
        return  # Don't toggle if collapsed
    
    self.submenu_open = not self.submenu_open
    
    # Animate submenu
    if self.submenu_open:
        self.submenu_widget.show()
        # Slide down animation
    else:
        # Slide up animation
        self.submenu_widget.hide()
    
    # Rotate chevron
    self.update_chevron_icon()
```

**6.1.4 Logout**

**Trigger:** Click "Logout" menu item

**Behavior:**
1. Show confirmation dialog
2. If confirmed:
   - Save current state
   - Close database connections
   - Clear sensitive data
   - Show login screen / exit application

**Code Flow:**
```python
def on_logout_clicked(self):
    reply = QMessageBox.question(
        self,
        'Confirm Logout',
        'Are you sure you want to logout?',
        QMessageBox.Yes | QMessageBox.No
    )
    
    if reply == QMessageBox.Yes:
        self.perform_logout()
```

### 6.2 Cashier Overview Interactions

**6.2.1 Refresh Data**

**Trigger:** Click refresh button

**Behavior:**
1. Show loading indicator (optional)
2. Fetch latest data from database
3. Update cashier cards
4. Clear search/filters (optional)
5. Reset to default sort

**Code Flow:**
```python
def on_refresh_clicked(self):
    # Show loading
    self.show_loading()
    
    # Fetch data (in background thread)
    self.fetch_data_thread = FetchDataThread(self.db)
    self.fetch_data_thread.data_ready.connect(self.on_data_loaded)
    self.fetch_data_thread.start()

def on_data_loaded(self, data):
    self.state.cashiers = data
    self.state.initialize_individual_views()
    self.render_cards()
    self.hide_loading()
```

**6.2.2 Toggle Unclaimed Field**

**Trigger:** Click iOS-style toggle switch

**Behavior:**
1. Toggle `show_unclaimed` state
2. Animate switch (300ms)
3. Update all cashier cards to show/hide unclaimed field
4. Save preference to database

**Code Flow:**
```python
def on_unclaimed_toggle_clicked(self):
    self.state.show_unclaimed = not self.state.show_unclaimed
    
    # Animate switch
    self.animate_switch()
    
    # Update all cards
    for card in self.cashier_cards:
        card.set_show_unclaimed(self.state.show_unclaimed)
    
    # Save preference
    self.save_preference('show_unclaimed_field', str(self.state.show_unclaimed))
```

**6.2.3 Show/Hide Unclaimed Tooltip**

**Trigger:** Hover over info button

**Behavior:**
1. On mouse enter: Show tooltip after 200ms delay
2. On mouse leave: Hide tooltip immediately

**Code Flow:**
```python
def on_info_button_enter(self):
    self.tooltip_timer = QTimer()
    self.tooltip_timer.setSingleShot(True)
    self.tooltip_timer.timeout.connect(self.show_tooltip)
    self.tooltip_timer.start(200)

def on_info_button_leave(self):
    if self.tooltip_timer:
        self.tooltip_timer.stop()
    self.hide_tooltip()
```

**6.2.4 Global View Toggle (View All / Hide All)**

**Trigger:** Click "View All" or "Hide All" button

**Behavior:**
1. Toggle `global_view_all` state
2. Update button text and icon
3. Set all individual card views to match global state
4. Re-render all cards with animation

**Code Flow:**
```python
def on_global_toggle_clicked(self):
    self.state.toggle_global_view()
    
    # Update button
    if self.state.global_view_all:
        self.global_button.setText('Hide All')
        self.global_button.setIcon(eye_off_icon)
    else:
        self.global_button.setText('View All')
        self.global_button.setIcon(eye_icon)
    
    # Update all cards
    for cashier_id, card in self.cashier_cards.items():
        card.set_expanded(self.state.individual_views[cashier_id])
```

**6.2.5 Search Cashiers**

**Trigger:** Type in search input (with debounce)

**Behavior:**
1. Debounce input (300ms delay)
2. Filter cashiers by name
3. Re-render filtered cards
4. Show "No results" message if empty

**Code Flow:**
```python
def on_search_text_changed(self, text):
    self.state.search_query = text
    
    # Debounce
    if self.search_timer:
        self.search_timer.stop()
    
    self.search_timer = QTimer()
    self.search_timer.setSingleShot(True)
    self.search_timer.timeout.connect(self.apply_filters)
    self.search_timer.start(300)

def apply_filters(self):
    filtered_cashiers = self.state.get_filtered_sorted_cashiers()
    self.render_cards(filtered_cashiers)
```

**6.2.6 Sort Cashiers**

**Trigger:** Select option from sort dropdown

**Behavior:**
1. Update `sort_option` state
2. Apply sorting to current filtered data
3. Re-render cards in new order

**Code Flow:**
```python
def on_sort_changed(self, option):
    self.state.sort_option = option
    filtered_cashiers = self.state.get_filtered_sorted_cashiers()
    self.render_cards(filtered_cashiers)
```

### 6.3 Cashier Card Interactions

**6.3.1 Toggle Individual Card View**

**Trigger:** Click eye/eye-off icon on card

**Behavior:**
1. Toggle individual card's expanded state
2. Animate height change (smooth transition)
3. Update icon (Eye ↔ EyeOff)
4. Don't affect other cards

**Code Flow:**
```python
def on_toggle_clicked(self):
    self.is_expanded = not self.is_expanded
    self.state.toggle_individual_view(self.cashier.id)
    
    # Animate height
    self.animate_height_change()
    
    # Update UI
    self.render_view()
```

**6.3.2 Print Transaction Card**

**Trigger:** Click printer button (expanded view only)

**Behavior:**
1. Generate print-friendly HTML/PDF
2. Show print dialog
3. Include cashier details and all transaction data

**Code Flow:**
```python
def on_print_clicked(self):
    # Generate print document
    doc = self.generate_print_document()
    
    # Show print dialog
    printer = QPrinter(QPrinter.HighResolution)
    dialog = QPrintDialog(printer, self)
    
    if dialog.exec() == QPrintDialog.Accepted:
        doc.print(printer)
```

**6.3.3 View Records**

**Trigger:** Click "View Records" button (expanded view only)

**Behavior:**
1. Open new dialog/page showing transaction history
2. Pass cashier ID to detail view
3. Load transactions from database

**Code Flow:**
```python
def on_view_records_clicked(self):
    # Open transaction details dialog
    dialog = TransactionDetailsDialog(self.cashier.id, self.db)
    dialog.exec()
```

**6.3.4 Hover Effects**

**All interactive elements should have hover states:**

```python
def enterEvent(self, event):
    # Change cursor to pointer
    self.setCursor(Qt.PointingHandCursor)
    
    # Apply hover styles
    self.setStyleSheet(self.get_hover_stylesheet())

def leaveEvent(self, event):
    # Reset cursor
    self.setCursor(Qt.ArrowCursor)
    
    # Reset styles
    self.setStyleSheet(self.get_default_stylesheet())
```

---

## 7. DATA FLOW & BUSINESS LOGIC

### 7.1 Application Startup Flow

```
1. Initialize Application
   └─> Load configuration
   └─> Setup logging

2. Initialize Database Connection
   └─> Connect to PostgreSQL
   └─> Verify tables exist
   └─> Run migrations if needed

3. Load User Preferences
   └─> Query user_preferences table
   └─> Apply sidebar state
   └─> Apply last viewed page

4. Create Main Window
   └─> Initialize Sidebar
   └─> Initialize Content Area
   └─> Show window

5. Load Initial Data
   └─> Query cashier overview data
   └─> Render Cashier Overview page
   └─> Start background update timer
```

### 7.2 Data Refresh Flow

**Automatic Refresh (Every 30 seconds):**

```
Timer Triggered (30s)
   │
   ├─> Query get_cashier_overview(CURRENT_DATE)
   │
   ├─> Transform data to CashierData objects
   │
   ├─> Compare with current data
   │   └─> If changed: Update UI
   │   └─> If same: No action
   │
   └─> Reschedule timer
```

**Manual Refresh (Button click):**

```
Refresh Button Clicked
   │
   ├─> Show loading indicator
   │
   ├─> Query get_cashier_overview(CURRENT_DATE)
   │
   ├─> Update state.cashiers
   │
   ├─> Re-render all cards
   │
   ├─> Hide loading indicator
   │
   └─> Show success toast (optional)
```

### 7.3 Transaction Data Flow

**Recording a New Transaction:**

```
Transaction Occurs (external system/device)
   │
   ├─> INSERT INTO transactions
   │   (cashier_id, transaction_type, amount, reference_number)
   │
   ├─> Trigger: trigger_update_summary()
   │   │
   │   └─> Call: update_transaction_summary(cashier_id, date)
   │       │
   │       ├─> Calculate totals from transactions table
   │       │
   │       ├─> Calculate COH = cash_in - cash_out - withdraw
   │       │
   │       └─> UPDATE transaction_summary
   │
   └─> (Dashboard picks up changes on next refresh)
```

### 7.4 Cashier Status Update Flow

**Device Heartbeat:**

```
Cashier Device Sends Heartbeat (every 10s)
   │
   ├─> UPDATE cashier_status
   │   SET is_online = TRUE,
   │       battery_percentage = {value},
   │       last_heartbeat = CURRENT_TIMESTAMP
   │   WHERE cashier_id = {id}
   │
   └─> Dashboard shows updated status on next refresh
```

**Offline Detection:**

```
Background Job (runs every minute)
   │
   └─> UPDATE cashier_status
       SET is_online = FALSE
       WHERE last_heartbeat < (CURRENT_TIMESTAMP - INTERVAL '1 minute')
```

### 7.5 Search & Filter Logic

**Filter Algorithm:**

```python
def apply_filters(cashiers, search_query, sort_option):
    # Step 1: Filter by search
    if search_query:
        filtered = [
            c for c in cashiers
            if search_query.lower() in c.name.lower()
        ]
    else:
        filtered = cashiers.copy()
    
    # Step 2: Sort
    if sort_option == 'name-asc':
        filtered.sort(key=lambda c: c.name)
    elif sort_option == 'name-desc':
        filtered.sort(key=lambda c: c.name, reverse=True)
    elif sort_option == 'online':
        # Online first, then offline
        filtered.sort(key=lambda c: (not c.is_online, c.name))
    elif sort_option == 'offline':
        # Offline first, then online
        filtered.sort(key=lambda c: (c.is_online, c.name))
    elif sort_option == 'coh-high':
        filtered.sort(key=lambda c: c.coh, reverse=True)
    elif sort_option == 'coh-low':
        filtered.sort(key=lambda c: c.coh)
    elif sort_option == 'bets-high':
        filtered.sort(key=lambda c: c.total_bets, reverse=True)
    elif sort_option == 'bets-low':
        filtered.sort(key=lambda c: c.total_bets)
    
    return filtered
```

### 7.6 Currency Calculations

**All monetary calculations must use Decimal type for precision:**

```python
from decimal import Decimal, ROUND_HALF_UP

def calculate_coh(cash_in, cash_out, withdraw):
    """
    Calculate Cash on Hand
    COH = Cash In - Cash Out - Withdraw
    """
    cash_in = Decimal(str(cash_in))
    cash_out = Decimal(str(cash_out))
    withdraw = Decimal(str(withdraw))
    
    coh = cash_in - cash_out - withdraw
    
    # Round to 2 decimal places
    return coh.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def format_currency(amount):
    """Format as Philippine Peso"""
    amount = Decimal(str(amount))
    formatted = f"{amount:,.2f}"
    return f"₱{formatted}"
```

---

## 8. PYSIDE6 IMPLEMENTATION GUIDE

### 8.1 Project Structure

```
dashboard_app/
│
├── main.py                      # Application entry point
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies
│
├── database/
│   ├── __init__.py
│   ├── connection.py            # Database connection management
│   ├── models.py                # Data models
│   └── queries.py               # SQL queries and ORM
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py           # Main application window
│   ├── sidebar.py               # Sidebar component
│   ├── cashier_overview.py     # Cashier Overview page
│   ├── cashier_card.py          # Individual cashier card
│   └── styles.py                # Shared stylesheets
│
├── utils/
│   ├── __init__.py
│   ├── formatting.py            # Currency, date formatting
│   └── icons.py                 # Icon management
│
└── resources/
    ├── icons/                   # SVG/PNG icons
    └── styles/                  # Additional CSS/QSS files
```

### 8.2 Dependencies (requirements.txt)

```
PySide6>=6.6.0
psycopg2-binary>=2.9.9
python-dotenv>=1.0.0
```

### 8.3 Main Application Entry Point

**main.py:**

```python
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from ui.main_window import MainWindow
from database.connection import DatabaseManager
from config import load_config

def main():
    # Load configuration
    config = load_config()
    
    # Initialize database
    db_manager = DatabaseManager(config['database'])
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Dashboard - Cashier Overview")
    app.setOrganizationName("Your Company")
    
    # Set global font
    font = app.font()
    font.setFamily("Inter, -apple-system, Segoe UI")
    font.setPointSize(10)
    app.setFont(font)
    
    # Create and show main window
    window = MainWindow(db_manager)
    window.show()
    
    # Start event loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
```

### 8.4 Stylesheet Management

**Using Qt Style Sheets (QSS) - Similar to CSS:**

```python
# ui/styles.py

def get_sidebar_stylesheet(is_expanded):
    return f"""
    QWidget#sidebar {{
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }}
    
    QPushButton.nav-button {{
        border: none;
        padding: 12px 16px;
        text-align: left;
        font-size: 14px;
        font-weight: 500;
        color: #374151;
        background-color: transparent;
    }}
    
    QPushButton.nav-button:hover {{
        background-color: #F3F4F6;
    }}
    
    QPushButton.nav-button:checked {{
        background-color: #DBEAFE;
        color: #2563EB;
    }}
    
    QPushButton.toggle-button {{
        border: none;
        border-radius: 8px;
        padding: 8px;
        background-color: transparent;
    }}
    
    QPushButton.toggle-button:hover {{
        background-color: #F3F4F6;
    }}
    """

def get_card_stylesheet():
    return """
    QWidget.cashier-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 16px;
    }
    
    QWidget.cashier-card:hover {
        /* Hover shadow effect - apply via QGraphicsDropShadowEffect */
    }
    
    QPushButton.action-button {
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        background-color: #2563EB;
        color: #FFFFFF;
        font-size: 14px;
        font-weight: 500;
    }
    
    QPushButton.action-button:hover {
        background-color: #1D4ED8;
    }
    """
```

### 8.5 Custom Widgets

**8.5.1 iOS-Style Toggle Switch**

```python
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QPainter, QColor, QPen

class ToggleSwitch(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._checked = False
        self._circle_position = 4  # Initial position
        
        self.setFixedSize(44, 24)
        self.setCursor(Qt.PointingHandCursor)
        
        # Animation
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.setDuration(300)
    
    @Property(int)
    def circle_position(self):
        return self._circle_position
    
    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()
    
    def mousePressEvent(self, event):
        self.toggle()
    
    def toggle(self):
        self._checked = not self._checked
        
        # Animate circle
        self.animation.setStartValue(self._circle_position)
        self.animation.setEndValue(24 if self._checked else 4)
        self.animation.start()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background track
        if self._checked:
            painter.setBrush(QColor("#2563EB"))
        else:
            painter.setBrush(QColor("#D1D5DB"))
        
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, 44, 24, 12, 12)
        
        # Draw circle
        painter.setBrush(QColor("#FFFFFF"))
        painter.drawEllipse(self._circle_position, 4, 16, 16)
```

**8.5.2 Flow Layout (for responsive card grid)**

```python
from PySide6.QtWidgets import QLayout
from PySide6.QtCore import QRect, QSize, Qt

class FlowLayout(QLayout):
    """
    Custom layout that arranges items in a responsive grid
    Similar to CSS Grid with auto-fill
    """
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        self._item_list = []
        self._spacing = spacing
        self.setContentsMargins(margin, margin, margin, margin)
    
    def addItem(self, item):
        self._item_list.append(item)
    
    def count(self):
        return len(self._item_list)
    
    def itemAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list[index]
        return None
    
    def takeAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list.pop(index)
        return None
    
    def minimumSize(self):
        size = QSize()
        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())
        return size
    
    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._do_layout(rect, False)
    
    def sizeHint(self):
        return self.minimumSize()
    
    def _do_layout(self, rect, test_only=False):
        x = rect.x()
        y = rect.y()
        line_height = 0
        spacing = self.spacing()
        
        min_card_width = 280
        available_width = rect.width()
        
        for item in self._item_list:
            widget = item.widget()
            if not widget:
                continue
            
            # Calculate item size
            item_width = max(min_card_width, widget.sizeHint().width())
            item_height = widget.sizeHint().height()
            
            # Check if need new line
            next_x = x + item_width + spacing
            if next_x - spacing > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + spacing
                line_height = 0
                next_x = x + item_width + spacing
            
            if not test_only:
                widget.setGeometry(QRect(x, y, item_width, item_height))
            
            x = next_x
            line_height = max(line_height, item_height)
        
        return y + line_height - rect.y()
    
    def spacing(self):
        if self._spacing >= 0:
            return self._spacing
        return 16  # Default spacing
```

### 8.6 Database Integration

**database/connection.py:**

```python
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, config):
        self.pool = SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password']
        )
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = self.pool.getconn()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.pool.putconn(conn)
    
    def close_all(self):
        """Close all connections"""
        self.pool.closeall()
```

**database/queries.py:**

```python
from typing import List
from .models import CashierData

class CashierQueries:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def get_cashier_overview(self, date=None) -> List[CashierData]:
        """Fetch cashier overview data for a specific date"""
        query = "SELECT * FROM get_cashier_overview(%s)"
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (date,))
            rows = cursor.fetchall()
            
            return [CashierData.from_db_row(row) for row in rows]
    
    def update_cashier_status(self, cashier_id, is_online, battery_percentage):
        """Update cashier device status"""
        query = """
        INSERT INTO cashier_status (cashier_id, is_online, battery_percentage, last_heartbeat)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT (cashier_id) DO UPDATE
        SET is_online = EXCLUDED.is_online,
            battery_percentage = EXCLUDED.battery_percentage,
            last_heartbeat = CURRENT_TIMESTAMP
        """
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (cashier_id, is_online, battery_percentage))
```

### 8.7 Threading for Database Operations

**Never block UI thread with database queries:**

```python
from PySide6.QtCore import QThread, Signal

class FetchDataThread(QThread):
    data_ready = Signal(list)
    error_occurred = Signal(str)
    
    def __init__(self, db_manager, query_func, *args):
        super().__init__()
        self.db = db_manager
        self.query_func = query_func
        self.args = args
    
    def run(self):
        try:
            data = self.query_func(*self.args)
            self.data_ready.emit(data)
        except Exception as e:
            self.error_occurred.emit(str(e))

# Usage in UI component:
def load_cashier_data(self):
    self.fetch_thread = FetchDataThread(
        self.db,
        self.queries.get_cashier_overview
    )
    self.fetch_thread.data_ready.connect(self.on_data_loaded)
    self.fetch_thread.error_occurred.connect(self.on_error)
    self.fetch_thread.start()
```

### 8.8 Icon Management

**Using Lucide Icons (SVG format):**

Option 1: Download SVG files and load as QIcon
```python
from PySide6.QtGui import QIcon

ICON_PATH = "resources/icons/"

ICONS = {
    'LayoutDashboard': QIcon(f"{ICON_PATH}layout-dashboard.svg"),
    'Calendar': QIcon(f"{ICON_PATH}calendar.svg"),
    'Users': QIcon(f"{ICON_PATH}users.svg"),
    # ... etc
}
```

Option 2: Use QtAwesome (Font Awesome alternative for Qt)
```python
# Install: pip install QtAwesome
import qtawesome as qta

ICONS = {
    'LayoutDashboard': qta.icon('fa5s.th-large'),
    'Calendar': qta.icon('fa5s.calendar'),
    'Users': qta.icon('fa5s.users'),
}
```

### 8.9 Signal/Slot Connections

**Connecting components:**

```python
# In MainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Create components
        self.sidebar = Sidebar()
        self.cashier_overview = CashierOverview(self.db)
        
        # Connect signals
        self.sidebar.menu_changed.connect(self.on_menu_changed)
        self.cashier_overview.refresh_requested.connect(self.refresh_data)
    
    def on_menu_changed(self, menu_id):
        # Switch page
        if menu_id == 'cashier-overview':
            self.stacked_widget.setCurrentWidget(self.cashier_overview)
        elif menu_id == 'settings':
            self.stacked_widget.setCurrentWidget(self.settings_page)
        # ... etc
```

---

## 9. POSTGRESQL INTEGRATION

### 9.1 Connection Configuration

**config.py:**

```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'dashboard_db'),
    'user': os.getenv('DB_USER', 'dashboard_user'),
    'password': os.getenv('DB_PASSWORD', 'your_password'),
}

def load_config():
    return {
        'database': DATABASE_CONFIG
    }
```

**.env file (not committed to git):**

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dashboard_db
DB_USER=dashboard_user
DB_PASSWORD=your_secure_password
```

### 9.2 Database Initialization Script

**scripts/init_database.sql:**

```sql
-- Run this script to initialize the database

-- Create database
CREATE DATABASE dashboard_db;

-- Connect to database
\c dashboard_db

-- Create tables (see section 2.2-2.8 for full schema)
-- ... all CREATE TABLE statements ...

-- Create stored procedures
-- ... all CREATE FUNCTION statements ...

-- Create triggers
-- ... all CREATE TRIGGER statements ...

-- Insert sample data
-- ... INSERT statements ...

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE dashboard_db TO dashboard_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dashboard_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO dashboard_user;
```

### 9.3 Migration System (Optional but Recommended)

**Using Alembic for database migrations:**

```bash
pip install alembic psycopg2-binary
alembic init migrations
```

**migrations/versions/001_initial_schema.py:**

```python
"""Initial schema

Revision ID: 001
Create Date: 2026-02-14
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Create cashiers table
    op.create_table(
        'cashiers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False, unique=True),
        # ... etc
    )
    # ... other tables

def downgrade():
    op.drop_table('cashiers')
    # ... reverse changes
```

### 9.4 Data Access Layer

**database/models.py:**

```python
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class CashierData:
    id: int
    name: str
    is_online: bool
    battery_percentage: int
    total_bets: Decimal
    cash_in: Decimal
    cash_out: Decimal
    draw_bets: Decimal
    cancel_bets: Decimal
    unclaimed: Decimal
    withdraw: Decimal
    coh: Decimal
    
    @classmethod
    def from_db_row(cls, row):
        return cls(
            id=row[0],
            name=row[1],
            is_online=row[2],
            battery_percentage=row[3],
            total_bets=Decimal(str(row[4])),
            cash_in=Decimal(str(row[5])),
            cash_out=Decimal(str(row[6])),
            draw_bets=Decimal(str(row[7])),
            cancel_bets=Decimal(str(row[8])),
            unclaimed=Decimal(str(row[9])),
            withdraw=Decimal(str(row[10])),
            coh=Decimal(str(row[11]))
        )

@dataclass
class Transaction:
    id: int
    cashier_id: int
    transaction_type: str
    amount: Decimal
    transaction_date: str
    reference_number: Optional[str]
    notes: Optional[str]
```

### 9.5 Query Optimization

**Indexes for Performance:**

```sql
-- Already covered in section 2, but key indexes:
CREATE INDEX idx_cashiers_name ON cashiers(name);
CREATE INDEX idx_transactions_cashier_date ON transactions(cashier_id, transaction_date);
CREATE INDEX idx_cashier_status_online ON cashier_status(is_online);
```

**Query Best Practices:**

1. Use stored procedures for complex queries
2. Use prepared statements to prevent SQL injection
3. Batch updates when possible
4. Use connection pooling (already implemented)
5. Cache frequently accessed data

### 9.6 Backup & Recovery

**Automated Backup Script (Linux/Mac):**

```bash
#!/bin/bash
# backup_database.sh

BACKUP_DIR="/path/to/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_NAME="dashboard_db"

pg_dump -U dashboard_user -h localhost $DB_NAME | gzip > "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sql.gz"

# Keep only last 7 days of backups
find $BACKUP_DIR -name "${DB_NAME}_*.sql.gz" -mtime +7 -delete
```

**Restore from Backup:**

```bash
gunzip < backup_file.sql.gz | psql -U dashboard_user -h localhost dashboard_db
```

---

## 10. RESPONSIVE DESIGN & LAYOUTS

### 10.1 Breakpoints

**Screen Size Categories:**

```python
BREAKPOINTS = {
    'xs': 0,      # Extra small (mobile)
    'sm': 640,    # Small (large mobile)
    'md': 768,    # Medium (tablet)
    'lg': 1024,   # Large (desktop)
    'xl': 1280,   # Extra large
    '2xl': 1536,  # 2X Extra large
}
```

### 10.2 Responsive Grid Layout

**Cashier Cards Grid Behavior:**

```
Window Width          | Cards per Row
---------------------|---------------
0 - 639px (xs/sm)    | 1 column
640 - 959px          | 2 columns
960 - 1279px         | 3 columns
1280 - 1599px        | 4 columns
1600px+              | 5+ columns
```

**Implementation in PySide6:**

```python
class ResponsiveCardGrid(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = FlowLayout()
        self.setLayout(self.layout)
    
    def resizeEvent(self, event):
        """Recalculate grid on window resize"""
        super().resizeEvent(event)
        self.layout.update()
```

### 10.3 Sidebar Responsive Behavior

**Desktop (>= 1024px):**
- Default: Expanded (256px)
- User can toggle collapse/expand
- State persists across sessions

**Tablet (768px - 1023px):**
- Default: Collapsed (80px) to save space
- User can toggle expand
- Auto-collapse when clicking outside (optional)

**Mobile (< 768px):**
- Default: Hidden (overlay mode)
- Show via hamburger menu
- Slide in/out animation
- Overlay darkens background

### 10.4 Content Area Padding

**Responsive Padding:**

```python
def get_content_padding(window_width):
    if window_width < 640:
        return 16  # xs/sm: 16px
    elif window_width < 1024:
        return 24  # md: 24px
    else:
        return 32  # lg+: 32px
```

### 10.5 Typography Scaling

**Responsive Font Sizes:**

```python
# Desktop
FONT_SIZES_DESKTOP = {
    'xs': 12,
    'sm': 14,
    'base': 16,
    'lg': 18,
    'xl': 20,
    '2xl': 24,
}

# Mobile
FONT_SIZES_MOBILE = {
    'xs': 11,
    'sm': 13,
    'base': 15,
    'lg': 17,
    'xl': 19,
    '2xl': 22,
}
```

---

## 11. ICONS & ASSETS

### 11.1 Icon Library

**Using Lucide Icons (lucide.dev):**

Download SVG files for these icons:
- LayoutDashboard
- Calendar
- Users
- FileText
- Settings
- Wrench
- ChevronLeft
- ChevronRight
- ChevronDown
- ChevronUp
- LogOut
- Eye
- EyeOff
- Search
- ArrowUpDown
- HelpCircle
- RefreshCw
- Printer
- Battery
- BatteryLow
- BatteryFull

**Icon Sizes:**
- Small: 14px (help icons)
- Medium: 18px (card actions)
- Large: 20px (navigation, main actions)
- Extra Large: 22px (header icon)

### 11.2 Loading Icons as QIcon

```python
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtSvg import QSvgRenderer

class IconManager:
    def __init__(self, icon_path="resources/icons/"):
        self.icon_path = icon_path
        self.cache = {}
    
    def get_icon(self, name, size=20, color=None):
        """
        Get icon by name
        Args:
            name: Icon name (e.g., 'LayoutDashboard')
            size: Icon size in pixels
            color: Optional color override (hex string)
        """
        cache_key = f"{name}_{size}_{color}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        icon_file = f"{self.icon_path}{name.lower()}.svg"
        
        if color:
            # Modify SVG color
            icon = self._create_colored_icon(icon_file, color, size)
        else:
            icon = QIcon(icon_file)
        
        self.cache[cache_key] = icon
        return icon
    
    def _create_colored_icon(self, svg_file, color, size):
        # Read SVG and replace color
        with open(svg_file, 'r') as f:
            svg_content = f.read()
        
        # Replace stroke/fill colors
        svg_content = svg_content.replace('currentColor', color)
        
        # Render to QIcon
        renderer = QSvgRenderer(svg_content.encode())
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        return QIcon(pixmap)
```

### 11.3 Asset Organization

```
resources/
├── icons/
│   ├── layout-dashboard.svg
│   ├── calendar.svg
│   ├── users.svg
│   ├── file-text.svg
│   ├── settings.svg
│   ├── wrench.svg
│   ├── chevron-left.svg
│   ├── chevron-right.svg
│   ├── chevron-down.svg
│   ├── chevron-up.svg
│   ├── log-out.svg
│   ├── eye.svg
│   ├── eye-off.svg
│   ├── search.svg
│   ├── arrow-up-down.svg
│   ├── help-circle.svg
│   ├── refresh-cw.svg
│   ├── printer.svg
│   ├── battery.svg
│   ├── battery-low.svg
│   └── battery-full.svg
│
├── fonts/
│   └── Inter/
│       ├── Inter-Regular.ttf
│       ├── Inter-Medium.ttf
│       ├── Inter-SemiBold.ttf
│       └── Inter-Bold.ttf
│
└── images/
    └── logo.png
```

### 11.4 Font Loading

```python
from PySide6.QtGui import QFontDatabase

def load_fonts():
    font_path = "resources/fonts/Inter/"
    fonts = [
        "Inter-Regular.ttf",
        "Inter-Medium.ttf",
        "Inter-SemiBold.ttf",
        "Inter-Bold.ttf"
    ]
    
    for font in fonts:
        QFontDatabase.addApplicationFont(f"{font_path}{font}")
```

---

## 12. TESTING CHECKLIST

### 12.1 Functional Testing

**Sidebar:**
- [ ] Toggle expand/collapse works
- [ ] Animation is smooth (300ms)
- [ ] Icons show/hide correctly
- [ ] Submenu (Operate) opens/closes when expanded
- [ ] Submenu stays closed when sidebar is collapsed
- [ ] Active state highlights correct item
- [ ] Navigation switches content area correctly
- [ ] Logout shows confirmation dialog
- [ ] Preferences are saved to database
- [ ] Tooltips appear when sidebar is collapsed

**Cashier Overview:**
- [ ] Data loads from database correctly
- [ ] All 20 cashiers are displayed
- [ ] Refresh button reloads data
- [ ] Refresh animation works
- [ ] Global View All/Hide All toggles all cards
- [ ] Individual card toggle works independently
- [ ] Unclaimed toggle shows/hides field in all cards
- [ ] Unclaimed toggle state persists
- [ ] Info tooltip appears on hover
- [ ] Search filters cashiers by name
- [ ] Search is case-insensitive
- [ ] Search debounces (300ms)
- [ ] All 8 sort options work correctly
- [ ] Empty state shows when no results
- [ ] Currency formatting is correct (₱X,XXX.XX)

**Cashier Card:**
- [ ] Collapsed view shows name and status
- [ ] Expanded view shows all details
- [ ] Toggle animation is smooth
- [ ] Battery icon changes based on percentage
  - [ ] >= 80%: BatteryFull (green)
  - [ ] 20-79%: Battery (yellow)
  - [ ] < 20%: BatteryLow (red)
- [ ] Online/Offline badge color is correct
- [ ] Print button opens print dialog
- [ ] View Records button navigates correctly
- [ ] All transaction values display correctly
- [ ] COH is calculated correctly
- [ ] Unclaimed field hides when toggle is off

**Responsive Grid:**
- [ ] Cards adjust to window size
- [ ] No horizontal scrolling needed
- [ ] Minimum card width is 280px
- [ ] Cards grow to fill space evenly
- [ ] Grid reflows on window resize

### 12.2 Database Testing

- [ ] Connection pool works correctly
- [ ] Queries return expected data
- [ ] Stored procedure (get_cashier_overview) works
- [ ] Transaction summary updates correctly
- [ ] COH calculation is accurate
- [ ] Trigger updates summary on transaction insert
- [ ] Status updates work in real-time
- [ ] Preferences save and load correctly
- [ ] Connection errors are handled gracefully
- [ ] Query errors don't crash application

### 12.3 Performance Testing

- [ ] Application starts in < 3 seconds
- [ ] Data loads in < 1 second (for 20 cashiers)
- [ ] No UI freezing during database queries
- [ ] Smooth animations (60fps)
- [ ] Search responds quickly (< 300ms)
- [ ] Memory usage is reasonable (< 200MB)
- [ ] No memory leaks over extended use

### 12.4 Visual Testing

**Colors:**
- [ ] All colors match specification
- [ ] Hover states are visible
- [ ] Active states are distinct
- [ ] Status indicators (online/offline) are clear
- [ ] Contrast is sufficient for readability

**Typography:**
- [ ] Font family loads correctly
- [ ] Font sizes match specification
- [ ] Font weights are correct
- [ ] Line heights provide good readability
- [ ] Text truncates appropriately

**Spacing:**
- [ ] Padding is consistent
- [ ] Margins are appropriate
- [ ] Gap between elements is correct
- [ ] No overlapping elements

**Borders & Shadows:**
- [ ] Border radius matches specification
- [ ] Border colors are correct
- [ ] Shadows appear on hover
- [ ] Shadow intensity is appropriate

### 12.5 Cross-Platform Testing

- [ ] Works on Windows 10/11
- [ ] Works on macOS
- [ ] Works on Linux (Ubuntu/Fedora)
- [ ] Icons render correctly on all platforms
- [ ] Fonts load correctly on all platforms
- [ ] Database connection works on all platforms

### 12.6 Error Handling

- [ ] Database connection errors show user-friendly message
- [ ] Query errors are logged
- [ ] Network errors are handled gracefully
- [ ] Invalid data doesn't crash application
- [ ] Empty states display correctly
- [ ] Error dialogs are informative

### 12.7 Edge Cases

- [ ] Search with no results shows message
- [ ] Search with special characters works
- [ ] Very long cashier names display correctly
- [ ] Very large/small currency amounts format correctly
- [ ] Zero values display as ₱0.00
- [ ] Negative COH displays correctly
- [ ] 100% battery shows full icon
- [ ] 0% battery shows low icon
- [ ] All cards collapsed doesn't break layout
- [ ] All cards expanded doesn't break layout

### 12.8 User Experience

- [ ] All buttons have hover effects
- [ ] Cursor changes to pointer on clickable elements
- [ ] Tooltips are informative
- [ ] Loading states are visible
- [ ] Transitions feel smooth and natural
- [ ] No unnecessary animations
- [ ] Keyboard navigation works (Tab, Enter, Space)
- [ ] Focus indicators are visible
- [ ] Color-blind friendly (status uses icons + colors)

---

## APPENDIX A: Quick Reference

### Color Variables

```python
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
    
    # Blue
    'blue_50': '#EFF6FF',
    'blue_100': '#DBEAFE',
    'blue_200': '#BFDBFE',
    'blue_500': '#3B82F6',
    'blue_600': '#2563EB',
    'blue_700': '#1D4ED8',
    
    # Green
    'green_100': '#D1FAE5',
    'green_500': '#10B981',
    'green_600': '#059669',
    'green_700': '#047857',
    
    # Red
    'red_100': '#FEE2E2',
    'red_500': '#EF4444',
    'red_600': '#DC2626',
    'red_700': '#B91C1C',
    
    # Yellow
    'yellow_600': '#D97706',
    
    # White
    'white': '#FFFFFF',
}
```

### Common Dimensions

```python
DIMENSIONS = {
    'sidebar_expanded': 256,
    'sidebar_collapsed': 80,
    'header_height': 64,
    'card_min_width': 280,
    'button_height': 40,
    'input_height': 48,
    'icon_sm': 14,
    'icon_md': 18,
    'icon_lg': 20,
    'icon_xl': 22,
}
```

### Database Quick Commands

```sql
-- View all cashiers with current status
SELECT * FROM get_cashier_overview(CURRENT_DATE);

-- Update transaction summary for a cashier
SELECT update_transaction_summary(1, CURRENT_DATE);

-- Add a transaction
INSERT INTO transactions (cashier_id, transaction_type, amount, reference_number)
VALUES (1, 'cashin', 5000.00, 'TXN123456');

-- Update cashier status
UPDATE cashier_status 
SET is_online = TRUE, battery_percentage = 85
WHERE cashier_id = 1;
```

---

## APPENDIX B: Implementation Priority

**Phase 1 - Foundation (Week 1):**
1. Setup project structure
2. Create database schema
3. Implement database connection
4. Create main window shell

**Phase 2 - Core UI (Week 2):**
1. Implement Sidebar component
2. Implement basic routing/navigation
3. Create Cashier Overview layout
4. Create Cashier Card component

**Phase 3 - Functionality (Week 3):**
1. Implement data fetching from database
2. Implement search and sort
3. Implement global/individual toggles
4. Implement refresh functionality

**Phase 4 - Polish (Week 4):**
1. Add animations and transitions
2. Implement responsive design
3. Add error handling
4. Optimize performance

**Phase 5 - Testing (Week 5):**
1. Functional testing
2. Database testing
3. Performance testing
4. Bug fixes

---

## APPENDIX C: Common Patterns

### Pattern 1: Database Query with Loading State

```python
def fetch_data(self):
    # Show loading
    self.loading_overlay.show()
    
    # Create worker thread
    self.worker = FetchDataThread(self.db, self.queries.get_cashier_overview)
    self.worker.data_ready.connect(self.on_data_loaded)
    self.worker.error_occurred.connect(self.on_error)
    self.worker.start()

def on_data_loaded(self, data):
    self.cashiers = data
    self.render_ui()
    self.loading_overlay.hide()

def on_error(self, error_msg):
    self.loading_overlay.hide()
    QMessageBox.critical(self, "Error", f"Failed to load data: {error_msg}")
```

### Pattern 2: Animated Property Change

```python
def animate_width(self, target_width):
    self.animation = QPropertyAnimation(self, b"minimumWidth")
    self.animation.setDuration(300)
    self.animation.setStartValue(self.width())
    self.animation.setEndValue(target_width)
    self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
    self.animation.start()
```

### Pattern 3: Debounced Input

```python
def on_search_changed(self, text):
    if hasattr(self, 'search_timer') and self.search_timer.isActive():
        self.search_timer.stop()
    
    self.search_timer = QTimer()
    self.search_timer.setSingleShot(True)
    self.search_timer.timeout.connect(lambda: self.apply_search(text))
    self.search_timer.start(300)
```

---

## CONCLUSION

This document provides a complete specification for migrating the React-based Dashboard application to PySide6 with PostgreSQL. Every visual detail, interaction, database schema, and implementation pattern has been documented.

**Key Points to Remember:**

1. **Database First:** Design your database schema carefully - it's harder to change later
2. **Thread Safety:** Never block the UI thread with database operations
3. **Decimal Precision:** Always use Decimal type for currency calculations
4. **Responsive Design:** Test on multiple screen sizes
5. **Error Handling:** Always handle database and network errors gracefully
6. **Performance:** Use connection pooling, indexes, and caching
7. **User Experience:** Smooth animations and immediate feedback

**Resources:**

- PySide6 Documentation: https://doc.qt.io/qtforpython/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Lucide Icons: https://lucide.dev/
- Qt Stylesheets: https://doc.qt.io/qt-6/stylesheet-reference.html

Good luck with your implementation! 🚀
