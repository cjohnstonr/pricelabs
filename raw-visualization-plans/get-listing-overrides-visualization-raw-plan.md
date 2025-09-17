# Get Listing Overrides Visualization Plan

## Data Structure Analysis

Based on the API response structure analysis from the actual examples, the GET `/v1/listings/{listing_id}/overrides` endpoint returns:

**Empty State Response:**
```json
{
  "overrides": []
}
```

**Populated Response (from update example):**
```json
{
  "overrides": [
    {
      "date": "2025-09-17",
      "price": "150",
      "price_type": "fixed",
      "currency": "USD",
      "min_stay": 2
    }
  ]
}
```

**Extended Structure (inferred from field patterns):**
```json
{
  "overrides": [
    {
      "date": "2025-09-17",
      "price": "150",
      "price_type": "fixed|percent",
      "currency": "USD",
      "min_stay": 2,
      "min_price": 100,
      "min_price_type": "fixed",
      "max_price": 200,
      "max_price_type": "fixed",
      "check_in_check_out_enabled": "1|0",
      "check_in": "0000010",
      "check_out": "0000001",
      "reason": "Special Event Pricing"
    }
  ]
}
```

## Visual Layout Design

### 1. Primary Layout Structure

#### Header Section
- **Title**: "Listing Price Overrides"
- **Listing Context Bar**: Display listing ID and quick navigation
- **Summary Statistics Panel**: 
  - Total active overrides count
  - Date range coverage (earliest to latest override)
  - Price type distribution (fixed vs. percentage)
  - Average override value

#### Main Content Area
- **Calendar Grid View** (Primary visualization)
- **Data Table View** (Secondary, toggleable)
- **Timeline Chart View** (Optional, for trend analysis)

### 2. Calendar Grid View (Primary)

#### Layout Structure
- Monthly calendar grid with navigation controls
- Each date cell displays override information when present
- Month/year navigation with quick jump controls
- View mode toggle (month, quarter, year overview)

#### Date Cell Design
```
┌─────────────────┐
│ 17      [$]    │ ← Date + Override indicator icon
│ $150 (Fixed)   │ ← Price + Type badge
│ Min: 2 nights  │ ← Minimum stay requirement
│ USD            │ ← Currency identifier
└─────────────────┘
```

#### Empty Date Cell
```
┌─────────────────┐
│ 18             │ ← Date only
│                │ ← No override data
│ + Add Override │ ← Action prompt on hover
│                │
└─────────────────┘
```

