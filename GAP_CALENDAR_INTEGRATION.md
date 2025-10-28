# Gap Calendar Component - Integration Guide

## Quick Integration (10 Minutes)

**Component:** Gap Calendar Visualization
**Target File:** `listingv5.html`
**Insertion Point:** Line 1191 (between Pricing Table and Booked Days sections)

---

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ Access to `listingv5.html` file
- ✅ Text editor (VS Code, Sublime, etc.)
- ✅ Understanding that this component visualizes **gaps** (available dates between bookings)
- ✅ Backup of `listingv5.html` (optional but recommended)

---

## 🎯 What You're Installing

The Gap Calendar Component provides:
- **Visual calendar grid** showing all booking gaps in the 90-day forecast
- **Color-coded gap types** (single night, weekend, long gaps)
- **Interactive tooltips** with gap details and pricing
- **Filters** to show all days or gaps-only, minimum gap size
- **Month navigation** to browse through the 90-day window

---

## 📦 Step 1: Test the Standalone Component

**Before integrating**, test the component standalone to verify it works:

```bash
# Navigate to the Pricelabs directory
cd "/Users/AIRBNB/Cursor_Projects/Pricelabs V4/Pricelabs"

# Open the standalone component in your browser
open gap-calendar-component.html
# OR on Windows:
start gap-calendar-component.html
```

**What you should see:**
- Calendar grid for November 2024
- Mock gaps displayed (3-night gap, 2-night gap, single-night gap, 7-night gap)
- Hover tooltips showing gap details
- Working filter controls and month navigation

**If the component doesn't work standalone, DO NOT integrate it yet.** Debug the standalone version first.

---

## 📝 Step 2: Locate the Integration Point

1. **Open `listingv5.html` in your text editor**

2. **Find the exact insertion point:**
   - Use Find (Ctrl+F / Cmd+F)
   - Search for: `<!-- Booked Days Component -->`
   - You should find this around **line 1192**

3. **Verify the context:**

   **Before (Lines 1185-1190):**
   ```html
                   </thead>
                   <tbody id="pricing-table-body">
                       <!-- Will be populated dynamically -->
                   </tbody>
               </table>
           </div>  <!-- End of pricing table container -->
   ```

   **Insertion point (Line 1191):**
   ```html
           <!-- 🎯 INSERT GAP CALENDAR HERE 🎯 -->
   ```

   **After (Lines 1192-1195):**
   ```html
           <!-- Booked Days Component -->
           <div class="booked-days-component" id="booked-days-section" style="display: none;">
               <div class="booked-days-title">
                   Booked Days vs Market Analysis
   ```

---

## 🎨 Step 3: Add Component CSS

1. **Open `gap-calendar-component.html`** in your editor

2. **Locate the CSS section** (between `<style>` tags, around lines 10-400)

3. **Copy ALL styles** from this comment onwards:
   ```css
   /* ===== GAP CALENDAR COMPONENT STYLES ===== */
   ```

   Down to (but NOT including):
   ```css
   /* ===== Info Banner (for standalone demo) ===== */
   ```

4. **In `listingv5.html`, find the closing `</style>` tag** (around line 1100)

5. **Paste the CSS BEFORE the closing `</style>` tag:**

   ```html
       /* ===== EXISTING STYLES END ===== */

       /* ===== GAP CALENDAR COMPONENT STYLES ===== */
       /* Added: 2024-10-24 - Gap Calendar Component */

       .gap-calendar-container {
           background: white;
           border-radius: 12px;
           /* ... rest of copied CSS ... */
       }

       /* ... all gap calendar styles ... */

   </style>  <!-- Existing closing tag -->
   ```

**✅ Checkpoint:** Save the file. No errors should appear (HTML/CSS syntax is valid).

---

## 🏗️ Step 4: Add Component HTML

1. **Back in `gap-calendar-component.html`**, locate the HTML section:

   **Copy from:**
   ```html
   <!-- ===== GAP CALENDAR COMPONENT HTML ===== -->
   ```

   **To:**
   ```html
   <!-- Global Tooltip Portal Container -->
   <div id="global-tooltip-portal" class="tooltip-portal-container"></div>
   ```

   **Note:** Do NOT copy the demo banner or the `<script>` tag yet.

