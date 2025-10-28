# Frontend Testing Guide: Z-Index Stacking Context Issue

## Quick Reference Testing Commands

### Browser DevTools Console Commands

```javascript
// 1. Identify all stacking contexts in the page
Array.from(document.querySelectorAll('*')).filter(el => {
    const style = getComputedStyle(el);
    return (
        (style.position !== 'static' && style.zIndex !== 'auto') ||
        style.opacity < 1 ||
        style.transform !== 'none' ||
        style.filter !== 'none' ||
        style.perspective !== 'none' ||
        style.isolation === 'isolate' ||
        style.mixBlendMode !== 'normal' ||
        style.willChange === 'transform' || style.willChange === 'opacity'
    );
}).map(el => ({
    element: el,
    class: el.className,
    tag: el.tagName,
    zIndex: getComputedStyle(el).zIndex,
    position: getComputedStyle(el).position
}));

// 2. Check specific tooltip z-index and stacking context
const tooltip = document.querySelector('.booking-window-tooltip');
if (tooltip) {
    const rect = tooltip.getBoundingClientRect();
    console.log('Tooltip Info:', {
        computedZIndex: getComputedStyle(tooltip).zIndex,
        position: getComputedStyle(tooltip).position,
        bounds: rect,
        parent: tooltip.offsetParent,
        parentZIndex: tooltip.offsetParent ? getComputedStyle(tooltip.offsetParent).zIndex : null
    });
}

// 3. Find the problematic tbody tr elements
document.querySelectorAll('tbody tr').forEach((tr, index) => {
    const style = getComputedStyle(tr);
    if (style.position !== 'static') {
        console.log(`Row ${index + 1} creates stacking context:`, {
            position: style.position,
            zIndex: style.zIndex
        });
    }
});

// 4. Test tooltip visibility
function testTooltipVisibility() {
    const badges = document.querySelectorAll('.booking-window-status');
    badges.forEach((badge, i) => {
        badge.dispatchEvent(new MouseEvent('mouseenter'));
        const tooltip = badge.querySelector('.booking-window-tooltip');
        if (tooltip) {
            const rect = tooltip.getBoundingClientRect();
            const elementsAbove = document.elementsFromPoint(
                rect.left + rect.width/2,
                rect.top + rect.height/2
            );
            console.log(`Badge ${i + 1} tooltip covered by:`,
                elementsAbove.filter(el => !tooltip.contains(el) && el !== tooltip)
            );
        }
        badge.dispatchEvent(new MouseEvent('mouseleave'));
    });
}

// 5. Highlight all stacking contexts
function highlightStackingContexts() {
    const style = document.createElement('style');
    style.textContent = `
        *[style*="position: relative"],
        *[style*="position: absolute"],
        *[style*="position: fixed"],
        *[style*="position: sticky"] {
            outline: 2px solid red !important;
            outline-offset: -2px !important;
        }
    `;
    document.head.appendChild(style);

    // Also highlight computed styles
    document.querySelectorAll('*').forEach(el => {
        const computed = getComputedStyle(el);
        if (computed.position !== 'static' && computed.zIndex !== 'auto') {
            el.style.outline = '2px dashed blue';
            el.style.outlineOffset = '-1px';
        }
    });
}
```

---

## Manual Testing Checklist

### Phase 1: Initial State Verification

1. **Load the Page**
   - URL: `/Users/AIRBNB/Cursor_Projects/Pricelabs V4/Pricelabs/listingv5.html`
   - Ensure pricing table is fully loaded
   - Verify at least 10 rows are present

2. **Open DevTools**
   - Chrome: Cmd+Option+I (Mac) or F12 (Windows)
   - Navigate to Elements tab
   - Open Console for command testing

### Phase 2: Visual Inspection

1. **Hover Test Sequence**
   - [ ] Hover over first row's booking window badge
   - [ ] Observe: Is tooltip fully visible?
   - [ ] Observe: Are any parts cut off by the row below?

2. **Middle Row Test**
   - [ ] Hover over a middle row's booking window badge (row 5-10)
   - [ ] Check: Can you see the entire tooltip?
   - [ ] Check: Does the row below overlap the tooltip?

3. **Last Row Test**
   - [ ] Hover over the last row's booking window badge
   - [ ] Verify: Tooltip appears without clipping

4. **Screenshot Evidence**
   - [ ] Take screenshot of clipped tooltip (before fix)
   - [ ] Take screenshot of working tooltip (after fix)

### Phase 3: CSS Inspection

1. **Element Inspector Steps**
   ```
   1. Right-click on a booking window badge
   2. Select "Inspect"
   3. In Elements panel, hover to trigger tooltip
   4. Locate .booking-window-tooltip in DOM
   5. Check Computed styles tab
   6. Look for:
      - z-index value (should be 9999)
      - position value (should be absolute)
      - Actual stacking context parent
   ```

2. **Parent Chain Inspection**
   ```
   For each parent element going up:
   - tbody tr (CHECK: position value)
   - tbody (CHECK: position value)
   - table (CHECK: position value)
   - .table-container (CHECK: overflow values)
   ```

3. **3D Layer Visualization** (Chrome only)
   ```
   1. Open DevTools
   2. Press Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows)
   3. Type "Show Layers"
   4. Select "Show Layers" from command palette
   5. Observe the 3D layer stack
   6. Identify which layers are above tooltip
   ```

### Phase 4: Browser Testing Matrix

