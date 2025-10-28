# Gap Calendar Component - Build Plan

## Phase 2: Detailed Implementation Strategy

**Date:** 2025-10-24
**Component:** Gap Calendar Visualization
**Target:** Drop-in component for listingv5.html

---

## 1. Component Structure

### File Organization

**Single-File Approach (RECOMMENDED):**
```
gap-calendar-component.html
├── <style> section (inline CSS)
├── <div> component HTML structure
└── <script> section (inline JavaScript)
```

**Benefits:**
- ✅ Easy to test standalone
- ✅ Simple copy-paste integration
- ✅ No external dependencies
- ✅ Self-contained and portable

### HTML Structure Mockup

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gap Calendar Component - Standalone</title>

    <!-- Dependencies (for standalone testing) -->
    <script src="https://cdn.jsdelivr.net/npm/dayjs@1/dayjs.min.js"></script>

    <style>
        /* ===== GAP CALENDAR COMPONENT STYLES ===== */
        /* Copy these styles to listingv5.html <style> section */

        /* Container matching existing .table-container pattern */
        .gap-calendar-container { }

        /* Header with controls */
        .gap-calendar-header { }

        /* Calendar grid layout */
        .gap-calendar-grid { }

        /* Individual day cells */
        .gap-calendar-day { }

        /* Gap variations */
        .gap-calendar-day.gap { }
        .gap-calendar-day.gap-weekend { }
        .gap-calendar-day.gap-single { }
        .gap-calendar-day.gap-long { }
        .gap-calendar-day.booked { }
        .gap-calendar-day.today { }

        /* Tooltips using existing portal system */
        .gap-tooltip { }

        /* Legend */
        .gap-calendar-legend { }
    </style>
</head>
<body>
    <!-- ===== GAP CALENDAR COMPONENT HTML ===== -->
    <!-- Copy this section to listingv5.html at line 1191 -->

    <div class="gap-calendar-container table-container" id="gap-calendar-container">
        <!-- Header with title and controls -->
        <div class="gap-calendar-header table-header">
            <h3>Gap Calendar - Available Booking Dates</h3>
            <div class="gap-calendar-controls filter-container">
                <!-- Filter dropdown -->
                <label for="gap-filter">Show:</label>
                <select id="gap-filter" class="filter-select">
                    <option value="gaps-only" selected>Gaps Only</option>
                    <option value="all-days">All Days (Gaps Highlighted)</option>
                </select>

                <!-- Gap size filter -->
                <label for="gap-size-filter">Minimum Gap:</label>
                <select id="gap-size-filter" class="filter-select">
                    <option value="1" selected>All Gaps</option>
                    <option value="2">2+ Nights</option>
                    <option value="3">3+ Nights</option>
                    <option value="7">Week+</option>
                </select>

                <!-- Month navigation -->
                <div class="month-nav">
                    <button id="prev-month" class="btn-nav" title="Previous Month">←</button>
                    <span id="current-month-label">November 2024</span>
                    <button id="next-month" class="btn-nav" title="Next Month">→</button>
                </div>
            </div>
        </div>

        <!-- Calendar grid body -->
        <div id="gap-calendar-body" class="gap-calendar-body">
            <!-- Will be populated by renderGapCalendar() -->
        </div>

        <!-- Legend explaining colors -->
        <div class="gap-calendar-legend">
            <div class="legend-item">
                <span class="legend-swatch gap"></span>
                <span>Available (Gap)</span>
            </div>
            <div class="legend-item">
                <span class="legend-swatch gap-weekend"></span>
                <span>Weekend Gap</span>
            </div>
            <div class="legend-item">
                <span class="legend-swatch gap-single"></span>
                <span>Single Night Gap</span>
            </div>
            <div class="legend-item">
                <span class="legend-swatch booked"></span>
                <span>Booked (Context)</span>
            </div>
            <div class="legend-item">
                <span class="legend-swatch today"></span>
                <span>Today</span>
            </div>
        </div>
    </div>

    <script>
        /* ===== GAP CALENDAR COMPONENT JAVASCRIPT ===== */
        /* Copy these functions to listingv5.html <script> section */

        // Global state for gap calendar
        let gapCalendarData = {
            gaps: [],
            priceData: [],
            currentMonth: new Date(),
            filters: {
                showMode: 'gaps-only',
                minGapSize: 1
            }
        };

        /**
         * Main rendering function - Call this after pricingData loads
         * @param {Array} priceData - 90-day pricing data from pricingData[0].data
         */
        function renderGapCalendar(priceData) {
            // Implementation...
        }

        /**
         * Identifies all gaps in the price data
         * @param {Array} priceData - Array of day objects
         * @returns {Array} Array of gap objects
         */
        function identifyGaps(priceData) {
            // Implementation...
        }

        /**
         * Builds the calendar grid HTML
         * @param {Array} gaps - Array of gap objects
         * @param {Array} priceData - Full price data
         * @param {Date} monthDate - Month to render
         */
        function buildCalendarGrid(gaps, priceData, monthDate) {
            // Implementation...
        }

        /**
         * Creates tooltip content for a calendar day
         * @param {Object} day - Day data object
         * @param {Object} gapInfo - Gap metadata for this day
         */
        function createGapTooltipContent(day, gapInfo) {
            // Implementation...
        }

        /**
         * Attaches tooltip hover handlers using portal system
         */
        function attachGapTooltipHandlers() {
            // Implementation...
        }

        /**
         * Handles filter changes
         */
        function handleGapFilterChange() {
            // Implementation...
        }

        /**
         * Handles month navigation
         */
        function navigateMonth(direction) {
            // Implementation...
        }

        // For standalone testing with mock data
        if (typeof pricingData === 'undefined') {
            // Load mock data for standalone testing
            const mockData = generateMockData();
            renderGapCalendar(mockData);
        }
    </script>
