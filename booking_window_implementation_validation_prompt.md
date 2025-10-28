# AI Agent Task: Validate and Enhance Booking Window Risk Implementation Plan

## Context

We are adding a "Booking Window Risk" feature to a PriceLabs dashboard (listingv5.html). This feature will show users whether their unbookable dates are past their typical booking window based on market data.

**Core Concept:**
- Market data shows average booking windows by month (e.g., June = 48 days in advance)
- For each unbookable future date, calculate if we're past the typical booking window
- Display risk level in the table with color coding

## Your Mission

Take the implementation plan below and:

1. **Create a standalone test JavaScript file** that validates all assumptions and logic
2. **Run actual tests** with sample data to verify the approach works
3. **Identify edge cases** we haven't considered
4. **Propose enhancements** based on test findings
5. **Update the implementation plan** with any necessary corrections

---

# IMPLEMENTATION PLAN TO VALIDATE

# Implementation Plan: Booking Window Risk Analysis for Listing v5 Table

## Phase 1: Data Architecture & API Strategy

### 1.1 Identify Required Data Sources
**Already Available:**
- ✅ Market KPI Booking Window data (from `/api/neighborhood`)
  - Monthly averages: `Y_values[1]` = [31.0, 22.0, 22.0, 23.0, ...]
  - Time periods: `X_values` = ["Sep 2023", "Oct 2023", ...]
- ✅ Daily pricing data (from `/api/listing_prices`)
  - Each day's check-in date
  - Booking status
  - Current price

**Need to Calculate:**
- ❌ Booking window lookup by month
- ❌ Risk threshold date for each check-in date
- ❌ Days past/until booking window
- ❌ Risk level classification

### 1.2 Data Flow Architecture
```
Step 1: Fetch neighborhood data
  ↓
Step 2: Extract booking window by month into lookup table
  {
    "Jan": 25 days,
    "Feb": 28 days,
    "Mar": 30 days,
    ...
    "Jun": 48 days,
    ...
  }
  ↓
Step 3: For each day in pricing table:
  - Extract month from check-in date (e.g., "2025-06-15" → "Jun")
  - Lookup booking window for that month (e.g., Jun → 48 days)
  - Calculate risk threshold = check-in date - booking window
  - Calculate days from today to risk threshold
  - Classify risk level
  ↓
Step 4: Render in table with color coding
```

## Phase 2: Implementation Strategy

### 2.1 Where to Insert in Existing Code

**Current listingv5.html structure:**
```
1. Data fetching section (lines ~1600-1900)
   - fetchListingData()
   - fetchNeighborhoodData() ← WE ADD BOOKING WINDOW PROCESSING HERE
   - fetchReservationData()

2. Table rendering section (lines ~1900-2100)
   - renderPricingTable()
   - For each day: calculate columns ← WE ADD NEW COLUMN HERE

3. Helper functions section (lines ~2100-2300)
   - calculateOptimizedTarget()
   - formatters, etc. ← WE ADD BOOKING WINDOW HELPERS HERE
```

### 2.2 New Data Structures Needed

**Global variable (add near top with other globals):**
```javascript
let bookingWindowLookup = {}; // Store monthly booking windows
```

**Data structure example:**
```javascript
bookingWindowLookup = {
  "Jan": 25,
  "Feb": 28,
  "Mar": 30,
  "Apr": 35,
  "May": 40,
  "Jun": 48,
  "Jul": 45,
  "Aug": 38,
  "Sep": 32,
  "Oct": 28,
  "Nov": 25,
  "Dec": 22
}
```

### 2.3 New Functions to Create

#### Function 1: `buildBookingWindowLookup(neighborhoodData)`
**Purpose:** Convert Market KPI monthly data into month-name lookup table

**Input:**
```javascript
{
  "Market KPI": {
    "Category": {
      "5": {  // bedroom count
        "X_values": ["Sep 2023", "Oct 2023", "Nov 2023", ...],
        "Y_values": [
          [...],  // Y_values[0]
          [31.0, 22.0, 22.0, ...],  // Y_values[1] = Booking Window
          ...
        ]
      }
    }
  }
}
```

**Output:**
```javascript
{
  "Jan": 25,
  "Feb": 28,
  ...
}
```

