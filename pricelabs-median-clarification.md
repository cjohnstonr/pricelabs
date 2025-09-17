# PriceLabs Median Price Clarification Needed

## Questions for PriceLabs Support:

### 1. **Median Booked Price Definition**
Does the "Median Booked" price in the neighborhood data API response include:
- [ ] A) Accommodation/nightly rate only
- [ ] B) Accommodation + cleaning fees (total per night)
- [ ] C) All fees including service fees, taxes, etc.

### 2. **Percentile Prices (25th, 50th, 75th, 90th)**
Are these percentiles calculated from:
- [ ] A) Base nightly rates only
- [ ] B) Effective rates (accommodation + cleaning amortized)
- [ ] C) Total booking value per night

### 3. **When Comparing Our Performance**
When calculating "% vs Market", should we compare:
- [ ] A) Our base rate vs market median
- [ ] B) Our effective rate (with cleaning) vs market median
- [ ] C) Depends on market median calculation method

## Current Implementation Assumptions:

```javascript
// Current: Comparing base rate only
const nightlyRate = rental_revenue / nights;
const percentageVsMarket = ((nightlyRate - marketMedian) / marketMedian) * 100;

// Alternative: Including cleaning fees
const effectiveRate = (rental_revenue + cleaning_fees) / nights;
const percentageVsMarket = ((effectiveRate - marketMedian) / marketMedian) * 100;
```

## Impact on Optimization:

### If Median is **Accommodation Only**:
- Current calculation is correct
- Example: Our $186 vs Market $245 = -24% performance

### If Median **Includes Cleaning**:
- Need to use effective rate
- Example: Our $269 vs Market $245 = +9.8% performance

**This 34% difference completely changes optimization recommendations!**

## Test Data to Provide Support:
- Listing ID: 50758913
- Property: 3 bedroom
- Base rate: $267
- Cleaning fee: $250
- Sample booking: 3 nights at $557 accommodation + $250 cleaning

## Temporary Solution Until Clarification:

Add a dashboard toggle:
```html
<label>
  Market Comparison Mode:
  <select id="comparison-mode">
    <option value="base">Base Rate Only (default)</option>
    <option value="effective">Include Cleaning Fees</option>
  </select>
</label>
```

This lets users choose based on their market knowledge.