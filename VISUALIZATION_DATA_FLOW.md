# Data Flow Visualization - Pricing Optimization Columns

## Current State (BROKEN) - Why We See N/A

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FRONTEND (listingv5.html)                        │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ Line 1119: Fetch reservation data
                              ▼
        ┌──────────────────────────────────────────────────┐
        │ http://localhost:5050/api/reservation_data/ID    │
        │        ?start_date=2025-01-01                    │
        │        &end_date=2025-12-31                      │
        └──────────────────────────────────────────────────┘
                              │
                              │ ❌ 404 NOT FOUND
                              ▼
        ┌──────────────────────────────────────────────────┐
        │   FLASK SERVER (listing_viewer_app.py)           │
        │                                                   │
        │   ✅ /api/listing/<id>                           │
        │   ✅ /api/listing_prices/<id>                    │
        │   ✅ /api/neighborhood/<id>                      │
        │   ❌ /api/reservation_data/<id>  ← MISSING!      │
        └──────────────────────────────────────────────────┘
                              │
                              │ Returns nothing
                              ▼
        ┌──────────────────────────────────────────────────┐
        │  JavaScript Variable State                       │
        │                                                   │
        │  reservationData = null                          │
        │  bookedDaysInsights = {                          │
        │    avgPercentVsMarket: null,     ← ❌           │
        │    totalBookings: 0,                             │
        │    isDataAvailable: false        ← ❌           │
        │  }                                               │
        └──────────────────────────────────────────────────┘
                              │
                              │ Line 1827: if (isDataAvailable) → FALSE
                              ▼
        ┌──────────────────────────────────────────────────┐
        │  Table Rendering (Line 1841-1848)                │
        │                                                   │
        │  avgPercentText = "N/A"          ← ❌           │
        │  optimizedTarget = null          ← ❌           │
        │  adjustmentText = "N/A"          ← ❌           │
        └──────────────────────────────────────────────────┘
                              │
                              ▼
        ┌──────────────────────────────────────────────────┐
        │  USER SEES IN TABLE:                             │
        │                                                   │
        │  OUR AVG VS MARKET:      N/A                     │
        │  OPTIMIZED TARGET:       N/A                     │
        │  PRICE ADJUSTMENT %:     N/A                     │
        └──────────────────────────────────────────────────┘
