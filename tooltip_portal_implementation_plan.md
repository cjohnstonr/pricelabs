# Tooltip Portal Pattern - Detailed Implementation Plan

**Status:** READY FOR REVIEW - DO NOT IMPLEMENT YET
**Created:** 2025-10-24
**File:** listingv5.html
**Solution:** Portal Pattern (Solution 1 from investigation report)

---

## 📋 Executive Summary

This plan implements a **tooltip portal system** that moves tooltips outside the table's stacking context to fix the z-index clipping issue while preserving sticky header functionality.

### Key Strategy
1. Keep existing tooltip HTML generation unchanged
2. Move tooltips to global container on hover using JavaScript
3. Position tooltips using fixed positioning relative to viewport
4. Return tooltips to original location after hover

### Success Criteria
- ✅ Tooltips appear on top of all table rows
- ✅ Sticky headers remain functional
- ✅ Tooltips position correctly below badges
- ✅ Works after table refresh/filtering
- ✅ No visual glitches or flickering
- ✅ Performance impact < 5ms per tooltip

---

## 🔍 Current Code Analysis

### Existing Structure

**HTML Generation Flow:**
```
formatBookingWindowDisplay() [line 2323]
  ↓ generates HTML string
updatePricingTable() [line 1887]
  ↓ sets row.innerHTML [line 2147]
tbody.appendChild(row) [line 2168]
```

**Current Tooltip Activation:**
```css
/* Line 854-858 - CSS-only hover */
.booking-window-status:hover .booking-window-tooltip {
    opacity: 1;
    transform: translateX(-50%) translateY(4px);
    pointer-events: auto;
}
```

**Problematic Stacking Context:**
```css
/* Line 353-355 - Creates stacking context */
thead th {
    position: sticky;
    top: 0;
}

/* Line 340 - Row-level stacking contexts */
tbody tr {
    position: relative;
}
```

### Integration Points Identified

| Function | Line | Purpose | Modification Needed |
|----------|------|---------|---------------------|
| `updatePricingTable()` | 1887 | Renders table rows | Add tooltip initialization call |
| `formatBookingWindowDisplay()` | 2323 | Generates tooltip HTML | NO CHANGE |
| `DOMContentLoaded` handler | 1288 | Page initialization | Add global container creation |
| Filter onChange | 1138 | Table refresh | Already calls updatePricingTable() |
| `loadBookedDaysComponent()` | 2382 | Late table refresh | Already calls updatePricingTable() |

### JavaScript Patterns Observed

**Conventions in Current Code:**
- ✅ Uses vanilla JavaScript (no jQuery)
- ✅ Global variables declared at top of script section
- ✅ Functions use `async/await` for API calls
- ✅ DOM manipulation uses `getElementById`, `createElement`, `querySelector`
- ✅ Event listeners added in DOMContentLoaded
- ✅ Console logging for debugging
- ✅ Error handling with try/catch blocks
- ✅ Inline event handlers for simple cases (`onchange`)

**Naming Conventions:**
- Functions: `camelCase` (updatePricingTable, formatBookingWindowDisplay)
- Constants: `UPPER_SNAKE_CASE` (not prevalent)
- Variables: `camelCase` (tbody, tooltipData)
- Element IDs: `kebab-case` (pricing-table-body, availability-filter)

---

## 🎯 Implementation Plan

### Phase 1: HTML Structure Addition

**Location:** Before `</body>` tag (line 2659)

**Add Global Tooltip Container:**
```html
    <!-- Global Tooltip Portal Container -->
    <div id="global-tooltip-portal" class="tooltip-portal-container"></div>

    </script>
</body>
</html>
```

**Rationale:**
- Placed at end of body to ensure it's above all other content in DOM order
- Will have highest z-index via CSS
- Named descriptively to avoid conflicts

---

### Phase 2: CSS Modifications

**Location A:** After line 851 (within tooltip CSS section)

**Add Portal Container Styles:**
```css
        /* Global Tooltip Portal Container */
        .tooltip-portal-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 99999;
            /* Higher than tooltip's 9999 to ensure it's on top */
        }
```