**Algorithm:**
```javascript
1. Extract bedroom category from listing data
2. Get X_values (time periods) and Y_values[1] (booking windows)
3. Filter to only monthly data (exclude "Last 365 Days", etc.)
4. Group by month name (extract "Oct" from "Oct 2023")
5. Calculate average booking window per month
6. Return lookup object
```

---

#### Function 2: `calculateBookingWindowRisk(checkInDate, bookingStatus)`
**Purpose:** Calculate risk metrics for a specific date

**Input:**
- `checkInDate`: "2025-06-15"
- `bookingStatus`: "Booked" or ""

**Output:**
```javascript
{
  bookingWindow: 48,           // days
  riskThresholdDate: "2025-05-16",
  daysUntilWindow: -5,         // negative = past window
  riskLevel: "high",           // "safe" | "watch" | "risk" | "high"
  displayText: "5 days OVERDUE",
  colorClass: "risk-high"
}
```

**Algorithm:**
```javascript
1. If booking status is "Booked", return null (no risk for booked dates)
2. Extract month from check-in date ("2025-06-15" → "Jun")
3. Lookup booking window (bookingWindowLookup["Jun"] = 48)
4. Calculate risk threshold date = checkInDate - bookingWindow days
5. Calculate days until window = riskThresholdDate - today
6. Classify risk:
   - daysUntilWindow > 7: "safe" (green)
   - daysUntilWindow 0-7: "watch" (yellow)
   - daysUntilWindow -7 to 0: "risk" (orange)
   - daysUntilWindow < -7: "high" (red)
7. Generate display text and color class
8. Return risk object
```

---

#### Function 3: `formatBookingWindowDisplay(riskData)`
**Purpose:** Format risk data for table display

**Input:** Risk object from Function 2

**Output:** HTML string
```html
<span class="booking-window-status risk-high">
  🔴 5 days OVERDUE
  <div class="tooltip">
    Window opened: May 16<br>
    Typical booking: 48 days before
  </div>
</span>
```

**Display Rules:**
- **Safe** (>7 days until window): `✅ Opens in X days`
- **Watch** (0-7 days until): `⚠️ Opens in X days`
- **Risk** (0-7 days past): `🚨 X days overdue`
- **High Risk** (>7 days past): `🔴 X days OVERDUE`
- **Booked**: `—` (no risk)

## Phase 3: Table Integration

### 3.1 Column Placement Strategy

**Current columns (left to right):**
1. Date
2. Day of Week
3. Price
4. Min Stay
5. Booking Status
6. Market Median
7. Our Avg vs Market
8. Top End Pricing
9. vs Top End

**Proposed new column placement:**

**Option A: After "Booking Status" (makes logical sense)**
```
1. Date
2. Day of Week
3. Price
4. Min Stay
5. Booking Status
6. ⭐ BOOKING WINDOW RISK ⭐  ← NEW COLUMN HERE
7. Market Median
8. Our Avg vs Market
9. Top End Pricing
10. vs Top End
```

**Option B: After "vs Top End" (keeps pricing columns together)**
```
1. Date
2. Day of Week
3. Price
4. Min Stay
5. Booking Status
6. Market Median
7. Our Avg vs Market
8. Top End Pricing
9. vs Top End
10. ⭐ BOOKING WINDOW RISK ⭐  ← NEW COLUMN HERE
```

**Recommendation:** **Option A** - Place after "Booking Status" because:
- Risk is related to booking likelihood
- Separates "what is" (status/price) from "what should be" (market comparisons)
- Creates clear visual separation between actual state and analytical metrics

### 3.2 Column Header Design

**Header text:** "Booking Window"

**Tooltip/subtitle:** "Days until/past typical booking window for this date"

**Header styling:**
- Icon: ⏰ or 📅
- Color: Purple/blue to distinguish from pricing columns
- Sticky header behavior (same as other columns)

### 3.3 Cell Rendering Logic

