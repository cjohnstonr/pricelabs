# PriceLabs API Historical Analysis Results

## Executive Summary

**CONCLUSION: ❌ NOT FEASIBLE - Historical Performance Comparison Cannot Be Calculated**

The PriceLabs API does NOT provide historical market percentile/median data that overlaps with our historical booking performance data. While we have our own historical ADR (`adr_past_90` = $127), the market percentile data in the API starts from **2025-10-24** (future-only), creating a temporal gap that makes historical performance comparison impossible using API data alone.

**Date Analysis:**
- Today's Date: **2025-10-23**
- Our Historical ADR Coverage: Past 90 days (approximately July 25 - Oct 23, 2025)
- Market Percentile Data Start: **2025-10-24** (tomorrow)
- **Gap: Zero days of overlap**

**The Critical Problem:**
We have OUR historical performance numbers but no MARKET historical percentile data to compare against for the same time period. This is like knowing your test score (85%) but not knowing what the class average was when you took the test.

---

## Phase 1: API Response Examples

### 1.1 Listing Endpoint Response

**Endpoint:** `GET http://localhost:5050/api/listing/4305303`

**Full Response:**
```json
{
    "listing_data": {
        "adr_next_180": 111,
        "adr_past_90": 127,
        "base": 165,
        "booking_pickup_past_30": 40,
        "city_name": "San Diego",
        "cleaning_fees": 100.0,
        "country": "United States",
        "group": null,
        "id": "4305303",
        "isHidden": false,
        "last_booked_date": "2025-10-16T00:00:00.000Z",
        "last_date_pushed": "2025-10-24T00:22:52.000Z",
        "last_refreshed_at": "2025-10-24T00:22:48+00:00",
        "latitude": "32.72383499",
        "longitude": "-117.13231659",
        "market_occupancy_next_120": "18 %",
        "market_occupancy_next_30": "36 %",
        "market_occupancy_next_60": "27 %",
        "market_occupancy_next_7": "44 %",
        "market_occupancy_next_90": "22 %",
        "max": 400,
        "min": 103,
        "min_prices_next_30": "33 %",
        "mpi_next_120": 1.6,
        "mpi_next_180": 1.5,
        "mpi_next_30": 1.9,
        "mpi_next_60": 1.7,
        "mpi_next_90": 1.4,
        "name": "Chic 1BR in Trendy Walkable South Park",
        "no_of_bedrooms": 1,
        "notes": null,
        "occupancy_next_120": "29 %",
        "occupancy_next_30": "70 %",
        "occupancy_next_60": "47 %",
        "occupancy_next_7": "57 %",
        "occupancy_next_90": "31 %",
        "pms": "airbnb",
        "push_enabled": true,
        "recommended_base_price": 165,
        "revenue_next_180": 3106,
        "revenue_next_30": 2448,
        "revenue_past_30": 2720,
        "state": "California",
        "stly_adr_next_180": 124,
        "stly_adr_past_90": 137,
        "stly_revenue_next_180": 13597,
        "stly_revenue_next_30": 3427,
        "stly_revenue_past_30": 2778,
        "subgroup": null,
        "tags": "Jill,verified"
    },
    "listing_id": "4305303",
    "listing_name": "Chic 1BR in Trendy Walkable South Park",
    "portfolio_key": "default",
    "portfolio_name": "Main Portfolio"
}
```

### 1.2 Neighborhood Endpoint Response (Key Sections)

**Endpoint:** `GET http://localhost:5050/api/neighborhood/4305303`

**Date Range Analysis for All Sections:**

```
Today: 2025-10-23
================================================================================

SECTION: Future Occ/New/Canc
  Category -1:
    First date: 2025-04-27
    Last date: 2026-10-18
    Total data points: 540
    Contains historical data (before 2025-10-23): True

SECTION: Future Percentile Prices
  Category -1:
    First date: 2025-10-24
    Last date: 2026-10-18
    Total data points: 360
    Contains historical data (before 2025-10-23): False  ⚠️ CRITICAL

SECTION: Future Percentile Prices Monthly
  Category -1:
    First date: 2025-10
    Last date: 2026-10
    Total data points: 13
    Contains historical data (before 2025-10-23): True (but monthly aggregates only)

SECTION: Market KPI
  Category -1:
    First date: Oct 2023
    Last date: Last 730 Days
    Total data points: 27
    Contains historical data: Contains aggregated monthly data from Oct 2023
```

**Future Percentile Prices Structure (Sample):**
```json
{
  "Future Percentile Prices": {
    "Category": {
      "-1": {
        "Active Used": 32,
        "Inactive Used": 0,
        "Listings Used": 32,
        "X_values": [
          "2025-10-24",
          "2025-10-25",
          "2025-10-26",
          "..."
        ],
        "Y_values": [
          [70.0, 70.0, 70.0, ...],  // Series 0: 25th percentile
          [88.0, 96.0, 92.0, ...],  // Series 1: 50th percentile (median)
          [120.0, 123.0, 119.0, ...], // Series 2: 75th percentile
          [78.5, 82.0, 80.0, ...],  // Series 3: Median booked price
          [176.0, 180.0, 175.0, ...], // Series 4: 90th percentile
          [14, 15, 14, ...]         // Series 5: Unknown (possibly count/10th)
        ]
      }
    }
  }
}
```