**Location B:** Line 854-858 (MODIFY existing hover rule)

**Current Code:**
```css
        .booking-window-status:hover .booking-window-tooltip {
            opacity: 1;
            transform: translateX(-50%) translateY(4px);
            pointer-events: auto;
        }
```

**CHANGE TO:**
```css
        /* Hover rule DISABLED - JavaScript will handle tooltip visibility */
        /* .booking-window-status:hover .booking-window-tooltip {
            opacity: 1;
            transform: translateX(-50%) translateY(4px);
            pointer-events: auto;
        } */
```

**Rationale:**
- JavaScript will now control tooltip visibility
- CSS hover rule would conflict with portal positioning
- Commented out for easy rollback if needed

---

### Phase 3: JavaScript Implementation

#### 3A. Global Variables Declaration

**Location:** After line 1285 (with other global variables)

**Add:**
```javascript
        // Tooltip Portal System
        let activeTooltip = null;
        let tooltipCleanupTimer = null;
```

**Rationale:**
- Tracks currently visible tooltip to prevent multiple simultaneous tooltips
- Cleanup timer handles delayed return of tooltip to original parent

---

#### 3B. Portal System Core Functions

**Location:** After line 2357 (after formatBookingWindowDisplay function)

**Add Complete Portal System:**
```javascript
        // ============= TOOLTIP PORTAL SYSTEM =============

        /**
         * Creates global tooltip portal container in DOM if it doesn't exist
         * Called once on DOMContentLoaded
         */
        function createTooltipPortal() {
            if (document.getElementById('global-tooltip-portal')) {
                return; // Already exists
            }

            const portal = document.createElement('div');
            portal.id = 'global-tooltip-portal';
            portal.className = 'tooltip-portal-container';
            document.body.appendChild(portal);

            console.log('[Tooltip Portal] Global container created');
        }

        /**
         * Initializes tooltip event listeners for all booking window badges
         * Called after table is rendered/updated
         */
        function initializeTooltipPortals() {
            // Find all booking window status badges that have tooltips
            const badges = document.querySelectorAll('.booking-window-status');

            console.log(`[Tooltip Portal] Initializing ${badges.length} tooltip badges`);

            badges.forEach(badge => {
                const tooltip = badge.querySelector('.booking-window-tooltip');
                if (!tooltip) return;

                // Store reference to original parent for cleanup
                if (!tooltip.dataset.initialized) {
                    tooltip._originalParent = badge;
                    tooltip.dataset.initialized = 'true';

                    // Add event listeners to badge
                    badge.addEventListener('mouseenter', handleBadgeHover);
                    badge.addEventListener('mouseleave', handleBadgeLeave);
                }
            });
        }

        /**
         * Handles mouseenter on booking window badge
         * Portals the tooltip to global container and positions it
         */
        function handleBadgeHover(event) {
            const badge = event.currentTarget;
            const tooltip = badge.querySelector('.booking-window-tooltip');

            if (!tooltip) return;

            // Clear any pending cleanup
            if (tooltipCleanupTimer) {
                clearTimeout(tooltipCleanupTimer);
                tooltipCleanupTimer = null;
            }

            // Hide any currently active tooltip
            if (activeTooltip && activeTooltip !== tooltip) {
                hideTooltip(activeTooltip);
            }

            // Show this tooltip
            showTooltipInPortal(badge, tooltip);
            activeTooltip = tooltip;
        }

        /**
         * Handles mouseleave on booking window badge
         * Hides tooltip with delay to allow moving to tooltip
         */
        function handleBadgeLeave(event) {
            const badge = event.currentTarget;
            const tooltip = badge.querySelector('.booking-window-tooltip');

            if (!tooltip) return;

            // Delay hiding to allow user to move mouse to tooltip
            tooltipCleanupTimer = setTimeout(() => {
                hideTooltip(tooltip);
                if (activeTooltip === tooltip) {
                    activeTooltip = null;
                }
            }, 100); // 100ms grace period
        }

        /**
         * Shows tooltip in global portal with fixed positioning
         * @param {HTMLElement} badge - The badge element being hovered
         * @param {HTMLElement} tooltip - The tooltip to show
         */
        function showTooltipInPortal(badge, tooltip) {
            const portal = document.getElementById('global-tooltip-portal');
            if (!portal) {
                console.error('[Tooltip Portal] Global container not found!');
                return;
            }

            // Get badge position relative to viewport
            const badgeRect = badge.getBoundingClientRect();

            // Calculate tooltip position
            const left = badgeRect.left + (badgeRect.width / 2);
            const top = badgeRect.bottom + 4; // 4px gap (matches CSS)

            // Move tooltip to portal
            portal.appendChild(tooltip);

            // Apply fixed positioning
            tooltip.style.position = 'fixed';
            tooltip.style.top = top + 'px';
            tooltip.style.left = left + 'px';
            tooltip.style.transform = 'translateX(-50%)'; // Center horizontally
            tooltip.style.zIndex = '99999';

            // Make visible (trigger CSS transition)
            requestAnimationFrame(() => {
                tooltip.style.opacity = '1';
                tooltip.style.pointerEvents = 'auto';
            });

            console.log('[Tooltip Portal] Tooltip shown at', { left, top });
        }

        /**
         * Hides tooltip and returns it to original parent
         * @param {HTMLElement} tooltip - The tooltip to hide
         */
        function hideTooltip(tooltip) {
            if (!tooltip) return;

            // Fade out
            tooltip.style.opacity = '0';
            tooltip.style.pointerEvents = 'none';

            // Wait for CSS transition (200ms) then return to parent
            setTimeout(() => {
                const originalParent = tooltip._originalParent;

                if (originalParent && tooltip.style.opacity === '0') {
                    // Return to original parent
                    originalParent.appendChild(tooltip);

                    // Reset to CSS-controlled positioning
                    tooltip.style.position = '';
                    tooltip.style.top = '';
                    tooltip.style.left = '';
                    tooltip.style.transform = '';
                    tooltip.style.zIndex = '';

                    console.log('[Tooltip Portal] Tooltip returned to original parent');
                }
            }, 200); // Match CSS transition duration
        }

        /**
         * Cleanup function to remove all tooltip event listeners
         * Useful for testing/debugging
         */
        function cleanupTooltipPortals() {
            const badges = document.querySelectorAll('.booking-window-status');
            badges.forEach(badge => {
                badge.removeEventListener('mouseenter', handleBadgeHover);
                badge.removeEventListener('mouseleave', handleBadgeLeave);
            });

            if (activeTooltip) {
                hideTooltip(activeTooltip);
                activeTooltip = null;
            }

            console.log('[Tooltip Portal] Cleaned up all tooltip listeners');
        }
```