```

---

## Fixed State (WORKING) - How It Should Work

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FRONTEND (listingv5.html)                        │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ Line 1119: Fetch reservation data
                              ▼
        ┌──────────────────────────────────────────────────┐
        │ http://localhost:5050/api/reservation_data/ID    │
        │        ?start_date=2025-01-01                    │
        │        &end_date=2025-12-31                      │
        └──────────────────────────────────────────────────┘
                              │
                              │ ✅ 200 OK
                              ▼
        ┌──────────────────────────────────────────────────┐
        │   FLASK SERVER (listing_viewer_app.py)           │
        │                                                   │
        │   ✅ NEW ENDPOINT ADDED:                         │
        │   @app.route('/api/reservation_data/<id>')       │
        │   def get_reservation_data(listing_id):          │
        │       api_client = get_api_client(listing_id)    │
        │       return api_client.get_reservation_data()   │
        └──────────────────────────────────────────────────┘
                              │
                              │ Calls PriceLabs API
                              ▼
        ┌──────────────────────────────────────────────────┐
        │   PRICELABS API (/v1/reservation_data)           │
        │                                                   │
        │   Returns: {                                     │
        │     "data": [                                    │
        │       {                                          │
        │         "check_in": "2025-02-15",                │
        │         "no_of_days": 3,                         │
        │         "rental_revenue": 495.00,                │
        │         "booking_status": "booked",              │
        │         "listing_id": "778..."                   │
        │       },                                         │
        │       ... 15 more bookings                       │
        │     ]                                            │
        │   }                                              │
        └──────────────────────────────────────────────────┘
                              │
                              │ ✅ Returns to frontend
                              ▼
        ┌──────────────────────────────────────────────────┐
        │  processBookedDaysData() - Line 1895            │
        │                                                   │
        │  For each booking:                               │
        │    1. Calculate nightly rate = revenue / nights  │
        │    2. Get market median for those dates          │
        │    3. Calculate: (rate - median) / median * 100  │
        │                                                   │
        │  Results:                                        │
        │    Booking 1: +12.3% vs market                   │
        │    Booking 2: +8.7% vs market                    │
        │    Booking 3: +15.2% vs market                   │
        │    ... 13 more bookings                          │
        │                                                   │
        │  Average: +11.4% vs market                       │
        └──────────────────────────────────────────────────┘
                              │
                              │ Line 1979-1994
                              ▼
        ┌──────────────────────────────────────────────────┐
        │  updateBookedDaysSummary()                       │
        │                                                   │
        │  bookedDaysInsights = {                          │
        │    avgPercentVsMarket: +11.4,    ← ✅           │
        │    totalBookings: 16,                            │
        │    isDataAvailable: true         ← ✅           │
        │    lastCalculated: "2025-10-23..."               │
        │  }                                               │
        └──────────────────────────────────────────────────┘
                              │
                              │ Line 1176: updatePricingTable() called
                              ▼
        ┌──────────────────────────────────────────────────┐
        │  For each day in 90-day forecast:                │
        │                                                   │
        │  Day: 2025-10-24                                 │
        │  Market Median (from neighborhood API): $180     │
        │  Current Price (from pricing API): $165          │
        │  Avg Performance: +11.4%                         │
        │                                                   │
        │  ✅ Column 1 Calculation:                        │
        │     avgPercentText = "+11.4%"                    │
        │     avgPercentClass = "positive"                 │
        │                                                   │
        │  ✅ Column 2 Calculation:                        │
        │     optimizedTarget = $180 × 1.114 = $200.52     │
        │                                                   │
        │  ✅ Column 3 Calculation:                        │
        │     adjustment = ($200.52 - $165) / $165 * 100   │
        │                = +21.5%                          │
        │     category = "increase-significant"            │
        │     adjustmentText = "Increase 21.5%"            │
        └──────────────────────────────────────────────────┘
                              │
                              ▼
        ┌──────────────────────────────────────────────────┐
        │  USER SEES IN TABLE (with color coding):         │
        │                                                   │
        │  OUR AVG VS MARKET:      +11.4% (green)          │
        │  OPTIMIZED TARGET:       $201                    │
        │  PRICE ADJUSTMENT %:     Increase 21.5% (green)  │
        └──────────────────────────────────────────────────┘
```

---

## Calculation Deep Dive - Example with Real Numbers

```
┌────────────────────────────────────────────────────────────────┐
│  STEP 1: Gather Historical Booking Data                       │
└────────────────────────────────────────────────────────────────┘

Your Past Bookings (from Reservation API):
┌──────────┬────────┬─────────┬────────────┬────────────────┐
│ Check-in │ Nights │ Revenue │ Nightly    │ Market Median  │
├──────────┼────────┼─────────┼────────────┼────────────────┤
│ 2025-02  │   3    │  $495   │  $165/nt   │  $150/nt       │
│ 2025-03  │   2    │  $340   │  $170/nt   │  $155/nt       │
│ 2025-04  │   5    │  $875   │  $175/nt   │  $160/nt       │
│ 2025-05  │   1    │  $180   │  $180/nt   │  $165/nt       │
└──────────┴────────┴─────────┴────────────┴────────────────┘

Performance Calculation:
┌──────────┬────────────┬────────────────┬──────────────────┐
│ Booking  │ Your Rate  │ Market Median  │ % vs Market      │
├──────────┼────────────┼────────────────┼──────────────────┤
│ Feb      │   $165     │     $150       │ +10.0%           │
│ Mar      │   $170     │     $155       │  +9.7%           │
│ Apr      │   $175     │     $160       │  +9.4%           │
│ May      │   $180     │     $165       │  +9.1%           │
├──────────┼────────────┼────────────────┼──────────────────┤
│ AVERAGE  │   $172.50  │    $157.50     │ +9.5%     ← ✅  │
└──────────┴────────────┴────────────────┴──────────────────┘

COLUMN 1 VALUE: +9.5%
Meaning: You consistently book at 9.5% above market


┌────────────────────────────────────────────────────────────────┐
│  STEP 2: Calculate Optimized Target for Tomorrow              │
└────────────────────────────────────────────────────────────────┘

Tomorrow's Date: 2025-10-24

Market Data (from Neighborhood API):
  Market Median Booked Price: $200

Optimization Formula:
  Optimized Target = Market Median × (1 + Your Performance %)
                   = $200 × (1 + 0.095)
                   = $200 × 1.095
                   = $219

COLUMN 2 VALUE: $219
Meaning: Recommended price based on your historical success


┌────────────────────────────────────────────────────────────────┐
│  STEP 3: Calculate Price Adjustment from Current Price        │
└────────────────────────────────────────────────────────────────┘

Your Current Price (from Pricing API): $190

Adjustment Formula:
  Adjustment % = ((Target - Current) / Current) × 100
               = (($219 - $190) / $190) × 100
               = ($29 / $190) × 100
               = 15.3%

Category Logic:
  - adjustment > 10%  → "increase-significant" (GREEN)
  - adjustment > 2%   → "increase-moderate" (YELLOW)
  - adjustment < -10% → "decrease-significant" (RED)
  - adjustment < -2%  → "decrease-moderate" (ORANGE)
  - else              → "optimal" (BLUE)

  15.3% > 10% → GREEN "increase-significant"

COLUMN 3 VALUE: "Increase 15.3%" (GREEN)
Meaning: You should raise your price by $29 to hit optimal target
```