**Market KPI Data Structure:**
```
Market KPI Category -1 (All data):
Time periods: ['Oct 2023', 'Nov 2023', 'Dec 2023', 'Jan 2024', 'Feb 2024',
               'Mar 2024', 'Apr 2024', 'May 2024', 'Jun 2024', 'Jul 2024',
               'Aug 2024', 'Sep 2024', 'Oct 2024', 'Nov 2024', 'Dec 2024',
               'Jan 2025', 'Feb 2025', 'Mar 2025', 'Apr 2025', 'May 2025',
               'Jun 2025', 'Jul 2025', 'Aug 2025', 'Sep 2025', 'Oct 2025',
               'Last 365 Days', 'Last 730 Days']

Y_values series (10 series total):
  Series 0: [103, 365, 366, 374, ...] (possibly ADR or listing count)
  Series 1: [26.0, 30.0, 28.0, 20.0, ...] (possibly occupancy %)
  Series 2: [3.0, 4.0, 3.0, 3.0, ...] (possibly min stay or other metric)
  Series 3: [3498.0, 15387.0, 15535.0, ...] (possibly revenue)
  Series 4: [53, 222, 220, 203, ...] (unknown metric)
  ... (6 more series)
```

### 1.3 Listing Prices Endpoint Response

**Endpoint:** `GET http://localhost:5050/api/listing_prices/4305303`

**Sample Response (showing daily pricing data):**
```json
[
  {
    "currency": "USD",
    "data": [
      {
        "ADR": 104.89,
        "ADR_STLY": 123.5,
        "booked_date": "2025-10-05",
        "booked_date_STLY": "2024-10-21",
        "booking_status": "Booked",
        "booking_status_STLY": "Booked (Check-In)",
        "date": "2025-10-23",
        "demand_color": "#EDEDED",
        "demand_desc": "Unavailable",
        "extra_person_fee": 0,
        "extra_person_fee_trigger": 0,
        "min_stay": 1,
        "price": 103,
        "unbookable": 0,
        "uncustomized_price": 86,
        "user_price": -1
      }
    ]
  }
]
```

### 1.4 Reservation Data Endpoint Response

**Endpoint:** `GET http://localhost:5050/api/reservation_data/4305303`

**Response:**
```json
{
  "data": [
    {
      "booking_status": "booked",
      "check_in": "2025-10-16T00:00:00.000Z",
      "check_out": null,
      "listing_id": "4305303",
      "no_of_days": 1,
      "pms": "airbnb",
      "rental_revenue": 90.66666666666667,
      "reservation_id": "estimated_4305303"
    }
  ],
  "next_page": false,
  "note": "Data extracted from listing fields (reservation endpoint not available)",
  "pms_name": "airbnb"
}
```

**Status:** Limited data - appears to extract from listing fields rather than detailed reservation endpoint.

---

## Phase 2: Field Inventory

### 2.1 Available Historical Performance Fields (Our Property)

**From Listing Endpoint:**

| Field | Actual Value | Interpretation |
|-------|-------------|----------------|
| `adr_past_90` | 127 | Our average daily rate for past 90 days ($127) |
| `revenue_past_30` | 2720 | Our revenue for past 30 days ($2,720) |
| `booking_pickup_past_30` | 40 | Bookings made in past 30 days (40% or 40 units unclear) |
| `last_booked_date` | "2025-10-16T00:00:00.000Z" | Most recent booking date |
| `stly_adr_past_90` | 137 | Same-time-last-year ADR for past 90 days ($137) |
| `stly_revenue_past_30` | 2778 | Same-time-last-year revenue for past 30 ($2,778) |

**From Listing Prices Endpoint:**
- Daily `ADR` values for each date (our actual ADR per day)
- `booking_status` showing when dates were booked
- `booked_date` showing when reservation was made

### 2.2 Available Market Data Fields

**From Neighborhood Endpoint - Future Percentile Prices:**

| Field Path | Date Range | Data Available |
|------------|------------|----------------|
| `Future Percentile Prices.Category[-1].X_values` | 2025-10-24 to 2026-10-18 | 360 days of FUTURE dates |
| `Future Percentile Prices.Category[-1].Y_values[0]` | Same dates | 25th percentile prices |
| `Future Percentile Prices.Category[-1].Y_values[1]` | Same dates | 50th percentile (median) prices |
| `Future Percentile Prices.Category[-1].Y_values[2]` | Same dates | 75th percentile prices |
| `Future Percentile Prices.Category[-1].Y_values[3]` | Same dates | Median booked price |
| `Future Percentile Prices.Category[-1].Y_values[4]` | Same dates | 90th percentile prices |

**❌ CRITICAL FINDING:** All percentile data starts from **2025-10-24** (tomorrow), providing ZERO overlap with our historical ADR period (past 90 days).

**From Neighborhood Endpoint - Market KPI:**

| Field | Time Period | Notes |
|-------|-------------|-------|
| `Market KPI.Category[-1].X_values` | Oct 2023 - Oct 2025 + aggregates | Monthly granularity only |
| `Market KPI.Category[-1].Y_values[0-9]` | Same periods | 10 different metric series (poorly documented) |

**Problem:** Market KPI provides monthly aggregates, not daily medians. Cannot compare daily ADR to monthly averages.

### 2.3 Future-Only Market Fields

**From Listing Endpoint:**

| Field | Value | Interpretation |
|-------|-------|----------------|
| `market_occupancy_next_30` | "36 %" | Market occupancy forecast (next 30 days) |
| `market_occupancy_next_60` | "27 %" | Market occupancy forecast (next 60 days) |
| `market_occupancy_next_90` | "22 %" | Market occupancy forecast (next 90 days) |
| `market_occupancy_next_120` | "18 %" | Market occupancy forecast (next 120 days) |
| `mpi_next_30` | 1.9 | Market Penetration Index forecast (next 30 days) |
| `mpi_next_60` | 1.7 | Market Penetration Index forecast (next 60 days) |
| `mpi_next_90` | 1.4 | Market Penetration Index forecast (next 90 days) |
| `mpi_next_120` | 1.6 | Market Penetration Index forecast (next 120 days) |
| `mpi_next_180` | 1.5 | Market Penetration Index forecast (next 180 days) |