</body>
</html>
```

---

## 2. Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ loadDashboard() - Line 1340                                     │
│   ↓                                                              │
│ Fetch pricingData from API                                      │
│   ↓                                                              │
│ pricingData[0].data (90 days) - Line 1365                       │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ↓
┌─────────────────────────────────────────────────────────────────┐
│ renderGapCalendar(priceData) - NEW FUNCTION                     │
│   │                                                              │
│   ├─→ identifyGaps(priceData)                                   │
│   │     └─→ Returns: [{startDate, days[], length, type}]        │
│   │                                                              │
│   ├─→ classifyDays(priceData, gaps)                             │
│   │     └─→ Returns: Map of date → {isGap, gapInfo, isWeekend}  │
│   │                                                              │
│   ├─→ buildCalendarGrid(gaps, priceData, currentMonth)          │
│   │     │                                                        │
│   │     ├─→ getMonthBoundaries(currentMonth)                    │
│   │     ├─→ createDayCell(day, classification) × 30-31 days     │
│   │     └─→ Append to #gap-calendar-body                        │
│   │                                                              │
│   └─→ attachGapTooltipHandlers()                                │
│         │                                                        │
│         ├─→ Find all .gap-calendar-day elements                 │
│         ├─→ Attach mouseenter/mouseleave                        │
│         └─→ Use existing showTooltipInPortal() system           │
└─────────────────────────────────────────────────────────────────┘
                        │
                        ↓
┌─────────────────────────────────────────────────────────────────┐
│ User Interactions                                               │
│   │                                                              │
│   ├─→ Hover day → showTooltipInPortal(badge, tooltip)           │
│   ├─→ Change filter → handleGapFilterChange() → re-render       │
│   └─→ Navigate month → navigateMonth(±1) → re-render            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Gap Detection Algorithm (Enhanced)

### Core Function: `identifyGaps()`

```javascript
/**
 * Identifies all booking gaps in the pricing data
 * A gap is a sequence of consecutive available days bounded by bookings
 *
 * @param {Array} priceData - Array of day objects with date, price, demand_desc
 * @returns {Array} Array of gap objects
 *
 * Gap object structure:
 * {
 *   startDate: "2024-11-03",
 *   startIndex: 2,
 *   endDate: "2024-11-05",
 *   endIndex: 4,
 *   days: [day1, day2, day3],
 *   length: 3,
 *   type: "medium",          // "single", "short", "medium", "long"
 *   hasWeekend: true,
 *   prevBookingEnd: "2024-11-02",
 *   nextBookingStart: "2024-11-06",
 *   avgPrice: 170,
 *   minStay: 2
 * }
 */
