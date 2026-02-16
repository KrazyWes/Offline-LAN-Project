# Complete Dashboard System Algorithm & Visual Specification
## Comprehensive Step-by-Step Documentation

> **IMPORTANT DATA NOTE**: All cashier names, transaction amounts, and other data displayed in the current prototype are **MOCK DATA for demonstration and prototyping purposes only**. In a production environment, all data should be retrieved from the appropriate database tables through secure API endpoints.

---

## Table of Contents
1. [System Architecture Overview](#system-architecture-overview)
2. [Visual Design Specifications](#visual-design-specifications)
3. [Sidebar Navigation Component](#sidebar-navigation-component)
4. [Cashier Overview Main Screen](#cashier-overview-main-screen)
5. [Data Structure & Database Schema](#data-structure--database-schema)
6. [Complete User Interaction Flows](#complete-user-interaction-flows)
7. [Detailed Algorithm Explanations](#detailed-algorithm-explanations)
8. [Responsive Design Breakpoints](#responsive-design-breakpoints)

---

## 1. System Architecture Overview

### Component Hierarchy
```
App (Root Component)
├── Sidebar Component
│   ├── Header Section (with collapse/expand toggle)
│   ├── Main Navigation Items
│   │   ├── Cashier overview
│   │   ├── Event overview
│   │   ├── Accounts
│   │   ├── Reports and database
│   │   └── Operate (with expandable sub-menu)
│   │       ├── Operator A
│   │       └── Operator B
│   └── Bottom Navigation Section (separated by border)
│       ├── Settings
│       ├── Utility
│       └── Logout
└── Main Content Area
    └── CashierOverview Component
        ├── Header Section
        │   ├── Title & Subtitle
        │   └── Control Buttons (Unclaimed Toggle, Hide All/View All)
        ├── Filter Section
        │   ├── Search Bar
        │   └── Sort Dropdown
        └── Cashier Cards Grid
            └── CashierCard Components (20 cards max in prototype)
```

---

## 2. Visual Design Specifications

### Color Palette

#### Primary Colors
- **Blue Primary**: `#2563eb` (rgb(37, 99, 235)) - Used for buttons, active states, and COH display
- **Blue Hover**: `#1d4ed8` (rgb(29, 78, 216)) - Hover state for blue buttons
- **Blue Light**: `#dbeafe` (rgb(219, 234, 254)) - Active navigation background
- **Blue Extra Light**: `#eff6ff` (rgb(239, 246, 255)) - Printer button background

#### Status Colors
- **Green (Online)**: `#22c55e` (rgb(34, 197, 94)) - Online status indicator
- **Green Light**: `#dcfce7` (rgb(220, 252, 231)) - Online badge background
- **Green Dark**: `#15803d` (rgb(21, 128, 61)) - Online badge text
- **Red (Offline)**: `#ef4444` (rgb(239, 68, 68)) - Offline status indicator
- **Red Light**: `#fee2e2` (rgb(254, 226, 226)) - Offline badge background
- **Red Dark**: `#991b1b` (rgb(153, 27, 27)) - Offline badge text

#### Battery Status Colors
- **Battery Full (≥80%)**: `#16a34a` (rgb(22, 163, 74)) - Green, good battery
- **Battery Medium (20-79%)**: `#ca8a04` (rgb(202, 138, 4)) - Yellow, moderate battery
- **Battery Low (<20%)**: `#dc2626` (rgb(220, 38, 38)) - Red, critical battery

#### Neutral Colors
- **White**: `#ffffff` - Background for cards and sidebar
- **Gray 50**: `#f9fafb` - Page background
- **Gray 100**: `#f3f4f6` - Hover states
- **Gray 200**: `#e5e7eb` - Borders
- **Gray 300**: `#d1d5db` - Inactive toggle background
- **Gray 400**: `#9ca3af` - Icon colors
- **Gray 500**: `#6b7280` - Label text
- **Gray 600**: `#4b5563` - Secondary text
- **Gray 700**: `#374151` - Navigation text
- **Gray 800**: `#1f2937` - Primary heading text

### Typography

#### Font Family
- **Default**: System font stack (uses browser's native sans-serif font)
- **Font Size Base**: 16px (1rem)

#### Font Sizes
- **Extra Small (xs)**: 12px (0.75rem) - Used for labels like "Total Bets", "Cash In"
- **Small (sm)**: 14px (0.875rem) - Used for navigation items, button text
- **Base**: 16px (1rem) - Used for normal text, inputs
- **Large (lg)**: 18px (1.125rem) - Used for cashier names (h3)
- **Extra Large (xl)**: 20px (1.25rem) - Used for COH amount
- **2XL**: 24px (1.5rem) - Used for page titles (h1)

#### Font Weights
- **Normal**: 400 - Regular text
- **Medium**: 500 - Navigation items, labels
- **Semibold**: 600 - Cashier names, field values
- **Bold**: 700 - Main titles, COH value

### Spacing System

#### Padding Values
- **p-2**: 8px - Small button padding, icon containers
- **p-4**: 16px - Card padding (collapsed), sidebar header horizontal
- **p-5**: 20px - Card padding (expanded)
- **px-3**: 12px horizontal - Status badges
- **py-1**: 4px vertical - Status badges
- **px-4 py-2**: 16px horizontal, 8px vertical - Buttons
- **px-4 py-3**: 16px horizontal, 12px vertical - Navigation items, search input

#### Gap Values
- **gap-2**: 8px - Small element spacing
- **gap-3**: 12px - Medium element spacing (header icons)
- **gap-4**: 16px - Card grid spacing

#### Margin Values
- **mb-4**: 16px bottom - Section spacing in cards
- **mt-1**: 4px top - Subtitle spacing
- **mt-2**: 8px top - Divider spacing

### Border & Shadow

#### Border Radius
- **rounded-lg**: 8px - Cards, buttons, inputs
- **rounded-full**: 9999px - Status dots, badges, toggle switch

#### Border Width & Color
- **border**: 1px solid #e5e7eb (gray-200) - Card borders, sidebar dividers
- **border-t**: 1px solid #e5e7eb (gray-200) - Section separators

#### Shadow Values
- **shadow-sm**: Small shadow for cards at rest
  - `box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05)`
- **shadow-md**: Medium shadow for cards on hover
  - `box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)`
- **shadow-lg**: Large shadow for tooltips
  - `box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)`

### Icon Specifications

#### Icon Library
- **Source**: lucide-react package
- **Default Size**: 20px (width and height)
- **Small Size**: 16px, 18px (for chevrons, help icon)

#### Icons Used
1. **Sidebar Navigation**:
   - `LayoutDashboard` (20px) - Cashier overview
   - `Calendar` (20px) - Event overview
   - `Users` (20px) - Accounts
   - `FileText` (20px) - Reports and database
   - `Wrench` (20px) - Operate, Utility
   - `Settings` (20px) - Settings
   - `LogOut` (20px) - Logout
   - `ChevronLeft`/`ChevronRight` (20px) - Sidebar toggle
   - `ChevronDown`/`ChevronUp` (16px) - Sub-menu toggle

2. **Cashier Overview**:
   - `Eye` (18px) - View/expand button
   - `EyeOff` (18px) - Hide/collapse button
   - `Search` (20px) - Search input icon
   - `ArrowUpDown` (20px) - Sort dropdown icon
   - `HelpCircle` (14px) - Info tooltip icon

3. **Cashier Cards**:
   - `Printer` (20px) - Print button
   - `BatteryFull` (20px) - Battery ≥80%
   - `Battery` (20px) - Battery 20-79%
   - `BatteryLow` (20px) - Battery <20%
   - `Eye` (18px) - Expand card
   - `EyeOff` (18px) - Collapse card

---

## 3. Sidebar Navigation Component

### Visual Structure (Expanded State)

```
┌────────────────────────────────────────┐
│  Dashboard                      [<]    │ ← Header (64px height, white bg, gray-200 bottom border)
├────────────────────────────────────────┤
│  [icon] Cashier overview              │ ← Active: blue-100 bg, blue-600 text
│  [icon] Event overview                │ ← Inactive: gray-700 text, hover gray-100 bg
│  [icon] Accounts                      │
│  [icon] Reports and database          │
│  [icon] Operate                   [v] │ ← Has chevron for sub-menu
│    └─ Operator A                      │ ← Sub-item (gray-50 bg, indented 56px)
│    └─ Operator B                      │
│                                        │ ← flex-1 space (pushes bottom items down)
├────────────────────────────────────────┤ ← Border separator (gray-200)
│  [icon] Settings                      │ ← Bottom section
│  [icon] Utility                       │
│  [icon] Logout                        │
└────────────────────────────────────────┘
```

**Dimensions**:
- **Expanded Width**: 256px (w-64)
- **Collapsed Width**: 80px (w-20)
- **Height**: 100vh (full screen height)
- **Header Height**: 64px (h-16)
- **Navigation Item Height**: Auto (based on padding: py-3 = 12px top + 12px bottom + content)

### Visual Structure (Collapsed State)

```
┌──────────┐
│    [<]   │ ← Header (only toggle button visible)
├──────────┤
│  [icon]  │ ← Icons centered, hover shows tooltip with title
│  [icon]  │
│  [icon]  │
│  [icon]  │
│  [icon]  │ ← Operate (sub-menu hidden when collapsed)
│          │
├──────────┤
│  [icon]  │ ← Settings (bottom section)
│  [icon]  │ ← Utility
│  [icon]  │ ← Logout
└──────────┘
```

### Sidebar Algorithm

#### Step 1: Initial State Setup
```javascript
INITIALIZE:
  - isExpanded = true (sidebar starts expanded)
  - isOperateOpen = false (Operate sub-menu starts closed)
  - activeItem = 'cashier-overview' (default active page)
```

#### Step 2: Sidebar Toggle Mechanism
```javascript
FUNCTION toggleSidebar():
  1. Read current isExpanded state
  2. Toggle state: isExpanded = !isExpanded
  3. IF transitioning from expanded to collapsed:
     a. Close Operate sub-menu: isOperateOpen = false
     b. This prevents visual glitches when re-expanding
  4. Apply CSS transition over 300ms
     - Width animates from 256px ↔ 80px
     - Text fades in/out using conditional rendering
```

**Visual Transition Details**:
- Duration: 300ms
- Easing: CSS default (ease)
- Properties animated: width
- Text shows/hides: Immediate (conditional rendering, no fade)

#### Step 3: Navigation Item Click Behavior
```javascript
FUNCTION handleNavItemClick(itemId):
  1. Check if item has sub-menu (Operate)
  2. IF item is "Operate":
     a. IF sidebar is expanded:
        - Toggle isOperateOpen state
        - Animate sub-menu slide down/up
     b. IF sidebar is collapsed:
        - Do nothing (sub-menu not accessible)
  3. ELSE (regular nav item):
     a. Set activeItem = itemId
     b. Trigger page content change in parent App component
```

#### Step 4: Active State Visual Logic
```javascript
FOR EACH navigation item:
  IF item.id === activeItem:
    - Apply background: bg-blue-100 (#dbeafe)
    - Apply text color: text-blue-600 (#2563eb)
  ELSE:
    - Apply text color: text-gray-700 (#374151)
    - On hover: bg-gray-100 (#f3f4f6)
```

#### Step 5: Logout Functionality
```javascript
FUNCTION handleLogout():
  1. Console log: "Logout clicked" (for debugging)
  2. Set activeItem = 'logout'
  3. IN PRODUCTION, SHOULD:
     a. Call logout API endpoint
     b. Clear authentication tokens from localStorage/cookies
     c. Clear user session data
     d. Redirect to login page
     e. Display logout confirmation message
```

### Sidebar Interaction Scenarios

#### Scenario 1: User Opens Operate Sub-Menu
**Pre-conditions**: Sidebar is expanded, Operate sub-menu is closed

**Step-by-step**:
1. User hovers over "Operate" → Background changes to gray-100
2. User clicks "Operate"
3. System checks: isExpanded === true
4. System toggles: isOperateOpen = true
5. Visual change:
   - Chevron icon rotates: ChevronDown → ChevronUp
   - Sub-menu container `<div className="bg-gray-50">` appears
   - "Operator A" and "Operator B" slide down into view
   - Each sub-item has 56px left padding (pl-14)
6. User can now click "Operator A" or "Operator B"

**Post-conditions**: Operate sub-menu is visible with 2 sub-items

#### Scenario 2: User Collapses Sidebar While Sub-Menu is Open
**Pre-conditions**: Sidebar is expanded, Operate sub-menu is open

**Step-by-step**:
1. User clicks chevron button (ChevronLeft icon)
2. System executes toggleSidebar()
3. System sets: isExpanded = false
4. System sets: isOperateOpen = false (forced closure)
5. Visual changes over 300ms:
   - Sidebar width: 256px → 80px
   - "Dashboard" text fades out
   - All navigation text fades out
   - All icons center themselves (justify-center)
   - Operate sub-menu disappears immediately
   - Chevron icon changes: ChevronLeft → ChevronRight
6. Tooltips become available on hover (title attribute)

**Post-conditions**: Sidebar is collapsed, only icons visible

#### Scenario 3: User Navigates to Different Page
**Pre-conditions**: User is on Cashier Overview page

**Step-by-step**:
1. User hovers over "Accounts" nav item
2. Visual feedback: Background changes to gray-100
3. User clicks "Accounts"
4. System calls: onActiveItemChange('accounts')
5. Visual changes:
   - Cashier overview: Remove blue-100 bg, change to gray-700 text
   - Accounts: Add blue-100 bg, change to blue-600 text
6. Parent App component updates content area
7. New page content loads (not yet implemented in prototype)

**Post-conditions**: Accounts nav item is active, main content area shows Accounts page

---

## 4. Cashier Overview Main Screen

### Layout Structure

```
┌───────────────────────────────────────────────────────────────────┐
│  Cashier Overview                         [?] [Toggle] [Hide All] │ ← Header Section (48px height)
│  Monitor all cashier transactions and statuses                    │   (gray-800 title, gray-500 subtitle)
├───────────────────────────────────────────────────────────────────┤
│  [🔍 Search cashier by name...]  [↕ Sort: Name A to Z      ▼]   │ ← Filter Section (56px height)
├───────────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐            │
│  │ Card 1  │  │ Card 2  │  │ Card 3  │  │ Card 4  │            │ ← Cards Grid
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘            │   (responsive columns)
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐            │
│  │ Card 5  │  │ Card 6  │  │ Card 7  │  │ Card 8  │            │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘            │
│                        ...                                         │
└───────────────────────────────────────────────────────────────────┘
```

### Header Section Detailed Breakdown

#### Title & Subtitle
```html
<h1 className="text-2xl font-bold text-gray-800">Cashier Overview</h1>
<p className="text-sm text-gray-500 mt-1">
  Monitor all cashier transactions and statuses
</p>
```
- **Title**: 24px size, 700 weight, #1f2937 color
- **Subtitle**: 14px size, 400 weight, #6b7280 color
- **Spacing**: 4px between title and subtitle

#### Unclaimed Toggle Switch (iOS-style)
Visual appearance:
```
OFF State:  [○────]  Gray-300 background (#d1d5db)
ON State:   [────○]  Blue-600 background (#2563eb)
```

**Dimensions**:
- **Width**: 44px (w-11)
- **Height**: 24px (h-6)
- **Switch Circle**: 16px diameter (h-4 w-4)
- **Padding**: 4px internal
- **Border Radius**: 9999px (fully rounded)

**Animation**:
- **Property**: transform (translateX)
- **Duration**: Instant (CSS transition default)
- **OFF position**: translateX(4px)
- **ON position**: translateX(24px)

**States**:
1. **OFF (showUnclaimed = false)**:
   - Background: gray-300
   - Circle position: Left (translateX(4px))
   - Result: Unclaimed field hidden in all cards

2. **ON (showUnclaimed = true)**:
   - Background: blue-600
   - Circle position: Right (translateX(24px))
   - Result: Unclaimed field visible in all cards

#### Info Button with Tooltip
```
Visual: [?] ← Gray-200 circle, 20px diameter
        ↓
    ┌──────────────────────────────────┐
    │ Toggle to show/hide unclaimed    │ ← Tooltip appears on hover
    │ amounts in all cashier cards     │   (gray-800 bg, white text)
    └──────────────────────────────────┘
```

**Info Button Specs**:
- **Size**: 20px × 20px (w-5 h-5)
- **Background**: gray-200 (#e5e7eb)
- **Hover Background**: gray-300 (#d1d5db)
- **Icon**: HelpCircle, 14px, gray-600 color
- **Border Radius**: rounded-full

**Tooltip Specs**:
- **Width**: 192px (w-48)
- **Padding**: 8px (p-2)
- **Background**: gray-800 (#1f2937)
- **Text Color**: white (#ffffff)
- **Font Size**: 12px (text-xs)
- **Position**: Below button (top-full mt-2)
- **Arrow**: 8px triangle pointing up, gray-800 color
- **Z-index**: 10 (above other elements)
- **Trigger**: onMouseEnter / onMouseLeave

#### Hide All / View All Button
```
View All Button:      Hide All Button:
┌──────────────┐      ┌──────────────┐
│ [👁] View All │      │ [👁‍🗨] Hide All│
└──────────────┘      └──────────────┘
Blue-600 bg           Blue-600 bg
White text            White text
```

**Button Specs**:
- **Padding**: 8px horizontal, 8px vertical (px-4 py-2)
- **Background**: blue-600 (#2563eb)
- **Hover Background**: blue-700 (#1d4ed8)
- **Text Color**: white (#ffffff)
- **Font Size**: 14px (implicit from button defaults)
- **Border Radius**: 8px (rounded-lg)
- **Icon Size**: 18px
- **Gap**: 8px between icon and text (gap-2)

**Function**: Toggles all cashier cards between expanded and collapsed views

### Search Bar Component

```
┌────────────────────────────────────────────────┐
│ 🔍  Search cashier by name...                  │ ← Input field (white bg, gray-300 border)
└────────────────────────────────────────────────┘
```

**Specifications**:
- **Width**: flex-1 (expands to fill available space)
- **Padding**: 40px left (pl-10), 16px right (pr-4), 12px vertical (py-3)
- **Border**: 1px solid gray-300 (#d1d5db)
- **Border Radius**: 8px (rounded-lg)
- **Background**: white (#ffffff)
- **Font Size**: 16px (base)
- **Placeholder Color**: gray-400 (#9ca3af)

**Search Icon**:
- **Position**: Absolute, left 12px (left-3), vertically centered
- **Size**: 20px
- **Color**: gray-400 (#9ca3af)

**Focus State**:
- **Border**: Removed (focus:border-transparent)
- **Ring**: 2px blue-500 (#3b82f6) ring around input
- **Outline**: None (outline-none)

**Search Algorithm**:
```javascript
FUNCTION filterBySearch(cashiers, searchQuery):
  1. IF searchQuery is empty string:
     RETURN all cashiers (no filtering)
  
  2. Convert searchQuery to lowercase: searchLower
  
  3. FOR EACH cashier in cashiers array:
     a. Convert cashier.name to lowercase
     b. Check if cashier.name contains searchLower substring
     c. IF yes: Include in filtered results
     d. IF no: Exclude from results
  
  4. RETURN filtered array
  
  5. IF filtered array is empty:
     - Display message: "No cashiers found matching "{searchQuery}""
     - Message styling: gray-500, 18px, centered, 48px vertical padding
```

### Sort Dropdown Component

```
┌────────────────────────────────────┐
│ ↕  Name: A to Z              ▼    │ ← Dropdown (white bg, gray-300 border)
└────────────────────────────────────┘
```

**Specifications**:
- **Width**: 256px (w-64) on desktop, full width on mobile
- **Padding**: 40px left (pl-10), 16px right (pr-4), 12px vertical (py-3)
- **Border**: 1px solid gray-300 (#d1d5db)
- **Border Radius**: 8px (rounded-lg)
- **Background**: white (#ffffff)
- **Font Size**: 16px (base)
- **Cursor**: pointer

**Sort Icon**:
- **Icon**: ArrowUpDown (lucide-react)
- **Position**: Absolute, left 12px, vertically centered
- **Size**: 20px
- **Color**: gray-400 (#9ca3af)
- **Pointer Events**: none (clicks pass through to select)

**Dropdown Options** (8 total):
1. "Name: A to Z" (value: 'name-asc')
2. "Name: Z to A" (value: 'name-desc')
3. "Status: Online First" (value: 'online')
4. "Status: Offline First" (value: 'offline')
5. "COH: Highest to Lowest" (value: 'coh-high')
6. "COH: Lowest to Highest" (value: 'coh-low')
7. "Total Bets: Highest to Lowest" (value: 'bets-high')
8. "Total Bets: Lowest to Highest" (value: 'bets-low')

### Cashier Cards Grid

**Responsive Grid Layout**:
```
Mobile (< 768px):     1 column  (grid-cols-1)
Tablet (≥ 768px):     2 columns (md:grid-cols-2)
Desktop (≥ 1024px):   3 columns (lg:grid-cols-3)
Large Desktop (≥ 1280px): 4 columns (xl:grid-cols-4)
```

**Grid Specifications**:
- **Gap**: 16px between cards (gap-4)
- **Alignment**: items-start (cards align to top, not stretched)
- **Container**: No fixed height, grows with content

---

## 5. Data Structure & Database Schema

### Cashier Data Interface (TypeScript)

```typescript
interface CashierData {
  id: number;                // Primary key, unique identifier
  name: string;              // Cashier full name (from users table)
  isOnline: boolean;         // Current connection status
  batteryPercentage: number; // Device battery level (0-100)
  totalBets: number;         // Sum of all bet transactions
  cashIn: number;            // Total cash received
  cashOut: number;           // Total cash disbursed
  drawBets: number;          // Cancelled due to draw
  cancelBets: number;        // Cancelled transactions
  unclaimed: number;         // Unclaimed winnings
  withdraw: number;          // Cash withdrawals
  coh: number;              // Cash on Hand (calculated)
}
```

### Database Schema (Production Implementation)

> **NOTE**: Current prototype uses mock data. In production, implement the following database structure:

#### Table: `cashiers`
```sql
CREATE TABLE cashiers (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  device_id VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### Table: `cashier_status`
```sql
CREATE TABLE cashier_status (
  id INT PRIMARY KEY AUTO_INCREMENT,
  cashier_id INT NOT NULL,
  is_online BOOLEAN DEFAULT FALSE,
  battery_percentage INT DEFAULT 100,
  last_heartbeat TIMESTAMP,
  device_info JSON,
  FOREIGN KEY (cashier_id) REFERENCES cashiers(id),
  INDEX idx_cashier_online (cashier_id, is_online)
);
```

#### Table: `transactions`
```sql
CREATE TABLE transactions (
  id INT PRIMARY KEY AUTO_INCREMENT,
  cashier_id INT NOT NULL,
  transaction_type ENUM('bet', 'cashin', 'cashout', 'withdraw', 'draw', 'cancel'),
  amount DECIMAL(10, 2) NOT NULL,
  transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  reference_number VARCHAR(50),
  status ENUM('pending', 'completed', 'cancelled') DEFAULT 'pending',
  FOREIGN KEY (cashier_id) REFERENCES cashiers(id),
  INDEX idx_cashier_date (cashier_id, transaction_date)
);
```

#### Table: `unclaimed_winnings`
```sql
CREATE TABLE unclaimed_winnings (
  id INT PRIMARY KEY AUTO_INCREMENT,
  cashier_id INT NOT NULL,
  ticket_number VARCHAR(50) UNIQUE NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  win_date TIMESTAMP,
  expiry_date TIMESTAMP,
  is_claimed BOOLEAN DEFAULT FALSE,
  FOREIGN KEY (cashier_id) REFERENCES cashiers(id),
  INDEX idx_unclaimed (cashier_id, is_claimed)
);
```

### Data Retrieval API Endpoints (Production)

#### GET `/api/cashiers/overview`
**Purpose**: Fetch all cashier data for the overview dashboard

**Response Format**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "John Smith",
      "isOnline": true,
      "batteryPercentage": 85,
      "totalBets": 45230.50,
      "cashIn": 78450.00,
      "cashOut": 23100.75,
      "drawBets": 0.00,
      "cancelBets": 0.00,
      "unclaimed": 5500.00,
      "withdraw": 15000.00,
      "coh": 40349.25
    },
    // ... more cashiers
  ],
  "timestamp": "2024-02-05T10:30:00Z"
}
```

**SQL Query (Backend)**:
```sql
SELECT 
  c.id,
  c.name,
  cs.is_online AS isOnline,
  cs.battery_percentage AS batteryPercentage,
  COALESCE(SUM(CASE WHEN t.transaction_type = 'bet' THEN t.amount ELSE 0 END), 0) AS totalBets,
  COALESCE(SUM(CASE WHEN t.transaction_type = 'cashin' THEN t.amount ELSE 0 END), 0) AS cashIn,
  COALESCE(SUM(CASE WHEN t.transaction_type = 'cashout' THEN t.amount ELSE 0 END), 0) AS cashOut,
  COALESCE(SUM(CASE WHEN t.transaction_type = 'draw' THEN t.amount ELSE 0 END), 0) AS drawBets,
  COALESCE(SUM(CASE WHEN t.transaction_type = 'cancel' THEN t.amount ELSE 0 END), 0) AS cancelBets,
  COALESCE(SUM(CASE WHEN uw.is_claimed = FALSE THEN uw.amount ELSE 0 END), 0) AS unclaimed,
  COALESCE(SUM(CASE WHEN t.transaction_type = 'withdraw' THEN t.amount ELSE 0 END), 0) AS withdraw,
  (
    COALESCE(SUM(CASE WHEN t.transaction_type = 'cashin' THEN t.amount ELSE 0 END), 0) -
    COALESCE(SUM(CASE WHEN t.transaction_type = 'cashout' THEN t.amount ELSE 0 END), 0) -
    COALESCE(SUM(CASE WHEN t.transaction_type = 'withdraw' THEN t.amount ELSE 0 END), 0)
  ) AS coh
FROM cashiers c
LEFT JOIN cashier_status cs ON c.id = cs.cashier_id
LEFT JOIN transactions t ON c.id = t.cashier_id AND t.status = 'completed'
LEFT JOIN unclaimed_winnings uw ON c.id = uw.cashier_id
GROUP BY c.id, c.name, cs.is_online, cs.battery_percentage
ORDER BY c.name ASC;
```

### Mock Data Generation (Current Prototype)

```javascript
FUNCTION generateMockCashiers():
  1. Initialize empty cashiers array
  
  2. Define 20 predefined names:
     ['John Smith', 'Maria Garcia', 'David Lee', ... 'Nancy Lewis']
  
  3. FOR i = 1 to 20:
     a. Generate random values:
        - totalBets = random integer between 10,000 and 60,000
        - cashIn = random integer between 20,000 and 100,000
        - cashOut = random integer between 5,000 and 45,000
        - withdraw = random integer between 5,000 and 35,000
        - isOnline = true if random() > 0.3 (70% probability)
        - batteryPercentage = random integer between 0 and 100
     
     b. Calculate COH:
        coh = cashIn - cashOut - withdraw
     
     c. Set prototype defaults:
        - drawBets = 0
        - cancelBets = 0
        - unclaimed = 0
     
     d. Create cashier object:
        {
          id: i,
          name: names[i-1],
          isOnline: calculatedBoolean,
          batteryPercentage: calculatedNumber,
          totalBets: randomNumber,
          cashIn: randomNumber,
          cashOut: randomNumber,
          drawBets: 0,
          cancelBets: 0,
          unclaimed: 0,
          withdraw: randomNumber,
          coh: calculatedCOH
        }
     
     e. Push to cashiers array
  
  4. RETURN cashiers array (length: 20)
```

**Important**: This mock data is stored in component state and resets on page refresh. In production, data must persist in database and refresh via API calls.

---

## 6. Complete User Interaction Flows

### Flow 1: User Searches for Specific Cashier

**Initial State**:
- All 20 cashiers visible in grid
- Search input is empty
- Cards sorted alphabetically (default)

**User Actions & System Responses**:

1. **User clicks search input**
   - Input border glows with blue-500 ring (2px)
   - Cursor appears in input field
   - Placeholder text visible: "Search cashier by name..."

2. **User types "mar"** (3 characters)
   - System executes filter on every keystroke (real-time)
   - Filter algorithm:
     ```javascript
     cashiers.filter(c => 
       c.name.toLowerCase().includes('mar')
     )
     ```
   - Results: "Maria Garcia", "Amanda Martin", "Karen Robinson" (3 matches)
   - Grid updates: Only 3 cards displayed
   - Other 17 cards removed from DOM
   - Layout: Mobile=1 col, Tablet=2 col, Desktop=3 col, XL=3 col

3. **User continues typing "ia"** (now "maria")
   - Filter re-executes with "maria"
   - Results: "Maria Garcia" (1 match)
   - Grid updates: Only 1 card displayed
   - Layout: 1 card regardless of screen size

4. **User backspaces to "mar"**
   - Filter re-executes
   - Results: 3 cards reappear
   - Smooth re-render (React reconciliation)

5. **User clears search (deletes all text)**
   - searchQuery becomes empty string
   - Filter check: `searchQuery === ''` → TRUE
   - Result: All 20 cashiers return to view
   - Grid restores to full layout

6. **User types "xyz"** (no matches)
   - Filter executes, returns empty array
   - Grid area displays:
     ```
     ┌────────────────────────────────────┐
     │                                    │
     │   No cashiers found matching "xyz" │
     │                                    │
     └────────────────────────────────────┘
     ```
   - Message: gray-500, 18px, centered, 48px vertical padding

**State Changes**:
- `searchQuery`: "" → "m" → "ma" → "mar" → "maria" → "mar" → "" → "xyz"
- `filteredAndSortedCashiers.length`: 20 → 3 → 1 → 3 → 20 → 0

### Flow 2: User Sorts Cashiers by COH (Highest to Lowest)

**Initial State**:
- 20 cashiers visible
- Current sort: "Name: A to Z"
- Example order: Amanda, Charles, David, Emily...

**User Actions & System Responses**:

1. **User clicks sort dropdown**
   - Dropdown expands showing 8 options
   - Current selection highlighted (Name: A to Z)
   - Options displayed:
     ```
     [✓] Name: A to Z
     [ ] Name: Z to A
     [ ] Status: Online First
     [ ] Status: Offline First
     [ ] COH: Highest to Lowest    ← User hovers here
     [ ] COH: Lowest to Highest
     [ ] Total Bets: Highest to Lowest
     [ ] Total Bets: Lowest to Highest
     ```
   - Hovered option background: gray-100

2. **User clicks "COH: Highest to Lowest"**
   - Dropdown closes
   - `sortOption` state changes: 'name-asc' → 'coh-high'
   - Sort algorithm executes:
     ```javascript
     filteredCashiers.sort((a, b) => b.coh - a.coh)
     ```
   - Example result (COH values):
     ```
     Position 1: Lisa Anderson    ₱72,345.50
     Position 2: David Lee        ₱68,120.25
     Position 3: Michael Brown    ₱64,890.00
     ...
     Position 20: Sarah Johnson   ₱15,230.75
     ```
   - Grid re-renders with new order
   - Animation: Cards smoothly reposition (React key-based reconciliation)

3. **User notices highest COH cashier**
   - Lisa Anderson card appears in top-left position
   - COH value displayed prominently: "₱72,345.50" in blue-600, 20px font

4. **User applies search while sorted**
   - User types "li" in search
   - System applies filter first, then sort
   - Process:
     ```javascript
     // Step 1: Filter
     const filtered = cashiers.filter(c => 
       c.name.includes('li')
     )
     // Results: Lisa Anderson, William Thomas
     
     // Step 2: Sort filtered results
     const sorted = filtered.sort((a, b) => 
       b.coh - a.coh
     )
     // Final order: Lisa (higher COH), William
     ```
   - Grid shows 2 cards in COH order

**State Changes**:
- `sortOption`: 'name-asc' → 'coh-high'
- `filteredAndSortedCashiers`: Reordered by COH descending

### Flow 3: User Toggles Global View (Hide All)

**Initial State**:
- All 20 cashiers in expanded view (full details visible)
- Button reads: "Hide All" with EyeOff icon
- `globalViewAll` = true
- `individualViews` = { 1: true, 2: true, ..., 20: true }

**User Actions & System Responses**:

1. **User hovers over "Hide All" button**
   - Background changes: blue-600 → blue-700
   - Transition: 150ms smooth color change
   - Cursor: pointer

2. **User clicks "Hide All" button**
   - System executes `handleGlobalToggle()` function
   - State changes:
     ```javascript
     setGlobalViewAll(false)  // true → false
     
     // Update all individual views
     setIndividualViews({
       1: false,
       2: false,
       3: false,
       ...
       20: false
     })
     ```
   - Button updates:
     - Text changes: "Hide All" → "View All"
     - Icon changes: EyeOff → Eye

3. **All 20 cards simultaneously collapse**
   - Transition occurs for each card
   - Collapsed card structure:
     ```
     ┌────────────────────────────┐
     │ ● Maria Garcia        [👁] │
     └────────────────────────────┘
     ```
   - Collapsed card dimensions:
     - Height: ~56px (auto-based on content)
     - Padding: 16px (p-4)
     - Shows: Status dot (8px), name, expand button
   - Grid re-flows: More cards visible per row due to reduced height
   - Scroll position maintained

4. **User scrolls down**
   - All cards remain collapsed
   - Individual expand buttons visible on each card
   - Smooth scrolling through list of 20 collapsed cards

5. **User clicks "View All" button**
   - System executes `handleGlobalToggle()` again
   - State changes:
     ```javascript
     setGlobalViewAll(true)  // false → true
     
     setIndividualViews({
       1: true,
       2: true,
       ...
       20: true
     })
     ```
   - Button reverts: "View All" → "Hide All", Eye → EyeOff

6. **All 20 cards simultaneously expand**
   - Each card shows full transaction details
   - Expanded card dimensions:
     - Height: ~500px (varies based on unclaimed toggle)
     - Padding: 20px (p-5)
     - Shows: Header, name, transaction grid, COH, View Records button
   - Grid adjusts: Fewer cards visible, scrollbar appears
   - Page scrolls to previous position (browser default)

**State Changes**:
- `globalViewAll`: true → false → true
- `individualViews`: All true → All false → All true
- Button text: "Hide All" → "View All" → "Hide All"

### Flow 4: User Toggles Individual Card View

**Initial State**:
- All cards expanded (global view = true)
- User focuses on "Maria Garcia" card in position 2

**User Actions & System Responses**:

1. **User locates Maria Garcia card**
   - Card shows:
     - Header: Printer button, Battery (85%), Online badge
     - Name: "Cashier: Maria Garcia"
     - Transaction grid (2 columns, 7-8 rows)
     - COH: ₱55,234.50 (blue, large)
     - View Records button
   - Card height: ~500px

2. **User hovers over collapse button (EyeOff icon)**
   - Button background: transparent → gray-100
   - Icon color remains gray-600
   - Transition: 150ms
   - Tooltip appears: "Hide details"

3. **User clicks collapse button**
   - System executes `handleIndividualToggle(2)` (Maria's ID)
   - State change:
     ```javascript
     setIndividualViews(prev => ({
       ...prev,
       2: false  // Only Maria's card affected
     }))
     ```
   - `globalViewAll` remains true (unchanged)

4. **Maria's card collapses**
   - Animation: Smooth height transition (CSS default)
   - Card contents change:
     - Header section disappears
     - Transaction grid disappears
     - COH section disappears
     - View Records button disappears
   - New collapsed view:
     ```
     ┌────────────────────────────┐
     │ ● Maria Garcia        [👁] │ ← Green dot (online)
     └────────────────────────────┘
     ```
   - Surrounding cards shift up to fill space
   - Grid layout adjusts automatically

5. **Other 19 cards remain expanded**
   - John Smith (position 1): Still showing full details
   - David Lee (position 3): Still showing full details
   - All others: Unaffected by Maria's collapse

6. **User clicks expand button on Maria's card**
   - System executes `handleIndividualToggle(2)` again
   - State change:
     ```javascript
     setIndividualViews(prev => ({
       ...prev,
       2: true  // Maria's card re-expanded
     }))
     ```

7. **Maria's card expands**
   - Full details return
   - Animation: Smooth height expansion
   - Card returns to ~500px height
   - Grid adjusts again

**Key Difference from Global Toggle**:
- Individual toggle affects only ONE card
- Does NOT change `globalViewAll` state
- Other cards maintain their current state
- If user later clicks "Hide All", Maria's individual state gets overridden

**State Changes**:
- `globalViewAll`: true (unchanged)
- `individualViews[2]`: true → false → true
- All other `individualViews` entries: Unchanged

### Flow 5: User Toggles Unclaimed Field Visibility

**Initial State**:
- Unclaimed toggle: ON (blue-600)
- All cards showing unclaimed field
- Unclaimed values: ₱0.00 (prototype default)

**User Actions & System Responses**:

1. **User notices unclaimed toggle in header**
   - Toggle position: Between page title and "Hide All" button
   - Current state: Switch in right position (ON)
   - Background: blue-600
   - Next to it: Info button [?]

2. **User hovers over info button (?)**
   - Button background: gray-200 → gray-300
   - Tooltip appears after 0ms (immediate):
     ```
     ┌──────────────────────────────────────┐
     │ Toggle to show/hide unclaimed        │
     │ amounts in all cashier cards         │
     └──────────────────────────────────────┘
               ▲ (arrow points to button)
     ```
   - Tooltip specs:
     - Width: 192px
     - Background: gray-800
     - Text: white, 12px
     - Padding: 8px
     - Shadow: Large (shadow-lg)
     - Arrow: 8px triangle, -4px top offset

3. **User moves mouse away from info button**
   - `onMouseLeave` event triggers
   - Tooltip disappears immediately
   - Button background returns to gray-200

4. **User clicks unclaimed toggle**
   - `onClick` event triggers
   - System executes:
     ```javascript
     setShowUnclaimed(!showUnclaimed)  // true → false
     ```
   - Toggle animation:
     - Background: blue-600 → gray-300 (instant color change)
     - Circle position: Right → Left (translateX(24px) → translateX(4px))
     - Transition: Smooth (CSS default ~150ms)

5. **All 20 cards update simultaneously**
   - For each expanded card:
     - Unclaimed row REMOVED from transaction grid
     - Grid adjusts from 8 rows to 7 rows
     - Example before:
       ```
       Total Bets    Cash In
       Cash Out      Draw Bets
       Cancel Bets   Unclaimed      ← This row removed
       Withdraw      [empty]
       ───────────────────────
       COH
       ```
     - Example after:
       ```
       Total Bets    Cash In
       Cash Out      Draw Bets
       Cancel Bets   Withdraw
       ───────────────────────
       COH
       ```
   - Card height reduces by ~24px (one row height)
   - Grid re-flows, more content visible
   - For collapsed cards: No visual change (unclaimed wasn't visible anyway)

6. **User clicks toggle again (turns ON)**
   - State changes: false → true
   - Toggle animation reverses
   - Background: gray-300 → blue-600
   - Circle: Left → Right

7. **Unclaimed field returns to all cards**
   - Row reappears in transaction grid
   - Each shows: "Unclaimed" label, "₱0.00" value
   - Card height increases by ~24px
   - Grid adjusts downward

**Production Note**:
- In live system, unclaimed values would be fetched from database
- Values would vary by cashier (not all ₱0.00)
- Toggle preference could be saved to user settings

**State Changes**:
- `showUnclaimed`: true → false → true
- `showTooltip`: false → true (on hover) → false
- Cards re-render count: All 20 cards (due to prop change)

### Flow 6: User Prints Transaction Card

**Initial State**:
- User viewing expanded card for "John Smith"
- Card shows all transaction details
- Printer button visible in top-left of card

**User Actions & System Responses**:

1. **User hovers over printer button**
   - Button specifications:
     - Size: 40px × 40px (p-2 with 20px icon)
     - Current background: blue-100 (#dbeafe)
     - Hover background: blue-200 (#bfdbfe)
     - Icon: Printer, 20px, blue-600 color
     - Border radius: 8px (rounded-lg)
   - Transition: 150ms smooth background change
   - Cursor: pointer
   - Tooltip: "Print transaction card"

2. **User clicks printer button**
   - System executes:
     ```javascript
     onClick={() => {
       console.log(`Print transaction card for ${cashier.name}`)
       window.print()
     }}
     ```
   - Console log appears in browser DevTools
   - Browser print dialog opens immediately

3. **Browser print dialog appears**
   - Dialog shows:
     - Printer selection dropdown
     - Page orientation (Portrait/Landscape)
     - Color options
     - Page range
     - Copies
     - Preview pane showing entire dashboard
   - Current behavior: Prints ENTIRE page (not just card)

4. **Production Implementation (Future)**
   - Should create print-specific view showing only the card
   - Print CSS should hide:
     - Sidebar navigation
     - Page header
     - Other cashier cards
     - Filter/search controls
   - Print CSS should show:
     - Only selected cashier's data
     - Company logo/header
     - Print timestamp
     - Footer with page numbers
   - Implementation:
     ```css
     @media print {
       .sidebar, .header, .other-cards {
         display: none !important;
       }
       .cashier-card {
         break-inside: avoid;
         page-break-inside: avoid;
       }
     }
     ```

5. **User cancels print dialog**
   - Dialog closes
   - Page returns to normal view
   - No changes to application state

**Production Enhancement Recommendations**:
1. Create dedicated print template component
2. Add print preview button
3. Generate PDF option (using library like jsPDF)
4. Include transaction details:
   - Cashier name and ID
   - Print date/time
   - Transaction summary
   - Battery status at print time
   - Last sync timestamp
5. Email/download options

### Flow 7: User Clicks "View Records" Button

**Initial State**:
- User viewing expanded card
- View Records button visible at bottom of card

**User Actions & System Responses**:

1. **User sees "View Records" button**
   - Button position: Full width of card, below COH section
   - Specifications:
     - Width: 100% (w-full)
     - Padding: 8px vertical, 16px horizontal (py-2 px-4)
     - Background: blue-600 (#2563eb)
     - Text: white (#ffffff), 14px (text-sm), 500 weight
     - Border radius: 8px (rounded-lg)
     - Text: "View Records"

2. **User hovers over button**
   - Background changes: blue-600 → blue-700
   - Transition: 150ms smooth
   - Cursor: pointer
   - No icon (text only)

3. **User clicks button**
   - System executes:
     ```javascript
     onClick={() => {
       console.log(`View records for ${cashier.name}`)
     }}
     ```
   - Console log appears: "View records for John Smith"
   - Currently: No further action (placeholder)

4. **Production Implementation (Future)**
   - Should navigate to detailed records page
   - Route: `/cashier-records/${cashierId}`
   - New page should display:
     - Transaction history table
     - Filters: Date range, transaction type
     - Export options
     - Pagination
     - Search within records
   - Example implementation:
     ```javascript
     onClick={() => {
       navigate(`/cashier-records/${cashier.id}`)
     }}
     ```

**Future Page Structure**:
```
┌──────────────────────────────────────────────────┐
│  ← Back to Overview                              │
│                                                   │
│  Transaction Records - John Smith                │
│  ┌──────────────────────────────────────────────┐ │
│  │ Date Range: [Jan 1] - [Jan 31]  [Filter]    │ │
│  │ Type: [All ▼]  Status: [All ▼]              │ │
│  └──────────────────────────────────────────────┘ │
│                                                   │
│  ┌──────────────────────────────────────────────┐ │
│  │ Date       │ Type   │ Amount   │ Status      │ │
│  ├────────────┼────────┼──────────┼─────────────┤ │
│  │ 2024-01-05 │ Bet    │ ₱500.00  │ Completed   │ │
│  │ 2024-01-05 │ CashIn │ ₱5000.00 │ Completed   │ │
│  │ ...                                           │ │
│  └──────────────────────────────────────────────┘ │
│                                                   │
│  Page 1 of 45           [< 1 2 3 ... 45 >]      │
└──────────────────────────────────────────────────┘
```

---

## 7. Detailed Algorithm Explanations

### Algorithm 1: Filter & Sort Pipeline

This is the core algorithm that processes cashier data before rendering.

```javascript
FUNCTION getFilteredAndSortedCashiers(
  cashiers: CashierData[],
  searchQuery: string,
  sortOption: SortOption
): CashierData[] {
  
  // STEP 1: FILTER BY SEARCH QUERY
  // Complexity: O(n) where n = number of cashiers
  
  LET filtered = []
  
  IF searchQuery === "" OR searchQuery === null:
    filtered = cashiers  // No filtering, use all cashiers
  ELSE:
    searchLower = searchQuery.toLowerCase()
    
    FOR EACH cashier IN cashiers:
      cashierNameLower = cashier.name.toLowerCase()
      
      IF cashierNameLower contains searchLower:
        ADD cashier to filtered array
      END IF
    END FOR
  END IF
  
  // At this point: filtered contains 0 to 20 cashiers
  // Example: If searchQuery="mar", filtered might have 3 cashiers
  
  
  // STEP 2: SORT FILTERED RESULTS
  // Complexity: O(m log m) where m = filtered.length
  
  LET sorted = [...filtered]  // Create copy to avoid mutation
  
  SWITCH sortOption:
    
    CASE 'name-asc':
      // Alphabetical A to Z
      sorted.sort((a, b) => {
        RETURN a.name.localeCompare(b.name)
      })
      // Example result order: "Amanda" before "Charles"
      BREAK
    
    CASE 'name-desc':
      // Alphabetical Z to A
      sorted.sort((a, b) => {
        RETURN b.name.localeCompare(a.name)
      })
      // Example result order: "William" before "Thomas"
      BREAK
    
    CASE 'online':
      // Online cashiers first, then offline
      sorted.sort((a, b) => {
        // Convert boolean to number: true=1, false=0
        aValue = a.isOnline ? 1 : 0
        bValue = b.isOnline ? 1 : 0
        RETURN bValue - aValue  // Descending (1 before 0)
      })
      // Result: All online cashiers, then all offline
      BREAK
    
    CASE 'offline':
      // Offline cashiers first, then online
      sorted.sort((a, b) => {
        aValue = a.isOnline ? 1 : 0
        bValue = b.isOnline ? 1 : 0
        RETURN aValue - bValue  // Ascending (0 before 1)
      })
      BREAK
    
    CASE 'coh-high':
      // Highest COH first
      sorted.sort((a, b) => {
        RETURN b.coh - a.coh  // Descending
      })
      // Example: ₱75,000 before ₱50,000 before ₱25,000
      BREAK
    
    CASE 'coh-low':
      // Lowest COH first
      sorted.sort((a, b) => {
        RETURN a.coh - b.coh  // Ascending
      })
      BREAK
    
    CASE 'bets-high':
      // Highest total bets first
      sorted.sort((a, b) => {
        RETURN b.totalBets - a.totalBets
      })
      BREAK
    
    CASE 'bets-low':
      // Lowest total bets first
      sorted.sort((a, b) => {
        RETURN a.totalBets - b.totalBets
      })
      BREAK
    
    DEFAULT:
      // No sorting, keep filtered order
      BREAK
  
  END SWITCH
  
  RETURN sorted
  
}

// USAGE IN COMPONENT:
const filteredAndSortedCashiers = getFilteredAndSortedCashiers(
  cashiers,
  searchQuery,
  sortOption
)

// Then render:
filteredAndSortedCashiers.map(cashier => (
  <CashierCard key={cashier.id} cashier={cashier} />
))
```

**Performance Analysis**:
- **Best Case**: O(n) when no sorting needed (unlikely)
- **Average Case**: O(n + m log m)
  - n = 20 (filter pass)
  - m = filtered results (varies 0-20)
  - Typically: O(20 + 20 log 20) ≈ O(86) operations
- **Worst Case**: O(n log n) when all cashiers match filter
  - O(20 log 20) ≈ O(86) operations
- **Conclusion**: Very fast, renders in <1ms

### Algorithm 2: COH (Cash on Hand) Calculation

The most important financial calculation in the system.

```javascript
FUNCTION calculateCOH(cashier: CashierData): number {
  
  // FORMULA: COH = Cash In - Cash Out - Withdraw
  // This represents the physical cash the cashier should have
  
  LET cashIn = cashier.cashIn         // Money received from customers
  LET cashOut = cashier.cashOut       // Money paid to customers (winnings)
  LET withdraw = cashier.withdraw     // Money withdrawn by cashier
  
  LET coh = cashIn - cashOut - withdraw
  
  RETURN coh
  
}

// EXAMPLE CALCULATION:
// Cashier: John Smith
// Cash In:   ₱78,450.00  (customers paid John)
// Cash Out:  ₱23,100.75  (John paid winning customers)
// Withdraw:  ₱15,000.00  (John withdrew for remittance)
// ────────────────────────
// COH = 78,450.00 - 23,100.75 - 15,000.00
// COH = ₱40,349.25
// 
// This means John should physically have ₱40,349.25 in cash
```

**Why These Fields?**
1. **Cash In**: All money received from customers
   - Includes: Bets, deposits, reloads
   - Does NOT include: Unclaimed winnings (not yet paid)

2. **Cash Out**: All money paid to customers
   - Includes: Winning payouts, refunds
   - Does NOT include: Withdrawals (see below)

3. **Withdraw**: Money removed from cashier's drawer
   - Includes: Manager pickups, bank deposits, remittances
   - Reduces available cash

4. **Why NOT included**:
   - **Total Bets**: Already counted in Cash In
   - **Draw Bets**: Refunded, counted in Cash Out
   - **Cancel Bets**: Refunded, counted in Cash Out
   - **Unclaimed**: Not yet paid out, doesn't affect current cash

**Production Note**: In live system, COH should be calculated server-side to prevent manipulation.

### Algorithm 3: Battery Icon Selection

Determines which battery icon and color to display based on percentage.

```javascript
FUNCTION getBatteryIcon(batteryPercentage: number): ReactElement {
  
  // LOGIC: Three-tier system based on battery level
  
  IF batteryPercentage >= 80:
    // Good battery level
    RETURN <BatteryFull 
      size={20} 
      className="text-green-600"  // #16a34a
    />
  
  ELSE IF batteryPercentage >= 20:
    // Moderate battery level
    RETURN <Battery 
      size={20} 
      className="text-yellow-600"  // #ca8a04
    />
  
  ELSE:
    // Critical battery level
    RETURN <BatteryLow 
      size={20} 
      className="text-red-600"  // #dc2626
    />
  
  END IF
  
}

// EXAMPLES:
// batteryPercentage = 95  →  🔋 Green (BatteryFull)
// batteryPercentage = 80  →  🔋 Green (BatteryFull) ← Boundary
// batteryPercentage = 79  →  🔋 Yellow (Battery)
// batteryPercentage = 50  →  🔋 Yellow (Battery)
// batteryPercentage = 20  →  🔋 Yellow (Battery) ← Boundary
// batteryPercentage = 19  →  🔋 Red (BatteryLow)
// batteryPercentage = 5   →  🔋 Red (BatteryLow)
// batteryPercentage = 0   →  🔋 Red (BatteryLow)
```

**Visual Appearance**:
- **BatteryFull**: Full battery icon, green
- **Battery**: Medium-filled battery icon, yellow
- **BatteryLow**: Empty battery icon, red

**Production Enhancement**:
- Add push notification when battery drops below 20%
- Highlight card border in red for critical battery
- Log battery history for device maintenance tracking

### Algorithm 4: Currency Formatting

Formats numbers as Philippine Peso with proper separators.

```javascript
FUNCTION formatCurrency(amount: number): string {
  
  // Handle null/undefined values
  const value = amount ?? 0
  
  // Use JavaScript Intl API for proper formatting
  const formatted = value.toLocaleString('en-PH', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
  
  // Prepend peso symbol
  RETURN `₱${formatted}`
  
}

// EXAMPLES:
// formatCurrency(45230.50)   →  "₱45,230.50"
// formatCurrency(1234567.89) →  "₱1,234,567.89"
// formatCurrency(0)          →  "₱0.00"
// formatCurrency(null)       →  "₱0.00"
// formatCurrency(undefined)  →  "₱0.00"
// formatCurrency(100)        →  "₱100.00"
// formatCurrency(100.5)      →  "₱100.50"
// formatCurrency(100.456)    →  "₱100.46" (rounds)
```

**Formatting Rules**:
1. **Thousands Separator**: Comma (,)
   - US/PH standard: 1,000 not 1.000
2. **Decimal Separator**: Period (.)
   - US/PH standard: 0.50 not 0,50
3. **Decimal Places**: Always 2
   - Even for whole numbers: 100.00 not 100
4. **Currency Symbol**: Philippine Peso (₱)
   - Unicode: U+20B1
   - Position: Before number (₱100 not 100₱)
5. **Negative Numbers**: -₱100.00
   - In production, handle negative COH with red text

**Why en-PH locale?**
- Matches Philippine number formatting standards
- Ensures consistency across different devices/browsers
- Handles currency rounding properly

### Algorithm 5: Global View Toggle with State Synchronization

Most complex state management in the application.

```javascript
FUNCTION handleGlobalToggle() {
  
  // STEP 1: Read current global state
  const currentState = globalViewAll  // true or false
  
  // STEP 2: Calculate new state (invert)
  const newState = !currentState
  
  // STEP 3: Update global state
  setGlobalViewAll(newState)
  
  // STEP 4: Create new individualViews object
  // This is the KEY step that synchronizes all cards
  const newIndividualViews = {}
  
  // STEP 5: Loop through all cashiers
  FOR EACH cashier IN cashiers:
    // Set every cashier's individual view to match global state
    newIndividualViews[cashier.id] = newState
  END FOR
  
  // Example after this loop:
  // If newState = false (Hide All clicked):
  // newIndividualViews = {
  //   1: false,
  //   2: false,
  //   3: false,
  //   ... all 20 entries set to false
  // }
  
  // STEP 6: Batch update all individual views
  setIndividualViews(newIndividualViews)
  
  // React will now re-render all 20 CashierCard components
  // Each receives new isExpanded prop (all true or all false)
  
}

// INTERACTION WITH INDIVIDUAL TOGGLES:
// 
// Scenario: User manually collapsed cards 2, 5, and 8
// Current state:
//   globalViewAll = true (because not all are hidden)
//   individualViews = {
//     1: true,  2: false, 3: true,  4: true,  5: false,
//     6: true,  7: true,  8: false, 9: true,  10: true,
//     ... etc
//   }
// 
// User clicks "Hide All":
//   1. newState = false
//   2. ALL individualViews become false (overrides manual states)
//   3. Result: All 20 cards collapse
// 
// User clicks "View All":
//   1. newState = true
//   2. ALL individualViews become true (previous collapse forgotten)
//   3. Result: All 20 cards expand
// 
// IMPORTANT: Global toggle always OVERRIDES individual states
```

**State Management Flow Diagram**:
```
User Clicks "Hide All"
        ↓
handleGlobalToggle() executes
        ↓
globalViewAll: true → false
        ↓
Calculate newIndividualViews
        ↓
Loop all 20 cashiers
        ↓
Set each id: false
        ↓
setIndividualViews({1:false, 2:false, ...})
        ↓
React detects state change
        ↓
Re-render CashierOverview
        ↓
Map through cashiers
        ↓
Render 20 CashierCard components
        ↓
Each receives isExpanded={false}
        ↓
Each card's render function checks isExpanded
        ↓
Each returns collapsed JSX
        ↓
DOM updates (all cards collapse)
        ↓
User sees all cards collapsed
```

---

## 8. Responsive Design Breakpoints

### Breakpoint System

Tailwind CSS uses mobile-first breakpoints:

```javascript
// Default (no prefix): 0px - 767px (Mobile)
// md: 768px - 1023px (Tablet)
// lg: 1024px - 1279px (Desktop)
// xl: 1280px+ (Large Desktop)
```

### Component Responsiveness

#### Cards Grid Layout

**Mobile (< 768px)**:
```
┌──────────────────┐
│   Card 1         │
├──────────────────┤
│   Card 2         │
├──────────────────┤
│   Card 3         │
├──────────────────┤
│   ...            │
└──────────────────┘
```
- **Columns**: 1 (grid-cols-1)
- **Card Width**: 100% of container
- **Gap**: 16px vertical
- **Visible Cards**: ~2-3 without scrolling

**Tablet (768px - 1023px)**:
```
┌─────────────┬─────────────┐
│   Card 1    │   Card 2    │
├─────────────┼─────────────┤
│   Card 3    │   Card 4    │
├─────────────┼─────────────┤
│   ...       │   ...       │
└─────────────┴─────────────┘
```
- **Columns**: 2 (md:grid-cols-2)
- **Card Width**: ~50% minus gap
- **Gap**: 16px horizontal and vertical
- **Visible Cards**: ~4-6 without scrolling

**Desktop (1024px - 1279px)**:
```
┌──────────┬──────────┬──────────┐
│  Card 1  │  Card 2  │  Card 3  │
├──────────┼──────────┼──────────┤
│  Card 4  │  Card 5  │  Card 6  │
├──────────┼──────────┼──────────┤
│  ...     │  ...     │  ...     │
└──────────┴──────────┴──────────┘
```
- **Columns**: 3 (lg:grid-cols-3)
- **Card Width**: ~33.33% minus gap
- **Gap**: 16px
- **Visible Cards**: ~6-9 without scrolling

**Large Desktop (≥ 1280px)**:
```
┌────────┬────────┬────────┬────────┐
│ Card 1 │ Card 2 │ Card 3 │ Card 4 │
├────────┼────────┼────────┼────────┤
│ Card 5 │ Card 6 │ Card 7 │ Card 8 │
├────────┼────────┼────────┼────────┤
│  ...   │  ...   │  ...   │  ...   │
└────────┴────────┴────────┴────────┘
```
- **Columns**: 4 (xl:grid-cols-4)
- **Card Width**: 25% minus gap
- **Gap**: 16px
- **Visible Cards**: ~8-12 without scrolling

#### Search & Sort Controls

**Mobile**:
```
┌──────────────────────────┐
│ 🔍 Search...             │
├──────────────────────────┤
│ ↕ Sort: Name A-Z    ▼   │
└──────────────────────────┘
```
- **Layout**: flex-col (stacked vertically)
- **Search Width**: 100%
- **Sort Width**: 100%
- **Gap**: 16px vertical

**Tablet & Desktop**:
```
┌───────────────────────┬──────────────┐
│ 🔍 Search...          │ ↕ Sort  ▼   │
└───────────────────────┴──────────────┘
```
- **Layout**: flex-row (side by side)
- **Search Width**: flex-1 (takes remaining space)
- **Sort Width**: 256px fixed
- **Gap**: 16px horizontal

#### Sidebar Behavior

**All Screen Sizes**:
- **Expanded**: 256px width
- **Collapsed**: 80px width
- **Always Visible**: No hamburger menu needed
- **Always Fixed**: Does not scroll with content

**Mobile Consideration**:
- For screens < 640px, consider:
  - Overlay sidebar (position: fixed, z-index)
  - Slide from left when opened
  - Backdrop overlay when open
  - (Not implemented in current prototype)

---

## Summary

This document provides a complete, detailed specification of the Dashboard system including:

1. **Visual Design**: Exact colors, fonts, spacing, and dimensions
2. **Component Structure**: Hierarchical breakdown with all elements
3. **Algorithms**: Step-by-step logic for all features
4. **User Flows**: Complete interaction scenarios with state changes
5. **Data Management**: Database schema and API structure
6. **Responsive Design**: Breakpoint behavior across devices

**Key Reminders**:
- All current data is MOCK DATA for prototyping
- Production system must fetch from database via secure APIs
- COH calculations must be server-side
- User authentication required for logout functionality
- Battery monitoring needs real device integration

This specification enables developers to:
- Understand every component's purpose
- Visualize the complete user experience
- Implement production features accurately
- Maintain consistency in design and behavior
- Debug issues by understanding expected behavior

---

**Document Version**: 1.0  
**Last Updated**: February 5, 2026  
**Status**: Complete Prototype Specification
