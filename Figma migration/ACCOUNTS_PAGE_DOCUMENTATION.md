# ACCOUNTS PAGE - COMPLETE SYSTEM DOCUMENTATION

## TABLE OF CONTENTS
1. [Overview](#overview)
2. [User Interface Specifications](#user-interface-specifications)
3. [Component Breakdown](#component-breakdown)
4. [Database Schema & Integration](#database-schema--integration)
5. [User Interactions & Behaviors](#user-interactions--behaviors)
6. [Functions & Logic](#functions--logic)
7. [Validation Rules](#validation-rules)
8. [PostgreSQL Migration Guide](#postgresql-migration-guide)

---

## OVERVIEW

### Purpose
The Accounts page is a comprehensive user management interface that allows administrators to:
- View all user accounts in a tabular format
- Search and filter users by name, email, or role
- Create new user accounts with role selection and validation
- Edit existing user accounts including role changes
- Delete user accounts with confirmation
- Monitor user status (Online, Offline, Away)
- Track last active timestamps
- Assign roles: Administrator, Cashier, Operator A, or Operator B

### Technology Stack
- **Frontend**: React with TypeScript
- **UI Framework**: Tailwind CSS
- **Icons**: Lucide React
- **State Management**: React useState hooks
- **Database (Migration Target)**: PostgreSQL

---

## USER INTERFACE SPECIFICATIONS

### Layout Structure
```
┌─────────────────────────────────────────────────────────┐
│  Header Section                                         │
│  ┌──────────────────────┐    ┌────────────────────┐   │
│  │ Title & Description  │    │ Create Account Btn │   │
│  └──────────────────────┘    └────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│  Search Bar                                             │
│  [🔍 Search by name, email, or role...]                │
├─────────────────────────────────────────────────────────┤
│  Stats Bar                                              │
│  Showing X users                                        │
├─────────────────────────────────────────────────────────┤
│  User Table                                             │
│  ┌───────┬──────┬────────┬─────────────┬─────────┐    │
│  │ User  │ Role │ Status │ Last Active │ Actions │    │
│  ├───────┼──────┼────────┼─────────────┼─────────┤    │
│  │ ...   │ ...  │ ...    │ ...         │ [✏️][🗑️] │    │
│  └───────┴──────┴────────┴─────────────┴─────────┘    │
└─────────────────────────────────────────────────────────┘
```

### Color Palette

#### Primary Colors
- **Background**: `#F3F4F6` (gray-200)
- **White Surfaces**: `#FFFFFF` (white)
- **Primary Action**: `#FBBF24` (yellow-400)
- **Primary Action Hover**: `#F59E0B` (yellow-500)

#### Role Badge Colors
| Role           | Background    | Text Color    | Border Color  |
|----------------|---------------|---------------|---------------|
| Administrator  | `#F3E8FF` (purple-100) | `#7C3AED` (purple-700) | `#E9D5FF` (purple-200) |
| Cashier        | `#D1FAE5` (green-100)  | `#047857` (green-700)  | `#A7F3D0` (green-200)  |
| Operator A     | `#DBEAFE` (blue-100)   | `#1D4ED8` (blue-700)   | `#BFDBFE` (blue-200)   |
| Operator B     | `#FEF3C7` (yellow-100) | `#A16207` (yellow-700) | `#FDE68A` (yellow-200) |

#### Status Colors
| Status  | Dot Color     | Badge Background | Badge Text    |
|---------|---------------|------------------|---------------|
| Online  | `#10B981` (green-500)  | `#D1FAE5` (green-100)  | `#047857` (green-700)  |
| Offline | `#9CA3AF` (gray-400)   | `#F3F4F6` (gray-100)   | `#374151` (gray-700)   |
| Away    | `#EAB308` (yellow-500) | `#FEF3C7` (yellow-100) | `#A16207` (yellow-700) |

#### Action Button Colors
| Action | Background    | Hover         | Text/Icon     |
|--------|---------------|---------------|---------------|
| Edit   | `#EFF6FF` (blue-50)  | `#DBEAFE` (blue-100)  | `#2563EB` (blue-600)  |
| Delete | `#FEF2F2` (red-50)   | `#FEE2E2` (red-100)   | `#DC2626` (red-600)   |

### Typography

#### Font Families
- **Default**: System font stack (from Tailwind defaults)

#### Font Sizes & Weights
| Element                  | Size      | Weight    | Color         |
|-------------------------|-----------|-----------|---------------|
| Page Title              | `1.5rem` (text-2xl) | `700` (font-bold) | `#1F2937` (gray-800) |
| Page Description        | `0.875rem` (text-sm) | `400` (normal) | `#6B7280` (gray-500) |
| Search Input            | `1rem` (text-base) | `400` (normal) | `#111827` (gray-900) |
| Stats Text (Normal)     | `0.875rem` (text-sm) | `400` (normal) | `#4B5563` (gray-600) |
| Stats Text (Bold)       | `0.875rem` (text-sm) | `600` (font-semibold) | `#111827` (gray-900) |
| Table Header            | `0.75rem` (text-xs) | `600` (font-semibold) | `#4B5563` (gray-600) |
| User Name               | `1rem` (text-base) | `500` (font-medium) | `#111827` (gray-900) |
| Role Badge              | `0.75rem` (text-xs) | `500` (font-medium) | varies by role |
| Status Badge            | `0.75rem` (text-xs) | `500` (font-medium) | varies by status |
| Last Active Text        | `0.875rem` (text-sm) | `400` (normal) | `#4B5563` (gray-600) |
| Modal Title             | `1.25rem` (text-xl) | `700` (font-bold) | `#1F2937` (gray-800) |
| Form Label              | `0.875rem` (text-sm) | `500` (font-medium) | `#374151` (gray-700) |
| Error Message           | `0.75rem` (text-xs) | `400` (normal) | `#EF4444` (red-500) |
| Button Text             | `1rem` (text-base) | `500` (font-medium) | varies by button |

### Spacing & Dimensions

#### Section Spacing
- **Outer container**: `space-y-6` (24px vertical gap between sections)
- **Header internal padding**: None (flex layout)
- **Search bar margin**: Included in `space-y-6`
- **Stats bar padding**: `px-6 py-3` (24px horizontal, 12px vertical)
- **Table container**: No padding (overflow container)

#### Button Dimensions
| Button              | Padding       | Size          |
|--------------------|---------------|---------------|
| Create Account     | `px-4 py-2`   | Auto width    |
| Edit Action        | `p-2`         | 16px icon     |
| Delete Action      | `p-2`         | 16px icon     |
| Modal Cancel       | `px-4 py-2`   | 50% width     |
| Modal Submit       | `px-4 py-2`   | 50% width     |
| Modal Close (X)    | `p-1`         | 20px icon     |

#### Form Elements
- **Input fields**: `px-3 py-2` (12px horizontal, 8px vertical)
- **Input height**: Auto (based on padding)
- **Form field spacing**: `space-y-5` (20px between fields)
- **Modal width**: `420px`
- **Modal max height**: `calc(100vh - 100px)`
- **Modal padding**: `p-6` (24px all sides)

#### Table Specifications
- **Cell padding**: `px-6 py-4` (24px horizontal, 16px vertical)
- **Avatar size**: `w-10 h-10` (40px × 40px)
- **Status indicator dot**: `w-3 h-3` (12px × 12px)
- **Status indicator position**: `bottom-0 right-0` (absolute positioning)
- **Badge icon size**: `12px`
- **Action icon size**: `16px`
- **Table max height**: `calc(100vh - 350px)` (with scrolling)

### Border Radius
- **Buttons**: `rounded-lg` (8px)
- **Input fields**: `rounded-lg` (8px)
- **Badges**: `rounded-full` (fully rounded)
- **Avatar**: `rounded-full` (circular)
- **Modal**: `rounded-xl` (12px)
- **Table container**: `rounded-lg` (8px)

### Shadows
- **Modal**: `shadow-2xl` (large, prominent shadow)
- **Buttons**: No shadow (flat design)
- **Cards**: No shadow (border-based design)

---

## COMPONENT BREAKDOWN

### 1. HEADER SECTION

#### Layout
```tsx
<div className="flex items-center justify-between">
  <div>
    <h1>Account Management</h1>
    <p>Manage user accounts and permissions</p>
  </div>
  <button>Create account</button>
</div>
```

#### Elements

**Title**
- Text: "Account Management"
- Classes: `text-2xl font-bold text-gray-800`

**Description**
- Text: "Manage user accounts and permissions"
- Classes: `text-sm text-gray-500 mt-1`

**Create Account Button**
- Position: Right-aligned in header
- Icon: Plus icon (18px) from Lucide React
- Text: "Create account"
- Colors:
  - Background: `bg-yellow-400`
  - Hover: `bg-yellow-500`
  - Text: `text-gray-900`
- Classes: `flex items-center gap-2 px-4 py-2 rounded-lg transition-colors font-medium`
- Behavior: Opens modal on click

---

### 2. SEARCH AND FILTER SECTION

#### Search Bar Structure
```tsx
<div className="relative">
  <Search icon (20px) at left-3 />
  <input type="text" placeholder="..." />
</div>
```

#### Search Bar Specifications
- **Icon**: Search icon from Lucide React
  - Size: 20px
  - Position: `absolute left-3 top-1/2 transform -translate-y-1/2`
  - Color: `text-gray-400`

- **Input Field**:
  - Width: `w-full`
  - Padding: `pl-10 pr-4 py-3` (40px left for icon)
  - Border: `border border-gray-300`
  - Radius: `rounded-lg`
  - Focus state:
    - Ring: `focus:ring-2 focus:ring-blue-500`
    - Border: `focus:border-transparent`
  - Placeholder: "Search by name, email, or role..."

#### Search Behavior
- Real-time filtering as user types
- Case-insensitive search
- Searches across: name, email, role fields
- Updates user count dynamically
- No debouncing (instant filter)

---

### 2.1 FILTER CONTROLS

#### Filter Bar Structure
```tsx
<div className="flex items-center gap-4 flex-wrap">
  <span>Filter by:</span>
  <!-- Role Filter -->
  <div className="flex items-center gap-2">
    <label>Role:</label>
    <select>...</select>
  </div>
  <!-- Status Filter -->
  <div className="flex items-center gap-2">
    <label>Status:</label>
    <select>...</select>
  </div>
  <!-- Clear Button (conditional) -->
  <button>Clear all filters</button>
</div>
```

#### Filter Section Specifications

**"Filter by:" Label**:
- Font size: `text-sm`
- Font weight: `font-medium`
- Color: `text-gray-700`

**Filter Group Container**:
- Layout: Flexbox with gap-2
- Alignment: Center

**Filter Labels**:
- Font size: `text-sm`
- Color: `text-gray-600`

**Dropdown Selects**:
- Padding: `px-3 py-1.5`
- Border: `border border-gray-300`
- Radius: `rounded-lg`
- Focus: `focus:ring-2 focus:ring-blue-500 focus:border-transparent`
- Outline: `outline-none`
- Font size: `text-sm`

#### Role Filter Options
```html
<option value="All">All Roles</option>
<option value="Administrator">Administrator</option>
<option value="Cashier">Cashier</option>
<option value="Operator A">Operator A</option>
<option value="Operator B">Operator B</option>
```

**Default**: "All"

#### Status Filter Options
```html
<option value="All">All Statuses</option>
<option value="Online">Online</option>
<option value="Offline">Offline</option>
<option value="Away">Away</option>
```

**Default**: "All"

#### Clear Filters Button

**Visibility Condition**:
```typescript
(roleFilter !== 'All' || statusFilter !== 'All' || searchQuery !== '')
```

**Styling**:
- Padding: `px-3 py-1.5`
- Font size: `text-sm`
- Color: `text-gray-600`
- Hover color: `hover:text-gray-900`
- Hover background: `hover:bg-gray-100`
- Radius: `rounded-lg`
- Transition: `transition-colors`

**Behavior**: 
Resets all filters when clicked:
```typescript
setRoleFilter('All');
setStatusFilter('All');
setSearchQuery('');
```

#### Combined Filter Logic

**Filter Algorithm**:
```typescript
const filteredUsers = users.filter(user => {
  // 1. Search filter (OR logic across multiple fields)
  const matchesSearch = searchQuery === '' || 
    user.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    user.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
    user.role.toLowerCase().includes(searchQuery.toLowerCase());
  
  // 2. Role filter (exact match or "All")
  const matchesRole = roleFilter === 'All' || user.role === roleFilter;
  
  // 3. Status filter (exact match or "All")
  const matchesStatus = statusFilter === 'All' || user.status === statusFilter;
  
  // 4. AND logic: ALL conditions must be true
  return matchesSearch && matchesRole && matchesStatus;
});
```

**Filter Priority**:
1. Search query (text matching)
2. Role filter (dropdown selection)
3. Status filter (dropdown selection)
4. All filters work together with AND logic

---

### 3. STATS BAR

#### Structure
```tsx
<div className="bg-white rounded-lg border border-gray-200 px-6 py-3">
  <div className="flex items-center justify-between flex-wrap gap-2">
    <p className="text-sm text-gray-600">
      Showing <span>{filteredUsers.length}</span> of <span>{users.length}</span> user{s}
    </p>
    
    {/* Active Filters Display (conditional) */}
    <div className="flex items-center gap-2">
      <span>Active filters:</span>
      {searchQuery && <span>Search: "{searchQuery}"</span>}
      {roleFilter !== 'All' && <span>Role: {roleFilter}</span>}
      {statusFilter !== 'All' && <span>Status: {statusFilter}</span>}
    </div>
  </div>
</div>
```

#### Specifications

**Container**:
- Background: `bg-white`
- Border: `border border-gray-200` (1px solid gray-200)
- Radius: `rounded-lg` (8px)
- Padding: `px-6 py-3` (24px horizontal, 12px vertical)

**Layout**:
- Display: Flex with justify-between
- Flex-wrap: Enabled for responsive
- Gap: 8px between elements

**User Count Display**:
- Font size: `text-sm` (14px)
- Color: `text-gray-600`
- Format: "Showing X of Y users"
- Numbers: `font-semibold text-gray-900`
- Pluralization: Automatic (adds 's' if count ≠ 1)

**Active Filters Display**:

*Visibility*:
```typescript
(roleFilter !== 'All' || statusFilter !== 'All' || searchQuery !== '')
```

*Layout*:
- Display: `flex items-center gap-2`
- Font size: `text-sm`
- Base color: `text-gray-600`

*Filter Badges*:

Search Badge:
- `bg-blue-100 text-blue-700`
- `px-2 py-1 rounded-md`
- Format: `Search: "{query}"`

Role Badge:
- `bg-purple-100 text-purple-700`
- `px-2 py-1 rounded-md`
- Format: `Role: {roleName}`

Status Badge:
- `bg-green-100 text-green-700`
- `px-2 py-1 rounded-md`
- Format: `Status: {statusName}`

#### Behavior
- Updates automatically based on search filter
- Shows total filtered results
- Always visible (even when 0 results)

---

### 4. USER TABLE

#### Structure
```tsx
<div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
  <div className="overflow-x-auto max-h-[calc(100vh-350px)] overflow-y-auto">
    <table className="w-full">
      <thead>...</thead>
      <tbody>...</tbody>
    </table>
  </div>
</div>
```

#### Table Headers
| Column      | Width      | Alignment | Text Transform |
|-------------|------------|-----------|----------------|
| User        | Auto       | Left      | UPPERCASE      |
| Role        | Auto       | Left      | UPPERCASE      |
| Status      | Auto       | Left      | UPPERCASE      |
| Last Active | Auto       | Left      | UPPERCASE      |
| Actions     | Auto       | Center    | UPPERCASE      |

**Header Styling**:
- Background: `bg-gray-50`
- Border: `border-b border-gray-200`
- Padding: `px-6 py-4`
- Text: `text-xs font-semibold text-gray-600 uppercase tracking-wider`

#### Table Rows

**Row Container**:
- Hover state: `hover:bg-gray-50 transition-colors`
- Divider: `divide-y divide-gray-200`
- Padding: `px-6 py-4` per cell

**User Cell**:
```tsx
<div className="flex items-center gap-3">
  <div className="relative">
    <img src={avatar} className="w-10 h-10 rounded-full" />
    <div className="status-dot" />
  </div>
  <div>
    <p className="font-medium text-gray-900">{name}</p>
  </div>
</div>
```

Components:
1. **Avatar**:
   - Size: 40px × 40px
   - Shape: Circular (`rounded-full`)
   - Source: `https://ui-avatars.com/api/?name={name}&background=random&size=128`
   
2. **Status Dot**:
   - Size: 12px × 12px (including border)
   - Position: Absolute bottom-right of avatar
   - Border: 2px white border
   - Colors: Green (online), Gray (offline), Yellow (away)
   
3. **Name**:
   - Weight: Medium (500)
   - Color: `text-gray-900`

**Role Cell**:
```tsx
<span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border">
  <Shield size={12} />
  {role}
</span>
```

Features:
- Shield icon (12px)
- Badge with role-specific colors
- Border and filled background
- Fully rounded corners

**Status Cell**:
```tsx
<span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium">
  <span className="w-1.5 h-1.5 rounded-full" />
  {status}
</span>
```

Features:
- Small dot indicator (6px)
- Status-specific colors
- Text label

**Last Active Cell**:
- Plain text display
- Color: `text-gray-600`
- Size: `text-sm`
- Examples: "Just now", "5 hours ago", "Never"

**Actions Cell**:
```tsx
<div className="flex items-center justify-center gap-2">
  <button className="edit-button">
    <Edit size={16} />
  </button>
  <button className="delete-button">
    <Trash2 size={16} />
  </button>
</div>
```

Edit Button:
- Background: `bg-blue-50`
- Hover: `bg-blue-100`
- Icon color: `text-blue-600`
- Icon size: 16px
- Padding: `p-2`
- Radius: `rounded-lg`
- Tooltip: "Edit user"

Delete Button:
- Background: `bg-red-50`
- Hover: `bg-red-100`
- Icon color: `text-red-600`
- Icon size: 16px
- Padding: `p-2`
- Radius: `rounded-lg`
- Tooltip: "Delete user"

#### Empty State
```tsx
<tr>
  <td colSpan={5} className="px-6 py-12 text-center">
    <p className="text-gray-500 text-lg">No users found matching "{query}"</p>
  </td>
</tr>
```

Specifications:
- Spans all 5 columns
- Centered text
- Large padding (48px vertical)
- Displays search query in message

---

### 5. CREATE ACCOUNT MODAL

#### Modal Structure
```
┌──────────────────────────────────────┐
│  Create New Account           [X]    │
├──────────────────────────────────────┤
│                                      │
│  Name *                              │
│  [input field]                       │
│                                      │
│  Username *                          │
│  [input field]                       │
│                                      │
│  Role *                              │
│  [dropdown: Administrator/           │
│   Cashier/Operator A/Operator B]     │
│                                      │
│  Password *                          │
│  [input field]              [👁️]    │
│                                      │
│  Confirm Password *                  │
│  [input field]              [👁️]    │
│                                      │
│  [Cancel]    [Create Account]        │
│                                      │
└──────────────────────────────────────┘
```

#### Modal Container
- Position: `fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2`
- Width: `420px`
- Max height: `calc(100vh - 100px)`
- Background: White
- Border: `1px solid #D1D5DB` (gray-300)
- Radius: `rounded-xl` (12px)
- Shadow: `shadow-2xl`
- Z-index: `z-50`
- Animation: `animate-slideIn`

#### Modal Header
- Layout: Flexbox (space between title and close button)
- Padding: `p-6` (24px)
- Border: `border-b border-gray-200`

Elements:
1. **Title**:
   - Text: "Create New Account"
   - Classes: `text-xl font-bold text-gray-800`
   
2. **Close Button**:
   - Icon: X from Lucide (20px)
   - Padding: `p-1`
   - Hover: `hover:bg-gray-100`
   - Radius: `rounded-lg`
   - Icon color: `text-gray-500`

#### Modal Body (Form)

**Form Container**:
- Padding: `p-6` (24px)
- Field spacing: `space-y-5` (20px between fields)
- Event: `onSubmit={handleCreateAccount}`

**Form Fields** (5 fields):

1. **Name Field**:
   ```tsx
   <div>
     <label htmlFor="name">
       Name <span className="text-red-500">*</span>
     </label>
     <input type="text" id="name" placeholder="Enter name" />
     {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
   </div>
   ```

2. **Username Field**:
   ```tsx
   <div>
     <label htmlFor="username">
       Username <span className="text-red-500">*</span>
     </label>
     <input type="text" id="username" placeholder="Enter username" />
     {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
   </div>
   ```

3. **Role Field**:
   ```tsx
   <div>
     <label htmlFor="role">
       Role <span className="text-red-500">*</span>
     </label>
     <select id="role" value={formData.role} onChange={...}>
       <option value="Administrator">Administrator</option>
       <option value="Cashier">Cashier</option>
       <option value="Operator A">Operator A</option>
       <option value="Operator B">Operator B</option>
     </select>
     {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
   </div>
   ```
   
   **Role Options**:
   - **Administrator**: Full system access and user management
   - **Cashier**: Handles transactions and cash operations
   - **Operator A**: Controls betting operations (primary operator interface)
   - **Operator B**: Controls betting operations (secondary operator interface)
   
   **Default Selection**: Cashier (when creating new account)

4. **Password Field**:
   ```tsx
   <div>
     <label htmlFor="password">
       Password <span className="text-red-500">*</span>
     </label>
     <div className="relative">
       <input type={showPassword ? 'text' : 'password'} />
       <button type="button" className="toggle-visibility">
         {showPassword ? <EyeOff /> : <Eye />}
       </button>
     </div>
     {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
   </div>
   ```

5. **Confirm Password Field**:
   ```tsx
   <div>
     <label htmlFor="confirmPassword">
       Confirm Password <span className="text-red-500">*</span>
     </label>
     <div className="relative">
       <input type={showConfirmPassword ? 'text' : 'password'} />
       <button type="button" className="toggle-visibility">
         {showConfirmPassword ? <EyeOff /> : <Eye />}
       </button>
     </div>
     {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
   </div>
   ```

**Label Specifications**:
- Classes: `block text-sm font-medium text-gray-700 mb-1`
- Required indicator: Red asterisk

**Input Specifications**:
- Width: `w-full`
- Padding: `px-3 py-2`
- Border: `border border-gray-300` (normal) or `border-red-500` (error)
- Radius: `rounded-lg`
- Focus: `focus:ring-2 focus:ring-blue-500 focus:border-transparent`
- Outline: `outline-none`

**Select/Dropdown Specifications** (Role field):
- Width: `w-full`
- Padding: `px-3 py-2`
- Border: `border border-gray-300` (normal) or `border-red-500` (error)
- Radius: `rounded-lg`
- Focus: `focus:ring-2 focus:ring-blue-500 focus:border-transparent`
- Outline: `outline-none`
- Options: 4 role choices (Administrator, Cashier, Operator A, Operator B)

**Password Toggle Button**:
- Position: `absolute right-3 top-1/2 transform -translate-y-1/2`
- Icon size: 18px
- Color: `text-gray-400` (normal), `text-gray-600` (hover)
- Icons: Eye (show) or EyeOff (hide)

**Error Message**:
- Color: `text-red-500`
- Size: `text-xs`
- Margin: `mt-1` (4px top)

#### Form Actions
```tsx
<div className="flex gap-3 pt-4">
  <button type="button" onClick={handleCloseModal}>
    Cancel
  </button>
  <button type="submit">
    Create Account
  </button>
</div>
```

**Cancel Button**:
- Flex: `flex-1` (50% width)
- Padding: `px-4 py-2`
- Border: `border border-gray-300`
- Text: `text-gray-700`
- Radius: `rounded-lg`
- Hover: `hover:bg-gray-50`
- Weight: `font-medium`

**Create Account Button**:
- Flex: `flex-1` (50% width)
- Padding: `px-4 py-2`
- Background: `bg-yellow-400`
- Hover: `bg-yellow-500`
- Text: `text-gray-900`
- Radius: `rounded-lg`
- Weight: `font-medium`

---

### 6. EDIT ACCOUNT MODAL

#### Modal Structure
Identical to Create Account Modal with following differences:

**Header**:
- Title: "Edit Account" (instead of "Create New Account")

**Form Fields**:
- Pre-filled with existing user data
- Username derived from user's name (lowercase, underscores)
- Password placeholder: "Enter new password"
- Confirm password placeholder: "Confirm new password"

**Submit Button**:
- Text: "Update Account"
- Background: `bg-blue-500` (instead of yellow)
- Hover: `bg-blue-600`
- Text: `text-white`

**Field IDs**:
- Prefixed with "edit-" to avoid conflicts:
  - `edit-name`
  - `edit-username`
  - `edit-password`
  - `edit-confirmPassword`

#### Behavior Differences
- Pre-populates form with user data
- Uses `handleUpdateAccount` instead of `handleCreateAccount`
- Closes via `handleCloseEditModal`

---

## DATABASE SCHEMA & INTEGRATION

### Current Implementation (Mock Data)

#### UserAccount Interface
```typescript
interface UserAccount {
  id: number;
  name: string;
  email: string;
  phone: string;
  role: 'Administrator' | 'Cashier' | 'Operator A' | 'Operator B';
  status: 'Online' | 'Offline' | 'Away';
  avatar: string;
  lastActive: string;
}
```

**Role Definitions**:
- **Administrator**: Full system access, can manage all users and settings
- **Cashier**: Handles cash transactions and cashier operations  
- **Operator A**: Primary betting operator interface access
- **Operator B**: Secondary betting operator interface access

#### Mock Data Generation
- Converts cashier data to user accounts
- Generates 20 users by default
- Auto-generates:
  - Email: `{firstname}.{lastname}@sabong.com`
  - Phone: Random 10-digit format
  - Avatar: UI Avatars API URL
  - Status: Based on online status
  - Last active: Random timestamps

### PostgreSQL Schema (Migration Target)

#### Table: `users`

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  phone VARCHAR(20),
  role VARCHAR(20) NOT NULL DEFAULT 'Cashier',
  status VARCHAR(20) NOT NULL DEFAULT 'Offline',
  avatar_url TEXT,
  last_active TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  CONSTRAINT valid_role CHECK (role IN ('Administrator', 'Cashier', 'Operator A', 'Operator B')),
  CONSTRAINT valid_status CHECK (status IN ('Online', 'Offline', 'Away'))
);

-- Indexes for performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_users_name ON users(name);

-- Updated timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
```

#### Table: `user_sessions`

```sql
CREATE TABLE user_sessions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  session_token VARCHAR(255) UNIQUE NOT NULL,
  ip_address VARCHAR(45),
  user_agent TEXT,
  login_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  logout_at TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE
);

-- Index for active session lookups
CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_sessions_token ON user_sessions(session_token);
CREATE INDEX idx_sessions_active ON user_sessions(is_active);
```

#### Table: `user_activity_log`

```sql
CREATE TABLE user_activity_log (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  action VARCHAR(50) NOT NULL,
  details JSONB,
  ip_address VARCHAR(45),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for activity queries
CREATE INDEX idx_activity_user_id ON user_activity_log(user_id);
CREATE INDEX idx_activity_timestamp ON user_activity_log(timestamp);
CREATE INDEX idx_activity_action ON user_activity_log(action);
```

### Database Operations

#### CREATE User
```sql
INSERT INTO users (
  username,
  password_hash,
  name,
  email,
  phone,
  role,
  status,
  avatar_url,
  last_active
) VALUES (
  $1,  -- username
  $2,  -- password_hash (bcrypt)
  $3,  -- name
  $4,  -- email
  $5,  -- phone
  'Cashier',
  'Offline',
  $6,  -- avatar_url
  NULL
) RETURNING *;
```

**Steps**:
1. Validate input data
2. Hash password using bcrypt (salt rounds: 10)
3. Generate email from name
4. Generate random phone number
5. Create avatar URL
6. Insert into database
7. Log activity (action: 'user_created')
8. Return new user object

#### READ Users (List with Search)
```sql
SELECT 
  id,
  username,
  name,
  email,
  phone,
  role,
  status,
  avatar_url,
  last_active,
  created_at,
  updated_at
FROM users
WHERE 
  (LOWER(name) LIKE LOWER($1) OR
   LOWER(email) LIKE LOWER($1) OR
   LOWER(role) LIKE LOWER($1))
ORDER BY created_at DESC;
```

**Parameters**:
- `$1`: Search query (wrapped with `%{query}%`)

#### UPDATE User
```sql
UPDATE users
SET
  username = $2,
  password_hash = $3,  -- Only if password changed
  name = $4,
  email = $5,
  updated_at = CURRENT_TIMESTAMP
WHERE id = $1
RETURNING *;
```

**Steps**:
1. Validate input data
2. If password provided, hash with bcrypt
3. Regenerate email from new name
4. Update avatar URL with new name
5. Execute update query
6. Log activity (action: 'user_updated')
7. Return updated user object

#### DELETE User
```sql
-- First, check if user exists and get details for logging
SELECT name FROM users WHERE id = $1;

-- Delete user (cascades to sessions and activity log)
DELETE FROM users WHERE id = $1 RETURNING *;
```

**Steps**:
1. Confirm deletion with user
2. Retrieve user details for logging
3. Execute delete (cascades to related tables)
4. Log activity (action: 'user_deleted')
5. Update UI state

#### UPDATE Status (Real-time)
```sql
UPDATE users
SET 
  status = $2,
  last_active = CURRENT_TIMESTAMP
WHERE id = $1;
```

**Trigger Events**:
- Login: Set status to 'Online'
- Logout: Set status to 'Offline'
- Idle (5 min): Set status to 'Away'
- Activity: Update last_active timestamp

---

## USER INTERACTIONS & BEHAVIORS

### 0. SEARCH AND FILTER INTERACTIONS

#### Search Interaction
**User Action**: Types in search box

**System Response**:
1. Captures input on every keystroke
2. Applies filter immediately (no delay)
3. Updates filtered user list
4. Updates count display
5. Shows/hides "Clear all filters" button
6. Displays search query in active filters badges

**Real-time Feedback**:
- User count changes: "Showing X of Y users"
- If no results: "No users found matching '{query}'"
- Active filter badge shows: "Search: '{query}'"

#### Role Filter Interaction
**User Action**: Selects role from dropdown

**System Response**:
1. Updates roleFilter state
2. Applies combined filter (search + role + status)
3. Updates user list and count
4. Shows active filter badge: "Role: {selected role}"
5. Shows "Clear all filters" button

**Filter Options**:
- All Roles (default - shows all)
- Administrator
- Cashier
- Operator A
- Operator B

#### Status Filter Interaction
**User Action**: Selects status from dropdown

**System Response**:
1. Updates statusFilter state
2. Applies combined filter (search + role + status)
3. Updates user list and count
4. Shows active filter badge: "Status: {selected status}"
5. Shows "Clear all filters" button

**Filter Options**:
- All Statuses (default - shows all)
- Online
- Offline
- Away

#### Clear All Filters Interaction
**User Action**: Clicks "Clear all filters" button

**System Response**:
1. Resets searchQuery to empty string
2. Resets roleFilter to 'All'
3. Resets statusFilter to 'All'
4. Shows all users (no filters)
5. Hides "Clear all filters" button
6. Removes all active filter badges
7. Updates count: "Showing {total} of {total} users"

**Button Visibility**:
- Only visible when at least one filter is active
- Disappears when all filters are cleared

#### Combined Filter Behavior

**Multi-Filter Example**:
```
Initial state: 20 users
↓
User types "John" in search
→ Shows 3 users named John
↓
User selects "Cashier" role
→ Shows 2 users (John who are Cashiers)
↓
User selects "Online" status
→ Shows 1 user (John who is a Cashier and Online)
```

**Filter Logic (AND operation)**:
```typescript
Show user IF:
  (matches search OR search is empty) AND
  (matches role OR role is "All") AND
  (matches status OR status is "All")
```

**Active Filters Display**:
- Shows all active filters as colored badges
- Each badge is individually colored
- Badge count can be 0 to 3
- Positioned in stats bar for visibility

#### Empty Results Behavior

**When No Users Match**:
- Table shows: "No users found matching '{searchQuery}'"
- Count shows: "Showing 0 of {total} users"
- Active filters still visible
- "Clear all filters" button available
- Suggestion: Clear filters to see all users

---

### 1. CREATE ACCOUNT FLOW

#### User Journey
1. User clicks "Create account" button in header
2. Modal slides in with animation (centered on screen)
3. User fills out form fields:
   - Name (required)
   - Username (required)
   - Password (required)
   - Confirm password (required)
4. Real-time validation shows errors under fields
5. User can toggle password visibility with eye icon
6. User submits form or cancels

#### Success Path
```
Click "Create account"
  ↓
Modal opens
  ↓
Fill form fields
  ↓
Validation passes
  ↓
Click "Create Account"
  ↓
[Database INSERT]
  ↓
New user appears in table
  ↓
Modal closes
  ↓
Form resets
  ↓
Success notification (if implemented)
```

#### Error Path
```
Fill form with invalid data
  ↓
Click "Create Account"
  ↓
Validation fails
  ↓
Error messages appear under fields
  ↓
Red border on invalid inputs
  ↓
User corrects errors
  ↓
Resubmit
```

#### Cancel Path
```
Click "Cancel" or "X"
  ↓
Modal closes
  ↓
Form data cleared
  ↓
Error messages cleared
  ↓
Password visibility reset
```

### 2. SEARCH FLOW

#### User Journey
1. User clicks in search bar
2. User types search query
3. Results filter in real-time
4. User count updates dynamically
5. Table shows filtered results
6. Empty state if no matches

#### Behavior Details
- **Debouncing**: None (instant filtering)
- **Case sensitivity**: Case-insensitive
- **Search fields**: name, email, role
- **Matching**: Partial match (contains)
- **Empty search**: Shows all users

#### Search Examples
| Query    | Matches                                      |
|----------|----------------------------------------------|
| "john"   | John Doe, Johnny Smith, john@sabong.com      |
| "admin"  | All users with Admin role                    |
| "@"      | All users (email always contains @)          |
| "xyz"    | Empty state if no matches                    |

### 3. EDIT USER FLOW

#### User Journey
1. User clicks Edit button (pencil icon) on table row
2. Edit modal opens with pre-filled data
3. User modifies fields
4. User submits or cancels

#### Success Path
```
Click Edit button
  ↓
Modal opens with user data
  ↓
Modify fields
  ↓
Validation passes
  ↓
Click "Update Account"
  ↓
[Database UPDATE]
  ↓
Table row updates
  ↓
Modal closes
  ↓
Form resets
```

#### Pre-filled Data
- **Name**: User's current name
- **Username**: Derived from name (lowercase, underscores)
- **Password**: Empty (requires new password)
- **Confirm Password**: Empty

#### Update Behavior
- Updates name in database
- Regenerates email based on new name
- Updates avatar URL with new name
- Requires password to be re-entered
- Validates password match

### 4. DELETE USER FLOW

#### User Journey
1. User clicks Delete button (trash icon) on table row
2. Browser confirmation dialog appears
3. User confirms or cancels

#### Confirmation Dialog
- **Message**: `Are you sure you want to delete user "{name}"? This action cannot be undone.`
- **Buttons**: OK (delete) or Cancel

#### Success Path
```
Click Delete button
  ↓
Confirmation dialog
  ↓
User confirms
  ↓
[Database DELETE]
  ↓
User removed from table
  ↓
User count updates
  ↓
Success notification (if implemented)
```

#### Cancel Path
```
Click Delete button
  ↓
Confirmation dialog
  ↓
User cancels
  ↓
No action taken
  ↓
Dialog closes
```

### 5. PASSWORD VISIBILITY TOGGLE

#### Behavior
- **Default state**: Hidden (type="password")
- **Icon**: Eye (hidden) or EyeOff (visible)
- **Click**: Toggles between text and password type
- **Independent**: Each field (password, confirm) toggles separately
- **Reset**: Returns to hidden when modal closes

### 6. RESPONSIVE TABLE SCROLLING

#### Horizontal Scrolling
- Activates when table width exceeds container
- Scrollbar appears at bottom
- All columns remain accessible

#### Vertical Scrolling
- Max height: `calc(100vh - 350px)`
- Scrollbar appears when content exceeds height
- Header remains fixed (sticky not implemented in current version)
- Smooth scrolling behavior

---

## FUNCTIONS & LOGIC

### State Management

#### Component State
```typescript
const [users, setUsers] = useState<UserAccount[]>([]);
const [searchQuery, setSearchQuery] = useState('');
const [roleFilter, setRoleFilter] = useState<UserAccount['role'] | 'All'>('All');
const [statusFilter, setStatusFilter] = useState<UserAccount['status'] | 'All'>('All');
const [showCreateModal, setShowCreateModal] = useState(false);
const [showEditModal, setShowEditModal] = useState(false);
const [showPassword, setShowPassword] = useState(false);
const [showConfirmPassword, setShowConfirmPassword] = useState(false);
const [editingUserId, setEditingUserId] = useState<number | null>(null);

const [formData, setFormData] = useState({
  username: '',
  password: '',
  confirmPassword: '',
  name: '',
  role: 'Cashier' as UserAccount['role'],
});

const [formErrors, setFormErrors] = useState({
  username: '',
  password: '',
  confirmPassword: '',
  name: '',
  role: '',
});
```

### Core Functions

#### 1. `generateUsersFromCashiers()`
**Purpose**: Convert cashier data to user accounts

**Returns**: `UserAccount[]`

**Logic**:
```typescript
const generateUsersFromCashiers = (): UserAccount[] => {
  const cashiers = generateMockCashiers();
  
  return cashiers.map(cashier => ({
    id: cashier.id,
    name: cashier.name,
    email: generateEmail(cashier.name),
    phone: generatePhone(),
    role: 'Cashier',
    status: cashier.isOnline ? 'Online' : 'Offline',
    avatar: `https://ui-avatars.com/api/?name=${encodeURIComponent(cashier.name)}&background=random&size=128`,
    lastActive: cashier.isOnline ? 'Just now' : `${Math.floor(Math.random() * 24)} hours ago`,
  }));
};
```

**PostgreSQL Equivalent**:
```sql
SELECT * FROM users ORDER BY created_at DESC;
```

---

#### 2. `filteredUsers` (Computed)
**Purpose**: Filter users based on search query

**Logic**:
```typescript
const filteredUsers = users.filter(user =>
  user.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
  user.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
  user.role.toLowerCase().includes(searchQuery.toLowerCase())
);
```

**PostgreSQL Equivalent**:
```sql
SELECT * FROM users
WHERE 
  LOWER(name) LIKE '%' || LOWER($1) || '%' OR
  LOWER(email) LIKE '%' || LOWER($1) || '%' OR
  LOWER(role) LIKE '%' || LOWER($1) || '%';
```

---

#### 3. `getRoleBadgeColor(role)`
**Purpose**: Return Tailwind classes for role badge styling

**Parameters**:
- `role`: UserAccount['role']

**Returns**: `string` (Tailwind classes)

**Logic**:
```typescript
const getRoleBadgeColor = (role: UserAccount['role']) => {
  switch (role) {
    case 'Admin':
      return 'bg-purple-100 text-purple-700 border-purple-200';
    case 'Manager':
      return 'bg-blue-100 text-blue-700 border-blue-200';
    case 'Cashier':
      return 'bg-green-100 text-green-700 border-green-200';
    case 'Operator':
      return 'bg-yellow-100 text-yellow-700 border-yellow-200';
    case 'Viewer':
      return 'bg-gray-100 text-gray-700 border-gray-200';
    default:
      return 'bg-gray-100 text-gray-700 border-gray-200';
  }
};
```

---

#### 4. `getStatusColor(status)`
**Purpose**: Return color class for status indicator dot

**Parameters**:
- `status`: UserAccount['status']

**Returns**: `string` (Tailwind color class)

**Logic**:
```typescript
const getStatusColor = (status: UserAccount['status']) => {
  switch (status) {
    case 'Online':
      return 'bg-green-500';
    case 'Offline':
      return 'bg-gray-400';
    case 'Away':
      return 'bg-yellow-500';
    default:
      return 'bg-gray-400';
  }
};
```

---

#### 5. `getStatusBadge(status)`
**Purpose**: Return classes for status badge background and text

**Parameters**:
- `status`: UserAccount['status']

**Returns**: `string` (Tailwind classes)

**Logic**:
```typescript
const getStatusBadge = (status: UserAccount['status']) => {
  switch (status) {
    case 'Online':
      return 'bg-green-100 text-green-700';
    case 'Offline':
      return 'bg-gray-100 text-gray-700';
    case 'Away':
      return 'bg-yellow-100 text-yellow-700';
    default:
      return 'bg-gray-100 text-gray-700';
  }
};
```

---

#### 6. `validateForm()`
**Purpose**: Validate all form fields and set error messages

**Returns**: `boolean` (true if valid, false if errors)

**Validation Rules**:

1. **Username**:
   - Required: Cannot be empty
   - Min length: 3 characters
   - Pattern: Only letters, numbers, and underscores
   - Regex: `/^[a-zA-Z0-9_]+$/`

2. **Name**:
   - Required: Cannot be empty
   - Min length: 2 characters

3. **Password**:
   - Required: Cannot be empty
   - Min length: 6 characters

4. **Confirm Password**:
   - Required: Cannot be empty
   - Must match: Must equal password field

**Logic**:
```typescript
const validateForm = () => {
  const errors = {
    username: '',
    password: '',
    confirmPassword: '',
    name: '',
  };

  let isValid = true;

  // Validate username
  if (!formData.username.trim()) {
    errors.username = 'Username is required';
    isValid = false;
  } else if (formData.username.length < 3) {
    errors.username = 'Username must be at least 3 characters';
    isValid = false;
  } else if (!/^[a-zA-Z0-9_]+$/.test(formData.username)) {
    errors.username = 'Username can only contain letters, numbers, and underscores';
    isValid = false;
  }

  // Validate name
  if (!formData.name.trim()) {
    errors.name = 'Name is required';
    isValid = false;
  } else if (formData.name.length < 2) {
    errors.name = 'Name must be at least 2 characters';
    isValid = false;
  }

  // Validate password
  if (!formData.password) {
    errors.password = 'Password is required';
    isValid = false;
  } else if (formData.password.length < 6) {
    errors.password = 'Password must be at least 6 characters';
    isValid = false;
  }

  // Validate confirm password
  if (!formData.confirmPassword) {
    errors.confirmPassword = 'Please confirm your password';
    isValid = false;
  } else if (formData.password !== formData.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match';
    isValid = false;
  }

  setFormErrors(errors);
  return isValid;
};
```

**Error Display**:
- Appears below each field
- Red text (`text-red-500`)
- Small size (`text-xs`)
- Input border turns red when error present

---

#### 7. `handleCreateAccount(e)`
**Purpose**: Process new account creation form submission

**Parameters**:
- `e`: React.FormEvent

**Behavior**:
1. Prevent default form submission
2. Validate form data
3. If invalid, stop and show errors
4. Create new user object
5. Add to users array
6. Reset form and close modal

**Logic**:
```typescript
const handleCreateAccount = (e: React.FormEvent) => {
  e.preventDefault();

  if (!validateForm()) {
    return;
  }

  const newUser: UserAccount = {
    id: users.length + 1,
    name: formData.name,
    email: generateEmail(formData.name),
    phone: generatePhone(),
    role: formData.role,
    status: 'Offline',
    avatar: `https://ui-avatars.com/api/?name=${encodeURIComponent(formData.name)}&background=random&size=128`,
    lastActive: 'Never',
  };

  setUsers([...users, newUser]);
  
  setFormData({
    username: '',
    password: '',
    confirmPassword: '',
    name: '',
    role: 'Cashier',
  });
  setFormErrors({
    username: '',
    password: '',
    confirmPassword: '',
    name: '',
    role: '',
  });
  setShowCreateModal(false);
};
```

**PostgreSQL Implementation**:
```typescript
const handleCreateAccount = async (e: React.FormEvent) => {
  e.preventDefault();

  if (!validateForm()) {
    return;
  }

  try {
    // Hash password
    const passwordHash = await bcrypt.hash(formData.password, 10);

    // Generate email and avatar
    const email = generateEmail(formData.name);
    const phone = generatePhone();
    const avatarUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(formData.name)}&background=random&size=128`;

    // Insert into database
    const result = await pool.query(
      `INSERT INTO users (username, password_hash, name, email, phone, role, status, avatar_url)
       VALUES ($1, $2, $3, $4, $5, 'Cashier', 'Offline', $6)
       RETURNING *`,
      [formData.username, passwordHash, formData.name, email, phone, avatarUrl]
    );

    // Log activity
    await pool.query(
      `INSERT INTO user_activity_log (user_id, action, details)
       VALUES ($1, 'user_created', $2)`,
      [result.rows[0].id, JSON.stringify({ created_by: currentUserId })]
    );

    // Fetch updated user list
    await fetchUsers();
    
    // Reset and close
    resetForm();
    setShowCreateModal(false);
    
    // Show success notification
    showNotification('User created successfully', 'success');
  } catch (error) {
    console.error('Error creating user:', error);
    showNotification('Failed to create user', 'error');
  }
};
```

---

#### 8. `handleCloseModal()`
**Purpose**: Close create modal and reset form state

**Logic**:
```typescript
const handleCloseModal = () => {
  setShowCreateModal(false);
  setFormData({
    username: '',
    password: '',
    confirmPassword: '',
    name: '',
  });
  setFormErrors({
    username: '',
    password: '',
    confirmPassword: '',
    name: '',
  });
  setShowPassword(false);
  setShowConfirmPassword(false);
};
```

**Behavior**:
- Closes modal
- Clears all form fields
- Clears all error messages
- Resets password visibility toggles

---

#### 9. `handleEditUser(user)`
**Purpose**: Open edit modal and populate with user data

**Parameters**:
- `user`: UserAccount

**Logic**:
```typescript
const handleEditUser = (user: UserAccount) => {
  setEditingUserId(user.id);
  setFormData({
    username: user.name.toLowerCase().replace(/\s+/g, '_'),
    password: '',
    confirmPassword: '',
    name: user.name,
  });
  setShowEditModal(true);
};
```

**Behavior**:
- Stores user ID being edited
- Pre-fills name field
- Generates username from name
- Leaves passwords empty (requires re-entry)
- Opens edit modal

---

#### 10. `handleUpdateAccount(e)`
**Purpose**: Process account update form submission

**Parameters**:
- `e`: React.FormEvent

**Logic**:
```typescript
const handleUpdateAccount = (e: React.FormEvent) => {
  e.preventDefault();

  if (!validateForm()) {
    return;
  }

  setUsers(users.map(user => 
    user.id === editingUserId 
      ? {
          ...user,
          name: formData.name,
          email: generateEmail(formData.name),
          avatar: `https://ui-avatars.com/api/?name=${encodeURIComponent(formData.name)}&background=random&size=128`,
          role: formData.role,
        }
      : user
  ));
  
  setFormData({
    username: '',
    password: '',
    confirmPassword: '',
    name: '',
    role: 'Cashier',
  });
  setFormErrors({
    username: '',
    password: '',
    confirmPassword: '',
    name: '',
    role: '',
  });
  setShowEditModal(false);
  setEditingUserId(null);
};
```

**Updated Fields**:
- Name
- Email (regenerated from name)
- Avatar (regenerated from name)
- Role (selected from dropdown)

**Not Updated** (in current implementation):
- Username (can be modified but not recommended)
- Password (requires new password entry and hashing)
- Status (managed by system)

**PostgreSQL Implementation**:
```typescript
const handleUpdateAccount = async (e: React.FormEvent) => {
  e.preventDefault();

  if (!validateForm()) {
    return;
  }

  try {
    const email = generateEmail(formData.name);
    const avatarUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(formData.name)}&background=random&size=128`;
    
    let query = `UPDATE users SET name = $2, email = $3, avatar_url = $4, username = $5`;
    let params = [editingUserId, formData.name, email, avatarUrl, formData.username];
    
    // If password was changed
    if (formData.password) {
      const passwordHash = await bcrypt.hash(formData.password, 10);
      query += `, password_hash = $6`;
      params.push(passwordHash);
    }
    
    query += ` WHERE id = $1 RETURNING *`;
    
    const result = await pool.query(query, params);

    // Log activity
    await pool.query(
      `INSERT INTO user_activity_log (user_id, action, details)
       VALUES ($1, 'user_updated', $2)`,
      [editingUserId, JSON.stringify({ updated_by: currentUserId, fields: ['name', 'email'] })]
    );

    // Refresh user list
    await fetchUsers();
    
    // Reset and close
    resetForm();
    setShowEditModal(false);
    setEditingUserId(null);
    
    showNotification('User updated successfully', 'success');
  } catch (error) {
    console.error('Error updating user:', error);
    showNotification('Failed to update user', 'error');
  }
};
```

---

#### 11. `handleCloseEditModal()`
**Purpose**: Close edit modal and reset form state

**Logic**:
```typescript
const handleCloseEditModal = () => {
  setShowEditModal(false);
  setEditingUserId(null);
  setFormData({
    username: '',
    password: '',
    confirmPassword: '',
    name: '',
  });
  setFormErrors({
    username: '',
    password: '',
    confirmPassword: '',
    name: '',
  });
  setShowPassword(false);
  setShowConfirmPassword(false);
};
```

**Behavior**:
- Closes modal
- Clears editing user ID
- Resets all form fields
- Clears error messages
- Resets password visibility

---

#### 12. `handleDeleteUser(userId, userName)`
**Purpose**: Delete user after confirmation

**Parameters**:
- `userId`: number
- `userName`: string

**Logic**:
```typescript
const handleDeleteUser = (userId: number, userName: string) => {
  if (window.confirm(`Are you sure you want to delete user "${userName}"? This action cannot be undone.`)) {
    setUsers(users.filter(user => user.id !== userId));
  }
};
```

**Behavior**:
1. Show browser confirmation dialog
2. If confirmed, filter out user from array
3. If cancelled, no action

**PostgreSQL Implementation**:
```typescript
const handleDeleteUser = async (userId: number, userName: string) => {
  if (window.confirm(`Are you sure you want to delete user "${userName}"? This action cannot be undone.`)) {
    try {
      // Log activity before deletion
      await pool.query(
        `INSERT INTO user_activity_log (user_id, action, details)
         VALUES ($1, 'user_deleted', $2)`,
        [userId, JSON.stringify({ deleted_by: currentUserId, user_name: userName })]
      );

      // Delete user (cascades to sessions and activity log)
      await pool.query('DELETE FROM users WHERE id = $1', [userId]);

      // Refresh user list
      await fetchUsers();
      
      showNotification('User deleted successfully', 'success');
    } catch (error) {
      console.error('Error deleting user:', error);
      showNotification('Failed to delete user', 'error');
    }
  }
};
```

---

## VALIDATION RULES

### Field-Level Validation

#### Username
| Rule | Validation | Error Message |
|------|-----------|---------------|
| Required | `!formData.username.trim()` | "Username is required" |
| Min Length | `formData.username.length < 3` | "Username must be at least 3 characters" |
| Pattern | `!/^[a-zA-Z0-9_]+$/.test(formData.username)` | "Username can only contain letters, numbers, and underscores" |

**Valid Examples**:
- `john_doe`
- `user123`
- `admin_user`
- `cashier_01`

**Invalid Examples**:
- `ab` (too short)
- `john doe` (space not allowed)
- `user@123` (@ not allowed)
- `` (empty)

---

#### Name
| Rule | Validation | Error Message |
|------|-----------|---------------|
| Required | `!formData.name.trim()` | "Name is required" |
| Min Length | `formData.name.length < 2` | "Name must be at least 2 characters" |

**Valid Examples**:
- `John Doe`
- `Maria Santos`
- `李明` (Chinese characters)
- `O'Brien` (apostrophes allowed)

**Invalid Examples**:
- `J` (too short)
- `` (empty)
- `   ` (whitespace only)

---

#### Password
| Rule | Validation | Error Message |
|------|-----------|---------------|
| Required | `!formData.password` | "Password is required" |
| Min Length | `formData.password.length < 6` | "Password must be at least 6 characters" |

**Valid Examples**:
- `password123`
- `abc123`
- `P@ssw0rd!`
- `123456`

**Invalid Examples**:
- `12345` (too short)
- `` (empty)

**Security Note**: 
- Current implementation only validates length
- Production should require:
  - Mixed case
  - Numbers
  - Special characters
  - Min length of 8-12 characters

---

#### Role
| Rule | Validation | Error Message |
|------|-----------|---------------|
| Required | Role must be selected (always has default value) | N/A - Always valid |

**Valid Options**:
- `Administrator`
- `Cashier` (default)
- `Operator A`
- `Operator B`

**Behavior**:
- Dropdown always has a selected value
- Defaults to "Cashier" for new accounts
- Pre-selected to user's current role when editing
- No validation errors possible (always valid selection)

**Role Descriptions**:
- **Administrator**: Full system access, user management capabilities
- **Cashier**: Cash transaction and cashier overview access
- **Operator A**: Primary betting operator interface
- **Operator B**: Secondary betting operator interface

---

#### Confirm Password
| Rule | Validation | Error Message |
|------|-----------|---------------|
| Required | `!formData.confirmPassword` | "Please confirm your password" |
| Match | `formData.password !== formData.confirmPassword` | "Passwords do not match" |

**Behavior**:
- Validates only after both fields have input
- Case-sensitive comparison
- Exact match required

---

### Form-Level Validation

#### Validation Timing
- **On submit**: Always validates before processing
- **On change**: No real-time validation (validates on submit only)
- **On blur**: Not implemented (could be added)

#### Validation Flow
```
User clicks Submit
  ↓
validateForm() called
  ↓
Check all fields sequentially
  ↓
Set errors object
  ↓
Return isValid boolean
  ↓
If invalid: Display errors and stop
  ↓
If valid: Process submission
```

#### Error State Management
```typescript
// Initial state (no errors)
formErrors = {
  username: '',
  password: '',
  confirmPassword: '',
  name: '',
  role: '',
}

// After validation with errors
formErrors = {
  username: 'Username is required',
  password: '',
  confirmPassword: 'Passwords do not match',
  name: '',
  role: '',  // Role field never has errors (always valid)
}
```

#### Error Display Conditions
```typescript
// Show error message
{formErrors.name && (
  <p className="text-red-500 text-xs mt-1">{formErrors.name}</p>
)}

// Red border on input
className={`... ${formErrors.name ? 'border-red-500' : 'border-gray-300'}`}
```

---

## POSTGRESQL MIGRATION GUIDE

### Setup & Configuration

#### Database Connection
```typescript
import { Pool } from 'pg';

const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME || 'sabong_dashboard',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

export default pool;
```

#### Environment Variables (.env)
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sabong_dashboard
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_SSL=false
```

---

### API Endpoints

#### GET /api/users
**Purpose**: Retrieve all users with optional search and filters

**Query Parameters**:
- `search`: Optional search string (searches name, email, role)
- `role`: Optional role filter ('Administrator', 'Cashier', 'Operator A', 'Operator B')
- `status`: Optional status filter ('Online', 'Offline', 'Away')

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "username": "john_doe",
      "name": "John Doe",
      "email": "john.doe@sabong.com",
      "phone": "09123456789",
      "role": "Cashier",
      "status": "Online",
      "avatar_url": "https://...",
      "last_active": "2024-01-15T10:30:00Z",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "count": 20
}
```

**Implementation**:
```typescript
app.get('/api/users', async (req, res) => {
  try {
    const { search, role, status } = req.query;
    
    let query = `
      SELECT id, username, name, email, phone, role, status, 
             avatar_url, last_active, created_at, updated_at
      FROM users
    `;
    
    const params = [];
    const conditions = [];
    let paramCount = 0;
    
    // Search filter
    if (search) {
      paramCount++;
      conditions.push(`(
        LOWER(name) LIKE $${paramCount} OR 
        LOWER(email) LIKE $${paramCount} OR 
        LOWER(role) LIKE $${paramCount}
      )`);
      params.push(`%${search.toLowerCase()}%`);
    }
    
    // Role filter
    if (role && role !== 'All') {
      paramCount++;
      conditions.push(`role = $${paramCount}`);
      params.push(role);
    }
    
    // Status filter
    if (status && status !== 'All') {
      paramCount++;
      conditions.push(`status = $${paramCount}`);
      params.push(status);
    }
    
    // Add WHERE clause if there are conditions
    if (conditions.length > 0) {
      query += ` WHERE ${conditions.join(' AND ')}`;
    }
    
    query += ` ORDER BY created_at DESC`;
    
    const result = await pool.query(query, params);
    
    res.json({
      success: true,
      data: result.rows,
      count: result.rows.length
    });
  } catch (error) {
    console.error('Error fetching users:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch users'
    });
  }
});
```

---

#### POST /api/users
**Purpose**: Create new user account

**Request Body**:
```json
{
  "username": "john_doe",
  "password": "password123",
  "name": "John Doe",
  "role": "Cashier"
}
```

**Request Parameters**:
- `username` (required): Unique username (3+ characters, alphanumeric and underscores only)
- `password` (required): Password (6+ characters)
- `name` (required): Full name (2+ characters)
- `role` (required): One of: "Administrator", "Cashier", "Operator A", "Operator B"

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 21,
    "username": "john_doe",
    "name": "John Doe",
    "email": "john.doe@sabong.com",
    "phone": "09123456789",
    "role": "Cashier",
    "status": "Offline",
    "avatar_url": "https://...",
    "last_active": null,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

**Implementation**:
```typescript
import bcrypt from 'bcrypt';

app.post('/api/users', async (req, res) => {
  try {
    const { username, password, name, role } = req.body;
    
    // Validate input
    if (!username || !password || !name || !role) {
      return res.status(400).json({
        success: false,
        error: 'Missing required fields'
      });
    }
    
    // Check username uniqueness
    const existingUser = await pool.query(
      'SELECT id FROM users WHERE username = $1',
      [username]
    );
    
    if (existingUser.rows.length > 0) {
      return res.status(409).json({
        success: false,
        error: 'Username already exists'
      });
    }
    
    // Hash password
    const passwordHash = await bcrypt.hash(password, 10);
    
    // Generate email, phone, avatar
    const email = generateEmail(name);
    const phone = generatePhone();
    const avatarUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=random&size=128`;
    
    // Validate role
    const validRoles = ['Administrator', 'Cashier', 'Operator A', 'Operator B'];
    if (!validRoles.includes(role)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid role. Must be one of: Administrator, Cashier, Operator A, Operator B'
      });
    }
    
    // Insert user
    const result = await pool.query(
      `INSERT INTO users (username, password_hash, name, email, phone, role, status, avatar_url)
       VALUES ($1, $2, $3, $4, $5, $6, 'Offline', $7)
       RETURNING id, username, name, email, phone, role, status, avatar_url, last_active, created_at, updated_at`,
      [username, passwordHash, name, email, phone, role, avatarUrl]
    );
    
    // Log activity
    await pool.query(
      `INSERT INTO user_activity_log (user_id, action, details)
       VALUES ($1, 'user_created', $2)`,
      [result.rows[0].id, JSON.stringify({ created_by: req.user?.id })]
    );
    
    res.status(201).json({
      success: true,
      data: result.rows[0]
    });
  } catch (error) {
    console.error('Error creating user:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to create user'
    });
  }
});
```

---

#### PUT /api/users/:id
**Purpose**: Update existing user account

**Request Body**:
```json
{
  "username": "john_doe_updated",
  "password": "newpassword123",
  "name": "John Doe Updated",
  "role": "Administrator"
}
```

**Request Parameters**:
- `username` (optional): Updated username
- `password` (optional): New password (only if changing)
- `name` (optional): Updated full name
- `role` (optional): Updated role - one of: "Administrator", "Cashier", "Operator A", "Operator B"

**Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "john_doe_updated",
    "name": "John Doe Updated",
    "email": "john.doeupdated@sabong.com",
    "phone": "09123456789",
    "role": "Administrator",
    "status": "Online",
    "avatar_url": "https://...",
    "last_active": "2024-01-15T10:30:00Z",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-15T11:00:00Z"
  }
}
```