function identifyGaps(priceData) {
    const gaps = [];
    let currentGap = null;

    // First pass: identify continuous available sequences
    for (let i = 0; i < priceData.length; i++) {
        const day = priceData[i];
        const isBooked = day.demand_desc === 'Unavailable';

        if (isBooked) {
            // End current gap if exists
            if (currentGap) {
                // Record when previous booking ended
                currentGap.nextBookingStart = day.date;
                currentGap.nextBookingIndex = i;
                gaps.push(currentGap);
                currentGap = null;
            }
        } else {
            // Available day - start or extend gap
            if (!currentGap) {
                // Start new gap
                currentGap = {
                    startDate: day.date,
                    startIndex: i,
                    days: [day],
                    prevBookingEnd: i > 0 && priceData[i - 1].demand_desc === 'Unavailable'
                        ? priceData[i - 1].date
                        : null,
                    prevBookingIndex: i > 0 && priceData[i - 1].demand_desc === 'Unavailable'
                        ? i - 1
                        : null
                };
            } else {
                // Extend current gap
                currentGap.days.push(day);
            }
        }
    }

    // Close final gap if exists (gap extends to end of 90-day window)
    if (currentGap) {
        currentGap.nextBookingStart = null; // No booking after
        currentGap.nextBookingIndex = null;
        gaps.push(currentGap);
    }

    // Second pass: enrich gap metadata
    return gaps.map(gap => {
        const { days } = gap;

        // Calculate derived properties
        const length = days.length;
        const endDate = days[days.length - 1].date;
        const endIndex = gap.startIndex + length - 1;

        // Classify gap type by length
        let type;
        if (length === 1) type = 'single';
        else if (length === 2) type = 'short';
        else if (length <= 4) type = 'medium';
        else type = 'long';

        // Check if gap includes weekend
        const hasWeekend = days.some(day => {
            const dayOfWeek = dayjs(day.date).format('ddd');
            return dayOfWeek === 'Sat' || dayOfWeek === 'Sun';
        });

        // Calculate average price
        const avgPrice = days.reduce((sum, d) => sum + (d.price || 0), 0) / length;

        // Get minimum stay requirement (max across gap days)
        const minStay = Math.max(...days.map(d => d.min_stay || 1));

        // Check if gap is bounded (has bookings on at least one side)
        const isBounded = gap.prevBookingEnd !== null || gap.nextBookingStart !== null;

        return {
            ...gap,
            endDate,
            endIndex,
            length,
            type,
            hasWeekend,
            avgPrice: Math.round(avgPrice),
            minStay,
            isBounded
        };
    });
}
```

### Helper Function: `classifyDay()`

```javascript
/**
 * Classifies a specific day in the context of gaps
 *
 * @param {Object} day - Day object
 * @param {Array} gaps - Array of gap objects
 * @returns {Object} Classification metadata
 */
function classifyDay(day, gaps) {
    const isBooked = day.demand_desc === 'Unavailable';

    if (isBooked) {
        return {
            type: 'booked',
            isGap: false,
            isWeekend: false,
            gapInfo: null
        };
    }

    // Find which gap this day belongs to (if any)
    const gap = gaps.find(g =>
        g.days.some(d => d.date === day.date)
    );

    if (!gap) {
        return {
            type: 'available-no-gap',
            isGap: false,
            isWeekend: false,
            gapInfo: null
        };
    }

    // Day is part of a gap
    const dayOfWeek = dayjs(day.date).format('ddd');
    const isWeekend = dayOfWeek === 'Sat' || dayOfWeek === 'Sun';

    // Find position within gap
    const positionInGap = gap.days.findIndex(d => d.date === day.date);

    return {
        type: 'gap',
        isGap: true,
        isWeekend,
        gapInfo: {
            gapLength: gap.length,
            gapType: gap.type,
            positionInGap,
            isFirstDay: positionInGap === 0,
            isLastDay: positionInGap === gap.length - 1,
            hasWeekend: gap.hasWeekend,
            prevBooking: gap.prevBookingEnd,
            nextBooking: gap.nextBookingStart,
            avgGapPrice: gap.avgPrice
        }
    };
}
```

---

## 4. Rendering Strategy

### Calendar Grid Layout

**Approach: CSS Grid (Recommended)**

```css
.gap-calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr); /* 7 days of week */
    gap: 4px;
    margin: 20px 0;
}

.gap-calendar-day-header {
    grid-column: span 1;
    text-align: center;
    font-size: 12px;
    font-weight: 600;
    color: #64748b;
    padding: 8px;
    background: #f8fafc;
    border-radius: 6px 6px 0 0;
}

.gap-calendar-day {
    aspect-ratio: 1;       /* Square cells */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    min-height: 60px;
}
```

### Month Boundaries Handling

```javascript
/**
 * Gets first day of month and total days to render
 *
 * @param {Date} monthDate - Target month
 * @returns {Object} Month metadata
 */
