# Get All Listings API Visualization Plan

## Data Structure Analysis

The Get All Listings API returns a JSON response with a single `listings` array containing comprehensive property data. Each listing object contains 50+ fields covering:

### Core Property Information
- **Identity**: `id`, `pms`, `name`
- **Location**: `latitude`, `longitude`, `country`, `city_name`, `state`
- **Property Details**: `no_of_bedrooms`
- **Pricing**: `min`, `base`, `max`, `recommended_base_price`
- **Organization**: `group`, `subgroup`, `tags`, `notes`
- **Settings**: `isHidden`, `push_enabled`, `last_date_pushed`

### Performance Metrics
- **Occupancy Data**: `occupancy_next_7/30/60` vs `market_occupancy_next_7/30/60`
- **Revenue Data**: `revenue_past_30`, `revenue_next_30/180`, `stly_revenue_*` (same-time-last-year)
- **ADR Data**: `adr_past_90`, `adr_next_180`, `stly_adr_*`
- **Market Performance**: `mpi_next_30/60/90/120/180` (Market Performance Index)
- **Booking Activity**: `last_booked_date`, `booking_pickup_past_30`
- **Pricing Analytics**: `min_prices_next_30`
- **Data Freshness**: `last_refreshed_at`

### Data Variations
- **Airbnb vs VRBO**: Different data completeness (VRBO listings often have null values)
- **Missing Data**: Some fields show "Unavailable", "-", or null values
- **Active vs Hidden**: Properties can be hidden or have push disabled

## Visualization Plan

### 1. Primary Dashboard Layout

#### Header Section
- **Total Properties Count** with breakdown by PMS (Airbnb/VRBO)
- **Portfolio Summary Cards**:
  - Total Active Listings
  - Total Hidden Listings
  - Push-Enabled Properties
  - Average Base Price

#### Main Content Area (Tabbed Interface)

### 2. Tab 1: Properties Overview

#### Interactive Map View
- **Clustered markers** by city/region
- **Color coding**:
  - Green: High-performing properties (MPI > 1.5)
  - Yellow: Average performing (MPI 0.8-1.5)
  - Red: Underperforming (MPI < 0.8)
  - Gray: No data available
- **Click functionality**: Popup with property summary
- **Filter controls**: By city, bedroom count, PMS type

#### Properties Grid/Table
- **Sortable columns**:
  - Property Name (with PMS icon)
  - Location (City, State)
  - Bedrooms
  - Base Price
  - Last Booking Date
  - MPI 30-day
  - Revenue (Past 30)
- **Row actions**: View details, edit settings
- **Bulk actions**: Hide/unhide, enable/disable push

### 3. Tab 2: Performance Analytics

#### Key Performance Indicators Grid
- **Revenue Performance**:
  - Current vs Last Year comparison charts
  - Revenue trend arrows (↑↓)
  - Total portfolio revenue
- **Occupancy Performance**:
  - Property vs Market occupancy comparison
  - Occupancy rate distribution histogram
- **Pricing Analysis**:
  - ADR trends and comparisons
  - Recommended vs Current base price gaps

#### Market Performance Index Dashboard
- **MPI Trend Charts**: Line charts for 30/60/90/120/180 day periods
- **MPI Distribution**: Histogram showing property performance spread
- **Top/Bottom Performers**: Tables with highest and lowest MPI properties

### 4. Tab 3: Revenue Deep Dive

#### Revenue Comparison Matrix
- **Side-by-side cards** for each property showing:
  - Current period revenue
  - Same-time-last-year revenue
  - Percentage change with color coding
  - Trend arrows and sparkline charts

#### Revenue Timeline Visualizations
- **Interactive charts** showing revenue patterns
- **Seasonality analysis** with year-over-year overlays
- **Booking pickup tracking** with calendar heatmaps

### 5. Tab 4: Operational Management

#### Push Management Interface
- **Properties by Push Status**:
  - Recently pushed (green indicators)
  - Push enabled but not recent (yellow)
  - Push disabled (red)
- **Last Push Activity**: Timeline view
- **Bulk Push Controls**: Enable/disable for multiple properties

#### Data Quality Dashboard
- **Missing Data Summary**: Properties with incomplete information
- **Stale Data Alerts**: Properties not refreshed recently
- **VRBO Data Gaps**: Specific tracking for VRBO properties with limited data

### 6. Interactive Elements Needed

#### Filtering and Search
- **Multi-select filters**:
  - PMS type (Airbnb/VRBO)
  - City/State
  - Bedroom count
  - Performance tier (High/Medium/Low MPI)
  - Tags
  - Hidden/Visible status
- **Search functionality**: By property name, ID, or location
- **Date range selectors**: For revenue and booking analysis

#### Data Export Options
- **CSV export** for filtered property lists
- **PDF reports** for performance summaries
- **API endpoint links** for developers

### 7. Color Coding and Visual Hierarchy

#### Color Scheme
- **Performance Colors**:
  - Excellent (MPI > 2.0): Dark Green (#2d5a2d)
  - Good (MPI 1.5-2.0): Green (#4a7c59)
  - Average (MPI 0.8-1.5): Yellow (#f4d03f)
  - Poor (MPI 0.5-0.8): Orange (#f39c12)
  - Critical (MPI < 0.5): Red (#e74c3c)
- **Status Colors**:
  - Active/Enabled: Blue (#3498db)
  - Hidden/Disabled: Gray (#95a5a6)
  - Recently Updated: Fresh green accent
- **Data Quality**:
  - Complete data: Standard text color
  - Missing data: Muted gray with italics
  - Stale data: Orange warning background

#### Typography Hierarchy
- **Property Names**: Bold, larger font
- **Metrics**: Monospace font for numbers
- **Locations**: Secondary color, smaller font
- **Status indicators**: Badge-style formatting

### 8. Special Considerations

#### Data Handling
- **Null Value Display**: Show "—" instead of "null" or empty
- **"Unavailable" Handling**: Consistent styling with explanation tooltips
- **Large Number Formatting**: Use commas and abbreviations (K, M) where appropriate
- **Percentage Display**: Consistent decimal places and % symbol

#### Performance Optimization
- **Lazy Loading**: Load property details on demand
- **Virtual Scrolling**: For large property lists
- **Caching**: Cache expensive calculations like performance metrics
- **Progressive Loading**: Show basic info first, enrich with performance data

#### Responsive Design
- **Mobile-first approach**: Stack cards vertically on smaller screens
- **Collapsible sections**: Allow users to focus on specific metrics
- **Touch-friendly controls**: Larger buttons and touch targets

#### Accessibility
- **High contrast mode**: Alternative color scheme for better visibility
- **Screen reader support**: Proper ARIA labels and descriptions
- **Keyboard navigation**: Full functionality without mouse
- **Color-blind friendly**: Use patterns/shapes in addition to colors

### 9. Advanced Features

#### Comparative Analysis Tools
- **Property Comparison**: Side-by-side comparison of up to 4 properties
- **Market Benchmarking**: Compare property performance to market averages
- **Historical Trends**: Overlay multiple time periods

#### Predictive Insights
- **Revenue Forecasting**: Based on current trends and seasonality
- **Occupancy Predictions**: Market-informed projections
- **Pricing Recommendations**: Smart suggestions based on performance data

#### Alerts and Notifications
- **Performance Alerts**: Notify when properties drop below thresholds
- **Data Freshness Warnings**: Alert for stale data
- **Opportunity Indicators**: Highlight underutilized properties

This comprehensive visualization plan transforms the complex API response data into an intuitive, actionable interface that serves both operational management and strategic analysis needs for property portfolio management.