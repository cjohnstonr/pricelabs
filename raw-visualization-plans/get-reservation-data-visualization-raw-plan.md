# Get Reservation Data Visualization Plan

Generated: 2025-09-16

## Data Structure Analysis

The Get Reservation Data API returns a structured response containing:
- **Top-level metadata**: `pms_name`, `next_page` (pagination indicator)
- **Reservations array**: Contains individual reservation objects with comprehensive booking details

### Individual Reservation Structure:
- **Identifiers**: `listing_id`, `listing_name`, `reservation_id`
- **Dates**: `check_in`, `check_out`, `booked_date`, `cancelled_on`
- **Financial**: `rental_revenue`, `total_cost`, `cleaning_fees`, `currency`
- **Booking Details**: `booking_status`, `no_of_days`
- **Optional Fields**: `channelConfirmationCode`, `guestName` (often null)

## Visual Layout Design

### 1. Main Dashboard Layout
```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER: Reservation Data Dashboard                              │
│ PMS: Airbnb | Total Reservations: X | Page Navigation          │
├─────────────────────────────────────────────────────────────────┤
│ KEY METRICS CARDS ROW                                           │
│ [Total Revenue] [Avg Stay] [Active Bookings] [Cancelled Rate]   │
├─────────────────────────────────────────────────────────────────┤
│ FILTERS & CONTROLS                                              │
│ Date Range | Status | Property | Sort Options                   │
├─────────────────────────────────────────────────────────────────┤
│ RESERVATION CARDS GRID                                          │
│ [Card 1] [Card 2] [Card 3]                                      │
│ [Card 4] [Card 5] [Card 6]                                      │
├─────────────────────────────────────────────────────────────────┤
│ DETAILED TABLE VIEW (Toggle)                                    │
│ Sortable columns with all reservation details                   │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Individual Reservation Card Design
```
┌─────────────────────────────────────────────────────────────────┐
│ 🏠 LISTING NAME (truncated with tooltip)           STATUS BADGE │
│ Reservation ID: HM3MFTWPAE                                      │
├─────────────────────────────────────────────────────────────────┤
│ 📅 Sep 1-4, 2025 (3 nights)                                    │
│ 💰 $969.64 revenue | $1,438.12 total                           │
│ 🧹 $400 cleaning fee                                            │
├─────────────────────────────────────────────────────────────────┤
│ Booked: Jul 23, 2025 | Cancelled: Jul 23, 2025                 │
│ [View Details] [Actions Menu ▼]                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Handling Nested Data Structures

### 1. Flat Structure Approach
- The reservation data is relatively flat, making visualization straightforward
- Group reservations by `listing_id` to show property-based clusters
- Create expandable sections for each property showing all its reservations

### 2. Data Relationships
- **Property Grouping**: Cluster reservations by `listing_id` and `listing_name`
- **Timeline View**: Show reservations on a calendar timeline
- **Financial Aggregation**: Sum revenues and costs by property and time period

### 3. Null Value Handling
- `channelConfirmationCode` and `guestName` often null - show "N/A" or hide fields
- Provide clear indicators when optional data is missing

## Key Metrics to Highlight

### 1. Primary KPIs (Top Cards)
- **Total Revenue**: Sum of all `rental_revenue` values with currency
- **Average Daily Rate**: `rental_revenue` / `no_of_days` across all reservations
- **Occupancy Rate**: Percentage of days booked vs. available
- **Cancellation Rate**: Percentage of reservations with `cancelled_on` dates

### 2. Secondary Metrics
- **Average Stay Length**: Mean of `no_of_days` values
- **Revenue per Property**: Grouped by `listing_id`
- **Booking Lead Time**: Days between `booked_date` and `check_in`
- **Cleaning Fee Impact**: Percentage of total cost from cleaning fees

### 3. Financial Breakdowns
- **Revenue vs. Total Cost**: Show margin analysis
- **Cleaning Fee Analysis**: Impact on total pricing
- **Property Performance**: Revenue ranking by listing

## Interactive Elements Needed

### 1. Filtering Controls
- **Date Range Picker**: Filter by check-in, check-out, or booking dates
- **Status Filter**: Toggle between booked, cancelled, or all
- **Property Selector**: Multi-select dropdown for specific listings
- **Revenue Range**: Slider for minimum/maximum revenue amounts

### 2. Sorting Options
- **Date Sorting**: By check-in, check-out, or booking date
- **Revenue Sorting**: Ascending/descending by revenue or total cost
- **Property Sorting**: Alphabetical by listing name
- **Stay Length**: Sort by number of days