function getMonthBoundaries(monthDate) {
    const firstDay = dayjs(monthDate).startOf('month');
    const lastDay = dayjs(monthDate).endOf('month');

    // What day of week does month start? (0 = Sunday)
    const startDayOfWeek = firstDay.day();

    // How many days in month?
    const daysInMonth = lastDay.date();

    // How many empty cells needed at start?
    const leadingEmpty = startDayOfWeek;

    // Total grid cells needed
    const totalCells = leadingEmpty + daysInMonth;

    // How many rows needed? (round up to full weeks)
    const rows = Math.ceil(totalCells / 7);

    return {
        firstDay: firstDay.format('YYYY-MM-DD'),
        lastDay: lastDay.format('YYYY-MM-DD'),
        startDayOfWeek,
        daysInMonth,
        leadingEmpty,
        totalCells,
        rows
    };
}
```

### Grid Construction

```javascript
/**
 * Builds the calendar grid for a specific month
 *
 * @param {Array} gaps - Gap objects
 * @param {Array} priceData - Full price data
 * @param {Date} monthDate - Month to render
 */
function buildCalendarGrid(gaps, priceData, monthDate) {
    const container = document.getElementById('gap-calendar-body');
    container.innerHTML = '';

    const boundaries = getMonthBoundaries(monthDate);
    const monthStart = dayjs(boundaries.firstDay);

    // Create grid wrapper
    const grid = document.createElement('div');
    grid.className = 'gap-calendar-grid';

    // Add day-of-week headers
    const dayHeaders = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'];
    dayHeaders.forEach(day => {
        const header = document.createElement('div');
        header.className = 'gap-calendar-day-header';
        header.textContent = day;
        grid.appendChild(header);
    });

    // Add leading empty cells
    for (let i = 0; i < boundaries.leadingEmpty; i++) {
        const emptyCell = document.createElement('div');
        emptyCell.className = 'gap-calendar-day empty';
        grid.appendChild(emptyCell);
    }

    // Add day cells
    for (let day = 1; day <= boundaries.daysInMonth; day++) {
        const date = monthStart.add(day - 1, 'day');
        const dateStr = date.format('YYYY-MM-DD');

        // Find corresponding day data
        const dayData = priceData.find(d => d.date === dateStr);

        if (dayData) {
            const classification = classifyDay(dayData, gaps);
            const cell = createDayCell(dayData, classification, day);
            grid.appendChild(cell);
        } else {
            // Date outside 90-day window
            const futureCell = document.createElement('div');
            futureCell.className = 'gap-calendar-day future';
            futureCell.innerHTML = `<div class="day-number">${day}</div>`;
            futureCell.title = 'Outside 90-day forecast';
            grid.appendChild(futureCell);
        }
    }

    container.appendChild(grid);
}
```

### Day Cell Creation

```javascript
/**
 * Creates a single calendar day cell
 *
 * @param {Object} dayData - Day data object
 * @param {Object} classification - Day classification from classifyDay()
 * @param {Number} dayNumber - Day of month (1-31)
 * @returns {HTMLElement} Day cell element
 */
function createDayCell(dayData, classification, dayNumber) {
    const cell = document.createElement('div');
    cell.className = 'gap-calendar-day';

    // Add classification classes
    if (classification.isGap) {
        cell.classList.add('gap');

        if (classification.gapInfo.gapType === 'single') {
            cell.classList.add('gap-single');
        } else if (classification.gapInfo.gapType === 'long') {
            cell.classList.add('gap-long');
        }

        if (classification.isWeekend) {
            cell.classList.add('gap-weekend');
        }
    } else if (classification.type === 'booked') {
        cell.classList.add('booked');
    }

    // Check if today
    const isToday = dayjs(dayData.date).isSame(dayjs(), 'day');
    if (isToday) {
        cell.classList.add('today');
    }

    // Day number
    const dayNum = document.createElement('div');
    dayNum.className = 'day-number';
    dayNum.textContent = dayNumber;
    cell.appendChild(dayNum);

    // Gap length badge (for multi-day gaps)
    if (classification.isGap && classification.gapInfo.gapLength > 1) {
        const badge = document.createElement('div');
        badge.className = 'gap-badge';
        badge.textContent = `${classification.gapInfo.gapLength}N`;
        cell.appendChild(badge);
    }

    // Price label
    if (dayData.price) {
        const priceLabel = document.createElement('div');
        priceLabel.className = 'day-price';
        priceLabel.textContent = `$${dayData.price}`;
        cell.appendChild(priceLabel);
    }

    // Store data for tooltip
    cell.dataset.date = dayData.date;
    cell.dataset.classification = JSON.stringify(classification);

    // Create tooltip (hidden by default)
    const tooltip = createGapTooltipContent(dayData, classification);
    cell.appendChild(tooltip);

    return cell;
}
```

---

## 5. Tooltip Integration Strategy

### Reusing Existing Portal System

```javascript
/**
 * Creates tooltip content for a calendar day
 * Uses same structure as booking-window-tooltip
 *
 * @param {Object} day - Day data
 * @param {Object} classification - Day classification
 * @returns {HTMLElement} Tooltip element
 */
