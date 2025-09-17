# Sprint: 002-pricing-optimization-integration

## TODO
- [ ] Create listingv5.html from listingv4.html as base
- [ ] Move "Median Booked" column to position 4 (after Our Price)
- [ ] Add "Our Avg vs Market" column (position 5)
- [ ] Add "Optimized Target" column (position 6)  
- [ ] Add "Price Adjustment %" column (position 7)
- [ ] Create global insights variable (bookedDaysInsights)
- [ ] Implement core pricing optimization calculation functions
- [ ] Add CSS styling for optimization columns and color coding
- [ ] Modify updatePricingTable() to include optimization calculations
- [ ] Update booked days component to export insights globally
- [ ] Add tooltips and visual indicators for user experience
- [ ] Test with various listing scenarios and edge cases

## Requirements

Transform the static 90-Day Pricing Forecast table into an intelligent pricing optimization tool by integrating historical booking performance data from the Booked Days Analysis component.

**GOAL:** Create data-driven pricing recommendations by applying historical booking performance to future market pricing data.

**KEY INTEGRATION:** 
- Extract avgPercentVsMarket from Booked Days component
- Apply to pricing forecast table with 4 new optimization columns:
  - "Our Avg vs Market" (shows historical performance)
  - "Optimized Target" (calculated: medianPrice * (1 + avgPercentVsMarket/100))
  - "Price Adjustment %" (calculated: ((target - current) / current) * 100)
  - Color coding for recommendations (green=increase, red=decrease, blue=optimal)

**PRIMARY FILE:** listingv5.html (enhanced copy of listingv4.html)

## Implementation Notes

**Data Flow:**
1. Booked Days component calculates avgPercentVsMarket from historical data
2. Global bookedDaysInsights variable stores this performance metric
3. Pricing table uses avgPercentVsMarket to calculate optimization recommendations
4. Visual indicators show pricing opportunities with color coding

**Calculation Logic:**
- optimizedTarget = medianPrice * (1 + avgPercentVsMarket/100)
- adjustmentPercent = ((optimizedTarget - currentPrice) / currentPrice) * 100
- Color coding: green (increase), red (decrease), blue (optimal range)

**Table Restructure:**
Move "Median Booked" next to "Our Price" and add 3 optimization columns before existing columns like "Min Stay" and "Gap Nights".

## Current Status
Sprint initialized. Ready to begin Phase 1: Create listingv5.html base file and restructure table columns.