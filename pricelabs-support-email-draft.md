# Email Draft for PriceLabs Support

## Subject: API Clarification Needed: Median Booked Price Components

---

**To:** support@pricelabs.co (or your support contact)  
**Subject:** API Clarification Needed: Median Booked Price Components  

---

Dear PriceLabs Support Team,

I'm developing an advanced pricing optimization dashboard using your API data and need clarification on how certain metrics are calculated to ensure accurate market comparisons.

## Specific Questions:

### 1. Median Booked Price Definition
In the Neighborhood API response under `Future Percentile Prices`, does the **"Median Booked"** price value include:
- Only the base accommodation/nightly rate?
- Accommodation rate + cleaning fees (amortized per night)?
- All fees including service fees and taxes?

### 2. Percentile Price Calculations
Are the percentile prices (25th, 50th, 75th, 90th) calculated from:
- Base nightly rates only?
- Effective rates (accommodation + cleaning fees divided by nights)?
- Total booking value per night including all fees?

### 3. Market Comparison Best Practice
When calculating our property's performance "% vs Market" for optimization decisions, should we compare:
- Our base nightly rate against the market median?
- Our effective rate (including amortized cleaning) against the market median?
- This depends on how the market median is calculated?

## Context - Real Example:

**Property:** Listing ID 50758913 (3-bedroom)
- **Base rate:** $267/night
- **Cleaning fee:** $250 per stay
- **Market Median (from API):** ~$245/night

**Example 3-night stay:**
- **Our base rate:** $186/night (accommodation only)
- **Our effective rate:** $269/night (including $83/night amortized cleaning)

**The Impact:**
- If median is base rate only: We're at -24% vs market
- If median includes cleaning: We're at +10% vs market

This 34-point difference completely changes our optimization strategy!

## Current Implementation:

```javascript
// Method A: Base rate comparison
const nightlyRate = rental_revenue / nights;
const vsMarket = ((nightlyRate - marketMedian) / marketMedian) * 100;

// Method B: Effective rate comparison  
const effectiveRate = (rental_revenue + cleaning_fees) / nights;
const vsMarket = ((effectiveRate - marketMedian) / marketMedian) * 100;
```

Which method aligns with how PriceLabs calculates market medians?

## Request:

Could you please clarify:
1. What components are included in the median booked prices?
2. The recommended approach for accurate market performance calculations?
3. If there's any documentation on this that I might have missed?

This clarification will ensure our optimization recommendations are properly calibrated to market realities.

Thank you for your help in ensuring we're using your excellent data correctly!

Best regards,  
[Your Name]  
[Your Contact Info]

---

## Additional Follow-up Questions (if needed):

1. Does the calculation method vary by market or region?
2. Are Airbnb's service fees ever included in these calculations?
3. Is there an API endpoint that provides this metadata?

---

## Quick Copy Version (simplified):

Hi PriceLabs Support,

Quick question about the API data: Does the "Median Booked" price in the neighborhood data include just the nightly rate, or does it include cleaning fees amortized per night?

For example, if a property charges $186/night + $250 cleaning for 3 nights:
- Base rate: $186/night
- Effective rate: $269/night (with cleaning)
- Market median shows: $245/night

Should I compare my $186 or my $269 against the $245 market median?

This significantly impacts our pricing optimization calculations.

Thanks!
[Your name]