# Get Listing Prices API Response Example

Generated: 2025-09-17T00:22:18+00:00

## Working Listing ID: 4305303 (airbnb)

## Response Structure

```json
[
  {
    "id": "4305303",
    "pms": "airbnb",
    "group": "Jill,verified",
    "currency": "USD",
    "last_refreshed_at": "2025-09-17T00:22:18+00:00",
    "data": [
      {
        "date": "2025-09-16",
        "price": 109,
        "user_price": -1,
        "uncustomized_price": 94,
        "min_stay": 1,
        "booking_status": "Booked",
        "booking_status_STLY": "Booked",
        "ADR": 111.86,
        "ADR_STLY": 115.04,
        "booked_date": "2025-08-19",
        "booked_date_STLY": "2024-08-31",
        "unbookable": 0,
        "extra_person_fee": 0,
        "extra_person_fee_trigger": 0,
        "demand_color": "#EDEDED",
        "demand_desc": "Unavailable"
      },
      {
        "date": "2025-09-17",
        "price": 109,
        "user_price": -1,
        "uncustomized_price": 86,
        "min_stay": 1,
        "booking_status": "Booked",
        "booking_status_STLY": "Booked",
        "ADR": 111.86,
        "ADR_STLY": 115.04,
        "booked_date": "2025-08-19",
        "booked_date_STLY": "2024-08-31",
        "unbookable": 0,
        "extra_person_fee": 0,
        "extra_person_fee_trigger": 0,
        "demand_color": "#EDEDED",
        "demand_desc": "Unavailable"
      },
      {
        "date": "2025-09-18",
        "price": 109,
        "user_price": 109,
        "uncustomized_price": 104,
        "min_stay": 1,
        "booking_status": "",
        "booking_status_STLY": "Booked",
        "ADR": -1,
        "ADR_STLY": 115.04,
        "booked_date": "-1",
        "booked_date_STLY": "2024-08-31",
        "unbookable": 0,
        "extra_person_fee": 0,
        "extra_person_fee_trigger": 0,
        "demand_color": "#c0f1958c",
        "demand_desc": "Low Demand"
      },
      {
        "date": "2025-09-19",
        "price": 109,
        "user_price": 109,
        "uncustomized_price": 104,
        "min_stay": 1,
        "booking_status": "",
        "booking_status_STLY": "Booked",
        "ADR": -1,
        "ADR_STLY": 115.04,
        "booked_date": "-1",
        "booked_date_STLY": "2024-08-31",
        "unbookable": 0,
        "extra_person_fee": 0,
        "extra_person_fee_trigger": 0,
        "demand_color": "#c0f1958c",
        "demand_desc": "Low Demand"
      },
      {
        "date": "2025-09-20",
        "price": 175,
        "user_price": 175,
        "uncustomized_price": 175,
        "min_stay": 1,
        "booking_status": "",
        "booking_status_STLY": "",
        "ADR": -1,
        "ADR_STLY": -1,
        "booked_date": "-1",
        "booked_date_STLY": "-1",
        "unbookable": 0,
        "extra_person_fee": 0,
        "extra_person_fee_trigger": 0,
        "demand_color": "#d4eb7b8c",
        "demand_desc": "Medium Demand"
      },
      {
        "date": "2025-09-21",
        "price": 175,
        "user_price": 175,
        "uncustomized_price": 175,
        "min_stay": 1,
        "booking_status": "",
        "booking_status_STLY": "",
        "ADR": -1,
        "ADR_STLY": -1,
        "booked_date": "-1",
        "booked_date_STLY": "-1",
        "unbookable": 0,
        "extra_person_fee": 0,
        "extra_person_fee_trigger": 0,
        "demand_color": "#d4eb7b8c",
        "demand_desc": "Medium Demand"
      },
      {
        "date": "2025-09-22",
        "price": 400,
        "user_price": 400,
        "uncustomized_price": 400,
        "min_stay": 1,
        "booking_status": "",
        "booking_status_STLY": "",
        "ADR": -1,
        "ADR_STLY": -1,
        "booked_date": "-1",
        "booked_date_STLY": "-1",
        "unbookable": 0,
        "extra_person_fee": 0,
        "extra_person_fee_trigger": 0,
        "demand_color": "#eb59598c",
        "demand_desc": "High Demand"
      },
      {
        "date": "2025-09-23",
        "price": 109,
        "user_price": 109,
        "uncustomized_price": 104,
        "min_stay": 1,
        "booking_status": "",
        "booking_status_STLY": "",
        "ADR": -1,
        "ADR_STLY": -1,
        "booked_date": "-1",
        "booked_date_STLY": "-1",
        "unbookable": 0,
        "extra_person_fee": 0,
        "extra_person_fee_trigger": 0,
        "demand_color": "#c0f1958c",
        "demand_desc": "Low Demand"
      }
    ]
  }
]
```

## Key Data Fields

### Response Array Level:
- `id` - Listing ID
- `pms` - Platform management system 
- `group` - Listing group/tags
- `currency` - Price currency
- `last_refreshed_at` - When data was last updated
- `data` - Array of daily pricing data

### Daily Data Fields:
- `date` - Date in YYYY-MM-DD format
- `price` - Your current price for this date
- `user_price` - Manual override price (-1 if none)
- `uncustomized_price` - Base algorithmic price before customizations
- `min_stay` - Minimum stay requirement
- `booking_status` - "Booked" if occupied, "" if available
- `booking_status_STLY` - Same time last year booking status
- `ADR` - Actual Daily Rate if booked (-1 if not booked)
- `ADR_STLY` - ADR from same time last year
- `booked_date` - When this date was booked (YYYY-MM-DD or "-1")
- `booked_date_STLY` - When same date was booked last year
- `unbookable` - 1 if date is blocked/unavailable, 0 if bookable
- `extra_person_fee` - Additional fee per extra guest
- `extra_person_fee_trigger` - Guest count that triggers extra fee
- `demand_color` - Hex color representing demand level
- `demand_desc` - Human readable demand level ("Low Demand", "Medium Demand", "High Demand", "Unavailable")

## Status Indicators:
- **Available**: `booking_status` = "", `ADR` = -1
- **Booked**: `booking_status` = "Booked", `ADR` > 0
- **Unavailable**: `demand_desc` = "Unavailable" or `unbookable` = 1

## Demand Levels:
- **Low Demand**: Green color (#c0f1958c)
- **Medium Demand**: Yellow color (#d4eb7b8c) 
- **High Demand**: Red color (#eb59598c)
- **Unavailable**: Gray color (#EDEDED)