| Browser | Version | Test Status | Issues Found | Notes |
|---------|---------|-------------|--------------|-------|
| Chrome | Latest | [ ] | | Primary test browser |
| Firefox | Latest | [ ] | | Check for Gecko differences |
| Safari | Latest | [ ] | | WebKit stacking quirks |
| Edge | Latest | [ ] | | Should match Chrome |
| Mobile Safari | iOS 15+ | [ ] | | Touch interaction |
| Chrome Mobile | Latest | [ ] | | Android testing |

### Phase 5: Fix Validation

After implementing the fix:

1. **Verify Removal of Stacking Context**
   ```javascript
   // Run in console - should return empty array or fewer elements
   Array.from(document.querySelectorAll('tbody tr')).filter(tr =>
       getComputedStyle(tr).position !== 'static'
   );
   ```

2. **Tooltip Z-Index Test**
   ```javascript
   // Should now compete globally
   const tooltip = document.querySelector('.booking-window-tooltip');
   console.log('Global z-index competition:', {
       tooltipZ: getComputedStyle(tooltip).zIndex,
       parentIsBody: tooltip.offsetParent === document.body
   });
   ```

3. **Interaction Test**
   - [ ] Rapidly hover across multiple badges
   - [ ] Verify smooth tooltip transitions
   - [ ] Check no visual glitches

4. **Scroll Test**
   - [ ] Add enough rows to enable vertical scroll
   - [ ] Scroll while tooltip is visible
   - [ ] Verify tooltip maintains correct position

---

## Debug Visualization Techniques

### Technique 1: Outline Stacking Contexts

Add this temporary CSS to visualize:
```css
/* Add to browser DevTools */
tbody tr {
    outline: 3px solid red !important;
    outline-offset: -3px !important;
}

.booking-window-status {
    outline: 2px solid blue !important;
    outline-offset: -2px !important;
}

.booking-window-tooltip {
    outline: 2px solid green !important;
}
```

### Technique 2: Z-Index Labels

```javascript
// Add z-index labels to all positioned elements
document.querySelectorAll('[style*="position"]').forEach(el => {
    const zIndex = getComputedStyle(el).zIndex;
    if (zIndex !== 'auto') {
        const label = document.createElement('div');
        label.textContent = `z: ${zIndex}`;
        label.style.cssText = `
            position: absolute;
            top: 0;
            right: 0;
            background: yellow;
            color: black;
            font-size: 10px;
            padding: 2px;
            z-index: 10000;
        `;
        el.style.position = 'relative';
        el.appendChild(label);
    }
});
```

### Technique 3: Force Tooltip Visibility

```javascript
// Make all tooltips visible for debugging
document.querySelectorAll('.booking-window-tooltip').forEach(tt => {
    tt.style.opacity = '1';
    tt.style.pointerEvents = 'auto';
    tt.style.border = '2px solid red';
});
```

---

## Success Criteria

### ✅ Pass Criteria
1. Tooltip appears completely above all table content
2. No parts of tooltip are clipped or hidden
3. Tooltip maintains position during scroll
4. All rows' tooltips work consistently
5. No regression in other table functionality

### ❌ Fail Criteria
1. Any portion of tooltip appears behind table rows
2. Tooltip is clipped at edges
3. Z-index changes don't take effect
4. Other positioned elements break
5. Table layout is disrupted

---

## Performance Checks

```javascript
// Measure tooltip hover performance
const perfTest = () => {
    const badges = document.querySelectorAll('.booking-window-status');
    const times = [];

    badges.forEach(badge => {
        const start = performance.now();
        badge.dispatchEvent(new MouseEvent('mouseenter'));
        badge.dispatchEvent(new MouseEvent('mouseleave'));
        const end = performance.now();
        times.push(end - start);
    });

    console.log('Tooltip Performance:', {
        avg: times.reduce((a,b) => a+b, 0) / times.length,
        max: Math.max(...times),
        min: Math.min(...times)
    });
};

perfTest();
```

Target metrics:
- Average hover response: < 16ms
- Maximum response: < 50ms
- No visible lag or jank

---

## Regression Testing

After fix implementation, verify:

1. **Table Functionality**
   - [ ] Sorting still works (if applicable)
   - [ ] Row hover effects work
   - [ ] Cell selection works
   - [ ] Horizontal scroll works

2. **Other Tooltips/Overlays**
   - [ ] Check if any other tooltips exist
   - [ ] Verify modals still work
   - [ ] Dropdowns function correctly

3. **Responsive Behavior**
   - [ ] Test at 1920px width
   - [ ] Test at 1366px width
   - [ ] Test at 768px width (tablet)
   - [ ] Test at 375px width (mobile)

---

## Quick Fix Verification

Run this after applying the fix:

```javascript
// Complete fix verification
(() => {
    const results = {
        trPosition: Array.from(document.querySelectorAll('tbody tr'))
            .every(tr => getComputedStyle(tr).position === 'static'),
        tooltipsFound: document.querySelectorAll('.booking-window-tooltip').length,
        stackingContextsReduced: Array.from(document.querySelectorAll('*'))
            .filter(el => {
                const s = getComputedStyle(el);
                return s.position !== 'static' && s.zIndex !== 'auto';
            }).length < 10,
        tooltipZIndex: (() => {
            const tt = document.querySelector('.booking-window-tooltip');
            return tt ? getComputedStyle(tt).zIndex : 'N/A';
        })()
    };

    const allPassed = results.trPosition && results.stackingContextsReduced;

    console.log(allPassed ? '✅ FIX VERIFIED' : '❌ FIX INCOMPLETE', results);
    return allPassed;
})();
```

Expected output: `✅ FIX VERIFIED`