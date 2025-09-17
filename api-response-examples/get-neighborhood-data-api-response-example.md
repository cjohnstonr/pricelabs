# Get Neighborhood Data API Response Example

Generated: 2025-09-17T00:22:18+00:00

## Working Listing ID: 4305303 (airbnb)

## Response Structure

```json
{
  "data": {
    "Listings Used": 350,
    "currency": "USD",
    "lat": 32.7238,
    "lng": -117.132,
    "source": "airbnb",
    "Future Percentile Prices": {
      "Category": {
        "1": {
          "X_values": [
            "2025-09-17",
            "2025-09-18",
            "2025-09-19",
            "2025-09-20",
            "2025-09-21",
            "2025-09-22",
            "2025-09-23"
          ],
          "Y_values": [
            [98.8, 98.8, 98.8, 98.8, 98.8, 208.2, 98.8],
            [117.8, 117.8, 117.8, 128.8, 128.8, 258.2, 117.8],
            [148.8, 148.8, 148.8, 168.8, 168.8, 318.2, 148.8],
            [125.6, 115.6, 115.6, 135.6, 135.6, 285.6, 115.6],
            [188.8, 188.8, 188.8, 218.8, 218.8, 388.2, 188.8]
          ],
          "Listings Used": 245,
          "Active Used": 245,
          "Inactive Used": 0
        }
      },
      "Labels": [
        "25th Percentile",
        "50th Percentile", 
        "75th Percentile",
        "Median Booked Price",
        "90th Percentile"
      ]
    },
    "Summary Table Base Price": {
      "Category": {
        "1": {
          "Y_values": [
            106,
            149,
            189,
            242,
            [],
            []
          ],
          "Listings Used": 245,
          "Active Used": 245,
          "Inactive Used": 0
        },
        "All": {
          "Y_values": [
            99,
            141,
            185,
            236,
            [],
            []
          ],
          "Listings Used": 350,
          "Active Used": 350,
          "Inactive Used": 0
        }
      },
      "Labels": [
        "25th Percentile Price( USD)",
        "50th Percentile Price( USD)",
        "75th Percentile Price( USD)",
        "90th Percentile Price( USD)"
      ]
    },
    "Future Occ/New/Canc": {
      "Category": {
        "1": {
          "X_values": [
            "2025-09-17",
            "2025-09-18",
            "2025-09-19",
            "2025-09-20",
            "2025-09-21",
            "2025-09-22",
            "2025-09-23"
          ],
          "Y_values": [
            [[87.5, 80.4, 65.7, 72.1, 68.9, 45.2, 75.3]],
            [[0, 0, 0, 0, 0, 0, 0]],
            [[0, 0, 0, 0, 0, 0, 0]],
            [[91.2, 100, 94.1, 89.3, 92.7, 78.4, 88.6]],
            [[91.2, 100, 94.1, 89.3, 92.7, 78.4, 88.6]],
            [[0, 0, 0, 0, 0, 0, 0]]
          ],
          "Listings Used": 245,
          "Active Used": 245,
          "Inactive Used": 0
        }
      },
      "Labels": [
        "Occupancy",
        "New Bookings",
        "Canceled Bookings", 
        "Occupancy_LY",
        "Occupancy_STLY",
        "New_Bookings_STLY"
      ]
    },
    "Neighborhood Data Source": "Nearby Listings"
  }
}
```

## Key Data Structures

### Main Response Fields:
- `Listings Used` - Number of listings in market analysis
- `currency` - Currency for all price data
- `lat`, `lng` - Geographic coordinates of listing
- `source` - Data source ("airbnb" or "vrbo")

### Future Percentile Prices:
**Structure**: Daily market price percentiles for different bedroom categories
- `Category` - Bedroom count categories (1, 2, 3, etc.)
- `X_values` - Array of dates (YYYY-MM-DD format)
- `Y_values` - 2D array with 5 rows:
  - Row 0: 25th percentile prices
  - Row 1: 50th percentile prices  
  - Row 2: 75th percentile prices
  - Row 3: Median booked prices
  - Row 4: 90th percentile prices
- `Labels` - Names for each Y_values row

### Summary Table Base Price:
**Structure**: Overall market pricing percentiles
- Same structure as Future Percentile Prices
- Contains historical price ranges (past 180 + future 180 days)
- "All" category includes all bedroom types

### Future Occ/New/Canc:
**Structure**: Occupancy and booking activity data
- `X_values` - Array of future dates
- `Y_values` - 2D array with 6 rows:
  - Row 0: Current occupancy rates
  - Row 1: New bookings count
  - Row 2: Cancellation count
  - Row 3: Occupancy last year (LY)
  - Row 4: Occupancy same time last year (STLY)
  - Row 5: New bookings same time last year

## Usage Notes:

### Extracting Daily Market Data:
```javascript
// Get percentiles for specific date
const dateIndex = data.Future_Percentile_Prices.Category['1'].X_values.indexOf('2025-09-20');
const p25 = data.Future_Percentile_Prices.Category['1'].Y_values[0][dateIndex]; // 25th percentile
const p50 = data.Future_Percentile_Prices.Category['1'].Y_values[1][dateIndex]; // 50th percentile
const p75 = data.Future_Percentile_Prices.Category['1'].Y_values[2][dateIndex]; // 75th percentile
const p90 = data.Future_Percentile_Prices.Category['1'].Y_values[4][dateIndex]; // 90th percentile
```

### Bedroom Categories:
- `"-1"` = Room (studio/private room)
- `"0"` = Studio
- `"1"` = 1 Bedroom
- `"2"` = 2 Bedroom
- etc.

### Market Occupancy:
```javascript
// Get market occupancy for specific date
const dateIndex = data.Future_Occ_New_Canc.Category['1'].X_values.indexOf('2025-09-20');
const marketOccupancy = data.Future_Occ_New_Canc.Category['1'].Y_values[0][0][dateIndex];
```

## Data Quality Indicators:
- `Active Used` - Number of active listings in analysis
- `Inactive Used` - Number of inactive listings included
- Higher listing counts = more reliable market data