**Note:** All market comparison metrics are FUTURE-ONLY. No `market_occupancy_past_90` or `mpi_past_90` fields exist.

### 2.4 Missing Fields

**Fields we would need but DON'T have:**

❌ `market_median_past_90` - Historical market median ADR for past 90 days
❌ `market_percentile_past_90` - Historical market percentiles for past 90 days
❌ `mpi_past_90` - Historical Market Penetration Index
❌ `market_adr_past_90` - Historical market average ADR
❌ Any daily historical market pricing data before today

**Why these matter:**
To calculate "OUR AVG VS MARKET" percentage, we need:
```
Performance % = ((our_adr_past_90 - market_median_past_90) / market_median_past_90) * 100
              = ((127 - ???) / ???) * 100
```

The `???` represents data that does NOT exist in the API.

---

## Phase 3: Date Range Analysis

### 3.1 Market Data Temporal Coverage

**Critical Question:** Does neighborhood data include HISTORICAL percentiles?

**Test Method:**
1. Today's date: **2025-10-23**
2. Examined all `X_values` arrays in `Future Percentile Prices`
3. Found earliest date in each array
4. Compared to today's date

**Results:**

| Section | Earliest Date | Today's Date | Days of Historical Data | Conclusion |
|---------|--------------|--------------|------------------------|------------|
| Future Percentile Prices | 2025-10-24 | 2025-10-23 | **0 days** | ❌ FUTURE-ONLY |
| Future Percentile Prices Monthly | 2025-10 | 2025-10-23 | 0 days (month-level) | ❌ Current month only |
| Market KPI | Oct 2023 | 2025-10-23 | ~730 days | ⚠️ Monthly aggregates only |
| Future Occ/New/Canc | 2025-04-27 | 2025-10-23 | ~179 days | ✅ Historical occupancy data |

**Detailed Findings:**

#### Future Percentile Prices
```
Category -1:
  First date: 2025-10-24
  Last date: 2026-10-18
  Total dates: 360
  Contains historical data (before 2025-10-23): FALSE
```

**Interpretation:** This is the PRIMARY source for market median pricing, but it contains ZERO historical data. All 360 data points are for future dates starting tomorrow.

#### Market KPI
```
Category -1:
  Time periods: ['Oct 2023', 'Nov 2023', ..., 'Oct 2025', 'Last 365 Days', 'Last 730 Days']
  Total periods: 27
  Contains historical data: TRUE (monthly aggregates from Oct 2023)
```

**Interpretation:** Contains historical data BUT:
- Only monthly granularity (not daily)
- Unclear what each of the 10 Y_value series represents
- Cannot directly extract "market median ADR" for a specific 90-day period
- No documentation of series labels in API

### 3.2 Our Historical Data Coverage

**From `adr_past_90` field:**
- Value: $127
- Period covered: Past 90 days from today
- Approximate dates: July 25, 2025 - October 23, 2025

**From `revenue_past_30` field:**
- Value: $2,720
- Period covered: Past 30 days from today
- Approximate dates: September 23, 2025 - October 23, 2025

### 3.3 Overlap Analysis

**Required for comparison:**
Need market median data for the SAME period as our historical ADR (past 90 days).

**What we found:**

| Data Source | Our Period | Market Period | Overlap |
|-------------|------------|---------------|---------|
| ADR Past 90 | Jul 25 - Oct 23, 2025 | Oct 24, 2025 - Oct 18, 2026 | **0 days** |
| Revenue Past 30 | Sep 23 - Oct 23, 2025 | Oct 24, 2025 - Oct 18, 2026 | **0 days** |

**Conclusion:**
☑️ Market data includes historical dates: **FALSE**
☑️ Market data is FUTURE-ONLY: **TRUE**
☑️ Zero days of overlap between our historical performance and market historical data: **TRUE**

---

## Phase 4: Feasibility Assessment

### Scenario B: NO Historical Market Data Available

## ❌ NOT FEASIBLE - Gap in Data

### 4.1 What We Have

**Our Historical Performance Data:**
- `adr_past_90` = $127 (our average daily rate, past 90 days)
- `revenue_past_30` = $2,720 (our revenue, past 30 days)
- `booking_pickup_past_30` = 40 (bookings made in past 30 days)
- `stly_adr_past_90` = $137 (same-time-last-year ADR)

**Market Data:**
- Future percentiles starting 2025-10-24 (tomorrow onwards)
- Monthly aggregates in Market KPI (Oct 2023 - Oct 2025)
- Future occupancy/cancellation data

### 4.2 What We're Missing

**Critical Missing Data:**
- Historical market median/percentile prices for dates **before 2025-10-24**
- Any daily market pricing data that overlaps with our `adr_past_90` period
- Documented meaning of Market KPI Y_value series

### 4.3 The Gap Explained

**What we need to calculate:**
```
OUR AVG VS MARKET % = ((our_adr - market_median) / market_median) × 100
                    = ((127 - ???) / ???) × 100
```

**Why we can't calculate it:**

1. **Temporal Mismatch:**
   - Our ADR: Past 90 days (Jul 25 - Oct 23, 2025)
   - Market percentiles: Future 360 days (Oct 24, 2025 - Oct 18, 2026)
   - **Gap: Complete non-overlap**

2. **No Historical Baseline:**
   - We have OUR historical performance ($127)
   - We DO NOT have MARKET historical performance for the same period
   - This is like knowing your test score but not knowing the class average