**Rationale for Design Decisions:**

1. **Function Naming:** Follows existing camelCase convention
2. **Console Logging:** Matches existing debug pattern for troubleshooting
3. **Dataset Attribute:** Uses `dataset.initialized` to prevent duplicate listeners
4. **Grace Period:** 100ms delay allows mouse movement to tooltip
5. **RequestAnimationFrame:** Ensures CSS transition triggers properly
6. **Error Handling:** Defensive checks for missing elements
7. **Cleanup Function:** Provided for debugging/testing scenarios

---

#### 3C. DOMContentLoaded Integration

**Location:** Line 1288-1301 (MODIFY existing DOMContentLoaded handler)

**Current Code:**
```javascript
        window.addEventListener('DOMContentLoaded', () => {
            const urlParams = new URLSearchParams(window.location.search);
            const listingId = urlParams.get('listing_id');
            const portfolioKey = urlParams.get('portfolio_key');

            if (listingId) {
                document.getElementById('listing-id-input').value = listingId;
                // Store portfolio_key for reference (backend auto-detects, but good for UX)
                if (portfolioKey) {
                    console.log(`Loading listing ${listingId} from portfolio: ${portfolioKey}`);
                }
                loadDashboard();
            }
        });
```

**CHANGE TO:**
```javascript
        window.addEventListener('DOMContentLoaded', () => {
            // Initialize tooltip portal system
            createTooltipPortal();

            const urlParams = new URLSearchParams(window.location.search);
            const listingId = urlParams.get('listing_id');
            const portfolioKey = urlParams.get('portfolio_key');

            if (listingId) {
                document.getElementById('listing-id-input').value = listingId;
                // Store portfolio_key for reference (backend auto-detects, but good for UX)
                if (portfolioKey) {
                    console.log(`Loading listing ${listingId} from portfolio: ${portfolioKey}`);
                }
                loadDashboard();
            }
        });
```

