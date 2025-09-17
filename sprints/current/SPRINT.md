# Sprint: 001-minimum-stay-column

## TODO
- [ ] Add minimum stay column header to pricing table
- [ ] Extract min_stay data from pricing API response
- [ ] Display minimum stay values in new table column
- [x] Create booked days comparison table component page
- [x] Integrate reservation data API endpoint for booked days
- [x] Compare our booked rates vs median booked prices by bedroom category
- [x] Calculate and display percentage over/under median

## Requirements

### 1. Minimum Stay Column (Original)
Add a "Min Stay" column to the existing 60-Day Pricing Forecast table in listingv3.html that displays the minimum stay requirement for each date. The data should come from the existing pricing data that's already being fetched from the `/api/listing_prices/{listing_id}` endpoint.

**Table Location**: 60-Day Pricing Forecast table (lines 642-665 in listingv3.html)
**Data Source**: `pricingData[0].data[].min_stay` field from existing API call
**Positioning**: Insert between "Our Price" and "Market Occ%" columns

### 2. Booked Days Comparison Component (New)
Create a standalone component-style page that compares our booked rates vs median booked prices for the same bedroom category.

**Features Required**:
- Show only booked days (skip available days from pricing data)
- Use reservation data API endpoint to get actual booked revenue
- Get median booked prices from neighborhood data API for bedroom category
- Calculate percentage over/under median for each booked day
- Component-style implementation for easy dashboard integration
- Responsive table design matching existing dashboard style

**Data Sources**:
- Reservation data: `/api/reservation_data` (rental_revenue, check_in, check_out, no_of_days)
- Median pricing: `/api/neighborhood_data/{listing_id}` (Future Percentile Prices > Category > bedroom_count > Y_values[3] = Median Booked Price)
- Listing info: `/api/listings` to get bedroom count for median lookup

## Implementation Notes
- Minimum stay data is already available in the `min_stay` field of each day's pricing data
- No additional API calls needed - use existing `pricingData` variable
- Position new column after "Our Price" to maintain logical flow
- Use simple numeric display (e.g., "1", "2", "3") for minimum stay values

## Current Status
Ready to implement - analyzing existing table structure and data flow.