function createGapTooltipContent(day, classification) {
    const tooltip = document.createElement('div');
    tooltip.className = 'booking-window-tooltip gap-tooltip';

    const date = dayjs(day.date);
    const formattedDate = date.format('dddd, MMMM D, YYYY');

    let content = `
        <strong>${formattedDate}</strong>
        <hr>
    `;

    if (classification.isGap) {
        const { gapInfo } = classification;

        content += `
            <div class="tooltip-row">
                <span class="tooltip-label">Status:</span>
                <span class="tooltip-value">Available (Gap)</span>
            </div>
            <div class="tooltip-row">
                <span class="tooltip-label">Gap Duration:</span>
                <span class="tooltip-value">${gapInfo.gapLength} night${gapInfo.gapLength > 1 ? 's' : ''}</span>
            </div>
            <div class="tooltip-row">
                <span class="tooltip-label">Our Price:</span>
                <span class="tooltip-value">$${day.price}</span>
            </div>
            <div class="tooltip-row">
                <span class="tooltip-label">Min Stay:</span>
                <span class="tooltip-value">${day.min_stay || 1} night${day.min_stay > 1 ? 's' : ''}</span>
            </div>
        `;

        if (gapInfo.prevBooking) {
            content += `
                <div class="tooltip-row">
                    <span class="tooltip-label">Prev Checkout:</span>
                    <span class="tooltip-value">${dayjs(gapInfo.prevBooking).format('MMM D')}</span>
                </div>
            `;
        }

        if (gapInfo.nextBooking) {
            content += `
                <div class="tooltip-row">
                    <span class="tooltip-label">Next Check-in:</span>
                    <span class="tooltip-value">${dayjs(gapInfo.nextBooking).format('MMM D')}</span>
                </div>
            `;
        }

        content += `
            <div class="tooltip-info">
                <em>${gapInfo.gapLength === 1 ? 'Single night gaps can be harder to fill' :
                     gapInfo.gapLength < 3 ? 'Short gap opportunity' :
                     'Ideal booking window'}</em>
            </div>
        `;
    } else if (classification.type === 'booked') {
        content += `
            <div class="tooltip-row">
                <span class="tooltip-label">Status:</span>
                <span class="tooltip-value">Booked</span>
            </div>
            <div class="tooltip-info">
                <em>This date is unavailable (booked)</em>
            </div>
        `;
    }

    tooltip.innerHTML = content;
    return tooltip;
}
```

### Attach Tooltip Handlers

```javascript
/**
 * Attaches tooltip event handlers to all calendar days
 * Reuses existing portal system from listingv5.html
 */
function attachGapTooltipHandlers() {
    const days = document.querySelectorAll('.gap-calendar-day:not(.empty)');

    console.log(`[Gap Calendar] Initializing tooltips for ${days.length} days`);

    days.forEach(day => {
        const tooltip = day.querySelector('.gap-tooltip');
        if (!tooltip) return;

        // Store reference for cleanup
        if (!tooltip.dataset.initialized) {
            tooltip._originalParent = day;
            tooltip.dataset.initialized = 'true';

            // Add event listeners (reuse existing handlers if available)
            day.addEventListener('mouseenter', (e) => handleGapDayHover(e, day, tooltip));
            day.addEventListener('mouseleave', (e) => handleGapDayLeave(e, tooltip));
        }
    });
}

/**
 * Handles hover on calendar day
 * Uses existing showTooltipInPortal() if available
 */
function handleGapDayHover(event, day, tooltip) {
    // Check if existing tooltip system is available
    if (typeof showTooltipInPortal === 'function') {
        showTooltipInPortal(day, tooltip);
        if (typeof activeTooltip !== 'undefined') {
            activeTooltip = tooltip;
        }
    } else {
        // Fallback: simple tooltip display
        tooltip.style.opacity = '1';
        tooltip.style.pointerEvents = 'auto';
    }
}