**For each row in the table:**
```javascript
// In the daily loop where we create table rows

const checkInDate = day.date;  // "2025-06-15"
const bookingStatus = day.booking_status;  // "Booked" or ""

// Calculate risk
const riskData = calculateBookingWindowRisk(checkInDate, bookingStatus);

// Render cell
let bookingWindowCell = '';
if (riskData === null) {
  // Booked dates show nothing
  bookingWindowCell = '<td class="booking-window-cell">—</td>';
} else {
  bookingWindowCell = `
    <td class="booking-window-cell ${riskData.colorClass}">
      ${riskData.displayText}
      <div class="tooltip-hover">
        Window: ${riskData.bookingWindow} days<br>
        Opens: ${formatDate(riskData.riskThresholdDate)}
      </div>
    </td>
  `;
}
```

## Phase 4: Visual Design

### 4.1 Color Coding System

**Match existing color patterns but distinct:**

```css
/* Safe - More than 7 days until window opens */
.risk-safe {
  color: #16a34a;           /* Green */
  background: #dcfce7;      /* Light green bg */
}

/* Watch - Within 7 days of window opening */
.risk-watch {
  color: #d97706;           /* Amber */
  background: #fef3c7;      /* Light amber bg */
}

/* Risk - Up to 7 days past window */
.risk-risk {
  color: #ea580c;           /* Orange */
  background: #fff7ed;      /* Light orange bg */
}

/* High Risk - More than 7 days past window */
.risk-high {
  color: #dc2626;           /* Red */
  background: #fef2f2;      /* Light red bg */
}

/* Booked - No risk */
.risk-booked {
  color: #64748b;           /* Gray */
  background: transparent;
}
```

### 4.2 Icon/Emoji Strategy

- ✅ Safe (green checkmark)
- ⚠️ Watch (yellow warning)
- 🚨 Risk (orange alert)
- 🔴 High Risk (red circle)
- — Booked (dash)

### 4.3 Tooltip Design

**Show on hover:**
```
╔════════════════════════════╗
║ Booking Window Details     ║
╠════════════════════════════╣
║ Typical window: 48 days    ║
║ Window opened: May 16      ║
║ Current status: 5 days late║
║                            ║
║ Market books Jun dates     ║
║ ~48 days in advance        ║
╚════════════════════════════╝
```

## Phase 5: Edge Cases & Error Handling

### 5.1 Missing Data Scenarios

**Scenario 1: No booking window data for a month**
- **Solution:** Use overall average across all available months
- **Display:** "⚠️ Estimated (avg)"

**Scenario 2: Future months not in historical data**
- **Solution:** Use same month from previous year
- **Example:** June 2026 → use June 2025 data

**Scenario 3: Bedroom category not found**
- **Solution:** Fall back to category "-1" (all bedrooms)
- **Display:** Works silently, no user notification

**Scenario 4: Booked dates**
- **Solution:** Return null from risk calculation
- **Display:** Show "—" (em dash)

### 5.2 Date Handling Edge Cases

**Past dates:**
- If check-in date is in the past → Skip risk calculation (already happened)
- Display: "—"

**Today's date:**
- Risk threshold is today or earlier → Show as high risk
- Display: "🔴 Late"

**Very far future (>365 days):**
- Risk calculation still applies
- Display normally (e.g., "✅ Opens in 300 days")

## Phase 6: Performance Considerations

### 6.1 Data Processing Optimization

**Build lookup table once:**
```javascript
// Call this ONCE after fetching neighborhood data
bookingWindowLookup = buildBookingWindowLookup(neighborhoodData);
```

**Reuse for all rows:**
```javascript
// In the daily loop - fast lookup
const bookingWindow = bookingWindowLookup[monthName];
```

**Expected performance:**
- Initial processing: ~10ms (one-time)
- Per-row calculation: <1ms
- Total for 365 rows: ~365ms (acceptable)

### 6.2 Rendering Strategy

**Progressive rendering:**
1. Render table structure first
2. Calculate and render each row
3. No need for separate passes

**No re-calculation on sort/filter:**
- Calculate once, store in row data object
- Re-use when table is re-sorted or filtered

## Phase 7: Testing Strategy

### 7.1 Unit Test Cases

**Test Function 1: buildBookingWindowLookup()**
```javascript
Input: Market KPI with known monthly values
Expected Output: {Jan: 25, Feb: 28, ...}
Verify: All 12 months present, reasonable values (15-60 days)
```

