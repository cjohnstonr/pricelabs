# Frontend Debug Report: Z-Index Stacking Context Issue

## Executive Summary

**Issue**: Booking window risk tooltips are being rendered behind subsequent table rows
**Severity**: HIGH
**Category**: 🎨 Layout Issue / CSS Stacking Context Problem
**Impact**: Critical UX failure - tooltips are partially hidden, making important information inaccessible
**Root Cause**: Table row stacking contexts are trapping tooltips within their own z-index hierarchy
**Confidence Level**: 95%
**Estimated Fix Time**: 30-45 minutes

---

## Problem Analysis

### Visual Symptoms
1. **Observed Behavior**:
   - Tooltip appears in dark background (#1f2937) with white text
   - Tooltip is correctly positioned below the badge
   - Tooltip is being clipped/covered by table rows that appear AFTER it in the DOM
   - The z-index: 9999 is not being respected

2. **Expected Behavior**:
   - Tooltip should appear on top of ALL page content
   - No table rows should overlay the tooltip
   - Full tooltip content should be visible without clipping

### Technical Investigation Results

#### 1. Stacking Context Creation Points

**Line 339-341: Critical Issue Found**
```css
tbody tr {
    position: relative;
}
```
**PROBLEM**: This creates a new stacking context for EVERY table row. Each row becomes its own isolated z-index universe.

**Line 766-767: Parent Container**
```css
.booking-window-cell {
    position: relative;
    overflow: visible;
}
```
**STATUS**: OK - overflow: visible allows content to escape

**Line 777: Badge Container**
```css
.booking-window-status {
    position: relative;
}
```
**PROBLEM**: Creates another nested stacking context within the row

**Line 834-843: Tooltip**
```css
.booking-window-tooltip {
    position: absolute;
    z-index: 9999;
}
```
**ISSUE**: The z-index: 9999 only applies within its parent stacking context (the table row)

#### 2. Stacking Context Hierarchy Map

```
document
└─ body
   └─ .table-container (no stacking context)
      └─ table (no stacking context)
         └─ tbody (no stacking context)
            ├─ tr (ROW 1) [position: relative - STACKING CONTEXT #1]
            │  └─ td.booking-window-cell [position: relative]
            │     └─ .booking-window-status [position: relative]
            │        └─ .booking-window-tooltip [z-index: 9999 - trapped in context #1]
            │
            ├─ tr (ROW 2) [position: relative - STACKING CONTEXT #2]
            │  └─ (renders ON TOP of row 1's tooltip regardless of z-index)
            │
            └─ tr (ROW 3) [position: relative - STACKING CONTEXT #3]
               └─ (also renders ON TOP of row 1's tooltip)
```

#### 3. Z-Index Competition Analysis

**Finding**: The z-index: 9999 on the tooltip is meaningless because:
1. Each `tbody tr` creates its own stacking context (line 339)
2. Stacking contexts are painted in DOM order
3. Later rows paint over earlier rows, regardless of child z-index values
4. The tooltip is trapped within its row's stacking context

#### 4. Contributing CSS Properties

**Primary Culprits**:
- Line 339: `tbody tr { position: relative; }` - Creates row-level stacking contexts
- Line 777: `.booking-window-status { position: relative; }` - Unnecessary nesting

**Secondary Issues**:
- Line 353-354: `thead th { position: sticky; }` - Creates stacking context for headers
- Line 280-281: `.table-container { overflow-x: auto; overflow-y: visible; }` - Mixed overflow might cause issues

---

## Root Cause Diagnosis

### The Core Problem

The tooltip is trapped within its parent row's stacking context. When `tbody tr` has `position: relative` (line 339), each table row becomes an isolated stacking context. This means:

1. The tooltip's z-index: 9999 only competes with other elements WITHIN that same row
2. The entire row (including its high z-index tooltip) is painted before the next row
3. DOM order trumps z-index when comparing different stacking contexts
4. Later rows will ALWAYS appear on top of earlier row's tooltips

### Why This Happens

CSS Stacking Context Rules:
- Elements with `position: relative/absolute/fixed/sticky` AND a z-index create stacking contexts
- Child z-index values cannot escape their parent's stacking context
- Sibling stacking contexts are painted in DOM order
- A z-index: 9999 inside context A cannot override context B that comes after it

---

## Solution Approaches (Conceptual)

### Option 1: Remove Stacking Context from Rows (RECOMMENDED)
**Strategy**: Eliminate `position: relative` from `tbody tr`
- Remove line 339-341 entirely
- This prevents rows from creating stacking contexts
- Tooltips can then compete globally with z-index: 9999
- **Pros**: Simple, clean, maintains current HTML structure
- **Cons**: May affect other positioned elements within rows

### Option 2: Portal Pattern (Most Robust)
**Strategy**: Move tooltip to document body on hover
- Create tooltip at body level when hovering
- Use JavaScript to position it absolutely relative to viewport
- Calculate position based on badge's getBoundingClientRect()
- **Pros**: Guarantees tooltip is always on top
- **Cons**: Requires JavaScript changes, more complex

### Option 3: Fixed Positioning (Quick Fix)
**Strategy**: Change tooltip to `position: fixed`
- Use JavaScript to calculate viewport coordinates
- Position tooltip using top/left instead of transforms
- **Pros**: Escapes all stacking contexts
- **Cons**: Requires JavaScript for positioning, scroll sync issues

### Option 4: Isolation Property
**Strategy**: Add `isolation: isolate` to specific containers
- Apply to `.table-container` to create controlled stacking context
- Move tooltip higher in DOM hierarchy
- **Pros**: Modern CSS solution
- **Cons**: Limited browser support, complex restructuring

---

## Recommended Fix Implementation Plan

### Step 1: Remove Row Stacking Contexts
1. Delete lines 339-341 (tbody tr position: relative)
2. Test if any other elements break (unlikely based on analysis)

### Step 2: Adjust Tooltip Parent if Needed
1. If step 1 isn't sufficient, remove position: relative from .booking-window-status (line 777)
2. Keep position: relative only on .booking-window-cell for tooltip positioning

### Step 3: Add Safeguard Styles
1. Add `pointer-events: none` to tbody to prevent interference
2. Add `pointer-events: auto` specifically to interactive elements
3. Consider adding `will-change: z-index` to tooltip for optimization

### Step 4: Test Edge Cases
1. Verify tooltip appears correctly on first row
2. Verify tooltip appears correctly on last row
3. Test with scrolling (horizontal and vertical)
4. Test on mobile viewport sizes

---

## Prevention Recommendations

### 1. Stacking Context Awareness
- Document all elements that create stacking contexts
- Use `position: relative` sparingly on container elements
- Consider using CSS custom properties for z-index management

### 2. Tooltip Architecture
- Implement a centralized tooltip system
- Use portal pattern for all overlay content
- Create a dedicated overlay container at body level

### 3. Development Practices
- Add CSS comments explaining stacking context creation
- Use browser DevTools "3D view" to visualize layer stacking
- Test overlays with multiple rows of content

### 4. Code Organization
```css
/* STACKING CONTEXT WARNING: This creates a new context */
.some-element {
    position: relative; /* Creates stacking context with z-index */
    z-index: 1;
}
```

---

## Testing Validation Checklist

### Visual Testing
- [ ] Tooltip fully visible when hovering any row
- [ ] Tooltip not clipped by subsequent rows
- [ ] Tooltip arrow points to correct badge
- [ ] Tooltip follows badge on window resize

### Technical Testing
- [ ] Check computed z-index in DevTools
- [ ] Verify stacking context hierarchy in 3D view
- [ ] Test with 20+ table rows
- [ ] Test with horizontal scroll
- [ ] Test on mobile devices

### Browser Testing
- [ ] Chrome/Edge (Blink engine)
- [ ] Firefox (Gecko engine)
- [ ] Safari (WebKit engine)
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

---

## Confidence Assessment

**Why 95% Confidence**:
1. Clear evidence of stacking context creation at line 339
2. Classic symptom pattern matching the diagnosis
3. Well-understood CSS specification behavior
4. Similar issues commonly seen in table-based layouts

**Remaining 5% Uncertainty**:
- Possible JavaScript dynamic styling not visible in static analysis
- Potential browser-specific rendering quirks
- Other CSS rules that might be injected at runtime

---

## Time Estimate Breakdown

- **Remove position: relative from tr**: 5 minutes
- **Test basic functionality**: 10 minutes
- **Implement additional safeguards**: 10 minutes
- **Cross-browser testing**: 10 minutes
- **Documentation updates**: 10 minutes
- **Total**: 45 minutes

---

## Additional Notes

1. **No transform or opacity issues found** - These would also create stacking contexts but are not present
2. **No filter or backdrop-filter properties** - These modern stacking context creators are absent
3. **overflow: visible is correctly set** - This allows content to escape, which is good
4. **The z-index: 9999 is high enough** - The value itself isn't the problem, it's the context isolation