3. **Market KPI Limitations:**
   - Monthly aggregates only (not daily)
   - Unclear metric definitions (10 series, no labels)
   - Cannot reliably extract daily median for specific 90-day period
   - Would require assumptions about which series represents ADR

### 4.4 Why We Can't Bridge the Gap

**Invalid Approaches (and why they fail):**

❌ **Use future market median as proxy for past:**
```python
# INVALID: Assumes market prices don't change over time
our_adr_past = 127
market_median_future = neighborhood_data['Future Percentile Prices']['Category']['-1']['Y_values'][1][0]  # Tomorrow's median
performance = ((127 - market_median_future) / market_median_future) * 100

# Why this fails:
# - Market prices vary seasonally (summer vs winter)
# - Current market median (Oct 24) ≠ market median 90 days ago (Jul-Oct average)
# - Would produce misleading performance metrics
```

❌ **Use monthly Market KPI data:**
```python
# INVALID: Monthly aggregates vs daily ADR comparison
our_adr_past_90 = 127  # Daily average over 90 days
market_kpi_oct = market_data['Market KPI']['Category']['-1']['Y_values'][?][?]  # Which series? Which month?

# Why this fails:
# - Unknown which Y_value series represents ADR/median
# - Monthly aggregate vs 90-day daily average (different time granularities)
# - No clear mapping between Market KPI series and percentile medians
# - API provides no documentation of series meanings
```

❌ **Infer from STLY (same-time-last-year) data:**
```python
# INVALID: Our STLY doesn't give us market STLY
our_adr_past = 127
our_adr_stly = 137

# Why this fails:
# - STLY data is OUR historical performance, not MARKET historical performance
# - Knowing we averaged $137 last year doesn't tell us what market median was
# - Cannot derive market baseline from our own performance alone
```

### 4.5 Mathematical Reality

**To calculate relative performance, we need:**

| Required Component | Available? | Source |
|--------------------|-----------|---------|
| Our historical ADR (numerator) | ✅ YES | `listing_data.adr_past_90` = 127 |
| Market historical median (denominator) | ❌ NO | Not in API for past dates |
| Time period alignment | ❌ NO | Our past vs market future |

**The equation cannot be solved:**
```
Performance % = (Our ADR - Market Median) / Market Median × 100
              = (127 - UNKNOWN) / UNKNOWN × 100
              = UNDEFINED
```

### 4.6 Data Availability Summary

**What PriceLabs API Provides:**

✅ Our property's historical performance (ADR, revenue, occupancy)
✅ Future market forecasts (percentiles, occupancy, pricing)
✅ Same-time-last-year comparisons (our property only)
✅ Future-looking market penetration indices
⚠️ Monthly market aggregates (poorly documented, unclear metrics)

**What PriceLabs API Does NOT Provide:**

❌ Historical market percentile prices (daily)
❌ Historical market median ADR
❌ Past market performance metrics
❌ Any market data before today (2025-10-23)
❌ Documentation of Market KPI series meanings

---

## Phase 5: Alternative Approaches

Since direct historical comparison is not possible, here are alternative approaches that CAN be implemented with available data:

### 5.1 Forward-Looking Market Comparison

**Status: ✅ FEASIBLE**

**What it provides:**
Compare our FUTURE pricing against market median to guide adjustments going forward.

**Implementation:**
```python
def calculate_future_pricing_position(listing_data, neighborhood_data):
    """
    Compare our future prices vs market median to guide pricing strategy.
    """
    # Our future ADR
    our_adr_next_180 = listing_data['adr_next_180']  # 111

    # Market median for next 180 days (average)
    percentile_data = neighborhood_data['data']['Future Percentile Prices']['Category']['-1']
    dates = percentile_data['X_values'][:180]  # First 180 days
    median_prices = percentile_data['Y_values'][1][:180]  # Series 1 = 50th percentile

    market_median_avg = sum(median_prices) / len(median_prices)

    # Calculate position
    position_vs_market = ((our_adr_next_180 - market_median_avg) / market_median_avg) * 100

    return {
        'our_forecast_adr': our_adr_next_180,
        'market_median_forecast': market_median_avg,
        'position_percentage': position_vs_market,
        'interpretation': 'above_market' if position_vs_market > 0 else 'below_market'
    }

# Example output:
# {
#   'our_forecast_adr': 111,
#   'market_median_forecast': 88,  (example)
#   'position_percentage': 26.1,
#   'interpretation': 'above_market'
# }
```

**Use case:**
- Show "Your pricing is projected 26% above market median"
- Guide future pricing adjustments
- Identify opportunities to increase rates or adjust for competitiveness

**Limitations:**
- Tells us FUTURE position, not PAST performance
- Cannot answer "How did we perform historically vs market?"
- Different business question than original requirement

### 5.2 Year-Over-Year Performance Tracking

**Status: ✅ FEASIBLE**

**What it provides:**
Track our own performance improvement over time.

**Implementation:**
```python
def calculate_yoy_performance(listing_data):
    """
    Calculate year-over-year performance change.
    """
    # Current period
    adr_past_90 = listing_data['adr_past_90']  # 127
    revenue_past_30 = listing_data['revenue_past_30']  # 2720

    # Same time last year
    stly_adr_past_90 = listing_data['stly_adr_past_90']  # 137
    stly_revenue_past_30 = listing_data['stly_revenue_past_30']  # 2778

    # Calculate changes
    adr_change_pct = ((adr_past_90 - stly_adr_past_90) / stly_adr_past_90) * 100
    revenue_change_pct = ((revenue_past_30 - stly_revenue_past_30) / stly_revenue_past_30) * 100

    return {
        'adr_yoy_change': adr_change_pct,
        'revenue_yoy_change': revenue_change_pct,
        'current_adr': adr_past_90,
        'last_year_adr': stly_adr_past_90,
        'interpretation': 'improved' if adr_change_pct > 0 else 'declined'
    }

# Example output:
# {
#   'adr_yoy_change': -7.3,  (127 vs 137 = -7.3% decline)
#   'revenue_yoy_change': -2.1,  (2720 vs 2778 = -2.1% decline)
#   'current_adr': 127,
#   'last_year_adr': 137,
#   'interpretation': 'declined'
# }
```