**Test Function 2: calculateBookingWindowRisk()**
```javascript
Test Case 1: Date 30 days in future, window is 30 days
  Expected: daysUntilWindow = 0, risk = "watch"

Test Case 2: Date 50 days in future, window is 30 days
  Expected: daysUntilWindow = 20, risk = "safe"

Test Case 3: Date 20 days in future, window is 30 days
  Expected: daysUntilWindow = -10, risk = "high"

Test Case 4: Booked status
  Expected: null (no risk for booked dates)
```

### 7.2 Integration Test Scenarios

**Scenario 1: Load page with Aerie property**
- Verify booking window column appears
- Verify June dates show 48-day window
- Verify risk colors are correct

**Scenario 2: Switch between properties**
- Verify booking windows update per property
- Verify different bedroom counts use different windows

**Scenario 3: Date range filtering**
- Filter to show only next 30 days
- Verify risk calculations still accurate

## Phase 8: Implementation Order

### Step-by-Step Execution Plan

**Step 1: Add helper functions (Lines ~2100-2300)**
1. buildBookingWindowLookup()
2. calculateBookingWindowRisk()
3. formatBookingWindowDisplay()

**Step 2: Modify data fetching (Lines ~1700-1800)**
1. In fetchNeighborhoodData() success handler
2. Call buildBookingWindowLookup()
3. Store result in global variable

**Step 3: Add table header (Lines ~900-920)**
1. Find existing <th> elements
2. Add new <th> after "Booking Status"
3. Add header text and tooltip

**Step 4: Add table cell (Lines ~1900-2000)**
1. Find daily loop where cells are created
2. Calculate risk for current day
3. Render new <td> with risk display

**Step 5: Add CSS styling (Lines ~700-750)**
1. Add .risk-safe, .risk-watch, .risk-risk, .risk-high classes
2. Add .booking-window-cell styling
3. Add tooltip hover styles

**Step 6: Test and debug**
1. Load page
2. Verify data appears
3. Check console for errors
4. Verify tooltips work
5. Test edge cases

## Phase 9: Alternative Approaches (For Discussion)

### Alternative A: Single "Risk Score" Column
Instead of text, show a single numeric risk score (0-100)
- **Pro:** More compact
- **Con:** Less intuitive, requires explanation

### Alternative B: Color-code existing "Booking Status" column
Add background color to show risk without new column
- **Pro:** No new column needed
- **Con:** Less information, harder to interpret

### Alternative C: Add risk indicator icon to "Date" column
Small icon next to date showing risk level
- **Pro:** Minimal space impact
- **Con:** Easy to miss, less prominent

**Recommendation:** Stick with dedicated column (original plan) because:
- Clear and prominent
- Room for detailed information
- Matches existing column structure
- Easy to sort/filter by

---

# Summary: Ready to Implement?

## What We Need to Build:
1. ✅ 3 new JavaScript functions
2. ✅ 1 new table column
3. ✅ 5 new CSS classes
4. ✅ Modify 2 existing functions (data fetching, table rendering)

## Estimated Code Changes:
- **New code:** ~150 lines
- **Modified code:** ~30 lines
- **Total impact:** ~180 lines across 3 sections of the file

## Risk Assessment:
- **Low risk** - Isolated changes, no modification to existing columns
- **High value** - Provides critical booking urgency insights
- **Testable** - Clear success criteria

---

# VALIDATION TASKS

## Specific Validation Tasks

### Task 1: Test Data Structure Conversion

**Create:** `test_booking_window_lookup.js`

**Test scenarios:**
1. Convert sample Market KPI data structure to monthly lookup table
2. Handle missing months
3. Handle multiple years of data (should average across years)
4. Handle edge case: only aggregate periods like "Last 365 Days"
5. Verify all 12 months are populated

**Sample input data:**
```javascript
const sampleMarketKPI = {
  "Category": {
    "5": {
      "X_values": ["Sep 2023", "Oct 2023", "Nov 2023", "Dec 2023", "Jan 2024",
                   "Feb 2024", "Mar 2024", "Apr 2024", "May 2024", "Jun 2024",
                   "Jul 2024", "Aug 2024", "Sep 2024", "Oct 2024",
                   "Last 365 Days", "Last 730 Days"],
      "Y_values": [
        [],  // Y_values[0]
        [31.0, 22.0, 22.0, 23.0, 13.0, 28.0, 30.0, 35.0, 40.0, 48.0,
         45.0, 38.0, 32.0, 25.0, 0, 0],  // Y_values[1] = Booking Window
        []
      ]
    }
  },
  "Labels": ["Total Available Days", "Booking Window", "LOS", "..."]
};
```