**Rationale:**
- Creates portal container as early as possible
- Runs before any dashboard loading
- One-time initialization

---

#### 3D. Table Update Integration

**Location:** Line 2168-2170 (MODIFY end of updatePricingTable function)

**Current Code:**
```javascript
                tbody.appendChild(row);
            });
        }
```

**CHANGE TO:**
```javascript
                tbody.appendChild(row);
            });

            // Initialize tooltip portals for newly rendered badges
            initializeTooltipPortals();
        }
```

**Rationale:**
- Called every time table is refreshed (filter change, data load)
- Ensures all new badges get event listeners
- `dataset.initialized` prevents duplicate listeners on existing badges

---

### Phase 4: Edge Case Handling

**Scroll Handling:**
- **Issue:** Fixed positioning is relative to viewport, not scroll position
- **Solution:** Current implementation uses `getBoundingClientRect()` which accounts for scroll
- **Status:** ✅ Handled automatically

**Window Resize:**
- **Issue:** Tooltip position may become incorrect if window resizes while tooltip is visible
- **Solution:** Hide tooltips on resize (optional enhancement)
- **Status:** ⚠️ Low priority - users rarely resize during hover

**Table Filter/Refresh:**
- **Issue:** Table rows get replaced, orphaning tooltips
- **Solution:** `hideTooltip()` gracefully handles missing original parent
- **Status:** ✅ Handled by cleanup timer

**Rapid Hover/Unhover:**
- **Issue:** Tooltip might flicker between states
- **Solution:** `clearTimeout()` on hover prevents premature cleanup
- **Status:** ✅ Handled by cleanup timer logic

**Multiple Simultaneous Hovers:**
- **Issue:** User hovers multiple badges quickly
- **Solution:** `activeTooltip` tracking ensures only one tooltip visible
- **Status:** ✅ Handled by state management

---

## 🧪 Testing Plan

### Manual Testing Checklist

**Basic Functionality:**
- [ ] Hover over booking window badge
- [ ] Tooltip appears below badge
- [ ] Tooltip is fully visible (not clipped by table rows)
- [ ] Tooltip disappears on mouse leave
- [ ] Tooltip appears on top of all subsequent rows

**Table Interactions:**
- [ ] Change availability filter → table refreshes → tooltips still work
- [ ] Scroll table horizontally → tooltips position correctly
- [ ] Scroll table vertically → tooltips position correctly
- [ ] Resize browser window → tooltips behave gracefully

**Edge Cases:**
- [ ] Hover badge quickly and move away → no orphaned tooltips
- [ ] Hover multiple badges in succession → only one tooltip visible
- [ ] Hover near viewport edge → tooltip doesn't clip off screen (⚠️ May need bounds checking)
- [ ] Open DevTools → no console errors
- [ ] Navigate to different listing → tooltips work on new data

**Performance:**
- [ ] No visible lag when hovering
- [ ] Table render time not significantly impacted
- [ ] Browser memory usage stable (check DevTools Performance tab)

**Cross-Browser:**
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if applicable)

### Automated Testing (Future Enhancement)

**Console Verification:**
```javascript
// Run in browser console after page load
console.log('Portal exists:', !!document.getElementById('global-tooltip-portal'));
console.log('Badge count:', document.querySelectorAll('.booking-window-status').length);
console.log('Tooltip count:', document.querySelectorAll('.booking-window-tooltip').length);
```

---

