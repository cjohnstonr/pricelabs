# Frontend Tooltip Z-Index Investigation

## Mission
Investigate why the booking window tooltip is being clipped by subsequent table rows instead of appearing on top of all elements. **DO NOT MODIFY ANY CODE** - only analyze and provide findings.

## Problem Description

### Current Behavior
When hovering over a booking window risk badge in the table, the tooltip appears but is **clipped/hidden by the table rows below it**. The tooltip shows partially but subsequent rows are rendering **on top of the tooltip** instead of the tooltip being **on top of everything**.

### Visual Evidence
Looking at the provided screenshot, you can see:
- The tooltip appears when hovering over "🔴 23 days OVERDUE" badge
- The dark tooltip box with "Booking Window Details" is visible
- **BUT** the table rows below are overlapping/covering parts of the tooltip
- The tooltip should be floating **above** all table content with the highest z-index

### Expected Behavior
The tooltip should:
1. Appear directly below the badge being hovered
2. Float **on top of ALL table elements** (rows, cells, other content)
3. Not be clipped or covered by any other elements
4. Have the highest stacking order in the visual hierarchy

## Technical Context

### Relevant File
`/Users/AIRBNB/Cursor_Projects/Pricelabs V4/Pricelabs/listingv5.html`

### Current CSS Implementation

**Tooltip CSS:**
```css
.booking-window-tooltip {
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%) translateY(8px);
    background: #1f2937;
    color: white;
    padding: 12px 16px;
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    z-index: 9999;  /* ← Very high z-index, should be on top */
    min-width: 280px;
    max-width: 320px;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease, transform 0.2s ease;
    font-size: 13px;
    line-height: 1.6;
    white-space: normal;
}

.booking-window-status:hover .booking-window-tooltip {
    opacity: 1;
    transform: translateX(-50%) translateY(4px);
    pointer-events: auto;
}
```

**Parent Elements:**
```css
.booking-window-cell {
    padding: 8px 12px;
    text-align: center;
    vertical-align: middle;
    font-size: 13px;
    position: relative;  /* ← Creates positioning context */
    overflow: visible;
}

.booking-window-status {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 6px;
    font-weight: 500;
    white-space: nowrap;
    position: relative;  /* ← Creates positioning context */
    cursor: help;
    transition: all 0.2s ease;
}

tbody tr {
    position: relative;  /* ← Each row has position: relative */
}

.table-container {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    overflow-x: auto;
    overflow-y: visible;
}

table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    overflow: visible;
}
```

### HTML Structure
```html
<div class="table-container">
    <table>
        <tbody id="pricing-table-body">
            <tr>  <!-- position: relative -->
                <td class="booking-window-cell">  <!-- position: relative, overflow: visible -->
                    <span class="booking-window-status">  <!-- position: relative -->
                        🔴 23 days OVERDUE
                        <div class="booking-window-tooltip">  <!-- position: absolute, z-index: 9999 -->
                            Booking Window Details
                            ...
                        </div>
                    </span>
                </td>
            </tr>
            <tr>  <!-- This row and subsequent rows are rendering ON TOP of tooltip -->
                ...
            </tr>
            <tr>
                ...
            </tr>
        </tbody>
    </table>
</div>
```

## Investigation Tasks

### 1. CSS Stacking Context Analysis
**Investigate:**
- Are table rows (`<tr>`) creating new stacking contexts that interfere with z-index?
- Does `position: relative` on `tbody tr` create a stacking context that traps child elements?
- Are there any CSS properties on table/tbody/tr that create stacking contexts? (transform, opacity, filter, will-change, etc.)
- What is the actual stacking order hierarchy from parent to child?

### 2. Z-Index Inheritance Issues
**Investigate:**
- Is the tooltip's `z-index: 9999` being respected within its stacking context?
- Are subsequent table rows in a different/higher stacking context?
- Does the tooltip need to escape its current positioning context to be on top?
- Are there any parent elements limiting the effective z-index scope?

### 3. Position: Relative Chain
**Investigate:**
- We have nested `position: relative` elements: `tr > td > span > div`
- Does this create multiple stacking contexts that isolate the tooltip?
- Should the tooltip be positioned relative to a higher-level container instead?
- Is the absolute positioning within too many relative parents?

### 4. Table-Specific Rendering Issues
**Investigate:**
- Do HTML tables have special rendering rules that affect z-index?
- Are `tbody`, `tr`, or `td` elements treated differently in the CSS stacking order?
- Could the table's `border-collapse: separate` affect stacking?
- Are there known browser quirks with table cell overflow and positioning?

### 5. Successful Test Page Comparison
**Key Finding:**
The tooltip works PERFECTLY in the isolated test page (`test_tooltip.html`) with the same CSS. The test page structure is:
```html
<table>
    <tbody>
        <tr>
            <td class="booking-window-cell">
                <span class="booking-window-status">
                    🔴 23 days OVERDUE
                    <div class="booking-window-tooltip">...</div>
                </span>
            </td>
        </tr>
    </tbody>
</table>
```

**Investigate:**
- What is different between the test page and the main dashboard?
- Are there parent containers in the main dashboard that don't exist in the test?
- Are there global CSS rules affecting the main dashboard but not the test page?
- Could JavaScript be dynamically adding styles that interfere?

## Deliverables

### Required Analysis Report
Provide a detailed markdown report with:

1. **Root Cause Identification**
   - Exactly why the tooltip is being clipped
   - Which CSS property/element is causing the stacking issue
   - The stacking context hierarchy diagram

2. **Stacking Context Diagram**
   - Visual representation of current stacking order
   - Show which elements create stacking contexts
   - Identify where the tooltip is "trapped"

3. **Comparison Analysis**
   - Why test_tooltip.html works vs why listingv5.html doesn't
   - List all structural/CSS differences
   - Identify the specific difference causing the problem

4. **Recommended Solutions** (DO NOT IMPLEMENT)
   - Option 1: [Describe approach, pros/cons]
   - Option 2: [Describe approach, pros/cons]
   - Option 3: [Describe approach, pros/cons]
   - **Recommended best solution with reasoning**

5. **CSS Changes Needed** (DESCRIBE ONLY)
   - Which selectors need modification
   - Which properties need to be added/removed/changed
   - Expected behavior after changes
   - Any potential side effects to watch for

## Investigation Guidelines

### DO:
- ✅ Read and analyze listingv5.html CSS thoroughly
- ✅ Compare with test_tooltip.html
- ✅ Research CSS stacking context rules
- ✅ Use browser DevTools inspection (if available) to check computed styles
- ✅ Provide specific line numbers and selectors
- ✅ Explain CSS concepts clearly
- ✅ Consider cross-browser compatibility

### DO NOT:
- ❌ Modify any code files
- ❌ Create new files (except your report)
- ❌ Run tests or execute changes
- ❌ Make assumptions without verification
- ❌ Provide vague recommendations

## Success Criteria

Your investigation is successful if you can:
1. Pinpoint the exact CSS property/element causing the clipping
2. Explain why the test page works but the main dashboard doesn't
3. Provide 2-3 actionable solutions with clear implementation steps
4. Include a visual diagram of the stacking context issue

## Notes

- The tooltip CSS is identical between test page (working) and main dashboard (broken)
- This suggests the issue is with parent/ancestor containers or global styles
- Focus on what's DIFFERENT between the two environments
- The z-index of 9999 should be sufficient - something is interfering with the stacking context

---

**Output your findings as:** `tooltip_investigation_report.md`