**Expected output:**
```javascript
{
  "Jan": 13,
  "Feb": 28,
  "Mar": 30,
  "Apr": 35,
  "May": 40,
  "Jun": 48,
  "Jul": 45,
  "Aug": 38,
  "Sep": 31.5,  // Average of 31 and 32
  "Oct": 23.5,  // Average of 22 and 25
  "Nov": 22,
  "Dec": 23
}
```

**Questions to answer:**
- What if we have 3+ years of data for the same month?
- What if a month is completely missing?
- What if booking window value is 0 or negative?

---

### Task 2: Test Risk Calculation Logic

**Create:** `test_risk_calculation.js`

**Test scenarios:**

**Scenario A: Safe (before window opens)**
```javascript
Input:
  checkInDate: "2025-06-15"
  todayDate: "2025-04-01"
  bookingWindow: 48 days
  bookingStatus: ""

Expected Output:
  {
    bookingWindow: 48,
    riskThresholdDate: "2025-04-28",
    daysUntilWindow: 27,  // April 28 - April 1
    riskLevel: "safe",
    displayText: "✅ Opens in 27 days"
  }
```

**Scenario B: Watch (window just opening)**
```javascript
Input:
  checkInDate: "2025-06-15"
  todayDate: "2025-04-26"
  bookingWindow: 48 days
  bookingStatus: ""

Expected Output:
  {
    riskThresholdDate: "2025-04-28",
    daysUntilWindow: 2,
    riskLevel: "watch",
    displayText: "⚠️ Opens in 2 days"
  }
```

**Scenario C: Risk (recently past window)**
```javascript
Input:
  checkInDate: "2025-06-15"
  todayDate: "2025-05-03"
  bookingWindow: 48 days
  bookingStatus: ""

Expected Output:
  {
    riskThresholdDate: "2025-04-28",
    daysUntilWindow: -5,
    riskLevel: "risk",
    displayText: "🚨 5 days overdue"
  }
```

**Scenario D: High Risk (deeply past window)**
```javascript
Input:
  checkInDate: "2025-06-15"
  todayDate: "2025-05-15"
  bookingWindow: 48 days
  bookingStatus: ""

Expected Output:
  {
    riskThresholdDate: "2025-04-28",
    daysUntilWindow: -17,
    riskLevel: "high",
    displayText: "🔴 17 days OVERDUE"
  }
```

**Scenario E: Booked (no risk)**
```javascript
Input:
  checkInDate: "2025-06-15"
  todayDate: "2025-05-15"
  bookingWindow: 48 days
  bookingStatus: "Booked"

Expected Output: null
```

**Questions to answer:**
- What are the exact thresholds for each risk level?
- Should thresholds be configurable or hardcoded?
- What happens with dates in the past?
- What happens with dates >365 days in the future?

---

### Task 3: Test Month Extraction & Lookup

**Create:** `test_month_lookup.js`

**Test date formats:**
```javascript
Test Cases:
1. "2025-06-15" → "Jun" → 48 days
2. "2025-12-31" → "Dec" → 23 days
3. "2025-01-01" → "Jan" → 13 days
4. "2025-02-28" → "Feb" → 28 days
5. "2025-02-29" → "Feb" → 28 days (leap year)
```

**Edge cases:**
- Invalid date format
- Date in wrong format (e.g., "06/15/2025" vs "2025-06-15")
- Null or undefined date
- Empty string

**Questions to answer:**
- Should we validate date format before processing?
- How to handle different date string formats?
- Should we use Date object or string parsing?

---

### Task 4: Test Display Formatting

**Create:** `test_display_format.js`

**Test all display text variations:**
```javascript
Test Cases:
1. daysUntilWindow = 30 → "✅ Opens in 30 days"
2. daysUntilWindow = 1 → "✅ Opens in 1 day" (singular)
3. daysUntilWindow = 0 → "⚠️ Opens today"
4. daysUntilWindow = -1 → "🚨 1 day overdue" (singular)
5. daysUntilWindow = -10 → "🔴 10 days OVERDUE"
6. null → "—"
```