## 🚨 Potential Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|---------|------------|
| Tooltip clips off screen near edges | Medium | Low | Add bounds checking in future iteration |
| Performance impact on large tables | Low | Medium | Current approach is lightweight; monitor |
| Tooltip orphaned if table refreshed during hover | Low | Low | Cleanup timer handles gracefully |
| CSS transition conflicts | Very Low | Low | Uses same timing as existing CSS |
| Event listener memory leaks | Very Low | High | Cleanup function provided; proper parent restoration |

---

## 📊 Performance Considerations

**Estimated Impact:**

| Operation | Current | With Portal | Difference |
|-----------|---------|-------------|------------|
| Table render (90 rows) | ~50ms | ~53ms | +3ms |
| Tooltip show | N/A | ~2ms | New operation |
| Tooltip hide | N/A | ~1ms | New operation |
| Memory overhead | 0 | ~5KB | Negligible |

**Optimization Notes:**
- Event listeners added per badge (not delegated) for simplicity
- If performance becomes an issue, consider event delegation on `tbody`
- `requestAnimationFrame` ensures efficient DOM updates

---

## 🔄 Rollback Plan

If issues arise, rollback is straightforward:

1. **Remove JavaScript additions:**
   - Remove portal functions (Phase 3B)
   - Remove `createTooltipPortal()` call from DOMContentLoaded
   - Remove `initializeTooltipPortals()` call from updatePricingTable

2. **Restore CSS:**
   - Uncomment the hover rule (line 854-858)

3. **Remove HTML:**
   - Delete global tooltip portal container div

**Estimated rollback time:** < 5 minutes

---

## 📝 Code Review Checklist

Before implementation approval:

- [ ] Plan reviewed by developer
- [ ] Line numbers verified in current listingv5.html
- [ ] JavaScript conventions match existing codebase
- [ ] CSS z-index hierarchy understood
- [ ] Edge cases documented
- [ ] Testing plan comprehensive
- [ ] Rollback plan clear
- [ ] Performance impact acceptable
- [ ] No breaking changes to existing functionality

---

## 🎯 Success Metrics

**Must Achieve:**
1. ✅ Tooltips appear on top of all table rows (100% of cases)
2. ✅ Sticky headers remain functional
3. ✅ No console errors
4. ✅ No visual glitches

**Nice to Have:**
1. Performance impact < 5ms per operation
2. Works on 95% of modern browsers
3. Graceful degradation if JavaScript fails

---

## 📅 Implementation Timeline

**Estimated Effort:**
- Phase 1 (HTML): 2 minutes
- Phase 2 (CSS): 3 minutes
- Phase 3 (JavaScript): 10 minutes
- Phase 4 (Edge cases): Already handled in Phase 3
- Testing: 15 minutes
- **Total:** ~30 minutes implementation + testing

---

## 🔍 Post-Implementation Verification

After implementation, verify:

```javascript
// Run in browser console
console.group('Tooltip Portal Verification');
console.log('✓ Portal exists:', !!document.getElementById('global-tooltip-portal'));
console.log('✓ Badge count:', document.querySelectorAll('.booking-window-status').length);
console.log('✓ Initialized badges:', document.querySelectorAll('[data-initialized="true"]').length);
console.log('✓ Active tooltip:', activeTooltip ? 'Yes' : 'No');
console.groupEnd();
```

**Expected Output:**
```
Tooltip Portal Verification
  ✓ Portal exists: true
  ✓ Badge count: 90 (or current row count)
  ✓ Initialized badges: 90 (should match badge count)
  ✓ Active tooltip: No (unless hovering)
```

---

## 📚 References

- **Investigation Report:** `tooltip_investigation_report.md`
- **Current File:** `listingv5.html` (2660 lines)
- **Test Page:** `test_tooltip.html` (100 lines)
- **CSS Stacking Context Spec:** [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_positioned_layout/Understanding_z-index/Stacking_context)

---

## ✅ Approval Sign-Off

**Plan Status:** ⏳ PENDING REVIEW

**Reviewer:** _________________
**Date:** _________________
**Approved:** ☐ YES  ☐ NO  ☐ NEEDS REVISION

**Notes:**
```
[Space for reviewer feedback]
```

---

**END OF IMPLEMENTATION PLAN**

*This document will be updated with actual implementation results and any deviations from the plan.*