#### Color Coding System
- **Price Type Indicators**:
  - Fixed prices: Solid blue border (#2563EB)
  - Percentage adjustments: Orange border (#EA580C)
  - No override: Light gray background (#F9FAFB)
- **Price Level Indicators**:
  - Low prices: Green background tint
  - Medium prices: Yellow background tint
  - High prices: Red background tint
- **Minimum Stay Visual Cues**:
  - 1-2 nights: Single border line
  - 3-5 nights: Double border line
  - 6+ nights: Thick border line

### 3. Data Table View (Secondary)

#### Table Structure
| Date | Price | Type | Currency | Min Stay | Actions |
|------|-------|------|----------|----------|---------|
| 2025-09-17 | $150 | Fixed | USD | 2 nights | Edit/Delete |

#### Column Details
1. **Date**: Sortable, formatted for clarity (YYYY-MM-DD)
2. **Price**: Prominent display with currency symbol
3. **Type**: Badge indicator (Fixed/Percent)
4. **Currency**: Three-letter code
5. **Min Stay**: Number + "nights" label
6. **Min/Max Prices**: Range display when available
7. **Check-in/out Rules**: Visual status icons when available
8. **Reason**: Truncated text with full tooltip
9. **Actions**: Edit and delete buttons

#### Table Features
- **Sorting**: All columns sortable
- **Filtering**: Date range, price type, currency
- **Search**: Text search through reason field
- **Pagination**: For large datasets
- **Export**: CSV download functionality

### 4. Nested Data Handling

#### Price Information Display
- **Primary**: Main override price with clear currency
- **Secondary**: Min/max price bounds (when available)
- **Type Badge**: Visual indicator for fixed vs. percentage
- **Calculation Display**: Show percentage changes from base price

#### Check-in/out Restrictions (when available)
- **Binary String Parsing**: Convert day codes to readable format
- **Weekly Grid**: 7-day visual representation
- **Tooltip Details**: Full weekday availability status

```
Check-in Days Available:
[Mon] [Tue] [Wed] [Thu] [Fri] [Sat] [Sun]
  ❌    ❌    ❌    ❌    ❌    ✅    ❌
```

#### Reason Field Handling
- **Truncation**: Show first 50 characters in table
- **Full Display**: Complete text in modal/tooltip
- **Categorization**: Group similar reasons with color coding

### 5. Key Metrics Dashboard

#### Summary Cards
- **Active Overrides**: Total count with trend indicator
- **Price Impact**: Average override vs. base price comparison
- **Date Coverage**: Percentage of upcoming days with overrides
- **Revenue Impact**: Projected revenue change from overrides

#### Analytics Charts
- **Price Distribution**: Histogram of override values
- **Type Breakdown**: Pie chart (Fixed vs. Percentage)
- **Temporal Patterns**: Timeline showing override frequency
- **Min Stay Analysis**: Bar chart of stay requirements

### 6. Interactive Elements

#### Calendar Interactions
- **Hover Effects**: Show detailed override popup
- **Click Actions**: Open edit modal for existing overrides
- **Empty Date Click**: Quick add override form
- **Multi-select**: Range selection for bulk operations
- **Context Menu**: Right-click for quick actions

#### Modal Components
- **Override Details**: Full information display with edit option
- **Add Override**: Form for creating new date overrides
- **Edit Override**: Modification form with validation
- **Bulk Actions**: Apply changes to multiple selected dates
- **Import Data**: CSV upload for bulk override creation

#### Filter Controls
- **Date Range Picker**: Select viewing period
- **Price Type Filter**: Show only fixed or percentage
- **Currency Filter**: Multi-select for mixed currency listings
- **Min Stay Filter**: Range slider for minimum night requirements

### 7. Visual Hierarchy

#### Typography Scale
- **Section Headers**: 24px bold for main sections
- **Card Titles**: 18px semi-bold for data cards
- **Price Values**: 16px bold with currency symbols
- **Date Labels**: 14px regular for date identifiers
- **Meta Information**: 12px muted for secondary details

#### Spacing System
- **Card Padding**: 16px internal spacing
- **Grid Gaps**: 8px between calendar cells
- **Section Margins**: 24px between major sections
- **Element Spacing**: 4px between related items

### 8. Special Considerations

#### Empty State Management
- **No Overrides**: Welcoming empty state with add prompt
- **Date Range Empty**: Message suggesting different time period
- **Loading States**: Skeleton placeholders during data fetch
- **Error States**: Clear error messages with retry options

#### Data Validation Indicators
- **Invalid Dates**: Red border with error tooltip
- **Price Conflicts**: Warning for illogical min/max ranges
- **Currency Mismatches**: Alert badges for inconsistent currencies
- **Date Overlaps**: Highlight conflicting override dates

#### Performance Optimization
- **Lazy Loading**: Load overrides by month chunks
- **Virtual Calendar**: Render only visible date range
- **Debounced Search**: Optimize filter performance
- **Cached Data**: Store recent override queries

#### Responsive Design
- **Mobile (< 768px)**: 
  - Single column card layout
  - Simplified date picker
  - Touch-optimized buttons
- **Tablet (768px - 1024px)**:
  - Condensed calendar grid
  - Collapsible sidebar
  - Touch and mouse support
- **Desktop (> 1024px)**:
  - Full calendar grid
  - Side-by-side views
  - Advanced filtering sidebar

### 9. Advanced Features

#### Bulk Operations
- **Range Selection**: Click and drag date selection
- **Template Overrides**: Save common override patterns
- **Batch Import**: CSV file upload with validation
- **Copy Operations**: Duplicate overrides to multiple dates

#### Smart Suggestions
- **Pattern Recognition**: Identify recurring override patterns
- **Seasonal Intelligence**: Suggest overrides based on historical data
- **Market Integration**: Connect with market pricing data
- **Event Correlation**: Suggest overrides for local events

#### Integration Features
- **External Calendar**: Sync with property management systems
- **Pricing Rules**: Connect with automated pricing strategies
- **Reporting**: Generate override performance reports
- **API Access**: Webhook notifications for override changes

### 10. Accessibility Features

#### Screen Reader Support
- **ARIA Labels**: Comprehensive labeling for all elements
- **Keyboard Navigation**: Full functionality without mouse
- **Focus Management**: Logical tab order and focus indicators
- **Screen Reader Announcements**: Status updates and changes

#### Visual Accessibility
- **High Contrast Mode**: Alternative color scheme option
- **Text Scaling**: Support for user font size preferences
- **Color Independence**: Patterns and icons supplement color coding
- **Reduced Motion**: Respect user motion preferences

### 11. Error Handling

#### API Error Management
- **Network Failures**: Retry mechanisms with exponential backoff
- **Authentication Errors**: Clear re-login prompts
- **Rate Limiting**: Queue requests with user feedback
- **Data Conflicts**: Merge conflict resolution workflows

#### User Input Validation
- **Date Validation**: Prevent past dates and invalid ranges
- **Price Validation**: Ensure positive values and reasonable ranges
- **Currency Validation**: Check against supported currencies
- **Business Rule Validation**: Enforce minimum stay logic

#### Recovery Mechanisms
- **Auto-save**: Prevent data loss during editing
- **Offline Mode**: Basic functionality without network
- **Conflict Resolution**: Handle concurrent editing scenarios
- **Backup Restoration**: Undo recent changes

This comprehensive visualization plan provides an intuitive interface for managing listing price overrides while gracefully handling both empty states and complex nested data structures. The design prioritizes usability, accessibility, and performance while offering powerful features for property managers.