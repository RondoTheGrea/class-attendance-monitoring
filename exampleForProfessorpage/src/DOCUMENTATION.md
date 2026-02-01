# Professor Dashboard - Attendance Monitoring System
## Complete UI/UX Documentation

---

## Table of Contents
1. [System Overview](#system-overview)
2. [Design System](#design-system)
3. [User Flow](#user-flow)
4. [Page Structure](#page-structure)
5. [Components Documentation](#components-documentation)
6. [Data Models](#data-models)
7. [Features & Functionality](#features--functionality)
8. [HTML/CSS Migration Guide](#htmlcss-migration-guide)

---

## System Overview

### Purpose
A web-based dashboard for professors to manage classroom attendance using QR code technology. Inspired by Google Classroom's clean interface and intuitive user experience.

### Core Concept
- Professors create and manage multiple classes
- Each class can have multiple weekly schedules
- QR codes are generated during scheduled class times
- Students scan QR codes to mark attendance
- Professors can post announcements and view attendance records

### Key Features
1. **Class Management** - Create and organize multiple classes
2. **Schedule Configuration** - Set up weekly recurring schedules
3. **QR-Based Attendance** - Time-restricted QR code scanning
4. **Announcements** - Post updates and notifications
5. **Attendance Tracking** - View historical attendance records

---

## Design System

### Color Palette

#### Primary Colors
- **Blue 600**: `#2563eb` - Primary actions, buttons
- **Blue 700**: `#1d4ed8` - Button hover states
- **Blue 50**: `#eff6ff` - Light backgrounds, badges
- **Blue 100**: `#dbeafe` - Decorative elements

#### Neutral Colors
- **Slate 900**: `#0f172a` - Primary text
- **Slate 700**: `#334155` - Secondary text
- **Slate 600**: `#475569` - Tertiary text
- **Slate 500**: `#64748b` - Muted text
- **Slate 400**: `#94a3b8` - Icons, borders
- **Slate 300**: `#cbd5e1` - Input borders
- **Slate 200**: `#e2e8f0` - Card borders
- **Slate 100**: `#f1f5f9` - Subtle backgrounds
- **Slate 50**: `#f8fafc` - Page background
- **White**: `#ffffff` - Card backgrounds

#### Accent Colors
- **Amber 50-800**: Warning states, no schedule indicator
- **Green 50-800**: Success states, attendance confirmed
- **Red 50-600**: Destructive actions, delete buttons

### Typography

#### Font Families
- **Primary**: System font stack (San Francisco, Segoe UI, etc.)
- All text uses the default system font for optimal performance

#### Font Sizes
- **3xl**: 30px - Page titles
- **2xl**: 24px - Section headers
- **xl**: 20px - Card titles
- **lg**: 18px - Subheadings
- **base**: 16px - Body text
- **sm**: 14px - Helper text, metadata
- **xs**: 12px - Fine print

#### Font Weights
- **Bold**: 700 - Main headings
- **Semibold**: 600 - Subheadings, labels
- **Medium**: 500 - Emphasized text
- **Normal**: 400 - Body text

### Spacing System
Based on 4px units:
- **1**: 4px
- **2**: 8px
- **3**: 12px
- **4**: 16px
- **5**: 20px
- **6**: 24px
- **8**: 32px
- **12**: 48px
- **16**: 64px
- **20**: 80px
- **24**: 96px

### Border Radius
- **sm**: 4px - Small elements
- **md**: 6px - Buttons, inputs
- **lg**: 8px - Cards
- **xl**: 12px - Large cards
- **2xl**: 16px - Modal dialogs
- **3xl**: 24px - Special elements
- **full**: 9999px - Circular elements

### Shadows
- **sm**: `0 1px 2px 0 rgb(0 0 0 / 0.05)` - Subtle elevation
- **md**: `0 4px 6px -1px rgb(0 0 0 / 0.1)` - Cards
- **lg**: `0 10px 15px -3px rgb(0 0 0 / 0.1)` - Elevated cards
- **xl**: `0 20px 25px -5px rgb(0 0 0 / 0.1)` - Modals
- **2xl**: `0 25px 50px -12px rgb(0 0 0 / 0.25)` - High elevation

---

## User Flow

### Primary Flow: From Dashboard to Attendance

```
1. DASHBOARD (Landing Page)
   ↓
   User clicks "Create Class"
   ↓
2. CREATE CLASS MODAL
   - Enter: Subject Name (required)
   - Enter: Section (optional)
   - Enter: Room (optional)
   - Enter: Description (optional)
   - Click "Create Class"
   ↓
3. DASHBOARD (Updated)
   - New class card appears
   - User clicks on class card
   ↓
4. CLASS DETAIL VIEW
   - Default tab: Overview
   - Shows class info and stats
   - User clicks "Schedule" tab
   ↓
5. SCHEDULE MANAGEMENT
   - Click "Add Schedule"
   - Select: Day of week
   - Select: Start time
   - Select: End time
   - Click "Add Schedule"
   - Repeat for additional schedules
   ↓
6. READY FOR ATTENDANCE
   - During scheduled class time
   - Click "Activate QR Scanning"
   ↓
7. QR CODE MODAL
   - QR code displays
   - Students scan with their devices
   - Attendance is recorded
   - Click "Close Scanner"
   ↓
8. ATTENDANCE TAB
   - View all attendance records
   - See who attended each session
   - Check scan times
```

### Secondary Flow: Posting Announcements

```
1. CLASS DETAIL VIEW
   ↓
2. Click "Announcements" tab
   ↓
3. ANNOUNCEMENTS SECTION
   - Enter announcement title
   - Enter announcement content
   - Click "Post Announcement"
   ↓
4. ANNOUNCEMENTS LIST
   - New announcement appears at top
   - Shows timestamp
   - Displays full content
```

---

## Page Structure

### 1. Dashboard Page (Main View)

#### Layout Structure
```
┌─────────────────────────────────────────────────┐
│ TOP NAVIGATION BAR                              │
│ ┌──────┐  Professor Dashboard        [+ Create]│
│ │ Icon │  Attendance Monitoring                 │
│ └──────┘                                        │
├─────────────────────────────────────────────────┤
│ MAIN CONTENT AREA                               │
│                                                 │
│  My Classes                                     │
│  You have X active classes                      │
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │  Class   │  │  Class   │  │  Class   │     │
│  │  Card 1  │  │  Card 2  │  │  Card 3  │     │
│  │          │  │          │  │          │     │
│  └──────────┘  └──────────┘  └──────────┘     │
│                                                 │
└─────────────────────────────────────────────────┘
```

#### Empty State Structure
```
┌─────────────────────────────────────────────────┐
│ TOP NAVIGATION BAR                              │
├─────────────────────────────────────────────────┤
│                                                 │
│               ┌────────┐                        │
│               │  Icon  │                        │
│               └────────┘                        │
│                                                 │
│          Welcome to Your Dashboard              │
│                                                 │
│     Create your first class to start managing   │
│     schedules, posting announcements...         │
│                                                 │
│          [Create Your First Class]              │
│                                                 │
└─────────────────────────────────────────────────┘
```

### 2. Class Detail View

#### Layout Structure
```
┌─────────────────────────────────────────────────┐
│ HEADER BAR (Sticky)                             │
│ [← Back to Dashboard]                           │
│                                                 │
│ ┌──┐  Introduction to Computer Science          │
│ │📚│  [Section A] [Room 301]                    │
│ └──┘  Brief class description...                │
│                          [Activate QR Scanning] │
├─────────────────────────────────────────────────┤
│ TAB NAVIGATION                                  │
│ [Overview] [Schedule] [Announcements] [Attend.] │
├─────────────────────────────────────────────────┤
│                                                 │
│ TAB CONTENT AREA                                │
│                                                 │
│ (Content changes based on active tab)           │
│                                                 │
└─────────────────────────────────────────────────┘
```

### 3. QR Code Modal

#### Layout Structure
```
        ┌───────────────────────────┐
        │  Attendance QR Code       │
        │  Students scan this code  │
        │                           │
        │  ┌─────────────────────┐  │
        │  │                     │  │
        │  │    ███  ███  ███    │  │
        │  │    ███  ███  ███    │  │
        │  │    QR CODE HERE     │  │
        │  │    ███  ███  ███    │  │
        │  │    ███  ███  ███    │  │
        │  │                     │  │
        │  └─────────────────────┘  │
        │                           │
        │  Intro to Computer Sci    │
        │  Section A                │
        │                           │
        │   [Close Scanner]         │
        │                           │
        └───────────────────────────┘
```

---

## Components Documentation

### Component 1: ClassCard

#### Purpose
Displays summary information for a single class in grid layout

#### Visual Structure
```
┌────────────────────────────────────────┐
│ Subject Name                      📚   │
│ [Section A] [Room 301]                 │
│                                        │
│ Brief description of the class...      │
│                                        │
│ ╔════════════════════════════════════╗ │
│ ║ 📅 Mondays  •  🕐 9:00 AM - 10:30 ║ │
│ ╚════════════════════════════════════╝ │
│                                        │
│ ─────────────────────────────────────  │
│ 👥 25 students         View Details →  │
└────────────────────────────────────────┘
```

#### HTML Structure
```html
<div class="class-card">
  <div class="class-card-header">
    <div class="class-info">
      <h3 class="class-title">Subject Name</h3>
      <div class="badges">
        <span class="badge badge-section">Section A</span>
        <span class="badge badge-room">
          <icon>📍</icon> Room 301
        </span>
      </div>
    </div>
    <div class="icon-container">
      <icon>📚</icon>
    </div>
  </div>
  
  <p class="class-description">Description text...</p>
  
  <div class="schedule-info">
    <icon>📅</icon> Mondays
    <span>•</span>
    <icon>🕐</icon> 9:00 AM - 10:30 AM
  </div>
  
  <div class="card-footer">
    <div class="student-count">
      <icon>👥</icon> 25 students
    </div>
    <div class="view-link">
      View Details <icon>→</icon>
    </div>
  </div>
</div>
```

#### CSS Classes
- `.class-card` - Main container, white background, rounded corners, shadow
- `.class-card-header` - Top section with title and icon
- `.class-title` - Large, bold text (20px, 700 weight)
- `.badge` - Small pill-shaped label
- `.badge-section` - Blue background badge
- `.badge-room` - Outlined badge with icon
- `.class-description` - Gray text, 2-line clamp
- `.schedule-info` - Gray rounded box with schedule details
- `.card-footer` - Bottom section with border-top

#### Interactive States
- **Hover**: Card elevates (shadow increase), slight upward translation
- **Hover .view-link**: Arrow icon moves right
- **Hover .class-title**: Text color changes to blue

### Component 2: CreateClassModal

#### Purpose
Modal dialog for creating a new class with basic information

#### Visual Structure
```
┌──────────────────────────────────────────┐
│ Create New Class                     ✕   │
│ Add basic class information...           │
│                                          │
│ Subject Name *                           │
│ ┌──────────────────────────────────────┐ │
│ │ e.g., Introduction to Computer Sci   │ │
│ └──────────────────────────────────────┘ │
│                                          │
│ Section          Room                    │
│ ┌─────────────┐  ┌─────────────────────┐│
│ │ e.g., A     │  │ e.g., Room 301      ││
│ └─────────────┘  └─────────────────────┘│
│                                          │
│ Description                              │
│ ┌──────────────────────────────────────┐ │
│ │ Brief description...                 │ │
│ │                                      │ │
│ └──────────────────────────────────────┘ │
│                                          │
│ ℹ️ You can add class schedules after...  │
│                                          │
│ ──────────────────────────────────────  │
│                    [Cancel] [Create]     │
└──────────────────────────────────────────┘
```

#### HTML Structure
```html
<div class="modal-overlay">
  <div class="modal-dialog">
    <div class="modal-header">
      <h2>Create New Class</h2>
      <p class="subtitle">Add basic class information...</p>
      <button class="close-button">✕</button>
    </div>
    
    <form class="modal-body">
      <div class="form-group">
        <label>Subject Name *</label>
        <input type="text" placeholder="e.g., Introduction...">
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label>Section</label>
          <input type="text" placeholder="e.g., A">
        </div>
        <div class="form-group">
          <label>Room</label>
          <input type="text" placeholder="e.g., Room 301">
        </div>
      </div>
      
      <div class="form-group">
        <label>Description</label>
        <textarea rows="3" placeholder="Brief description..."></textarea>
      </div>
      
      <div class="info-box">
        <icon>ℹ️</icon>
        <p>You can add class schedules after...</p>
      </div>
    </form>
    
    <div class="modal-footer">
      <button class="btn-cancel">Cancel</button>
      <button class="btn-primary">Create Class</button>
    </div>
  </div>
</div>
```

#### CSS Classes
- `.modal-overlay` - Full screen, semi-transparent black background
- `.modal-dialog` - White centered box, max-width 640px
- `.modal-header` - Title section
- `.modal-body` - Form content area
- `.form-group` - Individual input group with label
- `.form-row` - Horizontal layout for multiple inputs
- `.info-box` - Blue background info message
- `.modal-footer` - Button area with right alignment

### Component 3: ScheduleManager

#### Purpose
Interface for adding and managing weekly class schedules

#### Visual Structure
```
┌────────────────────────────────────────────┐
│ Weekly Schedule              [+ Add]       │
├────────────────────────────────────────────┤
│                                            │
│ ┌────────────────────────────────────────┐│
│ │ 📅  Monday                          🗑️ ││
│ │     🕐 9:00 AM - 10:30 AM             ││
│ └────────────────────────────────────────┘│
│                                            │
│ ┌────────────────────────────────────────┐│
│ │ 📅  Wednesday                       🗑️ ││
│ │     🕐 9:00 AM - 10:30 AM             ││
│ └────────────────────────────────────────┘│
│                                            │
└────────────────────────────────────────────┘
```

#### Empty State
```
┌────────────────────────────────────────────┐
│ Weekly Schedule              [+ Add]       │
├────────────────────────────────────────────┤
│                                            │
│               📅                           │
│                                            │
│        No schedules configured             │
│   Add class schedules to enable QR code    │
│         attendance scanning                │
│                                            │
└────────────────────────────────────────────┘
```

#### Adding New Schedule
```
┌────────────────────────────────────────────┐
│ ℹ️ Add a new class schedule. Make sure... │
│                                            │
│ Day of Week                                │
│ ┌──────────────────────────────────────┐  │
│ │ Select a day               ▼         │  │
│ └──────────────────────────────────────┘  │
│                                            │
│ Start Time          End Time               │
│ ┌─────────────┐     ┌─────────────────┐   │
│ │ 09:00       │     │ 10:30           │   │
│ └─────────────┘     └─────────────────┘   │
│                                            │
│                    [Cancel] [Add Schedule] │
└────────────────────────────────────────────┘
```

#### HTML Structure
```html
<div class="schedule-manager">
  <div class="schedule-header">
    <h3>Weekly Schedule</h3>
    <button class="btn-add">+ Add Schedule</button>
  </div>
  
  <div class="schedule-list">
    <div class="schedule-item">
      <div class="schedule-info">
        <div class="icon-container">
          <icon>📅</icon>
        </div>
        <div class="schedule-details">
          <p class="day">Monday</p>
          <p class="time">
            <icon>🕐</icon> 9:00 AM - 10:30 AM
          </p>
        </div>
      </div>
      <button class="btn-delete">🗑️</button>
    </div>
  </div>
  
  <!-- Add Schedule Form -->
  <div class="add-schedule-form">
    <div class="alert-info">
      <icon>ℹ️</icon>
      <p>Add a new class schedule...</p>
    </div>
    
    <div class="form-group">
      <label>Day of Week</label>
      <select>
        <option>Select a day</option>
        <option>Monday</option>
        <!-- ... -->
      </select>
    </div>
    
    <div class="form-row">
      <div class="form-group">
        <label>Start Time</label>
        <input type="time">
      </div>
      <div class="form-group">
        <label>End Time</label>
        <input type="time">
      </div>
    </div>
    
    <div class="form-actions">
      <button class="btn-cancel">Cancel</button>
      <button class="btn-primary">Add Schedule</button>
    </div>
  </div>
</div>
```

### Component 4: Class Detail View - Overview Tab

#### Visual Structure
```
┌────────────────────────────────────────────┐
│ Class Information                          │
├────────────────────────────────────────────┤
│ Subject            Section                 │
│ Intro to CS        A                       │
│                                            │
│ Room               Schedules               │
│ Room 301           3 per week              │
└────────────────────────────────────────────┘

┌──────────────┐ ┌──────────────┐ ┌─────────┐
│ 👥           │ │ 🔔           │ │ 📅      │
│              │ │              │ │         │
│ 25           │ │ 5            │ │ 12      │
│ Students     │ │ Announcements│ │ Sessions│
└──────────────┘ └──────────────┘ └─────────┘
```

#### HTML Structure
```html
<div class="overview-tab">
  <div class="info-card">
    <h3>Class Information</h3>
    <div class="info-grid">
      <div class="info-item">
        <p class="label">Subject</p>
        <p class="value">Intro to CS</p>
      </div>
      <div class="info-item">
        <p class="label">Section</p>
        <p class="value">A</p>
      </div>
      <div class="info-item">
        <p class="label">Room</p>
        <p class="value">Room 301</p>
      </div>
      <div class="info-item">
        <p class="label">Schedules</p>
        <p class="value">3 per week</p>
      </div>
    </div>
  </div>
  
  <div class="stats-grid">
    <div class="stat-card stat-blue">
      <div class="stat-icon">👥</div>
      <p class="stat-number">25</p>
      <p class="stat-label">Students</p>
    </div>
    
    <div class="stat-card stat-amber">
      <div class="stat-icon">🔔</div>
      <p class="stat-number">5</p>
      <p class="stat-label">Announcements</p>
    </div>
    
    <div class="stat-card stat-green">
      <div class="stat-icon">📅</div>
      <p class="stat-number">12</p>
      <p class="stat-label">Sessions</p>
    </div>
  </div>
</div>
```

### Component 5: Announcements Tab

#### Visual Structure
```
┌────────────────────────────────────────────┐
│ Post New Announcement                      │
├────────────────────────────────────────────┤
│ ┌──────────────────────────────────────┐  │
│ │ Announcement title...                │  │
│ └──────────────────────────────────────┘  │
│                                            │
│ ┌──────────────────────────────────────┐  │
│ │ Write your announcement here...      │  │
│ │                                      │  │
│ │                                      │  │
│ └──────────────────────────────────────┘  │
│                                            │
│ [🔔 Post Announcement]                     │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│ Midterm Exam Schedule     [Jan 28, 10:00]  │
├────────────────────────────────────────────┤
│ The midterm examination will be held on    │
│ February 15, 2026. Please review           │
│ chapters 1-5.                              │
└────────────────────────────────────────────┘
```

#### HTML Structure
```html
<div class="announcements-tab">
  <div class="post-card">
    <h3>Post New Announcement</h3>
    <input type="text" placeholder="Announcement title...">
    <textarea rows="4" placeholder="Write your announcement..."></textarea>
    <button class="btn-primary">
      <icon>🔔</icon> Post Announcement
    </button>
  </div>
  
  <div class="announcements-list">
    <div class="announcement-card">
      <div class="announcement-header">
        <h4>Midterm Exam Schedule</h4>
        <span class="timestamp">Jan 28, 10:00</span>
      </div>
      <div class="announcement-body">
        <p>The midterm examination will be held...</p>
      </div>
    </div>
  </div>
</div>
```

### Component 6: Attendance Tab

#### Visual Structure
```
┌────────────────────────────────────────────┐
│ Jan 29, 2026 9:00 AM          [3 present]  │
│ 🕐 09:00 - 10:30                           │
├────────────────────────────────────────────┤
│ ┌──────────────────────────────────────┐  │
│ │ ✓ Alice Johnson            9:05 AM   │  │
│ │   2024-001                           │  │
│ └──────────────────────────────────────┘  │
│                                            │
│ ┌──────────────────────────────────────┐  │
│ │ ✓ Bob Smith                9:03 AM   │  │
│ │   2024-002                           │  │
│ └──────────────────────────────────────┘  │
└────────────────────────────────────────────┘
```

#### HTML Structure
```html
<div class="attendance-tab">
  <div class="attendance-record">
    <div class="record-header">
      <div>
        <h4>Jan 29, 2026 9:00 AM</h4>
        <p class="schedule-time">
          <icon>🕐</icon> 09:00 - 10:30
        </p>
      </div>
      <span class="badge-success">3 present</span>
    </div>
    
    <div class="student-list">
      <div class="student-item">
        <div class="student-info">
          <icon class="check-icon">✓</icon>
          <div>
            <p class="student-name">Alice Johnson</p>
            <p class="student-id">2024-001</p>
          </div>
        </div>
        <p class="scan-time">9:05 AM</p>
      </div>
    </div>
  </div>
</div>
```

---

## Data Models

### Class Data Structure
```javascript
{
  id: "string",              // Unique identifier
  subject: "string",         // Class name (required)
  section: "string",         // Section identifier (optional)
  room: "string",            // Room location (optional)
  description: "string",     // Class description (optional)
  schedules: [Schedule],     // Array of schedule objects
  announcements: [Announcement], // Array of announcements
  attendance: [AttendanceRecord], // Array of attendance records
  createdAt: "ISO 8601 date" // Creation timestamp
}
```

### Schedule Data Structure
```javascript
{
  day: "string",         // Day of week (Monday-Sunday)
  startTime: "HH:MM",    // 24-hour format (e.g., "09:00")
  endTime: "HH:MM"       // 24-hour format (e.g., "10:30")
}
```

### Announcement Data Structure
```javascript
{
  id: "string",          // Unique identifier
  title: "string",       // Announcement title
  content: "string",     // Announcement content
  createdAt: "ISO 8601 date" // Creation timestamp
}
```

### Attendance Record Data Structure
```javascript
{
  id: "string",          // Unique identifier
  date: "ISO 8601 date", // Session date and time
  scheduleTime: "string", // Display format (e.g., "09:00 - 10:30")
  students: [Student]    // Array of students who attended
}
```

### Student Data Structure
```javascript
{
  id: "string",          // Unique identifier
  name: "string",        // Full name
  studentId: "string",   // Student ID number
  timeScanned: "ISO 8601 date" // Timestamp of QR scan
}
```

### QR Code Data Structure
```javascript
{
  classId: "string",     // Class identifier
  className: "string",   // Class name for display
  professorId: "string", // Professor identifier
  timestamp: "ISO 8601 date" // QR generation time
}
```

---

## Features & Functionality

### 1. Class Creation
**Location**: Dashboard → Create Class Modal

**Steps**:
1. Click "Create Class" button
2. Fill in subject name (required)
3. Optionally add section, room, description
4. Click "Create Class"
5. Modal closes, new class appears in dashboard

**Validation**:
- Subject name cannot be empty
- All other fields are optional

### 2. Schedule Management
**Location**: Class Detail → Schedule Tab

**Steps**:
1. Click "Add Schedule" button
2. Select day of week from dropdown
3. Select start time
4. Select end time
5. Click "Add Schedule"

**Validation**:
- All fields must be filled
- End time must be after start time
- No overlapping schedules on the same day

**Visual Feedback**:
- Conflict alert if times overlap
- New schedule appears immediately after adding
- Delete button appears on hover

### 3. QR Code Scanning
**Location**: Class Detail → Header → Activate QR Scanning

**Steps**:
1. Click "Activate QR Scanning" button
2. System checks if current time matches any schedule
3. If valid, QR code modal displays
4. QR code contains class and professor information
5. Students scan code to mark attendance

**Validation**:
- Must have at least one schedule configured
- Current day must match a scheduled day
- Current time must be between start and end time

**QR Code Content**:
```json
{
  "classId": "123",
  "className": "Intro to CS",
  "professorId": "PROF001",
  "timestamp": "2026-01-31T09:05:00Z"
}
```

### 4. Announcements
**Location**: Class Detail → Announcements Tab

**Steps**:
1. Enter announcement title
2. Enter announcement content
3. Click "Post Announcement"
4. Announcement appears at top of list

**Display**:
- Newest announcements first
- Shows title, content, and timestamp
- Preserves whitespace and line breaks

### 5. Attendance Tracking
**Location**: Class Detail → Attendance Tab

**Display**:
- Shows all past attendance sessions
- Groups by date and schedule time
- Lists all students who attended
- Shows individual scan times
- Displays count of present students

**Information Shown**:
- Session date and time
- Number of students present
- Student names and IDs
- Individual scan timestamps

---

## HTML/CSS Migration Guide

### Global Styles

#### CSS Reset and Base
```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", 
               Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: #0f172a;
  background-color: #f8fafc;
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}
```

#### Container
```css
.container {
  max-width: 1280px; /* 7xl */
  margin: 0 auto;
  padding: 0 24px;
}
```

#### Typography
```css
h1 {
  font-size: 30px;
  font-weight: 700;
  color: #0f172a;
}

h2 {
  font-size: 24px;
  font-weight: 700;
  color: #0f172a;
}

h3 {
  font-size: 20px;
  font-weight: 600;
  color: #0f172a;
}

h4 {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
}

p {
  font-size: 16px;
  line-height: 1.6;
  color: #334155;
}

.text-muted {
  color: #64748b;
}

.text-sm {
  font-size: 14px;
}

.text-xs {
  font-size: 12px;
}
```

#### Buttons
```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 16px;
  font-size: 14px;
  font-weight: 500;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background-color: #2563eb;
  color: white;
  box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
}

.btn-primary:hover {
  background-color: #1d4ed8;
}

.btn-lg {
  padding: 12px 20px;
  font-size: 16px;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 14px;
}

.btn-outline {
  background-color: white;
  border: 1px solid #cbd5e1;
  color: #334155;
}

.btn-outline:hover {
  background-color: #f8fafc;
}

.btn-ghost {
  background-color: transparent;
  color: #334155;
}

.btn-ghost:hover {
  background-color: #f1f5f9;
}
```

#### Cards
```css
.card {
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
  overflow: hidden;
}

.card-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
}

.card-content {
  padding: 20px 24px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
}
```

#### Badges
```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  font-size: 12px;
  font-weight: 500;
  border-radius: 9999px;
  white-space: nowrap;
}

.badge-secondary {
  background-color: #eff6ff;
  color: #1d4ed8;
  border: 1px solid #dbeafe;
}

.badge-outline {
  background-color: transparent;
  border: 1px solid #cbd5e1;
  color: #475569;
}

.badge-success {
  background-color: #dcfce7;
  color: #166534;
  border: 1px solid #bbf7d0;
}
```

#### Form Elements
```css
.form-group {
  margin-bottom: 16px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #334155;
}

input[type="text"],
input[type="time"],
select,
textarea {
  width: 100%;
  padding: 10px 12px;
  font-size: 14px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  background-color: white;
  transition: border-color 0.2s;
}

input:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgb(37 99 235 / 0.1);
}

textarea {
  resize: vertical;
  min-height: 80px;
}
```

#### Grid System
```css
.grid {
  display: grid;
  gap: 24px;
}

.grid-cols-1 {
  grid-template-columns: repeat(1, minmax(0, 1fr));
}

.grid-cols-2 {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.grid-cols-3 {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

@media (min-width: 768px) {
  .md\:grid-cols-2 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  
  .md\:grid-cols-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (min-width: 1024px) {
  .lg\:grid-cols-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
```

#### Utility Classes
```css
/* Spacing */
.mb-2 { margin-bottom: 8px; }
.mb-3 { margin-bottom: 12px; }
.mb-4 { margin-bottom: 16px; }
.mb-6 { margin-bottom: 24px; }
.mb-8 { margin-bottom: 32px; }

.mt-2 { margin-top: 8px; }
.mt-4 { margin-top: 16px; }
.mt-6 { margin-top: 24px; }

.p-4 { padding: 16px; }
.p-6 { padding: 24px; }
.px-4 { padding-left: 16px; padding-right: 16px; }
.px-6 { padding-left: 24px; padding-right: 24px; }
.py-4 { padding-top: 16px; padding-bottom: 16px; }

/* Flexbox */
.flex {
  display: flex;
}

.flex-col {
  flex-direction: column;
}

.items-center {
  align-items: center;
}

.justify-between {
  justify-content: space-between;
}

.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }
.gap-6 { gap: 24px; }

/* Borders */
.border {
  border: 1px solid #e2e8f0;
}

.border-t {
  border-top: 1px solid #f1f5f9;
}

.border-b {
  border-bottom: 1px solid #e2e8f0;
}

.rounded {
  border-radius: 6px;
}

.rounded-lg {
  border-radius: 8px;
}

.rounded-xl {
  border-radius: 12px;
}

.rounded-full {
  border-radius: 9999px;
}

/* Shadows */
.shadow {
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
}

.shadow-md {
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}

.shadow-lg {
  box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}

/* Text alignment */
.text-center {
  text-align: center;
}

.text-right {
  text-align: right;
}

/* Positioning */
.sticky {
  position: sticky;
}

.top-0 {
  top: 0;
}

.z-10 {
  z-index: 10;
}

/* Backgrounds */
.bg-white {
  background-color: white;
}

.bg-slate-50 {
  background-color: #f8fafc;
}

.bg-blue-50 {
  background-color: #eff6ff;
}

/* Transitions */
.transition {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}
```

### Specific Component Styles

#### Navigation Bar
```css
.nav-bar {
  background-color: white;
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  position: sticky;
  top: 0;
  z-index: 10;
}

.nav-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav-icon {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  color: white;
  padding: 10px;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}
```

#### Class Card
```css
.class-card {
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.class-card:hover {
  box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1);
  transform: translateY(-4px);
}

.class-card-header {
  padding: 20px;
  padding-bottom: 16px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.class-title {
  font-size: 20px;
  font-weight: 600;
  color: #0f172a;
  margin-bottom: 8px;
  transition: color 0.2s;
}

.class-card:hover .class-title {
  color: #2563eb;
}

.class-card-content {
  padding: 0 20px 20px;
}

.schedule-info {
  background-color: #f8fafc;
  border-radius: 8px;
  padding: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #334155;
}

.card-footer {
  padding: 16px 20px;
  padding-top: 12px;
  border-top: 1px solid #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.view-link {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  font-weight: 500;
  color: #2563eb;
  transition: gap 0.2s;
}

.class-card:hover .view-link {
  gap: 8px;
}
```

#### Modal
```css
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  padding: 16px;
}

.modal-dialog {
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 25px 50px -12px rgb(0 0 0 / 0.25);
  max-width: 640px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  padding: 24px;
  border-bottom: 1px solid #e2e8f0;
}

.modal-body {
  padding: 24px;
}

.modal-footer {
  padding: 24px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
```

#### Tabs
```css
.tabs-list {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  background-color: white;
  box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  border-radius: 8px;
  max-width: 672px;
  height: 48px;
}

.tab-trigger {
  padding: 12px 16px;
  font-size: 14px;
  font-weight: 500;
  color: #64748b;
  background-color: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 8px;
}

.tab-trigger:hover {
  color: #334155;
}

.tab-trigger.active {
  background-color: #2563eb;
  color: white;
}

.tab-content {
  margin-top: 24px;
}
```

#### QR Code Modal
```css
.qr-modal {
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 25px 50px -12px rgb(0 0 0 / 0.25);
  max-width: 448px;
  width: 100%;
}

.qr-container {
  background-color: white;
  padding: 24px;
  border-radius: 16px;
  box-shadow: inset 0 2px 4px 0 rgb(0 0 0 / 0.06);
  border: 4px solid #f1f5f9;
}

.qr-info {
  background-color: #f8fafc;
  padding: 16px;
  border-radius: 8px;
  text-align: center;
}
```

### Responsive Design

#### Breakpoints
```css
/* Mobile First Approach */

/* Small devices (landscape phones, 576px and up) */
@media (min-width: 576px) {
  .container {
    max-width: 540px;
  }
}

/* Medium devices (tablets, 768px and up) */
@media (min-width: 768px) {
  .container {
    max-width: 720px;
  }
  
  .md\:grid-cols-2 {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Large devices (desktops, 992px and up) */
@media (min-width: 992px) {
  .container {
    max-width: 960px;
  }
  
  .lg\:grid-cols-3 {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Extra large devices (large desktops, 1200px and up) */
@media (min-width: 1200px) {
  .container {
    max-width: 1140px;
  }
}

/* XXL devices (1400px and up) */
@media (min-width: 1400px) {
  .container {
    max-width: 1280px;
  }
}
```

#### Mobile Optimizations
```css
/* Stack cards on mobile */
@media (max-width: 767px) {
  .grid {
    grid-template-columns: 1fr;
  }
  
  .nav-container {
    flex-direction: column;
    gap: 16px;
  }
  
  .modal-dialog {
    margin: 16px;
  }
  
  .tabs-list {
    font-size: 12px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
}
```

---

## Backend Integration Notes

### API Endpoints (To Be Implemented)

#### Classes
```
GET    /api/classes              - Get all classes for professor
POST   /api/classes              - Create new class
GET    /api/classes/:id          - Get single class details
PUT    /api/classes/:id          - Update class information
DELETE /api/classes/:id          - Delete class
```

#### Schedules
```
POST   /api/classes/:id/schedules     - Add schedule to class
DELETE /api/classes/:id/schedules/:scheduleId - Remove schedule
PUT    /api/classes/:id/schedules/:scheduleId - Update schedule
```

#### Announcements
```
POST   /api/classes/:id/announcements - Create announcement
GET    /api/classes/:id/announcements - Get all announcements
DELETE /api/classes/:id/announcements/:announcementId - Delete announcement
```

#### Attendance
```
POST   /api/attendance/verify-qr      - Verify QR code and mark attendance
GET    /api/classes/:id/attendance    - Get attendance records
GET    /api/attendance/:recordId      - Get specific attendance record
```

#### QR Code
```
POST   /api/qr/generate               - Generate QR code for session
POST   /api/qr/scan                   - Student scans QR code
```

### Data Validation

#### Class Creation
- Subject: Required, string, 1-200 characters
- Section: Optional, string, 1-50 characters
- Room: Optional, string, 1-100 characters
- Description: Optional, string, 0-500 characters

#### Schedule
- Day: Required, enum (Monday-Sunday)
- Start Time: Required, time format (HH:MM)
- End Time: Required, time format (HH:MM), must be after start time

#### Announcement
- Title: Required, string, 1-200 characters
- Content: Required, string, 1-2000 characters

### Security Considerations
1. Professor authentication required for all endpoints
2. QR codes should expire after session ends
3. Students can only mark attendance during active sessions
4. Prevent duplicate attendance entries
5. Rate limiting on QR code generation
6. Validate professor owns the class before modifications

---

## Accessibility Guidelines

### ARIA Labels
```html
<!-- Buttons -->
<button aria-label="Create new class">
  <icon>+</icon> Create Class
</button>

<!-- Navigation -->
<nav aria-label="Main navigation">
  <button aria-label="Back to dashboard">
    <icon>←</icon> Back
  </button>
</nav>

<!-- Tabs -->
<div role="tablist">
  <button role="tab" aria-selected="true">Overview</button>
  <button role="tab" aria-selected="false">Schedule</button>
</div>

<!-- Modal -->
<div role="dialog" aria-labelledby="modal-title" aria-modal="true">
  <h2 id="modal-title">Create New Class</h2>
</div>
```

### Keyboard Navigation
- Tab through all interactive elements
- Enter/Space to activate buttons
- Escape to close modals
- Arrow keys for tab navigation

### Color Contrast
All text meets WCAG AA standards:
- Normal text: 4.5:1 ratio
- Large text: 3:1 ratio
- UI components: 3:1 ratio

### Screen Reader Support
- Meaningful alt text for icons
- Form labels properly associated
- Error messages announced
- Status updates announced

---

## Performance Considerations

### Optimization Strategies
1. Lazy load class detail view
2. Paginate attendance records if > 50
3. Debounce search/filter inputs
4. Cache QR code generation
5. Optimize images (if added later)

### Loading States
```html
<!-- Card skeleton -->
<div class="card skeleton">
  <div class="skeleton-header"></div>
  <div class="skeleton-content"></div>
</div>

<!-- Button loading -->
<button disabled>
  <spinner></spinner> Loading...
</button>
```

---

## Browser Support

### Target Browsers
- Chrome/Edge: Last 2 versions
- Firefox: Last 2 versions
- Safari: Last 2 versions
- Mobile Safari: Last 2 versions
- Chrome Android: Last 2 versions

### Required Features
- CSS Grid
- Flexbox
- CSS Custom Properties
- ES6 JavaScript
- LocalStorage
- Date/Time inputs

---

## Future Enhancements

### Planned Features
1. Export attendance to CSV/Excel
2. Student profile management
3. Attendance analytics and reports
4. Email notifications for announcements
5. Class templates
6. Bulk operations
7. Search and filter classes
8. Calendar view of schedules
9. Student mobile app for scanning
10. Attendance percentage calculations

---

## File Structure

```
project/
├── index.html
├── css/
│   ├── global.css
│   ├── components/
│   │   ├── buttons.css
│   │   ├── cards.css
│   │   ├── forms.css
│   │   ├── modals.css
│   │   └── tabs.css
│   └── pages/
│       ├── dashboard.css
│       └── class-detail.css
├── js/
│   ├── app.js
│   ├── components/
│   │   ├── ClassCard.js
│   │   ├── CreateClassModal.js
│   │   ├── ScheduleManager.js
│   │   └── QRCodeModal.js
│   └── utils/
│       ├── dateUtils.js
│       └── validation.js
└── assets/
    └── icons/
```

---

## Conclusion

This documentation provides a complete reference for implementing the Professor Dashboard Attendance Monitoring System in HTML/CSS. The design emphasizes:

- **Clean, modern UI** with Google Classroom inspiration
- **Intuitive user flow** from class creation to attendance tracking
- **Responsive design** that works on all devices
- **Accessible** components following WCAG guidelines
- **Maintainable** code structure with clear separation of concerns

For backend implementation, focus on:
- RESTful API design
- QR code security and time validation
- Real-time attendance updates
- Scalable database schema

The system is designed to be progressively enhanced with additional features while maintaining simplicity and usability.
