# Get Specific Listing Visualization Plan

Generated: 2025-09-16

## Overview
This plan outlines how to visualize the get-specific-listing API response data in an intuitive HTML interface that presents complex nested pricing, occupancy, and performance metrics in a clear, actionable format.

## 1. Visual Layout Structure

### Main Container Layout
- **Header Card**: Property identification and basic info
- **Performance Dashboard**: Key metrics in tiles/cards
- **Pricing Analysis Section**: Current and historical pricing data
- **Occupancy Analytics**: Current vs market occupancy comparisons
- **Revenue Tracking**: Revenue performance with trend indicators
- **Settings & Status Panel**: Push settings and operational status

## 2. Component Breakdown

### Header Card (Property Identity)
```
┌─────────────────────────────────────────────────────────┐
│ [PROPERTY ICON] PAG12161 · Mountaintop Estate...       │
│ 📍 Lakeside, California, United States                 │
│ 🛏️ 5 Bedrooms | 🏠 Airbnb | 🏷️ CJ, Pagosa           │
│ Status: [HIDDEN BADGE] [PUSH DISABLED BADGE]           │
└─────────────────────────────────────────────────────────┘
```

### Performance Dashboard (Top Metrics Grid)
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ Base Price  │ Revenue     │ Occupancy   │ MPI Score   │
│ $891        │ $3,440      │ 100%        │ 2.6         │
│ [vs $891]   │ [vs Market] │ [vs 46%]    │ [EXCELLENT] │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

### Pricing Analysis Section
**Visual Elements:**
- Price range slider showing min ($100) to max ($1,750) with current base ($891)
- Recommended price indicator vs current base price
- ADR comparison chart (current vs same-time-last-year)

### Occupancy Analytics
**Interactive Charts:**
- Dual-bar chart comparing property vs market occupancy (7, 30, 60 days)
- Color-coded performance indicators (green for outperforming market)
- MPI trend line for forward-looking periods

### Revenue Tracking
**Visualization Components:**
- Revenue comparison cards (past vs projected, current year vs STLY)
- Trend arrows indicating performance direction
- Booking pickup metrics with visual indicators

## 3. Nested Data Structure Handling

### Occupancy Data Grouping
```javascript
occupancyData = {
  periods: ['7 days', '30 days', '60 days'],
  property: [100, 100, 100],
  market: [46, 38, 31],
  comparison: ['outperforming', 'outperforming', 'outperforming']
}
```

### Revenue Data Organization
```javascript
revenueData = {
  historical: {
    past30: { current: 3440, stly: 10491 },
    past90_adr: { current: 974, stly: 1221 }
  },
  projected: {
    next30: { current: 441, stly: 15760 },
    next180: { current: 4389, stly: 69957, adr: 549, stly_adr: 760 }
  }
}
```

### MPI Data Structure
```javascript
mpiData = {
  current: 2.6,
  forecasts: [
    { period: '30 days', value: 2.6 },
    { period: '60 days', value: 3.2 },
    { period: '90 days', value: 4.0 },
    { period: '120 days', value: 4.5 },
    { period: '180 days', value: 6.1 }
  ]
}
```

## 4. Key Metrics to Highlight

### Critical Performance Indicators
1. **Occupancy Outperformance**: 100% vs market 46% (next 7 days)
2. **Revenue Underperformance**: Current revenue significantly below STLY
3. **MPI Strength**: Consistent strong market position (2.6-6.1)
4. **Pricing Opportunity**: Base price aligns with recommendation
5. **Booking Activity**: Recent booking (Sept 2nd) with 2 pickups in 30 days

### Alert-Worthy Metrics
- Revenue performance significantly below last year (highlight in orange/red)
- Occupancy well above market (highlight in green)
- Push disabled status (highlight as action item)
- Property hidden status (show as informational)

## 5. Interactive Elements

### Primary Interactions
1. **Time Period Toggles**: Switch between 7/30/60/90/180 day views
2. **Comparison Mode**: Toggle between absolute values and percentages
3. **Drill-Down Cards**: Click to expand detailed breakdowns
4. **Data Export**: Export current view as CSV/PDF
5. **Refresh Status**: Show last refresh time with manual refresh option

### Secondary Interactions
1. **Hover Tooltips**: Detailed explanations for each metric
2. **Settings Panel**: Toggle push settings (if permissions allow)
3. **Historical View**: Slide to see data trends over time
4. **Market Context**: Show market benchmark information

## 6. Color Coding & Visual Hierarchy

### Color Scheme
```css
:root {
  --success: #10B981 (outperforming metrics)
  --warning: #F59E0B (needs attention)
  --danger: #EF4444 (underperforming)
  --info: #3B82F6 (neutral information)
  --muted: #6B7280 (secondary data)
  --bg-primary: #FFFFFF
  --bg-secondary: #F9FAFB
}
```

### Visual Hierarchy
1. **Level 1**: Property name and key status indicators
2. **Level 2**: Performance dashboard tiles
3. **Level 3**: Detailed charts and comparisons
4. **Level 4**: Historical data and trends
5. **Level 5**: Metadata and timestamps

### Status Indicators
- **Green**: Outperforming market, strong MPI, good occupancy
- **Orange**: Revenue below STLY, attention needed
- **Red**: Critical underperformance or errors
- **Blue**: Neutral information, settings, metadata
- **Gray**: Disabled features, unavailable data

## 7. Special Considerations

### Data Availability Handling
- **"Unavailable" Data**: Show placeholder with explanation
- **Null Values**: Display as "Not Set" with option to configure
- **Zero Values**: Distinguish between "no data" and "zero performance"

### Responsive Design Considerations
- **Mobile**: Stack cards vertically, simplify charts
- **Tablet**: Two-column layout for main metrics
- **Desktop**: Full dashboard layout with side panels

### Performance Optimization
- **Lazy Loading**: Load detailed charts only when visible
- **Data Caching**: Cache API responses for quick re-renders
- **Progressive Enhancement**: Show basic data first, enhance with charts

### Accessibility Features
- **Screen Reader Support**: Proper ARIA labels for all metrics
- **Keyboard Navigation**: Tab through all interactive elements
- **High Contrast Mode**: Alternative color scheme for accessibility
- **Text Scaling**: Support browser zoom and text size preferences

### Real-Time Features
- **Auto-Refresh**: Option to auto-refresh data every X minutes
- **Change Indicators**: Show what changed since last refresh
- **Push Status**: Real-time indication of pricing push status
- **Alert Notifications**: Browser notifications for significant changes

## 8. Implementation Priority

### Phase 1 (MVP)
1. Basic property information card
2. Key metrics dashboard
3. Simple occupancy vs market comparison
4. Revenue performance indicators

### Phase 2 (Enhanced)
1. Interactive charts and graphs
2. Time period toggles
3. Historical comparisons
4. Detailed tooltips

### Phase 3 (Advanced)
1. Real-time updates
2. Export functionality
3. Advanced filtering options
4. Predictive trend indicators

This visualization plan creates a comprehensive, user-friendly interface that transforms complex API data into actionable insights for property managers and revenue optimization teams.