**Implementation**:
```typescript
app.put('/api/users/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { username, password, name, role } = req.body;
    
    // Check if user exists
    const existingUser = await pool.query(
      'SELECT id FROM users WHERE id = $1',
      [id]
    );
    
    if (existingUser.rows.length === 0) {
      return res.status(404).json({
        success: false,
        error: 'User not found'
      });
    }
    
    // Validate role if provided
    if (role) {
      const validRoles = ['Administrator', 'Cashier', 'Operator A', 'Operator B'];
      if (!validRoles.includes(role)) {
        return res.status(400).json({
          success: false,
          error: 'Invalid role. Must be one of: Administrator, Cashier, Operator A, Operator B'
        });
      }
    }
    
    // Generate updated fields
    const email = generateEmail(name);
    const avatarUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=random&size=128`;
    
    let query = `UPDATE users SET name = $2, email = $3, avatar_url = $4, username = $5`;
    let params = [id, name, email, avatarUrl, username];
    let paramCount = 5;
    
    // Update role if provided
    if (role) {
      paramCount++;
      query += `, role = $${paramCount}`;
      params.push(role);
    }
    
    // Update password if provided
    if (password) {
      const passwordHash = await bcrypt.hash(password, 10);
      paramCount++;
      query += `, password_hash = $${paramCount}`;
      params.push(passwordHash);
    }
    
    query += ` WHERE id = $1 RETURNING id, username, name, email, phone, role, status, avatar_url, last_active, created_at, updated_at`;
    
    const result = await pool.query(query, params);
    
    // Log activity
    const updatedFields = ['name', 'email', 'username'];
    if (role) updatedFields.push('role');
    if (password) updatedFields.push('password');
    
    await pool.query(
      `INSERT INTO user_activity_log (user_id, action, details)
       VALUES ($1, 'user_updated', $2)`,
      [id, JSON.stringify({ updated_by: req.user?.id, fields_updated: updatedFields })]
    );
    
    res.json({
      success: true,
      data: result.rows[0]
    });
  } catch (error) {
    console.error('Error updating user:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to update user'
    });
  }
});
```

---

#### DELETE /api/users/:id
**Purpose**: Delete user account

**Response**:
```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

