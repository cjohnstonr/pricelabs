# Gap Calendar Component - Codebase Analysis

## Phase 1: Comprehensive Analysis of listingv5.html

**Date:** 2025-10-24
**Analyzed File:** `/Users/AIRBNB/Cursor_Projects/Pricelabs V4/Pricelabs/listingv5.html`
**Purpose:** Understand existing patterns to build a seamless Gap Calendar component

---

## 1. Data Structure Documentation

### Primary Data Source: `pricingData`

**Location:** Global variable initialized at line 1284

**Structure:**
```javascript
pricingData = [
  {
    data: [
      {
        date: "2024-11-01",              // YYYY-MM-DD format
        price: 150,                       // Our nightly price
        demand_desc: "Medium Demand",     // OR "Unavailable" for booked
        min_stay: 2,                      // Minimum stay requirement
        adjustment_percent: 5.2,          // Price adjustment percentage
        // Additional fields from market data:
        // - Market percentiles (accessed separately via neighborhoodData)
        // - Occupancy rates (accessed separately)
      },
      // ... 90 days of data
    ]
  }
]
```

**Access Pattern:**
```javascript
// Get 90-day forecast
const priceData = pricingData[0].data.slice(0, 90);

// Check if day is booked
const isBooked = day.demand_desc === 'Unavailable';

// Check if day is available
const isAvailable = day.demand_desc !== 'Unavailable';
```

### Supporting Data: `neighborhoodData`

**Location:** Global variable for market data

**Relevant Fields:**
- `Future Percentile Prices` - Market pricing percentiles by bedroom count
- `Future Occ/New/Canc` - Market occupancy data
- Accessed via `neighborhoodData.data['Future Percentile Prices']`

**Usage in Gap Calendar:**
```javascript
// Get market median for tooltip comparison
if (percentileData && percentileData.Y_values) {
  const dateIndex = percentileData.X_values.indexOf(day.date);
  const medianPrice = percentileData.Y_values[3][dateIndex]; // Index 3 = median
}
```

---

## 2. Gap Detection Algorithm Analysis

### Existing Implementation: `calculateGapNights()`

**Location:** Lines 1920-1955 in `updatePricingTable()`

**Core Logic:**
```javascript
function calculateGapNights(index) {
    const currentDay = priceData[index];

    // Only calculate for available days
    if (currentDay.demand_desc === 'Unavailable') return 0;

    // Count total unavailable days in dataset
    const totalUnavailableDays = priceData.filter(day =>
        day.demand_desc === 'Unavailable'
    ).length;

    if (totalUnavailableDays === 0) return 'N/A';

    // Find previous unavailable day
    let prevUnavailableIndex = -1;
    for (let i = index - 1; i >= 0; i--) {
        if (priceData[i].demand_desc === 'Unavailable') {
            prevUnavailableIndex = i;
            break;
        }
    }

    // Find next unavailable day
    let nextUnavailableIndex = -1;
    for (let i = index + 1; i < priceData.length; i++) {
        if (priceData[i].demand_desc === 'Unavailable') {
            nextUnavailableIndex = i;
            break;
        }
    }

    // Must have bookings on both sides to be a gap
    if (prevUnavailableIndex === -1 || nextUnavailableIndex === -1) {
        return 'N/A'; // Not a gap, just continuous availability
    }

    // Count consecutive available days between the bookings
    return nextUnavailableIndex - prevUnavailableIndex - 1;
}
```

**Key Insights:**
- ✅ A gap requires unavailable days on BOTH sides
- ✅ Returns 'N/A' for continuous availability (no bookings bounding it)
- ✅ Returns 0 for unavailable days themselves
- ✅ Returns actual gap length for available days within gaps

**Enhancement Needed for Calendar:**

The existing function works per-day. We need to **group consecutive available days into gap objects**:

```javascript
// Proposed enhancement: identifyGaps()
function identifyGaps(priceData) {
  const gaps = [];
  let currentGap = null;

  for (let i = 0; i < priceData.length; i++) {
    const day = priceData[i];

    if (day.demand_desc === 'Unavailable') {
      // Close current gap if exists
      if (currentGap) {
        gaps.push(currentGap);
        currentGap = null;
      }
    } else {
      // Available day - start or extend gap
      if (!currentGap) {
        currentGap = {
          startDate: day.date,
          startIndex: i,
          days: [day],
          prevBookingEndIndex: i - 1 // For context
        };
      } else {
        currentGap.days.push(day);
      }
    }
  }

  // Close final gap if exists
  if (currentGap) {
    gaps.push(currentGap);
  }

  // Filter to only TRUE gaps (bounded by bookings)
  return gaps.filter(gap => {
    const hasPrevBooking = gap.startIndex > 0 &&
      priceData[gap.startIndex - 1].demand_desc === 'Unavailable';
    const hasNextBooking = gap.startIndex + gap.days.length < priceData.length &&
      priceData[gap.startIndex + gap.days.length].demand_desc === 'Unavailable';

    return hasPrevBooking || hasNextBooking; // At least one side bounded
  });
}
```

---

## 3. Existing Code Patterns & Conventions

### JavaScript Patterns

**1. Date Handling:**
```javascript
// Uses dayjs library (loaded at line 10)
const date = dayjs(day.date);
const dayOfWeek = date.format('ddd');      // "Mon", "Tue", etc.
const fullDate = date.format('MMM D, YYYY'); // "Nov 4, 2024"
const isWeekend = dayOfWeek === 'Sat' || dayOfWeek === 'Sun';
```

**2. DOM Manipulation:**
```javascript
// Vanilla JavaScript (no jQuery)
const tbody = document.getElementById('pricing-table-body');
tbody.innerHTML = '';

const row = document.createElement('tr');
row.className = 'weekend'; // Add class for styling

tbody.appendChild(row);
```

**3. Async Data Loading:**
```javascript
// Lines 1345-1393: Async/await pattern
async function loadDashboard() {
  try {
    const response = await fetch(`http://localhost:5050/api/listing/${listingId}`);
    const data = await response.json();
    // Process data...
  } catch (error) {
    console.error('Error loading data:', error);
  }
}
```

**4. Event Handling:**
```javascript
// Inline handlers in HTML
onchange="updatePricingTable()"

// Programmatic listeners
badge.addEventListener('mouseenter', handleBadgeHover);
badge.addEventListener('mouseleave', handleBadgeLeave);
```

### CSS Patterns

**1. Container Cards:**
```css
.table-container, .chart-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    margin-bottom: 30px;
}
```

**2. Color System:**
```css
/* Primary Actions */
--primary: #667eea;

/* Status Colors */
--success: #16a34a;    /* Green - good performance */
--warning: #facc15;    /* Yellow - moderate */
--danger: #dc2626;     /* Red - poor performance */

