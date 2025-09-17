# Revenue Breakdown Analysis for Listing 50758913
## Accommodation vs Cleaning Fee Analysis

### Key Insights
- **Cleaning Fee Impact**: Shorter stays have higher effective rates due to cleaning fee amortization
- **Market Comparison**: Should use **Effective Rate** (accommodation + cleaning/night) for accurate market comparison

## Detailed Revenue Breakdown Table (Sample 2024 Data)

| Check-in Date | Check-out | Nights | Accommodation Revenue | Nightly Rate | Cleaning Fee | Cleaning/Night | **Effective Rate** | Total Revenue | Impact of Cleaning |
|---------------|-----------|--------|----------------------|--------------|--------------|----------------|-------------------|---------------|-------------------|
| 2024-01-04 | 2024-01-07 | 3 | $557.00 | $185.67 | $250.00 | $83.33 | **$269.00** | $807.00 | +44.9% |
| 2024-01-12 | 2024-01-16 | 4 | $655.20 | $163.80 | $250.00 | $62.50 | **$226.30** | $905.20 | +38.2% |
| 2024-02-07 | 2024-02-11 | 4 | $891.00 | $222.75 | $250.00 | $62.50 | **$285.25** | $1,141.00 | +28.1% |
| 2024-02-23 | 2024-02-26 | 3 | $630.00 | $210.00 | $250.00 | $83.33 | **$293.33** | $880.00 | +39.7% |
| 2024-04-28 | 2024-05-04 | 6 | $1,198.80 | $199.80 | $250.00 | $41.67 | **$241.47** | $1,448.80 | +20.9% |
| 2024-05-08 | 2024-05-13 | 5 | $1,457.00 | $291.40 | $250.00 | $50.00 | **$341.40** | $1,707.00 | +17.2% |

### Analysis Formulas:
- **Nightly Rate** = `rental_revenue / no_of_days`
- **Cleaning per Night** = `cleaning_fees / no_of_days`
- **Effective Rate** = `(rental_revenue + cleaning_fees) / no_of_days`
- **Impact of Cleaning** = `(Effective Rate / Nightly Rate - 1) × 100%`

## Key Observations:

### 1. **Cleaning Fee Impact by Stay Length**
- **3-night stays**: Cleaning adds 40-45% to nightly rate
- **4-night stays**: Cleaning adds 28-38% to nightly rate
- **5-6 night stays**: Cleaning adds 17-21% to nightly rate

### 2. **Why This Matters for Pricing Optimization**
- When comparing to market median, we MUST use **Effective Rate**
- Market median prices likely include all fees
- Our optimization should consider total revenue per night, not just base rate

### 3. **Recommended Approach for Booked Days Component**

```javascript
// Calculate effective daily rate for accurate market comparison
const effectiveDailyRate = (rental_revenue + cleaning_fees) / nights;

// Compare to market median
const percentageVsMarket = ((effectiveDailyRate - marketMedian) / marketMedian) * 100;
```

## Implementation Recommendation:

### For the Booked Days Analysis Table:
Add these columns:
1. **Accommodation/Night**: Base nightly rate
2. **Cleaning/Night**: Amortized cleaning fee
3. **Effective Rate**: Total per night (for market comparison)
4. **Market Median**: From neighborhood data
5. **% vs Market**: Using effective rate

### Why Split Display Matters:
- **Transparency**: Shows guests true cost breakdown
- **Optimization**: Helps identify if base rate or cleaning fee needs adjustment
- **Short Stay Strategy**: Highlights premium for shorter bookings
- **Market Positioning**: Accurate comparison with competitors

## Visual Indicator Suggestions:
- 🟢 **Green**: When effective rate beats market by >5%
- 🟡 **Yellow**: Within ±5% of market
- 🔴 **Red**: Below market by >5%
- 📊 **Bar Chart**: Show accommodation vs cleaning fee visually