**Implementation**:
```typescript
app.delete('/api/users/:id', async (req, res) => {
  try {
    const { id } = req.params;
    
    // Get user details for logging
    const user = await pool.query(
      'SELECT name FROM users WHERE id = $1',
      [id]
    );
    
    if (user.rows.length === 0) {
      return res.status(404).json({
        success: false,
        error: 'User not found'
      });
    }
    
    // Log activity before deletion
    await pool.query(
      `INSERT INTO user_activity_log (user_id, action, details)
       VALUES ($1, 'user_deleted', $2)`,
      [id, JSON.stringify({ deleted_by: req.user?.id, user_name: user.rows[0].name })]
    );
    
    // Delete user (cascades to sessions and activity log)
    await pool.query('DELETE FROM users WHERE id = $1', [id]);
    
    res.json({
      success: true,
      message: 'User deleted successfully'
    });
  } catch (error) {
    console.error('Error deleting user:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to delete user'
    });
  }
});
```

---

### Frontend Integration

#### Service Layer (services/users.ts)
```typescript
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001/api';

export interface UserAccount {
  id: number;
  username: string;
  name: string;
  email: string;
  phone: string;
  role: 'Administrator' | 'Cashier' | 'Operator A' | 'Operator B';
  status: 'Online' | 'Offline' | 'Away';
  avatar_url: string;
  last_active: string | null;
  created_at: string;
  updated_at: string;
}

export const userService = {
  async getUsers(filters?: {
    search?: string;
    role?: string;
    status?: string;
  }): Promise<UserAccount[]> {
    const params = filters || {};
    const response = await axios.get(`${API_BASE_URL}/users`, { params });
    return response.data.data;
  },

  async createUser(data: {
    username: string;
    password: string;
    name: string;
    role: 'Administrator' | 'Cashier' | 'Operator A' | 'Operator B';
  }): Promise<UserAccount> {
    const response = await axios.post(`${API_BASE_URL}/users`, data);
    return response.data.data;
  },

  async updateUser(id: number, data: {
    username: string;
    password?: string;
    name: string;
    role: 'Administrator' | 'Cashier' | 'Operator A' | 'Operator B';
  }): Promise<UserAccount> {
    const response = await axios.put(`${API_BASE_URL}/users/${id}`, data);
    return response.data.data;
  },

  async deleteUser(id: number): Promise<void> {
    await axios.delete(`${API_BASE_URL}/users/${id}`);
  },
};
```

