# AI Agent Prompt: Build Gap Calendar Visualization Component

## 🎯 Mission Objective

Create a standalone, drop-in calendar component that visualizes booking **gaps only** (available date ranges between bookings) from the 90-Day Pricing Forecast data, with rich hover interactions and clean calendar-grid layout.

---

## 📋 Phase 1: Codebase Analysis (REQUIRED FIRST)

### Your First Task: Analyze Current Implementation

**File to Analyze:** `/Users/AIRBNB/Cursor_Projects/Pricelabs V4/Pricelabs/listingv5.html`

**What You Must Understand:**

1. **Data Structure Analysis:**
   - How is pricing data stored? (Look for `pricingData`, `priceData` variables)
   - What API endpoints provide the data? (Look for `/api/` fetch calls)
   - What fields are available per day? (date, price, demand_desc, min_stay, etc.)
   - How is "Unavailable" status determined? (`demand_desc === 'Unavailable'`)
   - Where is the gap nights calculation logic? (Search for `calculateGapNights` function)

2. **Existing Code Patterns:**
   - How does `updatePricingTable()` function work?
   - What JavaScript conventions are used? (vanilla JS, async/await, etc.)
   - How are date formatting done? (dayjs library? native Date?)
   - What CSS framework/styling patterns exist? (inline styles, classes?)
   - How are tooltips currently implemented? (we just built portal system)

3. **Visual Design System:**
   - What color scheme is used? (Extract from CSS variables or existing styles)
   - What typography/font sizes? (Check existing table headers, cards)
   - What spacing/padding conventions? (Look at `.table-container`, `.chart-card`)
   - How are status badges styled? (`.booking-window-status`, `.demand-badge`)
   - What's the card/container design pattern? (border-radius, shadows, etc.)

4. **Integration Points:**
   - Where does "90-Day Pricing Forecast Table" end in the HTML? (Find `</table>` after pricing table)
   - Where does "Booked Days vs Market Analysis" section start? (Find `id="booked-days-section"`)
   - What's the exact insertion point for new component?
   - What container classes are used for sections? (`.table-container`, `.chart-card`)

5. **Gap Detection Logic:**
   - Review the existing `calculateGapNights()` function (around line 1900)
   - Understand how it identifies gaps between unavailable days
   - Note edge cases: gaps at start/end, no gaps, single-day gaps
   - Understand filter logic (available vs all days)

**Deliverable 1:** Create `GAP_CALENDAR_ANALYSIS.md` with:
- Data structure documentation
- Gap detection algorithm explanation
- Existing styling conventions
- Integration points identified
- Sample data format

---

## 🎨 Phase 2: Component Design & Planning

### Your Second Task: Design the Gap Calendar Component

**Requirements:**

### A. Functional Requirements

**Primary Goal:** Help users quickly identify and understand booking gaps visually

**Must Have:**
1. **Show ONLY gaps** - Available date ranges between bookings
2. **Calendar grid layout** - Traditional month/week view
3. **Day of week headers** - Su, Mo, Tu, We, Th, Fr, Sa
4. **Gap highlighting** - Visual distinction for gap days vs booked days
5. **Hover interactions** - Rich tooltips with gap details
6. **Responsive design** - Works on desktop, adapts to screen size

**Gap Definition:**
```
A "gap" is a sequence of consecutive AVAILABLE days that:
- Are surrounded by UNAVAILABLE days (bookings) on both sides
- OR extend to the start/end of the 90-day window
- Have at least 1 night (can be single-day gaps)
```

**Data to Display:**

**On Calendar Card (visible):**
- Date number (1, 2, 3, etc.)
- Gap indicator (visual cue - color, icon, border)
- Gap length badge (e.g., "3 nights" for multi-day gaps)

**On Hover Tooltip (detailed):**
- Full date (e.g., "Monday, November 4, 2024")
- Day of week
- Gap duration (e.g., "Part of 5-night gap")
- Price for that night (from pricing data)
- Market median price (if available)
- Our price vs market (percentage)
- Min stay requirement
- Previous booking check-out date
- Next booking check-in date

