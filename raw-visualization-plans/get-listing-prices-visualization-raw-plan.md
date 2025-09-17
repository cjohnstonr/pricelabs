# Get Listing Prices API - Visualization Plan

Generated: 2025-09-16T15:32:39.048917

## Overview
The Get Listing Prices API returns complex pricing data for listings including daily prices, market factors, customizations, and detailed pricing breakdowns. This requires a sophisticated visualization approach to handle both error states and rich pricing analytics data.

## Data Structure Analysis

### Top-Level Response Structure
- **Array of listing objects** - Each represents one listing's pricing data
- **Error handling** - Some listings may return errors instead of pricing data
- **Mixed success/error responses** - Array can contain both successful and failed listing responses

### Successful Response Fields (Per Listing)
1. **Basic Info**: `id`, `pms`, `group`, `currency`, `last_refreshed_at`
2. **Length of Stay Pricing**: `los_pricing` object with adjustments
3. **Daily Price Data**: `data` array with extensive per-date information
4. **Market Factors**: Nested pricing adjustment explanations
5. **Customizations**: Applied pricing rules and adjustments
6. **Debug Information**: Technical pricing calculation details

### Daily Price Data Fields (Most Complex)
Each date entry contains:
- **Core Pricing**: `price`, `user_price`, `uncustomized_price`
- **Booking Rules**: `min_stay`, `check_in`, `check_out`
- **Market Data**: `booking_status`, `ADR`, `demand_color`, `demand_desc`
- **Discounts**: `weekly_discount`, `monthly_discount`
- **Fees**: `extra_person_fee`, `extra_person_fee_trigger`
- **Detailed Breakdowns**: `reason`, `market_factors`, `pricing_customizations`, `thresholds`

## Visualization Plan

### 1. Main Layout Structure

#### Header Section
- **API Endpoint Title**: "Get Listing Prices Results"
- **Timestamp**: Show when data was generated
- **Summary Stats**: Total listings processed, success count, error count
- **Filter Controls**: Date range picker, currency filter, error/success toggle

#### Content Layout
- **Two-column responsive layout**
- **Left column**: Listing summaries and controls (30% width)
- **Right column**: Detailed pricing visualization (70% width)

### 2. Left Column - Listing Management

#### Listing Summary Cards
```html
[Card for each listing]
├── Header: Listing ID + PMS badge
├── Status indicator (success/error)
├── Quick stats (if successful):
│   ├── Price range: $X - $Y
│   ├── Currency badge
│   └── Last refreshed timestamp
├── Error details (if failed):
│   ├── Error message
│   └── Error status badge
└── Click to select for detailed view
```

#### Error State Handling
- **Red border** for error cards
- **Error badges**: 
  - `LISTING_TOGGLE_OFF` - Orange warning
  - `LISTING_NOT_PRESENT` - Red error
  - `LISTING_NO_DATA` - Yellow info
- **Error explanations** with actionable advice

### 3. Right Column - Detailed Pricing Visualization

#### Top Section - Listing Overview
```html
[When listing selected]
├── Listing header with ID, PMS, Group
├── Currency and last refresh info
├── Length of Stay pricing table (if available)
└── Quick action buttons (refresh, edit, etc.)
```

#### Main Pricing Charts

##### Primary Chart - Price Timeline
- **Chart Type**: Line chart with multiple series
- **X-Axis**: Dates from the data array
- **Y-Axis**: Price values
- **Series**:
  1. **Recommended Price** (blue line) - `price` field
  2. **User Override Price** (green line) - `user_price` field  
  3. **Uncustomized Price** (gray dashed) - `uncustomized_price` field
- **Interactive Features**:
  - Hover tooltips with full date details
  - Click to drill down to specific date
  - Zoom/pan functionality
  - Demand color coding as background

##### Secondary Visualizations

###### Demand & Availability Chart
- **Chart Type**: Horizontal bar chart below price chart
- **Data**: `demand_desc` and `demand_color` per date
- **Visual**: Color-coded bars showing demand levels
- **Labels**: "Low Demand", "High Demand", etc.

###### Min Stay Requirements
- **Chart Type**: Step chart
- **Data**: `min_stay` values over time
- **Visual**: Steps showing minimum stay requirements
- **Color coding**: Different colors for different stay lengths

#### Bottom Section - Detailed Analytics