#### Updated Component Logic
```typescript
import { useEffect } from 'react';
import { userService } from '@/services/users';

export const Accounts = () => {
  const [users, setUsers] = useState<UserAccount[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Fetch users on mount
  useEffect(() => {
    fetchUsers();
  }, []);
  
  const fetchUsers = async (filters?: {
    search?: string;
    role?: string;
    status?: string;
  }) => {
    try {
      setLoading(true);
      const data = await userService.getUsers(filters);
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users:', error);
      // Show error notification
    } finally {
      setLoading(false);
    }
  };
  
  // Fetch users when filters change (with debouncing for search)
  useEffect(() => {
    const timer = setTimeout(() => {
      const filters: any = {};
      
      if (searchQuery) filters.search = searchQuery;
      if (roleFilter !== 'All') filters.role = roleFilter;
      if (statusFilter !== 'All') filters.status = statusFilter;
      
      fetchUsers(filters);
    }, 300); // 300ms debounce for search
    
    return () => clearTimeout(timer);
  }, [searchQuery, roleFilter, statusFilter]);
  
  const handleCreateAccount = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    try {
      await userService.createUser({
        username: formData.username,
        password: formData.password,
        name: formData.name,
        role: formData.role,
      });
      
      // Refresh user list
      await fetchUsers(searchQuery);
      
      // Reset and close
      resetForm();
      setShowCreateModal(false);
      
      // Show success notification
      showNotification('User created successfully', 'success');
    } catch (error) {
      console.error('Error creating user:', error);
      showNotification('Failed to create user', 'error');
    }
  };
  
  const handleUpdateAccount = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    try {
      await userService.updateUser(editingUserId!, {
        username: formData.username,
        password: formData.password || undefined,
        name: formData.name,
        role: formData.role,
      });
      
      // Refresh user list
      await fetchUsers(searchQuery);
      
      // Reset and close
      resetForm();
      setShowEditModal(false);
      setEditingUserId(null);
      
      showNotification('User updated successfully', 'success');
    } catch (error) {
      console.error('Error updating user:', error);
      showNotification('Failed to update user', 'error');
    }
  };
  
  const handleDeleteUser = async (userId: number, userName: string) => {
    if (window.confirm(`Are you sure you want to delete user "${userName}"? This action cannot be undone.`)) {
      try {
        await userService.deleteUser(userId);
        
        // Refresh user list
        await fetchUsers(searchQuery);
        
        showNotification('User deleted successfully', 'success');
      } catch (error) {
        console.error('Error deleting user:', error);
        showNotification('Failed to delete user', 'error');
      }
    }
  };
  
  // Rest of component...
};
```