**Use case:**
- Show "Your ADR decreased 7.3% vs same time last year"
- Track performance trends over time
- Identify seasonal patterns

**Limitations:**
- Compares against ourselves, not market
- Doesn't tell us if market also declined (could be market-wide trend)
- Cannot determine if we're outperforming or underperforming competitors

### 5.3 Market Penetration Index (MPI) Analysis

**Status: ✅ FEASIBLE (Future-Looking Only)**

**What it provides:**
Compare our pricing/occupancy against market using PriceLabs' calculated MPI.

**Implementation:**
```python
def analyze_market_penetration(listing_data):
    """
    Analyze our market position using forward-looking MPI metrics.
    """
    # MPI values from API (future-looking)
    mpi_next_30 = listing_data['mpi_next_30']  # 1.9
    mpi_next_60 = listing_data['mpi_next_60']  # 1.7
    mpi_next_90 = listing_data['mpi_next_90']  # 1.4

    # MPI interpretation:
    # MPI > 1.0 = pricing above market average
    # MPI = 1.0 = pricing at market average
    # MPI < 1.0 = pricing below market average

    avg_mpi = (mpi_next_30 + mpi_next_60 + mpi_next_90) / 3

    return {
        'mpi_30day': mpi_next_30,
        'mpi_60day': mpi_next_60,
        'mpi_90day': mpi_next_90,
        'average_mpi': avg_mpi,
        'interpretation': 'Premium pricing' if avg_mpi > 1.2 else
                         'Above market' if avg_mpi > 1.0 else
                         'Below market'
    }

# Example output:
# {
#   'mpi_30day': 1.9,
#   'mpi_60day': 1.7,
#   'mpi_90day': 1.4,
#   'average_mpi': 1.67,
#   'interpretation': 'Premium pricing'
# }
```

**Use case:**
- Show "You're priced 67% above market average for the next 90 days"
- Understand pricing strategy positioning
- Identify if premium pricing is sustainable

**Limitations:**
- Only available for FUTURE periods (`mpi_next_*`)
- No historical MPI available
- Cannot answer "How did we perform vs market in the past?"

### 5.4 Occupancy vs Market Occupancy Comparison

**Status: ✅ FEASIBLE (Future-Looking Only)**

**What it provides:**
Compare our projected occupancy against market averages.

**Implementation:**
```python
def compare_occupancy_rates(listing_data):
    """
    Compare our occupancy forecast vs market occupancy forecast.
    """
    # Our occupancy (remove % sign and convert)
    our_occ_30 = float(listing_data['occupancy_next_30'].rstrip(' %'))  # 70
    our_occ_90 = float(listing_data['occupancy_next_90'].rstrip(' %'))  # 31

    # Market occupancy
    market_occ_30 = float(listing_data['market_occupancy_next_30'].rstrip(' %'))  # 36
    market_occ_90 = float(listing_data['market_occupancy_next_90'].rstrip(' %'))  # 22

    # Calculate differentials
    diff_30 = our_occ_30 - market_occ_30
    diff_90 = our_occ_90 - market_occ_90

    return {
        'our_occupancy_30': our_occ_30,
        'market_occupancy_30': market_occ_30,
        'differential_30': diff_30,
        'our_occupancy_90': our_occ_90,
        'market_occupancy_90': market_occ_90,
        'differential_90': diff_90,
        'interpretation_30': f"{'Above' if diff_30 > 0 else 'Below'} market by {abs(diff_30):.1f}%",
        'interpretation_90': f"{'Above' if diff_90 > 0 else 'Below'} market by {abs(diff_90):.1f}%"
    }

# Example output:
# {
#   'our_occupancy_30': 70.0,
#   'market_occupancy_30': 36.0,
#   'differential_30': 34.0,
#   'interpretation_30': 'Above market by 34.0%',
#   'our_occupancy_90': 31.0,
#   'market_occupancy_90': 22.0,
#   'differential_90': 9.0,
#   'interpretation_90': 'Above market by 9.0%'
# }
```

**Use case:**
- Show "Your occupancy is 34% higher than market average for next 30 days"
- Identify if high pricing is reducing occupancy vs competitors
- Balance pricing vs occupancy strategy

**Limitations:**
- Only FUTURE occupancy forecasts available
- No historical occupancy vs market comparison
- Projections may not reflect actual outcomes

### 5.5 Revenue Performance Indicators

**Status: ✅ FEASIBLE (Limited)**

**What it provides:**
Track revenue trends using our own historical data.

