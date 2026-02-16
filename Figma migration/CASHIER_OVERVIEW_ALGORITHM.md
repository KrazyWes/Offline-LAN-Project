# Cashier Overview Algorithm Documentation

## Overview
This document describes the algorithm and logic flow for the Cashier Overview dashboard feature, which manages and displays transaction data for up to 20 cashiers with various filtering, sorting, and viewing options.

---

## 1. Data Structure

### CashierData Interface
```typescript
interface CashierData {
  id: number;              // Unique cashier identifier
  name: string;            // Cashier name
  isOnline: boolean;       // Online/offline status
  batteryPercentage: number; // Battery level (0-100)
  totalBets: number;       // Total bets amount
  cashIn: number;          // Cash in amount
  cashOut: number;         // Cash out amount
  drawBets: number;        // Draw bets amount (currently ₱0.00)
  cancelBets: number;      // Cancel bets amount (currently ₱0.00)
  unclaimed: number;       // Unclaimed amount (currently ₱0.00)
  withdraw: number;        // Withdraw amount
  coh: number;            // Cash on Hand (calculated)
}
```

---

## 2. Data Generation Algorithm

### Mock Data Generation Process
```
FUNCTION generateMockCashiers() -> CashierData[]
  1. Initialize empty cashiers array
  2. Define 20 predefined names
  3. FOR i = 1 to 20:
     a. Generate random transaction values:
        - totalBets = random(10000 to 60000)
        - cashIn = random(20000 to 100000)
        - cashOut = random(5000 to 45000)
        - withdraw = random(5000 to 35000)
     b. Calculate COH (Cash on Hand):
        coh = cashIn - cashOut - withdraw
     c. Determine online status (70% probability of being online)
     d. Generate random battery percentage (0-100)
     e. Set drawBets, cancelBets, unclaimed to 0
     f. Create cashier object and add to array
  4. Return cashiers array
```

**Key Calculations:**
- **COH Formula**: `COH = Cash In - Cash Out - Withdraw`
- **Online Probability**: 70% online (Math.random() > 0.3)

---

## 3. State Management

### Application State Variables
```typescript
1. cashiers: CashierData[]           // Immutable list of all cashiers
2. globalViewAll: boolean            // Global expand/collapse state
3. individualViews: Record<number, boolean>  // Per-cashier expand state
4. searchQuery: string               // Search filter text
5. sortOption: SortOption            // Current sort method
6. showUnclaimed: boolean            // Toggle unclaimed visibility
7. showTooltip: boolean              // Tooltip visibility state
```

### Sort Options
```typescript
type SortOption = 
  | 'name-asc'      // Alphabetical A-Z
  | 'name-desc'     // Alphabetical Z-A
  | 'online'        // Online cashiers first
  | 'offline'       // Offline cashiers first
  | 'coh-high'      // Highest COH first
  | 'coh-low'       // Lowest COH first
  | 'bets-high'     // Highest total bets first
  | 'bets-low'      // Lowest total bets first
```

---

## 4. Filtering Algorithm

### Search Filter Logic
```
FUNCTION filterBySearch(cashiers, searchQuery) -> CashierData[]
  IF searchQuery is empty:
    RETURN all cashiers
  
  searchLower = searchQuery.toLowerCase()
  
  RETURN cashiers WHERE:
    cashier.name.toLowerCase() contains searchLower
```

**Implementation:**
```typescript
const filtered = cashiers.filter(cashier =>
  cashier.name.toLowerCase().includes(searchQuery.toLowerCase())
);
```

---

## 5. Sorting Algorithm

### Multi-criteria Sort Logic
```
FUNCTION sortCashiers(cashiers, sortOption) -> CashierData[]
  SWITCH sortOption:
    CASE 'name-asc':
      SORT by name ascending (A to Z)
    
    CASE 'name-desc':
      SORT by name descending (Z to A)
    
    CASE 'online':
      SORT by isOnline descending (true first)
    
    CASE 'offline':
      SORT by isOnline ascending (false first)
    
    CASE 'coh-high':
      SORT by coh descending (highest first)
    
    CASE 'coh-low':
      SORT by coh ascending (lowest first)
    
    CASE 'bets-high':
      SORT by totalBets descending (highest first)
    
    CASE 'bets-low':
      SORT by totalBets ascending (lowest first)
  
  RETURN sorted cashiers
```

**Implementation:**
```typescript
const sorted = [...filtered].sort((a, b) => {
  switch (sortOption) {
    case 'name-asc':
      return a.name.localeCompare(b.name);
    case 'name-desc':
      return b.name.localeCompare(a.name);
    case 'online':
      return (b.isOnline ? 1 : 0) - (a.isOnline ? 1 : 0);
    case 'offline':
      return (a.isOnline ? 1 : 0) - (b.isOnline ? 1 : 0);
    case 'coh-high':
      return b.coh - a.coh;
    case 'coh-low':
      return a.coh - b.coh;
    case 'bets-high':
      return b.totalBets - a.totalBets;
    case 'bets-low':
      return a.totalBets - b.totalBets;
    default:
      return 0;
  }
});
```

---

## 6. View Toggle Algorithm

### Global View Toggle
```
FUNCTION handleGlobalToggle():
  1. Invert current globalViewAll state
  2. Create new individualViews object
  3. FOR EACH cashier:
     Set individualViews[cashier.id] = new globalViewAll state
  4. Update state with new individualViews
```

**Effect:**
- When toggled ON: All cards expand to show full details
- When toggled OFF: All cards collapse to show name only