##### Date Detail Panel (When Date Selected)
```html
[Expandable panel for selected date]
├── Price Breakdown Card:
│   ├── Final Price (large, prominent)
│   ├── User Override (if different)
│   ├── Uncustomized Price
│   └── Currency symbol
├── Booking Rules Card:
│   ├── Minimum Stay
│   ├── Check-in/out allowed badges
│   ├── Weekly/Monthly discount %
│   └── Extra person fees
├── Market Factors Card:
│   ├── Seasonality adjustment
│   ├── Demand factor breakdown
│   ├── Hotel vs STR demand split
│   └── Visual percentage indicators
├── Pricing Customizations Card:
│   ├── Last minute factors
│   ├── Occupancy adjustments
│   ├── Custom rules applied
│   └── Before/after price comparisons
└── Thresholds & Safety Card:
    ├── Min/Max price limits
    ├── Applied safety rules
    └── Constraint violations (if any)
```

##### Length of Stay Pricing Table
```html
[Table when LOS data available]
├── Columns: Stay Length | Adjustment % | Min Price | Max Price
├── Sortable by adjustment percentage
├── Color coding: Green for discounts, Red for premiums
└── Click to highlight dates with that LOS
```

### 4. Interactive Elements

#### Date Range Selection
- **Calendar widget** for selecting date ranges
- **Quick presets**: "Next 7 days", "Next month", "Custom range"
- **Sync with charts** to update displayed data

#### Price Comparison Tools
- **Toggle switches** for showing/hiding price series
- **Percentage view** option to show changes relative to base
- **Currency conversion** if multiple currencies present

#### Export & Sharing
- **Export buttons**: CSV, PDF report, PNG charts
- **Share link** generation for specific views
- **Print-friendly** layout option

### 5. Visual Design Specifications

#### Color Scheme
- **Primary Price Line**: #2563eb (blue)
- **User Override**: #16a34a (green) 
- **Uncustomized**: #64748b (gray)
- **Demand Colors**: Use API-provided `demand_color` values
- **Error States**: #dc2626 (red)
- **Warning States**: #ea580c (orange)
- **Success States**: #16a34a (green)

#### Typography
- **Headers**: 24px bold for main titles
- **Subheaders**: 18px semibold for section titles  
- **Body**: 14px regular for general text
- **Price Values**: 20px bold for prominent pricing
- **Monospace**: For IDs and technical values

#### Spacing & Layout
- **Card Padding**: 16px internal padding
- **Card Spacing**: 12px between cards
- **Section Margins**: 24px between major sections
- **Responsive Breakpoints**: 
  - Mobile: < 768px (single column)
  - Tablet: 768px - 1024px (adjusted ratios)
  - Desktop: > 1024px (full two-column)

### 6. Special Considerations

#### Performance Optimization
- **Lazy loading** for large date ranges
- **Virtualization** for extensive listing arrays
- **Chart debouncing** to prevent excessive re-renders
- **Progressive data loading** for complex breakdown data

#### Accessibility
- **ARIA labels** for all interactive elements
- **Keyboard navigation** support
- **Screen reader** compatible chart descriptions
- **High contrast mode** support
- **Alt text** for visual indicators

#### Error Recovery
- **Graceful degradation** when partial data fails
- **Retry mechanisms** for failed API calls
- **Offline indicators** when data is stale
- **Validation warnings** for inconsistent data

#### Data Handling Edge Cases
- **Missing dates** in data arrays
- **Currency mismatches** between listings
- **Timezone considerations** for date displays
- **Large price ranges** requiring logarithmic scales
- **Empty or null** pricing customizations

### 7. User Experience Flow

#### Initial Load
1. Show loading skeleton while fetching data
2. Display summary statistics first
3. Populate listing cards as data arrives
4. Auto-select first successful listing for detail view

#### Navigation Pattern
1. User selects listing from left panel
2. Right panel updates with pricing charts
3. User can select specific dates for detailed breakdown
4. Drill-down panels expand with comprehensive data
5. Easy return to overview via breadcrumbs

#### Mobile Experience
1. Single column layout with collapsible sections
2. Swipe navigation between listings
3. Tap-to-expand detail panels
4. Simplified chart interactions (touch-friendly)
5. Bottom sheet for date details

This visualization plan provides a comprehensive, user-friendly interface for understanding complex pricing data while handling both successful responses and various error states effectively.