**Implementation:**
```python
def analyze_revenue_performance(listing_data):
    """
    Analyze revenue trends and ADR efficiency.
    """
    # Historical data
    revenue_past_30 = listing_data['revenue_past_30']  # 2720
    adr_past_90 = listing_data['adr_past_90']  # 127

    # Future projections
    revenue_next_30 = listing_data['revenue_next_30']  # 2448
    revenue_next_180 = listing_data['revenue_next_180']  # 3106
    adr_next_180 = listing_data['adr_next_180']  # 111

    # Calculate trends
    revenue_trend = ((revenue_next_30 - revenue_past_30) / revenue_past_30) * 100
    adr_trend = ((adr_next_180 - adr_past_90) / adr_past_90) * 100

    # Estimated occupancy efficiency
    # (rough estimate based on revenue and ADR)
    daily_revenue_past = revenue_past_30 / 30
    daily_revenue_next = revenue_next_30 / 30

    return {
        'revenue_past_30': revenue_past_30,
        'revenue_next_30': revenue_next_30,
        'revenue_trend_pct': revenue_trend,
        'adr_past_90': adr_past_90,
        'adr_next_180': adr_next_180,
        'adr_trend_pct': adr_trend,
        'daily_revenue_past': daily_revenue_past,
        'daily_revenue_next': daily_revenue_next,
        'interpretation': 'Revenue increasing' if revenue_trend > 0 else 'Revenue declining'
    }

# Example output:
# {
#   'revenue_past_30': 2720,
#   'revenue_next_30': 2448,
#   'revenue_trend_pct': -10.0,
#   'adr_past_90': 127,
#   'adr_next_180': 111,
#   'adr_trend_pct': -12.6,
#   'daily_revenue_past': 90.67,
#   'daily_revenue_next': 81.60,
#   'interpretation': 'Revenue declining'
# }
```

**Use case:**
- Show "Revenue projected to decrease 10% next month"
- Identify negative trends early
- Prompt pricing strategy adjustments