2. **In `listingv5.html`, at line 1191**, paste the copied HTML:

   ```html
               </table>
           </div>

           <!-- ===== GAP CALENDAR COMPONENT ===== -->
           <!-- Added: 2024-10-24 -->

           <div class="gap-calendar-container table-container" id="gap-calendar-container">
               <!-- Full component HTML here -->
           </div>

           <!-- Global Tooltip Portal Container -->
           <!-- Note: This may already exist in listingv5.html - if so, skip this line -->
           <div id="global-tooltip-portal" class="tooltip-portal-container"></div>

           <!-- Booked Days Component -->
           <div class="booked-days-component" id="booked-days-section" style="display: none;">
   ```

3. **Check for duplicate tooltip portal:**
   - Search `listingv5.html` for `global-tooltip-portal`
   - If it already exists (around line 2862), **DO NOT add it again**
   - Delete the second instance you just pasted

**✅ Checkpoint:** The HTML should be inserted. Visual structure is in place (but not functional yet).

---

## ⚙️ Step 5: Add Component JavaScript

1. **Back in `gap-calendar-component.html`**, locate the JavaScript section:

   **Copy from:**
   ```javascript
   // ===== GLOBAL STATE =====
   ```

   **To:**
   ```javascript
   // ===== INITIALIZATION =====
   ```

   **Include everything EXCEPT:**
   - The `generateMockData()` function (we don't need mock data in integration)
   - The DOMContentLoaded event listener at the very end (we'll call it manually)

2. **In `listingv5.html`, find the existing `<script>` tag** (around line 1281)

3. **Scroll to the end of the existing JavaScript** (around line 2857, before `</script>`)

4. **Paste the copied JavaScript:**

   ```javascript
       // ===== EXISTING DASHBOARD JAVASCRIPT ENDS ===== //

       // ===== GAP CALENDAR COMPONENT JAVASCRIPT =====
       // Added: 2024-10-24

       // Global state for gap calendar
       let gapCalendarData = {
           gaps: [],
           priceData: [],
           currentMonthDate: new Date(),
           filters: {
               displayMode: 'gaps-only',
               minGapSize: 1
           }
       };

       // ... all gap calendar functions ...

   </script>  <!-- Existing closing tag -->
   ```

**⚠️ Important Notes:**

- **DO NOT copy** the mock data function
- **DO NOT copy** the initialization event listener
- **DO copy** all the core functions:
  - `renderGapCalendar()`
  - `identifyGaps()`
  - `classifyDay()`
  - `buildCalendarGrid()`
  - `createDayCell()`
  - `createGapTooltipContent()`
  - `attachGapTooltipHandlers()`
  - `handleDayHover()` / `handleDayLeave()`
  - `showTooltipInPortal()` / `hideTooltip()`
  - `handleGapFilterChange()`
  - `navigateMonth()`
  - `updateMonthLabel()`

**✅ Checkpoint:** JavaScript functions are added. No syntax errors should appear.

---

## 🔌 Step 6: Hook into Data Loading

Now we need to call `renderGapCalendar()` after the pricing data loads.

1. **In `listingv5.html`, find the `loadDashboard()` function** (around line 1340)

2. **Scroll to where dashboard components are rendered** (around line 1444-1448):

   ```javascript
   // Render dashboard components
   updateHeader();
   updateKeyMetrics();
   updateOccupancyChart();
   updatePriceTrendsChart();
   updatePricingTable();
   ```

3. **Add the gap calendar render call AFTER `updatePricingTable()`:**

   ```javascript
   // Render dashboard components
   updateHeader();
   updateKeyMetrics();
   updateOccupancyChart();
   updatePriceTrendsChart();
   updatePricingTable();

   // ===== RENDER GAP CALENDAR =====
   // Added: 2024-10-24
   if (pricingData && pricingData[0] && pricingData[0].data) {
       console.log('[Integration] Rendering Gap Calendar...');
       renderGapCalendar(pricingData[0].data.slice(0, 90));
   } else {
       console.warn('[Integration] No pricing data available for Gap Calendar');
   }
   ```

**✅ Checkpoint:** Gap calendar will now render when data loads.

---

## 🎨 Step 7: Verify Tooltip Portal Integration (Optional)

The Gap Calendar uses the **existing tooltip portal system** from listingv5.html.

**Check if portal functions exist:**

1. Search for `showTooltipInPortal` in `listingv5.html`
2. If found (around line 2477), you're good! The gap calendar will use the existing system.
3. If NOT found, the gap calendar has its own fallback implementation (no action needed).

**If you want to use the existing portal system:**

- The gap calendar's tooltip functions (`handleDayHover`, `showTooltipInPortal`, `hideTooltip`) are compatible
- You can rename the gap calendar versions to avoid conflicts, OR
- Simply let both coexist (they won't interfere)

---

## ✅ Step 8: Test the Integration

1. **Save `listingv5.html`**

2. **Start your Flask server** (or however you run the dashboard):
   ```bash
   python listing_viewer_app.py
   # OR
   python portfolio_manager.py
   ```

3. **Open the dashboard in your browser:**
   ```
   http://localhost:5050/listing?id=YOUR_LISTING_ID
   ```

4. **Verify the Gap Calendar appears:**
   - Should be between "90-Day Pricing Forecast" table and "Booked Days vs Market Analysis"
   - Should show a calendar grid with days of the week
   - Should show gaps highlighted in green
   - Hover should show tooltips with gap details

**Expected Appearance:**

```
┌─────────────────────────────────────────────┐
│ 90-Day Pricing Forecast                    │
│ [Large table with pricing data]            │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐  ← NEW COMPONENT
│ Gap Calendar - Available Booking Dates     │
│ ┌──────────────────────────────────────┐   │
│ │ Su Mo Tu We Th Fr Sa                 │   │
│ │ ⬜ ⬜ 🟢 🟢 🟢 ⬜ ⬜  (Week 1)         │   │
│ │ ⬜ 🟢 🟢 ⬜ ⬜ ⬜ ⬜  (Week 2)         │   │
│ └──────────────────────────────────────┘   │
│ [Legend: Available, Weekend, Single, etc.]  │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Booked Days vs Market Analysis             │
│ [Existing component]                        │
└─────────────────────────────────────────────┘
```

---

## 🧪 Testing Checklist

### Visual Tests

- [ ] Calendar grid renders correctly
- [ ] Day headers (Su, Mo, Tu, We, Th, Fr, Sa) are visible
- [ ] Gap days are highlighted in green
- [ ] Booked days are grayed out (in "All Days" mode)
- [ ] Today's date has a blue border highlight
- [ ] Gap length badges show on multi-day gaps
- [ ] Prices display under each day number

### Interaction Tests

- [ ] **Hover tooltips work** - Hover over any gap day shows details
- [ ] **Filter: "Gaps Only" vs "All Days"** - Switching changes display
- [ ] **Filter: Minimum gap size** - Filtering to "2+ Nights" hides single-night gaps
- [ ] **Month navigation** - Previous/Next buttons work
- [ ] **Current month label** updates when navigating

### Data Tests

- [ ] **Gap detection works** - Gaps are correctly identified between bookings
- [ ] **Gap types are classified** - Single (orange), Long (dark green), Weekend (darker green)
- [ ] **Tooltip data is accurate** - Check-in/out dates match booking windows
- [ ] **No console errors** - Open browser DevTools, check for red errors

---

## 🔧 Troubleshooting

### Problem: Calendar doesn't appear at all

**Possible causes:**
1. **CSS not loaded** - Check browser DevTools (Inspect Element) for `.gap-calendar-container`
2. **JavaScript error** - Check browser Console for errors
3. **No pricing data** - Check if `pricingData` is defined and has data

**Solutions:**
```javascript
// Debug: Check if data exists
console.log('pricingData:', pricingData);
console.log('Gap Calendar rendering:', pricingData && pricingData[0]);

// Debug: Force render with specific data
renderGapCalendar(pricingData[0].data.slice(0, 90));
```

---

### Problem: Gaps not detected correctly

**Possible causes:**
1. **Data format mismatch** - `demand_desc` field missing or different
2. **Date format issues** - Dates not in "YYYY-MM-DD" format

**Solutions:**
```javascript
// Debug: Check data structure
console.log('First day sample:', pricingData[0].data[0]);

// Verify demand_desc values
pricingData[0].data.slice(0, 10).forEach(day => {
    console.log(day.date, day.demand_desc);
});
```

---

### Problem: Tooltips not showing

**Possible causes:**
1. **Portal container missing** - `#global-tooltip-portal` doesn't exist
2. **Event listeners not attached** - `attachGapTooltipHandlers()` not called
3. **CSS z-index conflict** - Other elements blocking tooltips

**Solutions:**
```javascript
// Debug: Check portal exists
console.log('Tooltip portal:', document.getElementById('global-tooltip-portal'));

// Debug: Check event listeners attached
const days = document.querySelectorAll('.gap-calendar-day.gap');
console.log('Gap days with listeners:', days.length);

// Manually test tooltip
const firstGap = document.querySelector('.gap-calendar-day.gap');
if (firstGap) {
    const tooltip = firstGap.querySelector('.gap-tooltip');
    console.log('First gap tooltip:', tooltip);
}
```

---

### Problem: Styling looks wrong

**Possible causes:**
1. **CSS conflicts** - Existing styles overriding gap calendar styles
2. **Class names collision** - `.table-container` conflicts
3. **Responsive design issues** - Viewport too small

**Solutions:**
```css
/* Add higher specificity to gap calendar styles */
#gap-calendar-container.gap-calendar-container {
    /* Force styles */
}

/* Debug: Check computed styles */
.gap-calendar-day.gap {
    background: #e8f5e9 !important; /* Force green background */
}
```

---

### Problem: Filters don't work

**Possible causes:**
1. **`onchange` handlers not connected** - Check HTML attributes
2. **Filter function renamed** - Check function exists

**Solutions:**
```javascript
// Debug: Test filter manually
document.getElementById('gap-display-filter').value = 'all-days';
handleGapFilterChange();

// Check function exists
console.log('Filter function:', typeof handleGapFilterChange);
```

---

## 🎛️ Configuration Options

### Change Default Display Mode

In the JavaScript, modify `gapCalendarData` initialization:

```javascript
let gapCalendarData = {
    gaps: [],
    priceData: [],
    currentMonthDate: new Date(),
    filters: {
        displayMode: 'all-days',  // Changed from 'gaps-only'
        minGapSize: 2             // Changed from 1
    }
};
```

Then update the HTML `<select>` default:

```html
<select id="gap-display-filter" class="filter-select" onchange="handleGapFilterChange()">
    <option value="gaps-only">Gaps Only</option>
    <option value="all-days" selected>All Days (Gaps Highlighted)</option>
</select>
```

---

### Customize Gap Colors

In the CSS, modify the color variables:

```css
/* Available day (gap) - base green */
.gap-calendar-day.gap {
    background: #e3f2fd;       /* Light blue instead of green */
    border-color: #90caf9;
}

/* Weekend gap - darker */
.gap-calendar-day.gap-weekend {
    background: #bbdefb;
    border-color: #64b5f6;
}

/* Single night gap - orange/red */
.gap-calendar-day.gap-single {
    background: #ffebee;       /* Light red */
    border-color: #ef9a9a;
}
```

---

### Adjust Calendar Cell Size

For larger/smaller cells, modify:

```css
.gap-calendar-day {
    aspect-ratio: 1;          /* Keep square */
    min-height: 80px;         /* Increase from 60px for larger cells */
}

@media (max-width: 768px) {
    .gap-calendar-day {
        min-height: 40px;     /* Smaller on mobile */
    }
}
```

---

### Change Initial Month

To start on the first month with gaps (instead of current month):

```javascript
function renderGapCalendar(priceData) {
    gapCalendarData.priceData = priceData;
    gapCalendarData.gaps = identifyGaps(priceData);

    // Set to first gap month
    if (gapCalendarData.gaps.length > 0) {
        gapCalendarData.currentMonthDate = new Date(gapCalendarData.gaps[0].startDate);
    } else {
        gapCalendarData.currentMonthDate = new Date();  // Fallback to today
    }

    buildCalendarGrid();
    updateMonthLabel();
    attachGapTooltipHandlers();
}
```

---

## 🗑️ How to Remove the Component

If you need to remove the Gap Calendar:

1. **Remove HTML** - Delete the entire `<div class="gap-calendar-container">` block (line 1191+)

2. **Remove CSS** - Delete all styles under `/* ===== GAP CALENDAR COMPONENT STYLES =====` `

3. **Remove JavaScript** - Delete all gap calendar functions (search for "GAP CALENDAR")

4. **Remove render call** - Delete the `renderGapCalendar()` call from `loadDashboard()`

5. **Remove tooltip portal** (if added) - Delete `<div id="global-tooltip-portal">` if you added it

---

## 📊 Component Performance

**Expected performance:**
- **Render time:** < 100ms for 90 days of data
- **Memory usage:** Negligible (< 1MB)
- **DOM elements:** ~35-42 cells per month × 3 months = ~105-126 elements
- **No impact** on existing dashboard components

**Optimization tips:**
- Gap calculations are cached after first render
- Calendar only re-renders on filter changes or month navigation
- Tooltips use portal system (not duplicated per cell)

---

## 🎓 Understanding the Code

### Data Flow

```
pricingData[0].data (90 days)
    ↓
identifyGaps() → Array of gap objects
    ↓
classifyDay() → Metadata for each day
    ↓
buildCalendarGrid() → DOM elements
    ↓
attachGapTooltipHandlers() → Interactive tooltips
```

### Key Functions

| Function | Purpose | When Called |
|----------|---------|-------------|
| `renderGapCalendar()` | Main entry point | After data loads |
| `identifyGaps()` | Find all gaps | On initial render |
| `classifyDay()` | Determine day type | Per day render |
| `buildCalendarGrid()` | Create calendar HTML | On render/filter |
| `attachGapTooltipHandlers()` | Setup interactions | After grid built |
| `handleGapFilterChange()` | Apply filters | User changes filter |
| `navigateMonth()` | Change month view | User clicks nav buttons |

---

## 📚 Additional Resources

### Related Documentation

- `GAP_CALENDAR_ANALYSIS.md` - Detailed codebase analysis
- `GAP_CALENDAR_BUILD_PLAN.md` - Component architecture design
- `gap-calendar-component.html` - Standalone test version

### Useful Searches in listingv5.html

```javascript
// Find existing tooltip system
Search: "showTooltipInPortal"

// Find data loading sequence
Search: "loadDashboard"

// Find pricing table render
Search: "updatePricingTable"

// Find day.js usage
Search: "dayjs"
```

---

## ✅ Final Checklist

Before considering integration complete:

- [ ] Standalone component tested and working
- [ ] CSS copied to listingv5.html
- [ ] HTML inserted at line 1191
- [ ] JavaScript functions added to `<script>`
- [ ] Render call added to `loadDashboard()`
- [ ] Browser testing completed (Chrome, Firefox, Safari)
- [ ] Responsive design verified (desktop, tablet, mobile)
- [ ] Tooltips working properly
- [ ] Filters functional
- [ ] Month navigation working
- [ ] No console errors
- [ ] No visual conflicts with existing components
- [ ] Performance is acceptable
- [ ] Code is well-commented

---

## 🎉 Integration Complete!

You should now have a fully functional Gap Calendar component showing booking gaps in your PriceLabs dashboard.

**What to do next:**

1. **Use it!** - Identify gaps to focus on booking
2. **Customize** - Adjust colors, sizes, or default filters to your preference
3. **Share feedback** - Note any issues or improvement ideas
4. **Extend** - Consider adding features like:
   - Click to focus a specific gap
   - Export gap data to CSV
   - Gap analytics summary
   - Integration with booking platforms

---

**Need help?** Check the troubleshooting section or review the source files:
- `gap-calendar-component.html` - Full standalone version
- `GAP_CALENDAR_BUILD_PLAN.md` - Technical architecture details
- `GAP_CALENDAR_ANALYSIS.md` - Codebase analysis

---

**Version:** 1.0
**Created:** 2024-10-24
**Component:** Gap Calendar Visualization
**Status:** Production Ready ✅