### 3. View Toggles
- **Card vs. Table View**: Switch between visual cards and detailed table
- **Property Grouping**: Toggle grouped vs. flat view
- **Timeline View**: Calendar visualization of reservations
- **Chart Views**: Revenue trends, booking patterns, property performance

### 4. Action Controls
- **Pagination**: Navigate through multiple pages when `next_page` is true
- **Export Options**: CSV/PDF export of filtered data
- **Refresh Data**: Manual refresh button
- **Print View**: Optimized layout for printing

## Color Coding and Visual Hierarchy

### 1. Status Color Coding
- **Booked Reservations**: Green (#10B981) for active bookings
- **Cancelled Reservations**: Red (#EF4444) with strikethrough text
- **High Revenue**: Gold/yellow accent (#F59E0B) for premium bookings
- **Recent Bookings**: Blue accent (#3B82F6) for bookings within 7 days

### 2. Visual Hierarchy
- **Primary Information**: Large, bold text for listing names and reservation IDs
- **Financial Data**: Emphasized with currency symbols and larger font
- **Dates**: Consistent date formatting with calendar icons
- **Secondary Info**: Smaller, muted text for booking/cancellation dates

### 3. Property Differentiation
- **Property Cards**: Different background colors or borders per property
- **Property Icons**: Unique icons or images for each listing type
- **Revenue Indicators**: Progress bars or visual indicators for revenue levels

### 4. Data Density Management
- **Expandable Sections**: Collapse less critical information
- **Tooltips**: Show full details on hover for truncated content
- **Progressive Disclosure**: Show summary first, details on demand

## Special Considerations for This Endpoint

### 1. Pagination Handling
- **Next Page Indicator**: The `next_page` boolean requires pagination UI
- **Load More**: Implement infinite scroll or "Load More" button
- **Page Size**: Allow users to control how many reservations to display
- **Total Count**: Show total reservation count when available

### 2. Date Handling Complexity
- **Multiple Date Types**: Booking, check-in, check-out, cancellation dates
- **Time Zone Awareness**: Handle different time zones appropriately
- **Date Range Validation**: Ensure logical date range filtering
- **Relative Dates**: Show "X days ago" for recent bookings

### 3. Financial Data Precision
- **Currency Formatting**: Proper formatting for USD and other currencies
- **Decimal Precision**: Handle varying decimal places in revenue data
- **Zero Revenue Cases**: Special handling for $0.00 reservations
- **Fee Breakdowns**: Clear separation of base revenue vs. additional fees

### 4. Performance Considerations
- **Large Dataset Handling**: Efficient rendering for many reservations
- **Virtual Scrolling**: For very long lists of reservations
- **Lazy Loading**: Load details on demand to improve initial load time
- **Search Functionality**: Quick search across reservation and listing data

### 5. Data Quality Indicators
- **Missing Data Alerts**: Clear indicators when required fields are null
- **Data Freshness**: Show when data was last updated
- **Validation Errors**: Highlight inconsistent or suspicious data
- **Completeness Metrics**: Show percentage of complete vs. incomplete records

### 6. Mobile Responsiveness
- **Card Layout**: Optimize card design for mobile screens
- **Touch Interactions**: Swipe gestures for navigation
- **Condensed View**: Prioritize most important information on small screens
- **Collapsible Filters**: Accordion-style filters for mobile

### 7. Accessibility Features
- **Screen Reader Support**: Proper ARIA labels and descriptions
- **Keyboard Navigation**: Full keyboard accessibility
- **High Contrast Mode**: Support for accessibility color schemes
- **Text Scaling**: Support for increased font sizes

## Technical Implementation Notes

### 1. Component Structure
- **ReservationDashboard**: Main container component
- **ReservationCard**: Individual reservation display
- **MetricsPanel**: KPI cards and summary statistics
- **FilterPanel**: All filtering and sorting controls
- **DataTable**: Alternative tabular view

### 2. State Management
- **Filtered Data**: Maintain filtered reservation list
- **Sort State**: Current sorting criteria
- **View State**: Card vs. table, grouping options
- **Pagination State**: Current page and loading status

### 3. API Integration
- **Auto-refresh**: Periodic data updates
- **Error Handling**: Graceful handling of API failures
- **Loading States**: Skeleton screens during data fetching
- **Caching Strategy**: Cache frequently accessed data