---

### Migration Checklist

#### Backend Setup
- [ ] Install PostgreSQL database
- [ ] Create database schema (run SQL scripts)
- [ ] Set up environment variables
- [ ] Install Node.js dependencies (pg, bcrypt)
- [ ] Create API endpoints (GET, POST, PUT, DELETE)
- [ ] Implement authentication middleware
- [ ] Set up CORS configuration
- [ ] Add error handling and logging

#### Frontend Updates
- [ ] Create user service layer
- [ ] Update component to use API calls
- [ ] Implement loading states
- [ ] Add error handling and notifications
- [ ] Implement debounced search
- [ ] Update TypeScript interfaces
- [ ] Test all CRUD operations
- [ ] Add optimistic UI updates

#### Testing
- [ ] Test user creation with all roles
- [ ] Test user updates including role changes
- [ ] Test user deletion
- [ ] Test search functionality (including role search)
- [ ] Test validation (client + server)
- [ ] Test role dropdown functionality
- [ ] Test role validation on backend
- [ ] Test error scenarios
- [ ] Test concurrent operations
- [ ] Performance testing with large datasets

#### Security
- [ ] Implement password hashing (bcrypt)
- [ ] Add authentication middleware
- [ ] Validate all inputs server-side
- [ ] Implement rate limiting
- [ ] Add SQL injection protection (parameterized queries)
- [ ] Set up HTTPS in production
- [ ] Implement session management
- [ ] Add CSRF protection