/* Neutral Colors */
--gray-50: #f8fafc;
--gray-100: #f1f5f9;
--gray-200: #e2e8f0;
--gray-600: #64748b;
--gray-900: #1a202c;
```

**3. Typography:**
```css
/* Headers */
h3 { font-size: 18px; font-weight: 600; color: #1a202c; }

/* Labels */
.meta-item { font-size: 14px; color: #64748b; }

/* Small Text */
thead th { font-size: 12px; font-weight: 600; color: #64748b; }
```

**4. Badge Styling:**
```css
.demand-high {
    background: #dcfce7;
    color: #15803d;
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
}
```

---

## 4. Tooltip Portal System (Recently Implemented)

### Architecture

**Global Portal Container:**
- Element ID: `#global-tooltip-portal`
- Created at: Line 2388-2398 (`createTooltipPortal()`)
- Location: Appended to `<body>` at line 2862
- Purpose: Fixed-position container for all tooltips to avoid overflow issues

**Key Functions:**

1. **`createTooltipPortal()`** (Line 2388)
   - Creates global container if doesn't exist
   - Called once on DOMContentLoaded

2. **`initializeTooltipPortals()`** (Line 2405)
   - Finds all `.booking-window-status` badges
   - Attaches hover listeners
   - Called after table render

3. **`showTooltipInPortal(badge, tooltip)`** (Line 2477)
   - Calculates badge position via `getBoundingClientRect()`
   - Moves tooltip to portal
   - Applies fixed positioning
   - Centers horizontally with `translateX(-50%)`

4. **`hideTooltip(tooltip)`** (Line 2514)
   - Fades out with CSS transition
   - Returns tooltip to original parent
   - Resets inline styles

### Tooltip HTML Structure

```html
<span class="booking-window-status success">
    14 days early
    <div class="booking-window-tooltip">
        <strong>Booking Window Details</strong>
        <hr>
        <div class="tooltip-row">
            <span class="tooltip-label">Month:</span>
            <span class="tooltip-value">November</span>
        </div>
        <div class="tooltip-row">
            <span class="tooltip-label">Typical window:</span>
            <span class="tooltip-value">45 days</span>
        </div>
        <div class="tooltip-info">
            <em>Market books November dates ~45 days ahead</em>
        </div>
    </div>
</span>
```

### Tooltip CSS (Lines 833-915)

```css
.booking-window-tooltip {
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%) translateY(4px);
    background: rgba(0, 0, 0, 0.9);
    color: white;
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 12px;
    min-width: 250px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease, transform 0.2s ease;
    z-index: 9999;
}

.booking-window-tooltip::before {
    content: '';
    position: absolute;
    top: -6px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-bottom: 6px solid rgba(0, 0, 0, 0.9);
}
```

**Usage Pattern for Gap Calendar:**
```javascript
// When creating gap calendar tooltips:
// 1. Use same CSS classes
// 2. Follow same HTML structure
// 3. Call initializeTooltipPortals() after rendering
// 4. Portal system handles positioning automatically
```

---

## 5. Visual Design System

### Layout Grid

**Container Structure:**
```html
<div class="table-container"> <!-- or .chart-card -->
    <div class="table-header">
        <h3>Section Title</h3>
        <div class="filter-container">
            <!-- Controls -->
        </div>
    </div>
    <div class="table-body">
        <!-- Content -->
    </div>
</div>
```

### Status Badge System

**Demand Indicators:**
```css
.demand-high     { background: #dcfce7; color: #15803d; }
.demand-medium   { background: #fef9c3; color: #a16207; }
.demand-low      { background: #fee2e2; color: #dc2626; }
.demand-unavailable { background: #f1f5f9; color: #64748b; }
```

**Performance Badges:**
```css
.booking-window-status.success  { background: #dcfce7; color: #15803d; }
.booking-window-status.warning  { background: #fef3c7; color: #d97706; }
.booking-window-status.danger   { background: #fee2e2; color: #dc2626; }
```

### Spacing & Rhythm

```css
/* Vertical spacing */
margin-bottom: 30px;  /* Between major sections */
margin-bottom: 20px;  /* Between subsections */
margin-bottom: 8px;   /* Between related items */

/* Padding */
padding: 24px;        /* Card containers */
padding: 12px 16px;   /* Table cells, buttons */
padding: 4px 8px;     /* Badges, small elements */

/* Gaps */
gap: 20px;           /* Flex/grid main spacing */
gap: 10px;           /* Flex/grid tight spacing */
```

---

## 6. Integration Points

### Exact Insertion Location

**Target Area:** Between Pricing Table and Booked Days Component

**Line 1190:**
```html
            </div>  <!-- Close pricing table container -->

            <!-- 🎯 INSERT GAP CALENDAR HERE 🎯 -->

            <!-- Booked Days Component -->
            <div class="booked-days-component" id="booked-days-section" style="display: none;">
```

**Before Context (Lines 1185-1190):**
```html
                    </thead>
                    <tbody id="pricing-table-body">
                        <!-- Will be populated dynamically -->
                    </tbody>
                </table>
            </div>  <!-- End of .table-container for pricing table -->
```

**After Context (Lines 1192-1199):**
```html
            <!-- Booked Days Component -->
            <div class="booked-days-component" id="booked-days-section" style="display: none;">
                <div class="booked-days-title">
                    Booked Days vs Market Analysis
                    <div class="booked-days-property-info" id="booked-days-property-info">
                        <!-- Property info will be populated dynamically -->
                    </div>
                </div>
```

### Integration Snippet Template

```html
<!-- Line 1191 - INSERT GAP CALENDAR HERE -->

<!-- Gap Calendar Component -->
<div class="table-container" id="gap-calendar-container">
    <div class="table-header">
        <h3>Gap Calendar - Available Dates</h3>
        <div class="filter-container">
            <!-- Filter controls -->
        </div>
    </div>

    <div id="gap-calendar-body">
        <!-- Calendar grid will be rendered here -->
    </div>

    <div class="gap-calendar-legend">
        <!-- Legend -->
    </div>
</div>
```

---

## 7. Data Flow & Initialization Sequence

### Current Load Sequence

**Lines 1340-1448:**

```javascript
async function loadDashboard() {
    // 1. Get listing info (line 1347)
    const listingResponse = await fetch(`/api/listing/${listingId}`);
    listingData = await listingResponse.json();

    // 2. Get pricing data (line 1358)
    const pricesResponse = await fetch(`/api/listing_prices/${listingId}`);
    pricingData = await pricesResponse.json();

    // 3. Get neighborhood data (line 1369)
    const neighborhoodResponse = await fetch(`/api/neighborhood/${listingId}`);
    neighborhoodData = await neighborhoodResponse.json();

    // 4. Render dashboard components (line 1444-1448)
    updateHeader();
    updateKeyMetrics();
    updateOccupancyChart();
    updatePriceTrendsChart();
    updatePricingTable();  // ← Pricing table rendered here
}
```

**Gap Calendar Integration Point:**

```javascript
// In loadDashboard(), after line 1448:
updatePricingTable();

// 🎯 ADD GAP CALENDAR RENDER HERE
renderGapCalendar(pricingData[0].data);
```

---

## 8. Sample Data Format

### Typical Day Object

```javascript
{
  "date": "2024-11-04",
  "price": 175,
  "demand_desc": "Medium Demand",  // OR "Unavailable" for booked
  "min_stay": 2,
  "adjustment_percent": 3.5,
  "demand_pct": 0.65
}
```

### Sample 90-Day Dataset Structure

```javascript
const priceData = [
  { date: "2024-11-01", price: 150, demand_desc: "Unavailable", min_stay: 1 },
  { date: "2024-11-02", price: 150, demand_desc: "Unavailable", min_stay: 1 },
  { date: "2024-11-03", price: 165, demand_desc: "Low Demand", min_stay: 2 },    // ← Gap start
  { date: "2024-11-04", price: 170, demand_desc: "Medium Demand", min_stay: 2 }, // ← Gap
  { date: "2024-11-05", price: 175, demand_desc: "Medium Demand", min_stay: 2 }, // ← Gap end
  { date: "2024-11-06", price: 150, demand_desc: "Unavailable", min_stay: 1 },
  // ... 84 more days
];

// Gap identified: Nov 3-5 (3 nights)
```

---

## 9. Edge Cases to Handle

### Scenario 1: No Bookings in 90-Day Window
```javascript
// All days available - entire period is one "gap"
// Should we show this? Or mark as "No gaps (no bookings)"?
// DECISION: Show as continuous availability, not a gap
```

### Scenario 2: No Gaps (Fully Booked)
```javascript
// All days unavailable
// Display: "No gaps found - Fully booked!"
// Show empty state with encouraging message
```

### Scenario 3: Gap at Start of Window
```javascript
// First days available, then booking
// Nov 1-3: Available, Nov 4+: Booked
// DECISION: Show as gap (bounded on one side)
```

### Scenario 4: Gap at End of Window
```javascript
// Last days available after final booking
// ... Nov 87: Booked, Nov 88-90: Available
// DECISION: Show as gap (bounded on one side)
```

### Scenario 5: Single-Day Gap
```javascript
// Nov 5: Booked, Nov 6: Available, Nov 7: Booked
// DECISION: Show as 1-night gap (harder to fill)
// Special styling/indicator for single-day gaps
```

### Scenario 6: Partial Month at Edges
```javascript
// 90-day window may start mid-month
// Calendar should handle partial months gracefully
// Show month name even if only a few days visible
```

---

## 10. Recommended Color Scheme for Gap Calendar

### Gap Categories

Based on existing color system:

```css
/* Available days (gaps) - variations by context */
.gap-day {
  background: #e8f5e9;      /* Light green - base gap color */
  border: 1px solid #a5d6a7;
  color: #1b5e20;
}

.gap-day.weekend {
  background: #c8e6c9;      /* Darker green - weekend premium */
  border: 1px solid #81c784;
}

.gap-day.single {
  background: #fff3e0;      /* Orange tint - single-day gap (challenging) */
  border: 1px solid #ffcc80;
  color: #e65100;
}

.gap-day.long {
  background: #a5d6a7;      /* Rich green - 3+ nights (ideal) */
  border: 1px solid #66bb6a;
  color: #1b5e20;
}

/* Booked days (context only - dimmed) */
.booked-day {
  background: #f5f5f5;      /* Light gray - booked/unavailable */
  border: 1px solid #e0e0e0;
  color: #9e9e9e;
  opacity: 0.6;
}

/* Current date highlight */
.calendar-day.today {
  border: 2px solid #667eea; /* Primary color */
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}
```

### Gap Length Indicators

```css
/* Badge overlays on multi-day gaps */
.gap-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  background: #1b5e20;
  color: white;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 600;
}

.gap-badge.short { background: #e65100; } /* 1-2 nights */
.gap-badge.medium { background: #2e7d32; } /* 3-4 nights */
.gap-badge.long { background: #1b5e20; } /* 5+ nights */
```

---

## 11. Performance Considerations

### Data Size
- **90 days** = Maximum 90 day objects
- **Calendar cells** = ~35-42 per month × 3 months = ~105-126 DOM elements
- **Tooltips** = Portal-based (shared, not duplicated)

### Rendering Strategy
```javascript
// Efficient approach:
// 1. Calculate gaps ONCE when data loads
// 2. Cache gap objects
// 3. Render calendar grid from cached data
// 4. Only re-render on filter changes

let cachedGaps = null;

function renderGapCalendar(priceData) {
  if (!cachedGaps) {
    cachedGaps = identifyGaps(priceData);
  }

  buildCalendarGrid(cachedGaps, priceData);
  attachTooltipHandlers();
}
```

### DOM Manipulation
```javascript
// Use DocumentFragment for batch inserts
const fragment = document.createDocumentFragment();

days.forEach(day => {
  const cell = createDayCell(day);
  fragment.appendChild(cell);
});

container.appendChild(fragment); // Single DOM update
```

---

## 12. Accessibility Considerations

### Semantic HTML
```html
<table role="grid" aria-label="Gap Calendar">
  <thead>
    <tr>
      <th scope="col">Su</th>
      <th scope="col">Mo</th>
      <!-- ... -->
    </tr>
  </thead>
  <tbody>
    <tr>
      <td aria-label="Sunday, November 3, 2024 - Available (3-night gap)">
        3
      </td>
    </tr>
  </tbody>
</table>
```

### Keyboard Navigation
```javascript
// Make calendar cells keyboard accessible
cell.setAttribute('tabindex', '0');
cell.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    // Show tooltip or detail modal
  }
});
```

---

## Summary & Recommendations

### ✅ Ready to Use

1. **Data Source:** `pricingData[0].data.slice(0, 90)` - well-structured, reliable
2. **Gap Logic:** Existing `calculateGapNights()` provides solid foundation
3. **Tooltip System:** Recently implemented portal system is perfect for our needs
4. **Styling:** Comprehensive design system with clear patterns
5. **Integration Point:** Clean insertion location identified (line 1191)

### 🔧 Enhancements Needed

1. **Gap Grouping:** Convert per-day calculation to gap object grouping
2. **Calendar Grid:** Build month-based grid layout system
3. **Filter Controls:** Add gap size filtering (all/2+/3+/week+)
4. **Month Navigation:** If showing multiple months, add prev/next controls

### 🎯 Next Steps

1. ✅ **Phase 1 Complete** - Codebase analyzed
2. ⏭️ **Phase 2** - Design component architecture
3. ⏭️ **Phase 3** - Implement gap detection algorithm
4. ⏭️ **Phase 4** - Build standalone component
5. ⏭️ **Phase 5** - Create integration guide

---

**Analysis Complete!** Ready to proceed to Phase 2: Component Design & Planning.