### Individual View Toggle
```
FUNCTION handleIndividualToggle(cashierId):
  1. Clone current individualViews
  2. Invert the state for the specific cashierId
  3. Update state
```

**Behavior:**
- Each card can be independently expanded/collapsed
- Individual toggles don't affect the global state
- Global toggle overrides all individual states

---

## 7. Unclaimed Visibility Toggle Algorithm

### Toggle Logic
```
FUNCTION toggleUnclaimed():
  1. Invert showUnclaimed state
  2. Pass showUnclaimed prop to all CashierCard components
  3. Each card conditionally renders unclaimed field based on prop
```

**Rendering Logic in Card:**
```
IF showUnclaimed is true:
  RENDER unclaimed field in card
ELSE:
  SKIP unclaimed field (not rendered)
```

**Visual Indicator:**
- Toggle switch: Blue (ON) / Gray (OFF)
- Tooltip on hover: Explains functionality

---

## 8. Card Display Algorithm

### Card Rendering Logic
```
FUNCTION renderCard(cashier, isExpanded, showUnclaimed):
  IF NOT isExpanded:
    RENDER collapsed view:
      - Online/offline status indicator (dot)
      - Cashier name
      - Expand button (Eye icon)
  ELSE:
    RENDER expanded view:
      - Header section:
        * Print button
        * Battery indicator (icon based on percentage)
        * Online/offline status badge
        * Collapse button (EyeOff icon)
      - Cashier name
      - Transaction grid (2 columns):
        * Total Bets
        * Cash In
        * Cash Out
        * Draw Bets
        * Cancel Bets
        * Unclaimed (IF showUnclaimed is true)
        * Withdraw
        * COH (full width, highlighted)
      - View Records button
```

### Battery Icon Logic
```
FUNCTION getBatteryIcon(percentage):
  IF percentage >= 80:
    RETURN BatteryFull (green)
  ELSE IF percentage >= 20:
    RETURN Battery (yellow)
  ELSE:
    RETURN BatteryLow (red)
```

---

## 9. Complete Data Flow

### User Interaction Flow
```
1. USER enters search query
   ↓
2. SYSTEM filters cashiers by name
   ↓
3. USER selects sort option
   ↓
4. SYSTEM sorts filtered results
   ↓
5. SYSTEM renders cards with current view states
   ↓
6. USER toggles global/individual views
   ↓
7. SYSTEM updates display accordingly
   ↓
8. USER toggles unclaimed visibility
   ↓
9. SYSTEM shows/hides unclaimed field in all cards
```

### Rendering Pipeline
```
Raw Data (20 cashiers)
    ↓
[FILTER by search query]
    ↓
Filtered Data
    ↓
[SORT by selected option]
    ↓
Sorted & Filtered Data
    ↓
[MAP to CashierCard components]
    ↓
[APPLY view states (expanded/collapsed)]
    ↓
[APPLY unclaimed visibility]
    ↓
Final Rendered Grid
```

---

## 10. Performance Considerations

### Optimization Strategies
1. **State Management**: Use `Record<number, boolean>` for O(1) lookup of individual view states
2. **Memoization**: Individual views stored in object for quick access
3. **Conditional Rendering**: Only render expanded content when needed
4. **CSS Grid**: Responsive grid with `items-start` to prevent height issues
5. **Key Props**: Use unique `cashier.id` as key for React optimization

### Computational Complexity
- **Filtering**: O(n) - linear scan through all cashiers
- **Sorting**: O(n log n) - standard comparison sort
- **Rendering**: O(n) - map through filtered/sorted array
- **Individual Toggle**: O(1) - direct state lookup and update
- **Global Toggle**: O(n) - update all individual states

---

## 11. UI/UX Features

### Responsive Design
- **Mobile**: 1 column grid
- **Tablet (md)**: 2 column grid
- **Desktop (lg)**: 3 column grid
- **Large Desktop (xl)**: 4 column grid

### Interactive Elements
1. **Search Bar**: Real-time filtering as user types
2. **Sort Dropdown**: 8 sorting options with visual indicator
3. **Global Toggle Button**: Shows Eye/EyeOff icon based on state
4. **Individual Toggle**: Per-card expand/collapse
5. **Unclaimed Switch**: iOS-style toggle with tooltip
6. **Print Button**: Triggers print dialog for individual card
7. **View Records Button**: Placeholder for future functionality

### Visual Indicators
- **Online Status**: Green dot/badge or red dot/badge
- **Battery Level**: Color-coded icons (green/yellow/red)
- **COH Display**: Highlighted in blue, larger font
- **Currency Formatting**: Philippine Peso (₱) with 2 decimals

---

## 12. Future Enhancement Possibilities

### Potential Improvements
1. **Pagination**: Handle more than 20 cashiers
2. **Real-time Updates**: WebSocket connection for live data
3. **Export Functionality**: CSV/PDF export of filtered data
4. **Advanced Filters**: Date range, amount range, multiple criteria
5. **Analytics Dashboard**: Charts and graphs for trends
6. **Notification System**: Alerts for low battery or offline cashiers
7. **Print Preview**: Custom print layout before printing
8. **Audit Trail**: Track who viewed which records

---

## Summary

The Cashier Overview algorithm efficiently manages the display and interaction of cashier transaction data through:
- **Dynamic filtering** based on search queries
- **Multi-criteria sorting** with 8 different options
- **Flexible view management** (global and individual toggles)
- **Conditional rendering** for optimal performance
- **Responsive grid layout** adapting to screen size
- **Subtle UI controls** like the unclaimed visibility toggle

The system is designed to handle up to 20 cashiers in the prototype with room for scalability in production.
