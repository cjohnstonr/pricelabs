# PriceLabs API Structure Analysis - Historical Performance Insights

## Mission
Analyze the actual PriceLabs API response structures to determine if we can calculate historical performance metrics (our ADR vs market median) using ONLY the data available from the API endpoints.

## Critical Context

### Current Implementation Status
We have built three pricing optimization columns that require:
1. **OUR AVG VS MARKET** - Historical performance vs market median percentage
2. **OPTIMIZED TARGET** - AI-recommended price (Market Median × Performance Factor)
3. **PRICE ADJUSTMENT %** - Specific pricing guidance

Currently these columns show "N/A" because:
- We have booking data but it's from dates BEFORE the market data range
- Booking dates: Before Oct 24, 2025
- Market data range: Oct 24, 2025 - Oct 18, 2026
- No overlap = no comparison possible

### The Question
**Given the constraint that we cannot store external historical data and can ONLY use what the PriceLabs API returns, is there a way to calculate historical performance using available aggregate metrics?**

## Your Task

### Phase 1: API Data Collection

Make actual API calls to the Flask server endpoints and capture the FULL response structures:

1. **Listing Endpoint**
   ```
   GET http://localhost:5050/api/listing/4305303
   ```
   - Capture the complete JSON response
   - Focus on fields containing "past", "historical", "adr", "revenue", "occupancy"

2. **Neighborhood Endpoint**
   ```
   GET http://localhost:5050/api/neighborhood/<neighborhood_id>
   ```
   - Extract neighborhood_id from the listing response
   - Capture the complete JSON response
   - **CRITICAL**: Examine the date ranges in percentile data
     - Does it contain ONLY future dates?
     - Does it contain historical dates?
     - What is the earliest date available?

3. **Reservation Data Endpoint** (may fail, but try)
   ```
   GET http://localhost:5050/api/reservation_data/4305303
   ```
   - This endpoint exists but may return limited data
   - Capture whatever response you get

4. **Explore Other Endpoints**
   - Look at the listing response for references to other endpoints
   - Try any endpoints that might provide historical market data

### Phase 2: Field Inventory

Create a comprehensive inventory of available fields:

**Format:**
```markdown
## Available Historical Performance Fields

### From Listing Endpoint
- `adr_past_90`: [actual value] - [your interpretation]
- `revenue_past_30`: [actual value] - [your interpretation]
- `occupancy_past_90`: [actual value] - [your interpretation]
- `last_booked_date`: [actual value] - [your interpretation]
- [list ALL fields related to past performance]

### From Neighborhood Endpoint
- `Future Percentile Prices.Category[X].X_values`: [date range: earliest to latest]
- `Future Percentile Prices.Category[X].Y_values[3]`: [what this represents]
- [list ALL fields and their date coverage]

## Missing Fields
- [Fields we would need but don't have]
```

### Phase 3: Date Range Analysis

**CRITICAL ANALYSIS:** Determine the temporal coverage of market data.

```markdown
## Market Data Temporal Coverage

### Question: Does neighborhood data include HISTORICAL percentiles?

**Test Method:**
1. Get today's date: [YYYY-MM-DD]
2. Examine X_values array in percentile data
3. Find earliest date in array
4. Compare to today's date

**Results:**
- Earliest date in market data: [YYYY-MM-DD]
- Today's date: [YYYY-MM-DD]
- Days of historical data: [number] or "NONE - only future dates"

**Conclusion:**
[ ] Market data includes historical dates (dates before today)
[ ] Market data is FUTURE-ONLY (all dates are today or later)
```

### Phase 4: Feasibility Assessment

Based on ACTUAL data you found (not assumptions), answer:

#### Scenario A: If Historical Market Data EXISTS
```markdown
## ✅ FEASIBLE - Historical Comparison Possible

**Available Data:**
- Our historical ADR: `adr_past_90` = $[value]
- Historical market median: `[exact field path]` for dates [range]
- Date overlap: [number] days

**Proposed Calculation:**
```python
# Using actual field names from API
our_adr = listing_data['adr_past_90']
market_median_historical = neighborhood_data['[exact path to historical median]']
performance_percentage = ((our_adr - market_median_historical) / market_median_historical) * 100
```

**Limitations:**
- [What this doesn't tell us]
- [Accuracy concerns]
- [Edge cases]
```

#### Scenario B: If NO Historical Market Data
```markdown
## ❌ NOT FEASIBLE - Gap in Data

**What We Have:**
- Our historical performance: `adr_past_90`, `revenue_past_30`, etc.
- Market data: FUTURE percentiles only, starting [date]

**What We're Missing:**
- Historical market median/percentiles for past 90 days
- No baseline to compare our ADR against

**The Gap:**
We have OUR historical numbers but no MARKET historical numbers to compare against.
This is like knowing your test score (85%) but not knowing the class average.

**Why We Can't Bridge It:**
- Cannot infer historical market data from future projections
- Cannot assume past market median = future market median
- No valid mathematical relationship exists
```

### Phase 5: Alternative Approaches (if applicable)

If direct comparison isn't possible, explore:

1. **Can we use revenue_past_30 + occupancy_past_90 to estimate something meaningful?**
2. **Can we compare our FUTURE pricing vs market median to suggest adjustments?**
3. **Are there other aggregate metrics that provide insight?**

## Anti-Hallucination Requirements

### You MUST:
- [ ] Paste actual JSON responses (not summarized, actual text)
- [ ] Quote exact field names with quotes: `field_name`
- [ ] Show actual date values from responses: "2025-10-24"
- [ ] State "Field not found" if a field doesn't exist
- [ ] State "Endpoint failed" if an API call returns an error

### You MUST NOT:
- [ ] Assume fields exist without seeing them in responses
- [ ] Suggest calling external APIs (ClickUp, Google, etc.)
- [ ] Propose storing historical data ourselves
- [ ] Infer field meanings beyond what's documented
- [ ] Suggest scraping or external data sources

## Deliverable Format

Create a comprehensive analysis document with these sections:

1. **Executive Summary** - Can we or can't we? (One paragraph)
2. **API Response Examples** - Full JSON for each endpoint
3. **Field Inventory** - Comprehensive list with actual values
4. **Date Range Analysis** - Proof of historical vs future coverage
5. **Feasibility Assessment** - Scenario A or Scenario B
6. **Recommended Implementation** - If feasible, exact code. If not, explanation.

## Success Criteria

Your analysis is successful if:
1. Every claim is backed by actual API response data
2. Every field name is exact and verifiable
3. The feasibility conclusion is definitive (YES with calculation, or NO with explanation)
4. A developer could implement your recommendation immediately (if feasible)
5. OR we definitively know the feature cannot be built with available data (if not feasible)

## Getting Started

Begin by:
1. Starting the Flask server (if not already running): `cd "/Users/AIRBNB/Cursor_Projects/Pricelabs V4/Pricelabs" && python listing_viewer_app.py`
2. Testing the listing endpoint: `curl "http://localhost:5050/api/listing/4305303"`
3. Capturing the full response
4. Proceeding systematically through each endpoint

Remember: **Real data beats assumptions.** Show us what the API actually returns.