---

## ROLE SELECTION FEATURE SUMMARY

### Overview
The Accounts page now includes comprehensive role selection functionality, allowing administrators to assign specific roles to users during account creation and modification.

### Available Roles
1. **Administrator**
   - Full system access
   - User management capabilities
   - All feature access
   - Badge Color: Purple

2. **Cashier**
   - Cash transaction management
   - Cashier overview access
   - Transaction monitoring
   - Badge Color: Green
   - **Default role for new accounts**

3. **Operator A**
   - Primary betting operator interface
   - Fight management controls
   - Betting operations
   - Badge Color: Blue

4. **Operator B**
   - Secondary betting operator interface
   - Fight management controls
   - Betting operations
   - Badge Color: Yellow

### Implementation Details

#### UI Components
- **Dropdown Select**: Standard HTML `<select>` element with 4 options
- **Positioning**: Between Username and Password fields in both Create and Edit modals
- **Styling**: Consistent with other form inputs (same padding, border, focus states)
- **Default Value**: "Cashier" for new accounts
- **Pre-population**: Current user role when editing

#### Form Integration
- Added to `formData` state as `role` property
- Type-safe with TypeScript union type
- Required field (always has value, no validation errors)
- Persisted to database on create/update operations

#### Database Schema
- `role` column in `users` table: `VARCHAR(20) NOT NULL`
- CHECK constraint enforces valid values only
- Indexed for performance on role-based queries
- Default value: "Cashier"