---

## Why This Is Powerful

```
WITHOUT this data:                    WITH this data:
┌────────────────────────┐            ┌────────────────────────┐
│ Manual Price Setting   │            │ AI-Driven Optimization │
├────────────────────────┤            ├────────────────────────┤
│ ❌ Guess at pricing    │            │ ✅ Data-backed targets │
│ ❌ No market context   │            │ ✅ Market benchmarking │
│ ❌ Unknown performance │            │ ✅ Historical insights │
│ ❌ Random adjustments  │            │ ✅ Specific % guidance │
│ ❌ Leave money on table│            │ ✅ Maximize revenue    │
└────────────────────────┘            └────────────────────────┘

Scenario: Tomorrow's pricing decision

Current approach:                     Optimized approach:
"I'll set it at $190                  "Based on 16 bookings where I
because... that feels right?"         averaged +9.5% above market,
                                      and tomorrow's market median
                                      is $200, I should price at
                                      $219 for optimal revenue."

Result: Leave $29/night on table     Result: Maximize earnings
```

---

## Technical Implementation Flow

```
┌─────────────────────────────────────────────────────────────┐
│  IMPLEMENTATION CHECKLIST                                   │
└─────────────────────────────────────────────────────────────┘

1. Add Flask Endpoint
   ┌────────────────────────────────────────────────────┐
   │ File: listing_viewer_app.py                        │
   │ Line: ~728 (before if __name__ == '__main__':)     │
   │                                                     │
   │ @app.route('/api/reservation_data/<listing_id>')   │
   │ def get_reservation_data(listing_id):              │
   │     portfolio_info = get_portfolio(listing_id)     │
   │     api_client = get_api_client(listing_id)        │
   │     data = api_client.get_reservation_data(...)    │
   │     return jsonify(data)                           │
   └────────────────────────────────────────────────────┘
                          │
                          │ Restart Flask server
                          ▼
2. Test Endpoint
   ┌────────────────────────────────────────────────────┐
   │ Run: python test_reservation_endpoint.py           │
   │                                                     │
   │ Expected:                                          │
   │   ✅ PASS - Flask Endpoint                         │
   │   ✅ PASS - PriceLabs API                          │
   │   ✅ PASS - Neighborhood Data                      │
   │   ✅ PASS - Calculation Logic                      │
   └────────────────────────────────────────────────────┘
                          │
                          │ All tests pass
                          ▼
3. Manual Browser Test
   ┌────────────────────────────────────────────────────┐
   │ URL: http://localhost:5050/listingv5.html          │
   │                                                     │
   │ Check:                                             │
   │   • Columns populate with data                     │
   │   • Colors display correctly                       │
   │   • Calculations make sense                        │
   │   • No console errors                              │
   └────────────────────────────────────────────────────┘
                          │
                          │ Visual verification
                          ▼
4. Production Deployment
   ┌────────────────────────────────────────────────────┐
   │ • Commit changes                                   │
   │ • Document in changelog                            │
   │ • Deploy to production                             │
   │ • Monitor for errors                               │
   └────────────────────────────────────────────────────┘
```

---

## Summary

**Problem:** One missing API endpoint
**Solution:** 40 lines of Python code
**Impact:** Unlock AI-driven pricing optimization for 111 properties
**Time:** < 1 hour from start to production
**Risk:** Minimal (additive change, no breaking modifications)

This is a **high-value, low-risk** fix that will immediately provide actionable pricing insights to users.