**Limitations:**
- No market comparison (don't know if decline is property-specific or market-wide)
- Cannot determine if we're losing market share or market is declining overall

---

## Phase 6: Recommended Approach

### 6.1 What We CAN Build (Recommended Implementation)

Since historical market comparison is not feasible, implement a **Forward-Looking Pricing Intelligence Dashboard** with the following components:

#### Component 1: Future Market Position Analysis
```python
def get_pricing_intelligence(listing_id):
    """
    Comprehensive forward-looking pricing analysis.
    """
    listing = get_listing_data(listing_id)
    neighborhood = get_neighborhood_data(listing_id)

    # Get next 30 days of market median
    percentiles = neighborhood['data']['Future Percentile Prices']['Category']['-1']
    next_30_dates = percentiles['X_values'][:30]
    next_30_median = percentiles['Y_values'][1][:30]  # 50th percentile

    # Calculate average market median
    avg_market_median = sum(next_30_median) / len(next_30_median)

    # Our projected ADR
    our_adr_next = listing['adr_next_180']

    # Position calculation
    position_pct = ((our_adr_next - avg_market_median) / avg_market_median) * 100

    # MPI context
    mpi_30 = listing['mpi_next_30']

    return {
        'our_projected_adr': our_adr_next,
        'market_median_next_30': round(avg_market_median, 2),
        'position_vs_market_pct': round(position_pct, 1),
        'mpi_30_day': mpi_30,
        'recommendation': generate_pricing_recommendation(position_pct, mpi_30),
        'confidence': 'medium'  # Based on forecast data
    }

def generate_pricing_recommendation(position_pct, mpi):
    """
    Generate actionable pricing recommendation.
    """
    if position_pct > 20 and mpi > 1.5:
        return {
            'action': 'Consider reducing rates',
            'reason': 'Priced significantly above market with high MPI',
            'impact': 'May improve occupancy and total revenue'
        }
    elif position_pct < -10 and mpi < 0.8:
        return {
            'action': 'Consider increasing rates',
            'reason': 'Priced below market with low MPI',
            'impact': 'Opportunity to capture more revenue'
        }
    else:
        return {
            'action': 'Maintain current strategy',
            'reason': 'Pricing aligned with market positioning',
            'impact': 'Continue monitoring market trends'
        }
```

**Dashboard Display:**
```
┌─────────────────────────────────────────────┐
│ Forward Pricing Intelligence                │
├─────────────────────────────────────────────┤
│ Your Projected ADR (Next 180 Days)          │
│ $111                                        │
│                                             │
│ Market Median (Next 30 Days)                │
│ $88                                         │
│                                             │
│ Your Position vs Market                     │
│ +26.1% ABOVE MARKET                        │
│                                             │
│ Market Penetration Index                    │
│ 1.9x (Premium Pricing)                     │
│                                             │
│ Recommendation                              │
│ ⚠️ Consider reducing rates                 │
│ You're priced significantly above market.   │
│ Reducing rates may improve occupancy.       │
└─────────────────────────────────────────────┘
```

#### Component 2: Year-Over-Year Performance Tracking
```python
def get_yoy_performance(listing_data):
    """
    Track performance vs same time last year.
    """
    adr_current = listing_data['adr_past_90']
    adr_stly = listing_data['stly_adr_past_90']

    revenue_current = listing_data['revenue_past_30']
    revenue_stly = listing_data['stly_revenue_past_30']

    adr_change = ((adr_current - adr_stly) / adr_stly) * 100
    revenue_change = ((revenue_current - revenue_stly) / revenue_stly) * 100

    return {
        'adr_current': adr_current,
        'adr_last_year': adr_stly,
        'adr_change_pct': round(adr_change, 1),
        'revenue_current': revenue_current,
        'revenue_last_year': revenue_stly,
        'revenue_change_pct': round(revenue_change, 1),
        'trend': 'improving' if adr_change > 0 else 'declining'
    }
```

**Dashboard Display:**
```
┌─────────────────────────────────────────────┐
│ Year-Over-Year Performance                  │
├─────────────────────────────────────────────┤
│ ADR (Past 90 Days)                          │
│ Current: $127                               │
│ Last Year: $137                             │
│ Change: -7.3% ↓                            │
│                                             │
│ Revenue (Past 30 Days)                      │
│ Current: $2,720                             │
│ Last Year: $2,778                           │
│ Change: -2.1% ↓                            │
│                                             │
│ Trend Analysis                              │
│ ⚠️ Declining vs last year                  │
│ Market conditions may have changed.         │
└─────────────────────────────────────────────┘
```

#### Component 3: Occupancy Competitiveness
```python
def get_occupancy_analysis(listing_data):
    """
    Compare occupancy projections vs market.
    """
    our_occ_30 = float(listing_data['occupancy_next_30'].rstrip(' %'))
    market_occ_30 = float(listing_data['market_occupancy_next_30'].rstrip(' %'))

    our_occ_90 = float(listing_data['occupancy_next_90'].rstrip(' %'))
    market_occ_90 = float(listing_data['market_occupancy_next_90'].rstrip(' %'))

    diff_30 = our_occ_30 - market_occ_30
    diff_90 = our_occ_90 - market_occ_90

    return {
        'our_occupancy_30': our_occ_30,
        'market_occupancy_30': market_occ_30,
        'differential_30': round(diff_30, 1),
        'our_occupancy_90': our_occ_90,
        'market_occupancy_90': market_occ_90,
        'differential_90': round(diff_90, 1),
        'competitiveness': 'Strong' if diff_30 > 10 else 'Average' if diff_30 > -10 else 'Weak'
    }
```

**Dashboard Display:**
```
┌─────────────────────────────────────────────┐
│ Occupancy Competitiveness                   │
├─────────────────────────────────────────────┤
│ Next 30 Days                                │
│ Your Occupancy: 70%                         │
│ Market Average: 36%                         │
│ Differential: +34% ✓ STRONG                │
│                                             │
│ Next 90 Days                                │
│ Your Occupancy: 31%                         │
│ Market Average: 22%                         │
│ Differential: +9% ✓ ABOVE MARKET           │
│                                             │
│ Competitive Position                        │
│ ✓ Strong occupancy despite premium pricing │
└─────────────────────────────────────────────┘
```

### 6.2 Updated Column Definitions

**Replace the original "OUR AVG VS MARKET" column with:**

#### Option A: "FUTURE MARKET POSITION"
- **Label:** "VS MARKET (NEXT 30D)"
- **Calculation:** `((our_adr_next_180 - market_median_next_30_avg) / market_median_next_30_avg) * 100`
- **Display:** "+26.1%" or "-15.3%"
- **Color Coding:**
  - Green: -10% to +10% (competitive)
  - Yellow: +10% to +25% or -10% to -25% (watch)
  - Red: > +25% or < -25% (action needed)
- **Tooltip:** "Your projected ADR vs market median for next 30 days"

#### Option B: "YEAR-OVER-YEAR TREND"
- **Label:** "YOY ADR CHANGE"
- **Calculation:** `((adr_past_90 - stly_adr_past_90) / stly_adr_past_90) * 100`
- **Display:** "-7.3%" or "+12.5%"
- **Color Coding:**
  - Green: > +5% (improving)
  - Yellow: -5% to +5% (stable)
  - Red: < -5% (declining)
- **Tooltip:** "ADR change vs same period last year"

### 6.3 Implementation Code

**Recommended replacement for the current logic:**

```javascript
// Replace in listingv3.html pricing optimization table generation

function calculateMarketPosition(listingData, neighborhoodData) {
    // Get future market median (next 30 days average)
    const percentileData = neighborhoodData.data['Future Percentile Prices'].Category['-1'];
    const next30Dates = percentileData.X_values.slice(0, 30);
    const next30MedianPrices = percentileData.Y_values[1].slice(0, 30); // Series 1 = median

    const marketMedianAvg = next30MedianPrices.reduce((a, b) => a + b, 0) / next30MedianPrices.length;

    // Our projected ADR
    const ourAdr = listingData.adr_next_180;

    // Calculate position
    const positionPct = ((ourAdr - marketMedianAvg) / marketMedianAvg) * 100;

    return {
        value: positionPct,
        display: `${positionPct > 0 ? '+' : ''}${positionPct.toFixed(1)}%`,
        color: getPositionColor(positionPct),
        tooltip: `Your ADR ($${ourAdr}) is ${positionPct.toFixed(1)}% ${positionPct > 0 ? 'above' : 'below'} market median ($${marketMedianAvg.toFixed(0)})`,
        data: {
            ourAdr: ourAdr,
            marketMedian: marketMedianAvg
        }
    };
}

function getPositionColor(pct) {
    if (pct > 25) return '#ff4444'; // Red: too high
    if (pct > 10) return '#ffaa00'; // Yellow: above market
    if (pct > -10) return '#44ff44'; // Green: competitive
    if (pct > -25) return '#ffaa00'; // Yellow: below market
    return '#ff4444'; // Red: too low
}

function calculateYoyTrend(listingData) {
    const current = listingData.adr_past_90;
    const lastYear = listingData.stly_adr_past_90;

    if (!current || !lastYear) {
        return { value: null, display: 'N/A', color: '#cccccc' };
    }

    const changePct = ((current - lastYear) / lastYear) * 100;

    return {
        value: changePct,
        display: `${changePct > 0 ? '+' : ''}${changePct.toFixed(1)}%`,
        color: changePct > 5 ? '#44ff44' : changePct < -5 ? '#ff4444' : '#ffaa00',
        tooltip: `Current ADR ($${current}) vs last year ($${lastYear})`
    };
}

function generateOptimizedTarget(listingData, neighborhoodData) {
    // Get market median for next 30 days
    const percentileData = neighborhoodData.data['Future Percentile Prices'].Category['-1'];
    const next30MedianPrices = percentileData.Y_values[1].slice(0, 30);
    const marketMedian = next30MedianPrices.reduce((a, b) => a + b, 0) / next30MedianPrices.length;

    // Get MPI to understand current positioning
    const mpi = listingData.mpi_next_30 || 1.0;

    // Recommendation logic
    let targetAdr;
    let reasoning;

    if (mpi > 1.5) {
        // High MPI: consider pricing at 110% of market median
        targetAdr = marketMedian * 1.1;
        reasoning = "High MPI - reduce to improve occupancy";
    } else if (mpi < 0.8) {
        // Low MPI: can increase to 120% of market median
        targetAdr = marketMedian * 1.2;
        reasoning = "Low MPI - opportunity to increase rates";
    } else {
        // Moderate MPI: price at market median
        targetAdr = marketMedian;
        reasoning = "Optimal market positioning";
    }

    return {
        value: Math.round(targetAdr),
        display: `$${Math.round(targetAdr)}`,
        tooltip: `Recommended ADR based on market median ($${Math.round(marketMedian)}) and MPI (${mpi.toFixed(1)}): ${reasoning}`,
        reasoning: reasoning
    };
}

function calculatePriceAdjustment(currentBasePrice, optimizedTarget) {
    if (!currentBasePrice || !optimizedTarget) {
        return { value: null, display: 'N/A', color: '#cccccc' };
    }

    const adjustmentPct = ((optimizedTarget - currentBasePrice) / currentBasePrice) * 100;

    return {
        value: adjustmentPct,
        display: `${adjustmentPct > 0 ? '+' : ''}${adjustmentPct.toFixed(1)}%`,
        color: Math.abs(adjustmentPct) < 5 ? '#44ff44' : Math.abs(adjustmentPct) < 15 ? '#ffaa00' : '#ff4444',
        tooltip: `Adjust base price from $${currentBasePrice} to $${optimizedTarget} (${adjustmentPct > 0 ? 'increase' : 'decrease'} of ${Math.abs(adjustmentPct).toFixed(1)}%)`
    };
}
```

### 6.4 What This Achieves

**Provides actionable insights:**
- ✓ Shows competitive position vs market (forward-looking)
- ✓ Tracks performance trends over time
- ✓ Generates data-driven pricing recommendations
- ✓ Identifies opportunities for rate adjustments

**Limitations transparently communicated:**
- ✗ Cannot show historical performance vs market (data not available)
- ✗ Cannot answer "How did we perform in the past vs competitors?"
- ✓ CAN answer "Where do we stand vs market going forward?"
- ✓ CAN answer "How are we trending vs last year?"

---

## Summary and Conclusion

### Final Assessment

**Question:** Can we calculate historical performance metrics (our ADR vs market median) using ONLY PriceLabs API data?

**Answer:** **NO - Not Possible**

**Reason:** The PriceLabs API provides:
1. ✓ Our historical ADR (`adr_past_90` = $127)
2. ✗ Market percentile/median data ONLY for future dates (starting 2025-10-24)
3. Zero temporal overlap between our historical data and market historical data

**Analogy:** We have our test score ($127) but the API doesn't provide the class average for when we took the test. It only tells us what the class average will be for FUTURE tests.

### What We Can Build Instead

**Forward-Looking Pricing Intelligence Dashboard:**
- Future market position analysis (next 30-180 days)
- Year-over-year trend tracking (our performance vs ourselves)
- Occupancy competitiveness metrics (vs market forecasts)
- Data-driven pricing recommendations (based on MPI and market forecasts)

### Implementation Priority

**High Priority (Build These):**
1. Future Market Position column (replaces "OUR AVG VS MARKET")
2. Year-over-Year Trend column
3. Optimized Target calculation (using forward market data)
4. Price Adjustment recommendations

**Not Possible (Cannot Build):**
1. Historical performance vs market comparison
2. Past 90-day market benchmark analysis
3. Historical market share calculations

### Next Steps

1. **Update column definitions** in dashboard specification
2. **Implement forward-looking calculations** as shown in Section 6.3
3. **Add clear tooltips** explaining what metrics represent
4. **Document limitations** in user-facing documentation
5. **Consider future API enhancement requests** to PriceLabs for historical market data

---

## Appendix: API Endpoint Summary

### Available Endpoints (Tested)

| Endpoint | Status | Data Provided |
|----------|--------|---------------|
| `/api/listing/<id>` | ✓ Working | Listing details, historical ADR, future projections |
| `/api/neighborhood/<id>` | ✓ Working | Market percentiles (future), Market KPI (monthly), Occupancy data |
| `/api/listing_prices/<id>` | ✓ Working | Daily pricing data with ADR, booking status |
| `/api/reservation_data/<id>` | ⚠️ Limited | Basic reservation info (extracted from listing fields) |

### Key Data Structures

**Percentile Data Mapping:**
```
Y_values[0] = 25th percentile
Y_values[1] = 50th percentile (median) ← Most relevant for comparison
Y_values[2] = 75th percentile
Y_values[3] = Median booked price
Y_values[4] = 90th percentile
Y_values[5] = Unknown (possibly listing count or 10th percentile)
```

**Market KPI Series:**
```
10 different time series (Y_values[0-9])
- Unclear metric definitions
- Monthly granularity only
- Not suitable for daily ADR comparison
```

### Data Availability Timeline

```
Timeline Visualization:

                           TODAY
                             ↓
Past ←─────────────────── 2025-10-23 ────────────────────→ Future

Our ADR Past 90:
├─────────────────────────┤
Jul 25                Oct 23

Market Percentile Data:
                              ├──────────────────────────────────┤
                           Oct 24                            Oct 18, 2026

Gap: No Overlap ❌
```

---

**Analysis Completed:** 2025-10-23
**Analyst:** Claude (AI Assistant)
**Confidence Level:** High (based on actual API responses)
**Data Sources:** Real API calls to localhost:5050
**Recommendation Status:** Actionable alternatives provided