#### API Integration
- POST `/api/users` - Requires `role` in request body
- PUT `/api/users/:id` - Accepts `role` for updates
- Server-side validation of role values
- Role included in all user responses

### User Workflows

#### Creating Account with Role
1. Click "Create account" button
2. Fill in Name, Username fields
3. **Select Role from dropdown** (defaults to Cashier)
4. Enter Password and Confirm Password
5. Submit form
6. User created with selected role

#### Editing User Role
1. Click Edit button on user row
2. Modal opens with current role pre-selected
3. **Change role via dropdown**
4. Modify other fields as needed
5. Submit form
6. User role updated in database

### Migration Notes
When migrating from mock data to PostgreSQL:
- Existing users default to "Cashier" role
- Update SQL schema to use new role values
- Frontend already implements role selection
- Backend validation ensures data integrity

---

## ADVANCED FILTER SYSTEM SUMMARY

### Overview
The Accounts page includes a comprehensive filter system that allows users to quickly find and organize accounts using multiple criteria simultaneously.

### Filter Components

#### 1. Search Bar
- **Type**: Text input with search icon
- **Searches**: Name, email, and role fields
- **Behavior**: Real-time, case-insensitive
- **Position**: Top of page, full width

#### 2. Role Filter
- **Type**: Dropdown select
- **Options**: All Roles, Administrator, Cashier, Operator A, Operator B
- **Default**: "All Roles"
- **Badge Color**: Purple when active