**Questions to answer:**
- Should "1 day" vs "1 days" be handled (singular/plural)?
- Should we abbreviate long numbers (e.g., "30d" vs "30 days")?
- What's the maximum reasonable booking window (for display purposes)?

---

### Task 5: Test Integration with Real Data Structure

**Use actual API response:**
Download real neighborhood data for Aerie property and test:

```javascript
1. Extract Market KPI from real response
2. Build lookup table
3. Process 30 sample dates from pricing table
4. Verify all calculations produce reasonable results
5. Check for any runtime errors
```

**Questions to answer:**
- Does the real data structure match our assumptions?
- Are there any unexpected fields or variations?
- Do bedroom categories match what we expect?
- Are booking window values within reasonable range (10-90 days)?

---

### Task 6: Test Performance

**Create:** `test_performance.js`

**Benchmark scenarios:**
```javascript
1. Build lookup table from 27 months of data
   - Measure time: Should be <10ms

2. Calculate risk for 365 dates
   - Measure time: Should be <500ms

3. Format display for 365 dates
   - Measure time: Should be <100ms

4. Total table rendering with new column
   - Measure time: Should add <1 second to current render time
```

**Questions to answer:**
- Is there any noticeable performance impact?
- Should we cache calculated values?
- Can we optimize any loops?

---

### Task 7: Test Edge Case Matrix

**Create comprehensive edge case test:**

| Check-In Date | Today's Date | Booking Window | Booking Status | Expected Result |
|---------------|--------------|----------------|----------------|-----------------|
| 2025-06-15 | 2025-06-20 | 48 | "" | Past date - skip |
| 2025-06-15 | 2025-06-15 | 48 | "" | Check-in today - skip |
| 2025-06-15 | 2025-03-01 | 48 | "" | 79 days until window |
| 2025-06-15 | 2025-04-28 | 48 | "" | Window opens today |
| 2025-06-15 | 2025-06-14 | 48 | "" | 47 days overdue |
| 2025-06-15 | 2025-05-15 | 0 | "" | Invalid window - use fallback |
| 2025-06-15 | 2025-05-15 | null | "" | Missing data - use average |
| 2025-06-15 | 2025-05-15 | 48 | "Booked" | null (no risk) |

**Questions to answer:**
- What's the complete set of edge cases?
- How should we handle each one?
- Are there any cases that would crash the code?

---

### Task 8: Test Cross-Browser Compatibility

**Verify:**
1. Date manipulation works in all browsers
2. CSS classes render correctly
3. Tooltips display properly
4. No console errors

---

## Output Format

Please provide:

### 1. Test Results Summary
```
✅ Passed: X/Y tests
❌ Failed: List of failed tests with details
⚠️ Edge cases discovered: List with recommendations
```

### 2. Code for Test Functions
Provide complete, runnable JavaScript test code for each test file

### 3. Discovered Issues
List any problems found in the original plan

### 4. Recommended Changes
Specific modifications to the implementation plan based on test findings

### 5. Enhanced Implementation Plan
Updated version of the plan with:
- Corrected logic
- Additional edge case handling
- Optimizations discovered during testing
- More precise specifications based on test results

### 6. Risk Assessment
- High risk areas that need careful implementation
- Low risk areas that are straightforward
- Recommendations for staged rollout or feature flags

---

## Deliverables

1. **test_suite/** folder with all test JavaScript files
2. **test_results.md** with detailed findings
3. **implementation_plan_v2.md** with enhanced plan
4. **risk_matrix.md** documenting all edge cases and handling

## Success Criteria

- All core functionality tests pass
- Edge cases are identified and handled
- Performance benchmarks are met
- Implementation plan is validated and enhanced
- Code is ready for production implementation

---

## Notes for AI Agent

- Create actual runnable JavaScript code for tests
- Use console.log() to output test results
- Document any assumptions you make
- Flag any areas where the plan is unclear or potentially problematic
- Provide specific line-by-line corrections where needed
- Include performance measurements in your tests
- Test with realistic data whenever possible