/**
 * Handles leaving calendar day
 * Uses existing hideTooltip() if available
 */
function handleGapDayLeave(event, tooltip) {
    if (typeof hideTooltip === 'function') {
        // Use existing tooltip system with delay
        setTimeout(() => {
            hideTooltip(tooltip);
        }, 200);
    } else {
        // Fallback: simple hide
        tooltip.style.opacity = '0';
        tooltip.style.pointerEvents = 'none';
    }
}
```

---

## 6. Styling Approach

### CSS Class Hierarchy

```css
/* ===== GAP CALENDAR COMPONENT STYLES ===== */

/* Container - matches existing .table-container */
.gap-calendar-container {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    margin-bottom: 30px;
}

/* Header - matches existing .table-header */
.gap-calendar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    flex-wrap: wrap;
    gap: 15px;
}

.gap-calendar-header h3 {
    font-size: 18px;
    color: #1a202c;
    font-weight: 600;
    margin: 0;
}

/* Controls group */
.gap-calendar-controls {
    display: flex;
    align-items: center;
    gap: 15px;
    flex-wrap: wrap;
}

.gap-calendar-controls label {
    font-size: 14px;
    color: #64748b;
    font-weight: 500;
}

/* Month navigation */
.month-nav {
    display: flex;
    align-items: center;
    gap: 12px;
}

#current-month-label {
    font-size: 14px;
    font-weight: 600;
    color: #334155;
    min-width: 120px;
    text-align: center;
}

.btn-nav {
    padding: 6px 12px;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    background: white;
    color: #64748b;
    cursor: pointer;
    font-size: 16px;
    transition: all 0.2s;
}

.btn-nav:hover {
    background: #f8fafc;
    border-color: #cbd5e1;
}

.btn-nav:active {
    transform: scale(0.95);
}

/* Calendar grid */
.gap-calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 4px;
    margin: 20px 0;
}

/* Day headers */
.gap-calendar-day-header {
    text-align: center;
    font-size: 12px;
    font-weight: 600;
    color: #64748b;
    padding: 8px;
    background: #f8fafc;
    border-radius: 6px 6px 0 0;
}

/* Day cells - base */
.gap-calendar-day {
    aspect-ratio: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    min-height: 60px;
    border: 1px solid #e2e8f0;
    background: #ffffff;
}

.gap-calendar-day.empty {
    background: transparent;
    border: none;
    cursor: default;
}

/* Day number */
.day-number {
    font-size: 14px;
    font-weight: 600;
    color: #334155;
}

/* Day price */
.day-price {
    font-size: 10px;
    color: #64748b;
    margin-top: 2px;
}

/* Gap badge (nights indicator) */
.gap-badge {
    position: absolute;
    top: 4px;
    right: 4px;
    background: #1b5e20;
    color: white;
    font-size: 9px;
    padding: 2px 5px;
    border-radius: 3px;
    font-weight: 600;
    line-height: 1;
}

/* ===== Gap Day States ===== */

/* Available day (gap) - base green */
.gap-calendar-day.gap {
    background: #e8f5e9;
    border-color: #a5d6a7;
}

.gap-calendar-day.gap .day-number {
    color: #1b5e20;
}

.gap-calendar-day.gap .day-price {
    color: #2e7d32;
}

/* Weekend gap - darker green (premium) */
.gap-calendar-day.gap-weekend {
    background: #c8e6c9;
    border-color: #81c784;
}

/* Single night gap - orange tint (challenging) */
.gap-calendar-day.gap-single {
    background: #fff3e0;
    border-color: #ffcc80;
}

.gap-calendar-day.gap-single .day-number {
    color: #e65100;
}

.gap-calendar-day.gap-single .gap-badge {
    background: #e65100;
}

/* Long gap (3+ nights) - rich green (ideal) */
.gap-calendar-day.gap-long {
    background: #a5d6a7;
    border-color: #66bb6a;
}

.gap-calendar-day.gap-long .gap-badge {
    background: #1b5e20;
}

/* Booked day - gray (context only) */
.gap-calendar-day.booked {
    background: #f5f5f5;
    border-color: #e0e0e0;
    opacity: 0.6;
    cursor: default;
}

.gap-calendar-day.booked .day-number {
    color: #9e9e9e;
}

.gap-calendar-day.booked .day-price {
    color: #bdbdbd;
}