#### 3. Status Filter
- **Type**: Dropdown select
- **Options**: All Statuses, Online, Offline, Away
- **Default**: "All Statuses"
- **Badge Color**: Green when active

#### 4. Clear Filters Button
- **Visibility**: Shows when any filter is active
- **Action**: Resets all filters to default state
- **Position**: Right side of filter bar

### Filter Logic

#### Combined Filtering (AND Logic)
```
User is shown IF:
  (matches search query OR no search) AND
  (matches role filter OR role = "All") AND
  (matches status filter OR status = "All")
```

**Example**:
- Search: "John"
- Role: "Cashier"
- Status: "Online"
- **Result**: Shows only users named "John" who are Cashiers AND currently Online

### Active Filters Display

#### Visual Feedback
- **Location**: Stats bar, right side
- **Format**: Colored badge pills
- **Badge Types**:
  - Search: Blue badge with query text
  - Role: Purple badge with role name
  - Status: Green badge with status name

#### User Count Display
- **Format**: "Showing X of Y users"
- **X**: Filtered count (matching all criteria)
- **Y**: Total users in system
- **Updates**: Real-time as filters change

### Implementation Details

#### State Management
```typescript
const [searchQuery, setSearchQuery] = useState('');
const [roleFilter, setRoleFilter] = useState<UserAccount['role'] | 'All'>('All');
const [statusFilter, setStatusFilter] = useState<UserAccount['status'] | 'All'>('All');
```

#### Frontend Filtering (Current)
```typescript
const filteredUsers = users.filter(user => {
  const matchesSearch = searchQuery === '' || 
    user.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    user.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
    user.role.toLowerCase().includes(searchQuery.toLowerCase());
  
  const matchesRole = roleFilter === 'All' || user.role === roleFilter;
  const matchesStatus = statusFilter === 'All' || user.status === statusFilter;
  
  return matchesSearch && matchesRole && matchesStatus;
});
```

#### Backend Filtering (PostgreSQL Migration)
```sql
SELECT * FROM users
WHERE 
  (LOWER(name) LIKE '%search%' OR LOWER(email) LIKE '%search%' OR search IS NULL)
  AND (role = 'Cashier' OR role_filter = 'All')
  AND (status = 'Online' OR status_filter = 'All')
ORDER BY created_at DESC;
```

### User Experience Features

#### Performance
- **Frontend**: Instant filtering (no delay)
- **Backend**: Indexed columns for fast queries
- **Debounce**: 300ms on search input (when using API)

#### Visual Indicators
- Filter dropdowns highlight when not on "All"
- Active filter badges show what's being filtered
- User count updates in real-time
- "Clear all filters" appears when needed

#### Empty States
- When no results: "No users found matching '{query}'"
- Suggestion to clear filters
- All filter controls remain accessible

### Migration Considerations

#### Database Indexes
```sql
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_users_name_search ON users USING gin(to_tsvector('english', name));
CREATE INDEX idx_users_email_search ON users USING gin(to_tsvector('english', email));
```

#### API Query Parameters
- GET `/api/users?search=John&role=Cashier&status=Online`
- All parameters optional
- Backend builds dynamic WHERE clause

#### Frontend-Backend Sync
- Frontend filters locally (current implementation)
- Backend API accepts same filter parameters
- Easy migration path: swap filter logic to use API

---

## END OF DOCUMENTATION

**Document Version**: 3.0  
**Last Updated**: 2024-01-15 (Updated with Role Selection + Advanced Filter System)  
**Author**: System Documentation  
**Total Sections**: 9  
**Total Pages**: Comprehensive

This documentation covers every aspect of the Accounts page including:
- Complete UI specifications with filter system
- Component breakdown and interactions
- Database schema and indexing strategy
- User interaction flows and behaviors
- Function implementations and logic
- Comprehensive validation rules
- Advanced search and filter capabilities
- Complete PostgreSQL migration guide
- Role-based access control system