### B. Visual Design Requirements

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│  Gap Calendar - November 2024                    [Filter]│
├─────────────────────────────────────────────────────────┤
│  Su   Mo   Tu   We   Th   Fr   Sa                       │
├─────────────────────────────────────────────────────────┤
│       [1]  [2]  [3]  [4]  [5]  [6]   ← Booked (dim)     │
│  [7]  [8]  [9] [10] [11] [12] [13]   ← Gap (highlighted)│
│ [14] [15] [16] [17] [18] [19] [20]   ← Booked (dim)     │
│ [21] [22] [23] [24] [25] [26] [27]   ← Gap (highlighted)│
│ [28] [29] [30]                                           │
└─────────────────────────────────────────────────────────┘

Legend:
- Dim/grayed out = Booked (unavailable) - shown for context
- Highlighted/colored = Gap (available) - the focus
- Hover any date → Tooltip with details
```

**Color Scheme Suggestions:**
- **Gap days:** Light green/blue background (#e8f5e9 or similar)
- **Booked days:** Light gray background (#f5f5f5)
- **Weekend gaps:** Slightly darker green (premium pricing opportunity)
- **Single-day gaps:** Orange tint (harder to fill)
- **Multi-day gaps (3+):** Richer green (ideal for bookings)
- **Current date:** Subtle border highlight

**Card Styling:**
- Match existing `.chart-card` or `.table-container` style
- Card shadow: `0 1px 3px rgba(0,0,0,0.05)` (match existing)
- Border radius: `12px` (match existing)
- Padding: `24px` (match existing)
- Background: `white`

### C. Technical Requirements

**Component Architecture:**
```
gap-calendar-component/
├── gap-calendar.html       # Standalone HTML with embedded CSS/JS
├── gap-calendar.css        # Optional: Separate styles (or inline)
├── gap-calendar.js         # Optional: Separate logic (or inline)
└── README.md              # Integration instructions
```

**OR Single File Approach (RECOMMENDED):**
```
gap-calendar-component.html  # Everything in one file for easy drop-in
```

**Integration Method:**
```html
<!-- In listingv5.html, between pricing table and booked days section -->

<!-- EASY DROP-IN: Just insert this line -->
<div id="gap-calendar-container"></div>
<script src="gap-calendar-component.js"></script>

<!-- OR: Copy-paste the component HTML block directly -->
<div class="gap-calendar-card">
  <!-- Component HTML here -->
</div>
```

**Data Access Pattern:**
```javascript
// Component should access existing global data
// DO NOT duplicate data fetching

// Option 1: Read from existing global variables
const priceData = window.pricingData[0].data.slice(0, 90);

// Option 2: Hook into existing data flow
// Listen for when pricingData is loaded, then render calendar