/* Today highlight */
.gap-calendar-day.today {
    border: 2px solid #667eea;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

/* Future day (outside 90-day window) */
.gap-calendar-day.future {
    background: #fafafa;
    border-color: #f0f0f0;
    opacity: 0.5;
    cursor: default;
}

/* Hover states */
.gap-calendar-day.gap:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.gap-calendar-day.booked:hover,
.gap-calendar-day.empty:hover,
.gap-calendar-day.future:hover {
    transform: none;
}

/* ===== Legend ===== */

.gap-calendar-legend {
    display: flex;
    gap: 20px;
    padding: 16px;
    background: #f8fafc;
    border-radius: 8px;
    flex-wrap: wrap;
    justify-content: center;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: #64748b;
}

.legend-swatch {
    width: 24px;
    height: 24px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
}

.legend-swatch.gap {
    background: #e8f5e9;
    border-color: #a5d6a7;
}

.legend-swatch.gap-weekend {
    background: #c8e6c9;
    border-color: #81c784;
}

.legend-swatch.gap-single {
    background: #fff3e0;
    border-color: #ffcc80;
}

.legend-swatch.booked {
    background: #f5f5f5;
    border-color: #e0e0e0;
}

.legend-swatch.today {
    border: 2px solid #667eea;
    background: white;
}

/* ===== Responsive Design ===== */

@media (max-width: 768px) {
    .gap-calendar-header {
        flex-direction: column;
        align-items: stretch;
    }

    .gap-calendar-controls {
        flex-direction: column;
        align-items: stretch;
    }

    .gap-calendar-grid {
        gap: 2px;
    }

    .gap-calendar-day {
        min-height: 50px;
        font-size: 12px;
    }

    .day-number {
        font-size: 12px;
    }

    .day-price {
        font-size: 9px;
    }

    .gap-badge {
        font-size: 8px;
        padding: 1px 4px;
    }

    .gap-calendar-legend {
        gap: 10px;
        flex-direction: column;
    }
}
```

---

## 7. Integration Steps

### Step-by-Step Integration Guide

**Step 1: Create standalone component file**
- Build `gap-calendar-component.html` with all HTML/CSS/JS
- Test with mock data
- Verify tooltips work
- Validate responsive design

**Step 2: Prepare integration snippets**
- Extract CSS to copy into listingv5.html `<style>` section
- Extract JS functions to copy into `<script>` section
- Extract HTML structure as insertion block

**Step 3: Identify exact insertion points in listingv5.html**
- **HTML:** Line 1191 (after pricing table, before booked days)
- **CSS:** Within existing `<style>` tag (around line 11-1100)
- **JS:** Within existing `<script>` tag (around line 1281-2858)

**Step 4: Add render call to data load sequence**
```javascript
// In loadDashboard() function, after line 1448:
updatePricingTable();

// ADD THIS:
renderGapCalendar(pricingData[0].data);
```

**Step 5: Test integration**
- Load dashboard with real data
- Verify calendar renders correctly
- Check tooltip portal integration
- Validate filters work
- Test month navigation

---

## 8. Testing Plan

### Test Cases for Gap Detection

**Test Case 1: Simple gap**
```javascript
// Input:
[
  { date: "2024-11-01", demand_desc: "Unavailable" },
  { date: "2024-11-02", demand_desc: "Low Demand" },     // Gap
  { date: "2024-11-03", demand_desc: "Medium Demand" },  // Gap
  { date: "2024-11-04", demand_desc: "Unavailable" }
]

// Expected output:
{
  startDate: "2024-11-02",
  length: 2,
  type: "short",
  prevBookingEnd: "2024-11-01",
  nextBookingStart: "2024-11-04"
}
```

**Test Case 2: Single-night gap**
```javascript
// Input: Booked, Available, Booked
// Expected: Single-night gap with type="single"
```

**Test Case 3: Gap at start of window**
```javascript
// Input: First 3 days available, then booking
// Expected: Gap with prevBookingEnd=null, nextBookingStart set
```

**Test Case 4: Gap at end of window**
```javascript
// Input: Booking, then last 5 days available
// Expected: Gap with prevBookingEnd set, nextBookingStart=null
```

**Test Case 5: No gaps (fully booked)**
```javascript
// Input: All days "Unavailable"
// Expected: Empty gaps array []
```

**Test Case 6: No gaps (fully available)**
```javascript
// Input: All days available
// Expected: Single gap spanning entire window, isBounded=false
```

**Test Case 7: Weekend gap**
```javascript
// Input: Gap including Sat-Sun
// Expected: hasWeekend=true
```

### Visual Regression Scenarios

1. **Responsive layouts**
   - Desktop (1400px)
   - Tablet (768px)
   - Mobile (375px)

2. **Different gap patterns**
   - Many small gaps
   - Few large gaps
   - Mixed gap sizes
   - No gaps

3. **Month boundaries**
   - Month starting on Sunday
   - Month starting on Saturday
   - 28-day month
   - 31-day month

4. **Tooltip positioning**
   - First week (tooltip below)
   - Last week (tooltip above?)
   - Edge days (left/right adjustment)

### Browser Compatibility

Test in:
- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile Safari (iOS)
- ✅ Mobile Chrome (Android)

### Edge Cases

1. **Empty data:** No pricingData available
2. **Partial data:** Less than 90 days
3. **Missing fields:** Days without price or min_stay
4. **Invalid dates:** Malformed date strings
5. **Filter edge cases:** Min gap size larger than all gaps

---

## 9. Performance Optimization

### Rendering Optimizations

```javascript
// Use DocumentFragment for batch DOM inserts
function buildCalendarGrid(gaps, priceData, monthDate) {
    const fragment = document.createDocumentFragment();

    // Build all cells
    days.forEach(day => {
        const cell = createDayCell(day);
        fragment.appendChild(cell);
    });

    // Single DOM update
    container.appendChild(fragment);
}
```

### Caching Strategy

```javascript
// Cache gap calculations
let gapCache = new Map();

function getCachedGaps(priceData) {
    const dataHash = generateHash(priceData);

    if (gapCache.has(dataHash)) {
        return gapCache.get(dataHash);
    }

    const gaps = identifyGaps(priceData);
    gapCache.set(dataHash, gaps);
    return gaps;
}

// Simple hash function
function generateHash(data) {
    return data.map(d => `${d.date}:${d.demand_desc}`).join('|');
}
```

### Debouncing Filter Changes

```javascript
let filterTimeout = null;

function handleFilterChange() {
    clearTimeout(filterTimeout);

    filterTimeout = setTimeout(() => {
        // Re-render calendar with new filters
        renderGapCalendar(gapCalendarData.priceData);
    }, 300); // 300ms debounce
}
```

---

## 10. Deliverables Checklist

### Files to Create

- [x] `GAP_CALENDAR_ANALYSIS.md` - Phase 1 analysis ✅
- [ ] `GAP_CALENDAR_BUILD_PLAN.md` - This document (Phase 2) 🔄
- [ ] `gap-calendar-component.html` - Standalone component
- [ ] `GAP_CALENDAR_INTEGRATION.md` - Integration instructions
- [ ] `gap-calendar-test-data.js` - Mock data for testing (optional)

### Code Components

- [ ] Gap detection algorithm (`identifyGaps()`)
- [ ] Day classification logic (`classifyDay()`)
- [ ] Calendar grid builder (`buildCalendarGrid()`)
- [ ] Month boundary calculator (`getMonthBoundaries()`)
- [ ] Day cell creator (`createDayCell()`)
- [ ] Tooltip content generator (`createGapTooltipContent()`)
- [ ] Tooltip handlers (`attachGapTooltipHandlers()`)
- [ ] Filter handlers (`handleGapFilterChange()`)
- [ ] Month navigation (`navigateMonth()`)
- [ ] Main render function (`renderGapCalendar()`)

### CSS Classes

- [ ] `.gap-calendar-container`
- [ ] `.gap-calendar-header`
- [ ] `.gap-calendar-grid`
- [ ] `.gap-calendar-day` + variants
- [ ] `.gap-tooltip`
- [ ] `.gap-calendar-legend`
- [ ] `.month-nav`
- [ ] Responsive media queries

### Documentation

- [ ] Algorithm explanations
- [ ] API documentation for functions
- [ ] Integration step-by-step guide
- [ ] Configuration options
- [ ] Troubleshooting guide

---

## Summary

**Phase 2 Complete** - Comprehensive build plan created covering:

✅ Component structure and file organization
✅ Data flow and rendering pipeline
✅ Enhanced gap detection algorithm
✅ Calendar grid layout strategy
✅ Tooltip integration with existing portal system
✅ Complete CSS styling approach
✅ Integration steps
✅ Testing plan
✅ Performance optimizations

**Next Steps:**
- Proceed to Phase 3-4: Implementation
- Build the standalone component
- Create integration guide (Phase 5)

---

**Ready to build!** 🚀