// Option 3: Receive data as parameter
function renderGapCalendar(pricingData) { ... }
```

**Must Use Existing Patterns:**
- Use `dayjs` for date formatting (already loaded in listingv5.html)
- Follow existing JavaScript conventions (vanilla JS, no frameworks)
- Reuse existing CSS classes where possible
- Match tooltip portal system pattern (we just implemented this!)
- Use existing color variables/theme

### D. Interaction Requirements

**Hover Tooltip:**
- Use the NEW tooltip portal system we just implemented
- Position tooltip below calendar cell
- Show rich data (see "On Hover Tooltip" section above)
- Smooth fade in/out (200ms transition)
- Don't block adjacent cells

**Click Interaction (Optional Enhancement):**
- Click to "focus" a gap
- Highlight entire gap sequence
- Show gap summary modal/panel
- Allow gap filtering

**Filter Controls:**
- Toggle: "Show only gaps" vs "Show all days"
- Gap size filter: "All gaps" | "2+ nights" | "3+ nights" | "Week+"
- Month navigation: Previous/Next month arrows
- Quick jump: Dropdown to select month

### E. Performance Requirements

**Must Be Lightweight:**
- Render in < 100ms
- No janky scrolling
- Efficient DOM updates
- Lazy load months if showing more than current

**Data Efficiency:**
- Reuse existing data (don't duplicate API calls)
- Cache gap calculations
- Minimize DOM manipulation

---

## 🛠️ Phase 3: Implementation Plan

### Your Third Task: Create Detailed Build Plan

**Deliverable 2:** Create `GAP_CALENDAR_BUILD_PLAN.md` with:

1. **Component Structure:**
   - File organization
   - HTML structure mockup
   - CSS class naming convention
   - JavaScript module organization

2. **Data Flow Diagram:**
   ```
   listingv5.html pricingData
        ↓
   Gap Detection Algorithm
        ↓
   Gap Grouping/Categorization
        ↓
   Calendar Grid Rendering
        ↓
   Tooltip Interaction Layer
   ```

3. **Gap Detection Algorithm:**
   ```javascript
   // Pseudocode
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
         // Start or extend gap
         if (!currentGap) {
           currentGap = {
             startDate: day.date,
             startIndex: i,
             days: [day]
           };
         } else {
           currentGap.days.push(day);
         }
       }
     }

     // Close final gap if exists
     if (currentGap) gaps.push(currentGap);

     return gaps;
   }
   ```

4. **Rendering Strategy:**
   - How to build calendar grid (table vs grid CSS)
   - How to highlight gaps
   - How to handle month boundaries
   - How to handle partial months

5. **Styling Approach:**
   - CSS class hierarchy
   - Color coding system
   - Responsive breakpoints
   - Hover state styles

6. **Integration Steps:**
   ```
   Step 1: Create standalone component file
   Step 2: Test with sample data
   Step 3: Create integration snippet for listingv5.html
   Step 4: Document insertion point
   Step 5: Provide testing instructions
   ```

7. **Testing Plan:**
   - Test cases for gap detection
   - Visual regression scenarios
   - Browser compatibility checks
   - Edge cases to handle

---

## 📦 Phase 4: Build the Component

### Your Fourth Task: Implement the Gap Calendar

**Build Requirements:**

1. **Create Self-Contained Component:**
   - File: `gap-calendar-component.html`
   - Should work standalone (for testing)
   - Should integrate easily into listingv5.html
   - Include all HTML, CSS, JS in one file

2. **Component Template:**
   ```html
   <!DOCTYPE html>
   <!-- This component can be tested standalone OR integrated into listingv5.html -->

   <!-- INTEGRATION INSTRUCTIONS:
        1. Copy the <div class="gap-calendar-container"> block
        2. Paste into listingv5.html after pricing table
        3. Copy the <style> block into existing <style> section
        4. Copy the <script> block into existing <script> section
        5. Call renderGapCalendar(pricingData[0].data) after data loads
   -->

   <html>
   <head>
     <title>Gap Calendar Component - Standalone Test</title>
     <style>
       /* ===== GAP CALENDAR STYLES ===== */
       /* These can be copied to listingv5.html <style> section */

       .gap-calendar-container { ... }
       .gap-calendar-header { ... }
       .gap-calendar-grid { ... }
       .gap-calendar-day { ... }
       .gap-calendar-day.gap { ... }
       .gap-calendar-day.booked { ... }
       /* ... more styles ... */
     </style>
   </head>
   <body>
     <!-- Component HTML -->
     <div class="gap-calendar-container">
       <div class="gap-calendar-header">
         <h3>Gap Calendar - Available Dates</h3>
         <div class="gap-calendar-controls">
           <!-- Filter controls -->
         </div>
       </div>

       <div class="gap-calendar-body">
         <!-- Calendar grid will be rendered here -->
       </div>

       <div class="gap-calendar-legend">
         <!-- Legend explaining colors -->
       </div>
     </div>

     <script>
       /* ===== GAP CALENDAR JAVASCRIPT ===== */
       /* These functions can be copied to listingv5.html <script> section */

       function renderGapCalendar(priceData) {
         // Main rendering function
       }

       function identifyGaps(priceData) {
         // Gap detection logic
       }

       function buildCalendarGrid(gaps, priceData) {
         // Grid construction
       }

       function attachTooltipHandlers() {
         // Hover interaction setup
       }

       // For standalone testing, use mock data
       if (!window.pricingData) {
         // Mock data for standalone testing
         const mockData = [ /* sample 90 days */ ];
         renderGapCalendar(mockData);
       }
     </script>
   </body>
   </html>
   ```

3. **Calendar Grid Implementation:**
   - Use CSS Grid or Table for layout
   - 7 columns (days of week)
   - Dynamic rows based on month length
   - Proper month/week alignment

4. **Gap Highlighting Logic:**
   ```javascript
   // Classify each day
   function classifyDay(day, gaps) {
     // Is it in a gap?
     const gap = gaps.find(g =>
       g.days.some(d => d.date === day.date)
     );

     if (gap) {
       return {
         type: 'gap',
         gapLength: gap.days.length,
         gapPosition: gap.days.findIndex(d => d.date === day.date),
         isWeekend: isWeekend(day.date),
         isSingleDay: gap.days.length === 1
       };
     } else {
       return {
         type: 'booked',
         isBooked: day.demand_desc === 'Unavailable'
       };
     }
   }
   ```

5. **Tooltip Integration:**
   ```javascript
   // Use existing tooltip portal system
   function createGapTooltip(day, gapInfo) {
     const tooltip = document.createElement('div');
     tooltip.className = 'gap-calendar-tooltip booking-window-tooltip';
     tooltip.innerHTML = `
       <strong>${dayjs(day.date).format('dddd, MMMM D, YYYY')}</strong>
       <hr>
       <div class="tooltip-row">
         <span class="tooltip-label">Status:</span>
         <span class="tooltip-value">${gapInfo.type === 'gap' ? 'Available' : 'Booked'}</span>
       </div>
       ${gapInfo.type === 'gap' ? `
         <div class="tooltip-row">
           <span class="tooltip-label">Gap Duration:</span>
           <span class="tooltip-value">${gapInfo.gapLength} nights</span>
         </div>
         <div class="tooltip-row">
           <span class="tooltip-label">Our Price:</span>
           <span class="tooltip-value">$${day.price}</span>
         </div>
         <div class="tooltip-row">
           <span class="tooltip-label">Min Stay:</span>
           <span class="tooltip-value">${day.min_stay || 1} nights</span>
         </div>
       ` : ''}
     `;
     return tooltip;
   }
   ```

---

## 📋 Phase 5: Documentation & Integration

### Your Fifth Task: Create Integration Guide

**Deliverable 3:** Create `GAP_CALENDAR_INTEGRATION.md` with:

1. **Quick Start:**
   ```markdown
   # Quick Integration (5 minutes)

   ## Step 1: Open listingv5.html

   ## Step 2: Find insertion point
   Search for: `<!-- 90-Day Pricing Forecast Table -->`
   Find the closing `</div>` of that section

   ## Step 3: Insert component HTML
   Copy everything from gap-calendar-component.html's
   <div class="gap-calendar-container"> ... </div>

   ## Step 4: Copy styles
   Copy CSS from gap-calendar-component.html into
   listingv5.html's <style> section

   ## Step 5: Copy JavaScript
   Copy JS functions into listingv5.html's <script> section

   ## Step 6: Hook into data loading
   Add to renderDashboard() function:
   ```javascript
   renderGapCalendar(pricingData[0].data);
   ```

   ## Step 7: Test
   Load dashboard and verify calendar appears
   ```

2. **Exact Insertion Points:**
   - Line numbers in listingv5.html
   - Before/after context
   - What code to look for

3. **Configuration Options:**
   ```javascript
   const GAP_CALENDAR_CONFIG = {
     showOnlyGaps: true,
     minGapLength: 1,  // nights
     highlightWeekends: true,
     monthsToShow: 3,  // current + next 2
     colors: {
       gap: '#e8f5e9',
       booked: '#f5f5f5',
       weekend: '#c8e6c9',
       singleDay: '#fff3e0'
     }
   };
   ```

4. **Troubleshooting Guide:**
   - Calendar not appearing?
   - Gaps not detected correctly?
   - Tooltips not working?
   - Styling conflicts?

---

## ✅ Success Criteria

### The Component is Successful When:

**Functional:**
- ✅ Shows ONLY gaps (or toggleable to show all with gaps highlighted)
- ✅ Correctly identifies gaps using existing data
- ✅ Calendar grid layout with proper day-of-week alignment
- ✅ Hover tooltips work with rich information
- ✅ Filter controls function properly
- ✅ Integrates without breaking existing functionality

**Visual:**
- ✅ Matches existing dashboard design language
- ✅ Clear visual distinction between gaps and booked days
- ✅ Easy to scan and understand at a glance
- ✅ Professional, polished appearance
- ✅ Responsive design works on different screen sizes

**Technical:**
- ✅ Self-contained component (easy to drop in)
- ✅ No external dependencies (uses existing libs)
- ✅ Reuses existing data (no duplicate API calls)
- ✅ Clean, documented code
- ✅ Performant (< 100ms render time)
- ✅ No console errors or warnings

**Integration:**
- ✅ Drop-in ready (copy-paste integration)
- ✅ Clear integration instructions
- ✅ Doesn't conflict with existing code
- ✅ Can be easily customized/themed
- ✅ Can be easily removed if needed

---

## 🎯 Deliverables Summary

You will provide:

1. **`GAP_CALENDAR_ANALYSIS.md`**
   - Current codebase analysis
   - Data structure documentation
   - Existing patterns identified
   - Integration points mapped

2. **`GAP_CALENDAR_BUILD_PLAN.md`**
   - Component architecture design
   - Gap detection algorithm
   - Rendering strategy
   - Styling approach
   - Testing plan

3. **`gap-calendar-component.html`**
   - Standalone, self-contained component
   - Fully functional with mock data
   - Ready to integrate into listingv5.html

4. **`GAP_CALENDAR_INTEGRATION.md`**
   - Step-by-step integration guide
   - Exact insertion points
   - Configuration options
   - Troubleshooting tips

5. **`gap-calendar-test.html`** (Optional)
   - Standalone test page
   - Visual regression testing
   - Different gap scenarios

---

## 🚨 Critical Constraints

**DO NOT:**
- ❌ Modify listingv5.html directly (build external component only)
- ❌ Duplicate data fetching (reuse existing pricingData)
- ❌ Break existing functionality
- ❌ Introduce external dependencies
- ❌ Use complex frameworks (React, Vue, etc.)

**DO:**
- ✅ Analyze existing code thoroughly first
- ✅ Match existing design patterns
- ✅ Build modular, drop-in component
- ✅ Use existing libraries (dayjs, etc.)
- ✅ Follow existing JavaScript conventions
- ✅ Create clear documentation
- ✅ Test thoroughly before delivering

---

## 💡 Helpful Context

**About the Gaps:**
- Gaps represent available nights between bookings
- Critical for revenue management (empty nights = lost revenue)
- Users need to quickly see: How many gaps? How long? When?
- Weekend gaps are more valuable (higher rates possible)
- Single-night gaps are harder to fill (minimum stay issues)

**About the Users:**
- Property managers/hosts using PriceLabs
- Want to optimize pricing and reduce vacancy
- Need quick visual insights to make decisions
- May manage multiple properties
- Time-sensitive decision making

**About the Dashboard:**
- Currently shows 90-day pricing forecast in table format
- Has booking window risk indicators (we just fixed tooltips!)
- Uses color coding for performance indicators
- Professional, data-dense interface
- Sticky headers for easy navigation

---

## 🎓 Reference Materials

**Existing Files to Review:**
- `/Users/AIRBNB/Cursor_Projects/Pricelabs V4/Pricelabs/listingv5.html` - Main dashboard
- `/Users/AIRBNB/Cursor_Projects/Pricelabs V4/Pricelabs/test_tooltip.html` - Tooltip example
- Recent tooltip implementation docs in same directory

**Key Functions to Understand:**
- `updatePricingTable()` - How pricing table renders
- `calculateGapNights()` - Existing gap calculation logic
- `formatBookingWindowDisplay()` - Tooltip pattern example
- `initializeTooltipPortals()` - New tooltip system we built

**Libraries Available:**
- dayjs - Date formatting/manipulation
- Chart.js - Charting (not needed for calendar, but available)
- Vanilla JavaScript - No jQuery or frameworks

---

## 🚀 Get Started

**Your workflow:**
1. Read this entire prompt carefully
2. Analyze listingv5.html thoroughly (Phase 1)
3. Create analysis document
4. Design component architecture (Phase 2)
5. Create build plan document
6. Implement component (Phase 3-4)
7. Document integration steps (Phase 5)
8. Test thoroughly
9. Deliver all files with clear instructions

**Questions to ask yourself:**
- Do I understand the data structure completely?
- Have I identified all gaps correctly?
- Does my design match the existing UI?
- Is the component truly drop-in ready?
- Have I tested all edge cases?
- Are my instructions clear enough for non-technical users?

**Success looks like:**
A polished, professional calendar component that we can literally copy-paste into listingv5.html and have it work immediately, providing instant visual value to understand booking gaps at a glance.

---

## 🎯 Final Checklist

Before you submit your work:

- [ ] Analyzed entire listingv5.html codebase
- [ ] Documented data structures and patterns
- [ ] Created detailed build plan
- [ ] Built fully functional component
- [ ] Component works standalone with mock data
- [ ] Component has clear integration instructions
- [ ] All tooltips work properly
- [ ] Calendar grid aligns correctly
- [ ] Gaps are detected accurately
- [ ] Colors/styling match existing dashboard
- [ ] No console errors or warnings
- [ ] Code is clean and well-commented
- [ ] Documentation is comprehensive
- [ ] Ready for immediate integration

---

**Now begin with Phase 1: Codebase Analysis. Good luck!** 🚀
