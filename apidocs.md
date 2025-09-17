ApiHub Design Logo

Log In
PriceLabs Customer API
 1.0.0-oas3 
OAS 3.0
Using PriceLabs Customer API, users will be able to import PriceLabs' Dynamic prices per listing in any system. These prices are updated every 24 hours.

Click here to know more about Customer API and to know how you can enable it for your PriceLabs account.

Please reach out to support@pricelabs.co if you have any queries on the Customer API.

Once the Customer API is enabled for your PL account, please use copy the API key from Settings => API Details in your PriceLabs account and send it as X-API-Key in the header for each of the below endpoints.

Rate limiting & Timeout configuration
Each Customer API Key accessing the API has a limit of 1000 requests per hour. Reaching the rate limit will return a 429 Too Many Requests status code.

Please be aware that the processing time for your request may vary depending on the current server load. We recommend setting the client timeout to 300 seconds to allow for any potential delays, even though our aim is to respond to all requests within that timeframe.

PriceLabs Support - Website
Send email to PriceLabs Support
Servers

https://api.pricelabs.co
Customer APIs
Here are all the endpoints available in our Customer API


Listings


GET
/v1/listings
Get all listings in an account



This API call will return all the listings in a customer's account across all PMSs, with their minimum price, base price, recommended base price and maximum price along with other Performance Metrics available on the Pricing Dashboard and Multi-Calendar pages. You can find performance metrics after clicking "Add Metrics" button on the Pricing Dashboard or Multi Calendar.

Parameters
Name	Description
skip_hidden
string
(query)
This param can be used to filter hidden listings. Default is false which will return all listings including hidden listing. If set to true then hidden listings will not be returned in the response.


true
only_syncing_listings
string
(query)
This param can be used to filter listings based on their sync status. Default is false which will return all listings in the PriceLabs user account. If set to true then return only those listings will be returned whose sync is turned ON.


true
X-API-Key
string
(header)
{{API_KEY}}
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "listings": [
    {
      "id": "834874",
      "pms": "rentalsunited",
      "name": "Rentals United - PriceLabs1New",
      "latitude": 41.8781136,
      "longitude": -87.6297982,
      "country": "United States",
      "city_name": "Chicago",
      "state": "Illinois",
      "no_of_bedrooms": 3,
      "min": 90,
      "base": 145,
      "max": 200,
      "group": "testgroup",
      "subgroup": "testsubgroup",
      "tags": "testtag",
      "notes": "testnotes",
      "isHidden": false,
      "push_enabled": false,
      "occupancy_next_7": 100,
      "market_occupancy_next_7": 75,
      "occupancy_next_30": 90,
      "market_occupancy_next_30": 85,
      "occupancy_next_60": 87,
      "market_occupancy_next_60": 67,
      "occupancy_past_90": 78,
      "market_occupancy_past_90": 87,
      "revenue_past_7": "76,",
      "stly_revenue_past_7": 67,
      "recommended_base_price": 120,
      "last_date_pushed": "2023-03-15T11:23:21.000Z",
      "last_refreshed_at": "2023-04-10T14:06:29+00:00"
    }
  ]
}
No links

POST
/v1/listings
Update one or more listings in an account



You can either update a listing or a group of listings.

Required parameters:
(In case of min, base and max you can send all three, or any two or any one among the three)

id: Listing ID
pms: PMS name of the listing
min: Min price of the listing
base: Base price of the listing
max: Max price of the listing
Response Codes:
200: Parameters were updated
400: Invalid listing id or pms name; please check your request
Parameters
Name	Description
X-API-Key
string
(header)
{{API_KEY}}
Request body

application/json
Example Value
Schema
{
  "listings": [
    {
      "id": "2854562",
      "min": 899,
      "pms": "airbnb"
    }
  ]
}
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Examples

update listings
Example Value
Schema
{
  "listings": [
    {
      "base": 1200,
      "id": "2854562",
      "max": 1500,
      "min": 900
    },
    {
      "base": 1300,
      "id": "2590637",
      "max": 1800,
      "min": 800
    }
  ]
}
Headers:
Name	Description	Type
Age		string
Example: 1
Cache-Control		string
Example: max-age=0, private, must-revalidate
Connection		string
Example: keep-alive
Date		string
Example: Sat, 10 Nov 2018 03:27:04 GMT
ETag		string
Example: W/"7b50ffc2feb4b141dd5fa9ab4d1da33e"
Server		string
Example: nginx/1.10.3 (Ubuntu)
Status		string
Example: 200 OK
Strict-Transport-Security		string
Example: max-age=31536000;
Transfer-Encoding		string
Example: chunked
Vary		string
Example: Accept-Encoding
Via		string
Example: http/1.1 api-umbrella (ApacheTrafficServer [cMsSf ])
X-Cache		string
Example: MISS
X-Content-Type-Options		string
Example: nosniff
X-Frame-Options		string
Example: SAMEORIGIN
X-Request-Id		string
Example: 321b0732-466f-413f-b23a-067f7e787719
X-Runtime		string
Example: 0.048499
X-XSS-Protection		string
Example: 1; mode=block
No links

GET
/v1/listings/{listing_id}
Get a specific listing in an account



This API call will return a specific listing in a customer's account, with their minimum price, base price, recommended base price and maximum price along with other Performance Metrics available on the Pricing Dashboard and Multi-Calendar pages. You can find performance metrics after clicking "Add Metrics" button on the Pricing Dashboard or Multi Calendar.

Parameters
Name	Description
listing_id *
string
(path)
834874
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "listings": [
    {
      "id": "834874",
      "pms": "rentalsunited",
      "name": "Rentals United - PriceLabs1New",
      "latitude": 41.8781136,
      "longitude": -87.6297982,
      "country": "United States",
      "city_name": "Chicago",
      "state": "Illinois",
      "no_of_bedrooms": 2,
      "min": 90,
      "base": 145,
      "max": 200,
      "group": "testgroup",
      "subgroup": "testsubgroup",
      "tags": "testtag",
      "notes": "testnotes",
      "isHidden": false,
      "push_enabled": false,
      "occupancy_next_7": 100,
      "market_occupancy_next_7": 75,
      "occupancy_next_30": 90,
      "market_occupancy_next_30": 85,
      "occupancy_next_60": 87,
      "market_occupancy_next_60": 67,
      "occupancy_past_90": 78,
      "market_occupancy_past_90": 87,
      "revenue_past_7": "76,",
      "stly_revenue_past_7": 67,
      "recommended_base_price": 120,
      "last_date_pushed": "2023-03-15T11:23:21.000Z",
      "last_refreshed_at": "2023-04-10T14:06:29+00:00"
    }
  ]
}
No links

POST
/v1/add_listing_data
To add import newly added listings in PMS.



Use this API call to pull new listings that you have added in your PMS, please make sure the "listing_id" in the body is for an existing listing that was previously added to your PriceLabs account.

Note: This API call works only for "bookingsync" PMS.
Response on this API call has the following information:

"success": A success message "Successfully connected with BookingSync"
"lat_lng_listings": An array of listing Ids with missing latitude or longitude. Please update the latitude and longitude information in BookingSync and try this API call again to add these listing IDs in your PL account.
"listing_ids": An array of listing Ids that have been successully added in the PL account. You may head over to your PL account to review prices for these listings.
Parameters
No parameters

Request body

application/json
Example Value
Schema
{
  "listing": "12345",
  "pms_name": "bookingsync"
}
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "success": "Successfully connected with BookingSync",
    "lat_lng_listings": "12345, 23456",
    "listing_ids": "234321, 762636"
  }
]
No links
Date Specific Overrides (DSO)


GET
/v1/listings/{listing_id}/overrides
To fetch a listing's date specific overrides



Use this API to get your listing's date specific overrides

Note that,

check_in_check_out_enabled = 0, if check-in/check-out is disabled for the DSO.

check_in_check_out_enabled = 1, if check-in/check-out is enabled, followed by check_in and check_out values as a binary string of 7 characters, with each character specific for day of the week, starting Monday through Sunday.

0 = not allowed
1 = allowed
eg., check_in = 1000001 means check-in is allowed only on Monday and Sunday.
    check_out = 0010000 means check-out is allowed only on Wednesday.
Required parameters:
id: Listing ID in the URL
pms: PMS name of the listing as a parameter
Response Codes:
200: Request returned successfully
400: Invalid listing id or pms name; please check your request
Parameters
Name	Description
pms *
string
(query)
airbnb
X-API-Key
string
(header)
{{API_KEY}}
listing_id *
string
(path)
listing_id
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Examples

listing date level overrides
Example Value
Schema
{
  "overrides": [
    {
      "date": "2023-07-16",
      "price": "144",
      "price_type": "fixed",
      "currency": "EUR",
      "min_stay": 5,
      "min_price": 100,
      "min_price_type": "fixed",
      "max_price": 155,
      "max_price_type": "fixed",
      "check_in_check_out_enabled": "1",
      "check_in": "0000010",
      "check_out": "0000001",
      "reason": "Test Reason"
    },
    {
      "date": "2023-07-17",
      "price": "144",
      "price_type": "fixed",
      "currency": "EUR",
      "min_stay": 5,
      "min_price": 100,
      "min_price_type": "fixed",
      "max_price": 155,
      "max_price_type": "fixed",
      "check_in_check_out_enabled": "1",
      "check_in": "0000010",
      "check_out": "0000001",
      "reason": "Test Reason"
    },
    {
      "date": "2023-07-18",
      "price": "144",
      "price_type": "fixed",
      "currency": "EUR",
      "min_stay": 5,
      "min_price": 100,
      "min_price_type": "fixed",
      "max_price": 155,
      "max_price_type": "fixed",
      "check_in_check_out_enabled": "1",
      "check_in": "0000010",
      "check_out": "0000001",
      "reason": "Test Reason"
    },
    {
      "date": "2023-07-19",
      "price": "144",
      "price_type": "fixed",
      "currency": "EUR",
      "min_stay": 5,
      "min_price": 100,
      "min_price_type": "fixed",
      "max_price": 155,
      "max_price_type": "fixed",
      "check_in_check_out_enabled": "1",
      "check_in": "0000010",
      "check_out": "0000001",
      "reason": "Test Reason"
    },
    {
      "date": "2023-07-20",
      "price": "144",
      "price_type": "fixed",
      "currency": "EUR",
      "min_stay": 5,
      "min_price": 100,
      "min_price_type": "fixed",
      "max_price": 155,
      "max_price_type": "fixed",
      "check_in_check_out_enabled": "1",
      "check_in": "0000010",
      "check_out": "0000001",
      "reason": "Test Reason"
    },
    {
      "date": "2023-07-21",
      "price": "144",
      "price_type": "fixed",
      "currency": "EUR",
      "min_stay": 5,
      "min_price": 100,
      "min_price_type": "fixed",
      "max_price": 155,
      "max_price_type": "fixed",
      "check_in_check_out_enabled": "1",
      "check_in": "0000010",
      "check_out": "0000001",
      "reason": "Test Reason"
    },
    {
      "date": "2023-07-22",
      "price": "144",
      "price_type": "fixed",
      "currency": "EUR",
      "min_stay": 5,
      "min_price": 100,
      "min_price_type": "fixed",
      "max_price": 155,
      "max_price_type": "fixed",
      "check_in_check_out_enabled": "1",
      "check_in": "0000010",
      "check_out": "0000001",
      "reason": "Test Reason"
    }
  ]
}
Headers:
Name	Description	Type
Age		string
Example: 0
Cache-Control		string
Example: max-age=0, private, must-revalidate
Connection		string
Example: keep-alive
Date		string
Example: Sat, 10 Nov 2018 04:46:07 GMT
ETag		string
Example: W/"b47718cf4586d71392eade22200b4f0c"
Server		string
Example: nginx/1.10.3 (Ubuntu)
Status		string
Example: 200 OK
Strict-Transport-Security		string
Example: max-age=31536000;
Transfer-Encoding		string
Example: chunked
Vary		string
Example: Accept-Encoding
Via		string
Example: http/1.1 api-umbrella (ApacheTrafficServer [cMsSf ])
X-Cache		string
Example: MISS
X-Content-Type-Options		string
Example: nosniff
X-Frame-Options		string
Example: SAMEORIGIN
X-Request-Id		string
Example: c709e935-df8d-4467-b10f-e6b615d0e7cb
X-Runtime		string
Example: 0.205981
X-XSS-Protection		string
Example: 1; mode=block
No links

POST
/v1/listings/{listing_id}/overrides
Add/Update a listing's date specific override



Use this API to update a date specific override. Following conditions are to be followed strictly before you send the data to update

Rules:
When adding/updating price object make sure the price_type is one of the two (fixed or percent). If there is anything other than these two options then the update for price will be ignored.

When sending price_type as fixed make sure currency is exactly what you have in your PMS. If currency is different between date specific override and listing, your update will result in erroneous data.
When sending price_type as percent, the percentage change will be applied on the recommended base price.
When updating min_stay send an integer greater than 0.

When updating min_price object make sure the min_price_type is fixed or else update will result in erroneous data.

When sending min_price_type as fixed make sure currency is exactly what you have in your PMS.
If the flag update_children, which is a boolean flag, sent as true, the DSO will also be updated for all the child listings. If you send update_children as false, then DSO will only be updated for the parent listing and not for the child listings.

If price_type is fixed, then price represents the fixed price. If price_type is percent, then price is the percentage change on the recommended price and should have a value ranging from -75 to 500.

If min_price_type is fixed, then min_price is the fixed price. If min_price_type is percent_base or percent_min, then min_price represents a percentage change on the base price or the minimum price, respectively, and should have a value ranging from -75 to 500.

If max_price_type is fixed, then max_price is the fixed maximum price. If max_price_type is percent_base or percent_max, then max_price represents a percentage change on the listing base price or the maximum price, respectively, and should have a value ranging from -75 to 500.

Response:
Response will contain data for each date that was updated, if something was erroneous then the response will not have that object. The extra key child_listings_update_info is added to the response when update_children is true. If you pass update_children as true for a listing which does not have any child listing, an empty object will be sent back in child_listings_update_info.

Parameters
Name	Description
X-API-Key
string
(header)
{{API_KEY}}
listing_id *
string
(path)
listing_id
Request body

application/json
Example Value
Schema
{
  "pms": "apaleo",
  "update_children": true,
  "overrides": [
    {
      "date": "2023-07-16",
      "price": "122",
      "price_type": "fixed",
      "currency": "EUR",
      "min_stay": 8,
      "min_price": 99,
      "min_price_type": "fixed",
      "max_price": 149,
      "max_price_type": "fixed",
      "base_price": 100,
      "check_in_check_out_enabled": "1",
      "check_in": "0000010",
      "check_out": "0000001",
      "reason": "DSO update"
    },
    {
      "date": "2023-07-18",
      "price": "122",
      "price_type": "percent",
      "min_stay": 8,
      "check_in_check_out_enabled": "0",
      "reason": "DSO update"
    },
    {
      "date": "2023-07-20",
      "price": 0,
      "min_stay": 4,
      "check_in_check_out_enabled": "1",
      "check_in": "0010001",
      "check_out": "0000101",
      "reason": "DSO update"
    }
  ]
}
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Examples

listing date level overrides
Example Value
Schema
{
  "overrides": [
    {
      "date": "2023-07-16",
      "price": "122",
      "price_type": "fixed",
      "currency": "EUR",
      "min_stay": 8,
      "min_price": 99,
      "min_price_type": "fixed",
      "max_price": 149,
      "max_price_type": "fixed",
      "check_in_check_out_enabled": "1",
      "check_in": "0000010",
      "check_out": "0000001"
    },
    {
      "date": "2023-07-18",
      "price": "122",
      "price_type": "percent",
      "min_stay": 8,
      "check_in_check_out_enabled": "0"
    },
    {
      "date": "2023-07-20",
      "min_stay": 4,
      "check_in_check_out_enabled": "1",
      "check_in": "0010001",
      "check_out": "0000101"
    }
  ],
  "child_listings_update_info": {
    "test_listing_id_111": {
      "success": "true"
    }
  }
}
Headers:
Name	Description	Type
Age		string
Example: 0
Cache-Control		string
Example: max-age=0, private, must-revalidate
Connection		string
Example: keep-alive
Date		string
Example: Sat, 10 Nov 2018 04:46:01 GMT
ETag		string
Example: W/"3327b679f6575cd9cfb243355aea13cd"
Server		string
Example: nginx/1.10.3 (Ubuntu)
Status		string
Example: 200 OK
Strict-Transport-Security		string
Example: max-age=31536000;
Transfer-Encoding		string
Example: chunked
Vary		string
Example: Accept-Encoding
Via		string
Example: http/1.1 api-umbrella (ApacheTrafficServer [cMsSf ])
X-Cache		string
Example: MISS
X-Content-Type-Options		string
Example: nosniff
X-Frame-Options		string
Example: SAMEORIGIN
X-Request-Id		string
Example: 0389f7ef-24af-4a44-90f1-f0aa32e5ceca
X-Runtime		string
Example: 0.184497
X-XSS-Protection		string
Example: 1; mode=block
No links

DELETE
/v1/listings/{listing_id}/overrides
Delete a listing's date specific override



Use this API to delete a Date Specific Override(DSO). If you send update_children as true, then the DSO for child listing will also be deleted. If you send update_children as false, then DSO will only be deleted for the parent listing and not for the child listings.

Parameters
Name	Description
X-API-Key
string
(header)
{{API_KEY}}
listing_id *
string
(path)
listing_id
Request body

application/json
Example Value
Schema
{
  "overrides": [
    {
      "date": "2023-07-17"
    },
    {
      "date": "2023-07-19"
    },
    {
      "date": "2023-07-20"
    },
    {
      "date": "2023-07-25"
    }
  ],
  "pms": "airbnb",
  "update_children": true
}
Responses
Code	Description	Links
204	
A successful response with status 204. The response body will be empty

Media type

text/plain
Controls Accept header.
Examples

listing date level overrides
Example Value
Headers:
Name	Description	Type
Age		string
Example: 0
Cache-Control		string
Example: no-cache
Connection		string
Example: keep-alive
Date		string
Example: Sat, 10 Nov 2018 18:52:57 GMT
Server		string
Example: nginx/1.10.3 (Ubuntu)
Status		string
Example: 204 No Content
Strict-Transport-Security		string
Example: max-age=31536000;
Via		string
Example: http/1.1 api-umbrella (ApacheTrafficServer [cMs f ])
X-Cache		string
Example: MISS
X-Content-Type-Options		string
Example: nosniff
X-Frame-Options		string
Example: SAMEORIGIN
X-Request-Id		string
Example: b84864c3-118c-4014-acb4-1508c9db4fd0
X-Runtime		string
Example: 0.160643
X-XSS-Protection		string
Example: 1; mode=block
No links
Prices


POST
/v1/listing_prices
prices for listings



Use this API to get prices for your listings that exist in your PriceLabs account. Following conditions are to be followed strictly:

Rules:
Listing and their PMS have to exist in your PriceLabs account.
You may provide a date range using the "dateFrom" and "dateTo" fields in the request body, if you want to fetch prices for a specific date range. Kindly note that both "dateFrom" and "dateTo" should be valid current OR future dates. If any past dates are sent, then we will return prices for the entire calendar.
Response:
Response will contain price information that was last refreshed for each listing.

Error Statuses:
LISTING_NOT_PRESENT: This particular listing does not exist in PriceLabs, either it was deleted or was never added. Please re-connect this listing's PMS on PriceLabs and try again.

LISTING_NO_DATA: Prices were not fetched on PriceLabs. Please head over to PriceLabs and review prices and once you see recommendations then you can retry the API request to get prices for this listing.

LISTING_TOGGLE_OFF: Sync is turned OFF for the listing. Hence, the prices cannot be returned. Please head over to PriceLabs and turn the sync ON if you want to pull prices from API for this listing.

Parameters
Name	Description
X-API-Key
string
(header)
{{API_KEY}}
Request body

application/json
Example Value
Schema
{
  "listings": [
    {
      "id": "ABCDEF",
      "pms": "pms",
      "dateFrom": "2023-01-01",
      "dateTo": "2023-12-31",
      "reason": true
    },
    {
      "id": "12345",
      "pms": "airbnb"
    },
    {
      "id": "11051___123121",
      "pms": "lodgify"
    },
    {
      "id": "bcd32262-eb0d-4192-b2eb-3da30f380346",
      "pms": "orbirental"
    }
  ]
}
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Examples

Listing Prices
Example Value
Schema
[
  {
    "id": "PL111",
    "pms": "test_pms",
    "group": "",
    "currency": "EUR",
    "last_refreshed_at": "2023-07-13T08:17:53+00:00",
    "los_pricing": {
      "1": {
        "los_night": "1",
        "max_price": "",
        "min_price": "",
        "los_adjustment": "10"
      },
      "5": {
        "los_night": "5",
        "max_price": "",
        "min_price": "",
        "los_adjustment": "-5"
      },
      "7": {
        "los_night": "7",
        "max_price": "",
        "min_price": "",
        "los_adjustment": "-10"
      },
      "28": {
        "los_night": "28",
        "max_price": "",
        "min_price": "",
        "los_adjustment": "-20"
      }
    },
    "data": [
      {
        "date": "2023-07-13",
        "price": 93,
        "user_price": 250,
        "uncustomized_price": 93,
        "min_stay": 2,
        "booking_status": "",
        "booking_status_STLY": "",
        "ADR": -1,
        "ADR_STLY": -1,
        "booked_date": "-1",
        "booked_date_STLY": "-1",
        "unbookable": 1,
        "weekly_discount": 0.9,
        "monthly_discount": 0.8,
        "extra_person_fee": 15,
        "extra_person_fee_trigger": 6,
        "check_in": true,
        "check_out": false,
        "demand_color": "#c0f1958c",
        "demand_desc": "Low Demand",
        "reason": {
          "listing_info": {
            "ADR": -1,
            "avg_los": 0,
            "num_bookings": 0,
            "num_checkins": 0,
            "num_checkouts": 0,
            "booked_date": "-1",
            "date_STLY": "2023-01-17",
            "ADR_STLY": -1,
            "avg_los_STLY": 0,
            "num_bookings_STLY": 0,
            "num_checkins_STLY": 0,
            "num_checkouts_STLY": 0,
            "booked_date_STLY": "-1",
            "num_blocked": 0,
            "occupancy": 0,
            "max_price_limit": 99999,
            "min_price_limit": 10,
            "unbookable": 0,
            "currency": "USD",
            "price": "798",
            "uncustomized_price": "1262",
            "last_price": null,
            "price_with_default_discounts": "798",
            "locale": "en",
            "OfficialAirbnb": 0,
            "nhood_demand": "1",
            "availability": "1",
            "l_occupied": "0",
            "minstay_seasonal_profile": "",
            "nhood_occ": "20%",
            "customized_price": "798",
            "minimum_price": "600",
            "maximum_price": "20000",
            "base_price": "2000",
            "base_price_type": "Listing",
            "dso_flag": "0",
            "seasonal_base_price_flag": "0"
          }
        },
        "market_factors": {
          "0": {
            "key": "seasonality",
            "value": "-32%",
            "price": 1368,
            "title": "Seasonality"
          },
          "1": {
            "key": "demand_factor",
            "value": "-8%",
            "price": 1262,
            "title": "Demand Factor",
            "hotel_demand": "-0%",
            "str_demand": "-8%"
          }
        },
        "pricing_customizations": {
          "0": {
            "key": "last_min_factor",
            "value": "-26%",
            "price": 939,
            "title": "Last Minute Price Factor (default)"
          },
          "1": {
            "key": "listing_occ_pricing_factor",
            "value": "-15%",
            "price": 798,
            "title": "Occupancy Based Adjustment (default)"
          }
        },
        "thresholds": {
          "0": {
            "key": "min_price",
            "value": 600,
            "title": "Min Price (Safety)"
          },
          "1": {
            "key": "max_price",
            "value": 20000,
            "title": "Max Price (Safety)"
          }
        },
        "other_customizations": {},
        "final_price_override": {},
        "final_adjustments": {},
        "debug_info": {
          "base_price": 2000,
          "overall_mult": 0.4692823113828266,
          "overall_mult_custom": 0.4692823113828266,
          "uncustomized_price_raw": 1262,
          "forecast_occ": 0.2031,
          "forecast_prices": 305.4,
          "seasonality_without_price_adjuster": 0.62,
          "price_adjuster": 1,
          "demand_factor_tag": "",
          "reason_html": "Please refresh your browser"
        }
      },
      {
        "date": "2023-07-14",
        "price": 105,
        "user_price": 250,
        "uncustomized_price": 105,
        "min_stay": 3,
        "booking_status": "",
        "booking_status_STLY": "",
        "ADR": -1,
        "ADR_STLY": -1,
        "booked_date": "-1",
        "booked_date_STLY": "-1",
        "unbookable": 1,
        "weekly_discount": 0.9,
        "monthly_discount": 0.8,
        "extra_person_fee": 15,
        "extra_person_fee_trigger": 6,
        "check_in": false,
        "check_out": true,
        "demand_color": "#c0f1958c",
        "demand_desc": "Low Demand"
      },
      {
        "date": "2023-07-15",
        "price": 111,
        "user_price": 250,
        "uncustomized_price": 111,
        "min_stay": 3,
        "booking_status": "",
        "booking_status_STLY": "",
        "ADR": -1,
        "ADR_STLY": -1,
        "booked_date": "-1",
        "booked_date_STLY": "-1",
        "unbookable": 1,
        "weekly_discount": 0.9,
        "monthly_discount": 0.8,
        "extra_person_fee": 15,
        "extra_person_fee_trigger": 6,
        "check_in": true,
        "check_out": false,
        "demand_color": "#c0f1958c",
        "demand_desc": "Low Demand"
      },
      {
        "date": "2023-07-16",
        "price": 109,
        "user_price": 250,
        "uncustomized_price": 109,
        "min_stay": 2,
        "booking_status": "",
        "booking_status_STLY": "",
        "ADR": -1,
        "ADR_STLY": -1,
        "booked_date": "-1",
        "booked_date_STLY": "-1",
        "unbookable": 1,
        "weekly_discount": 0.9,
        "monthly_discount": 0.8,
        "extra_person_fee": 15,
        "extra_person_fee_trigger": 6,
        "check_in": false,
        "check_out": true,
        "demand_color": "#c0f1958c",
        "demand_desc": "Low Demand"
      },
      {
        "date": "2023-07-17",
        "price": 115,
        "user_price": 250,
        "uncustomized_price": 115,
        "min_stay": 2,
        "booking_status": "",
        "booking_status_STLY": "",
        "ADR": -1,
        "ADR_STLY": -1,
        "booked_date": "-1",
        "booked_date_STLY": "-1",
        "unbookable": 1,
        "weekly_discount": 0.9,
        "monthly_discount": 0.8,
        "extra_person_fee": 15,
        "extra_person_fee_trigger": 6,
        "check_in": true,
        "check_out": false,
        "demand_color": "#c0f1958c",
        "demand_desc": "Low Demand"
      },
      {
        "date": "2023-07-18",
        "price": 121,
        "user_price": 250,
        "uncustomized_price": 121,
        "min_stay": 2,
        "booking_status": "",
        "booking_status_STLY": "",
        "ADR": -1,
        "ADR_STLY": -1,
        "booked_date": "-1",
        "booked_date_STLY": "-1",
        "unbookable": 1,
        "weekly_discount": 0.9,
        "monthly_discount": 0.8,
        "extra_person_fee": 15,
        "extra_person_fee_trigger": 6,
        "check_in": false,
        "check_out": false,
        "demand_color": "#c0f1958c",
        "demand_desc": "Low Demand"
      },
      {
        "date": "2023-07-19",
        "price": 127,
        "user_price": 250,
        "uncustomized_price": 127,
        "min_stay": 2,
        "weekly_discount": 0.9,
        "monthly_discount": 0.8,
        "extra_person_fee": 15,
        "extra_person_fee_trigger": 6,
        "check_in": false,
        "check_out": false,
        "demand_color": "#c0f1958c",
        "demand_desc": "Low Demand"
      }
    ]
  }
]
No links

GET
/v1/fetch_rate_plans
Fetch rate plan adjustments for your listings



If your listings have rate plan adjusments, then you can use this API call to fetch those adjustments. You can fetch the prices for the default rate plan using the /listing_prices call and use the adjustments returned in this call to derive the prices of the non-default rate plans for your system.

Parameters
Name	Description
X-API-Key
string
(header)
{{API_KEY}}
listing_id
string
(query)
{{listing_id}}
pms_name
string
(query)
{{pms_name}}
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "rate_plans": {
      "id": "string",
      "pms": "string",
      "name": "string",
      "rateplans": {
        "rate_plan_id": {
          "name": "string",
          "type": "string",
          "default": "string",
          "plan_type": "string",
          "adjustment": 0,
          "update_type": "string"
        }
      }
    }
  }
]
No links
Neighborhood Data


GET
/v1/neighborhood_data
Get neighborhood data for a listing



Get neighborhood data for your listing with all stats that show up in the "Neighborhood Tab". The data returned by this API call will majorly contain:

Total number of listings considered in this neighborhood.

Basic listing information including currency, latitude and longitude of the listing.

Source of the data: The source of data will be Airbnb or VRBO as indicated in the response.

Future Percentile Prices for the listing: For each bedroom category identified by the key, we return a different percentile price for the market for each stay date. In order to comprehend this data, it is important to note that there are 4 key pieces of information in the response:

 Key
 X_values
 Y_values
 Labels


 Key details:
 -1: "Room"
 0: "Studio"
 1: "1BR" and so on.
X_values contain an array of future dates Labels: For "Future Percentile Prices," these will be the 25th Percentile, 50th Percentile, 75th Percentile, Median Booked Price, 90th Percentile.

Y_values: There are 5 corresponding arrays in Y_values. These 5 arrays in Y_values denote the data for the labels mentioned in the "Labels" array for each date in X_values.

In the example given in the success response below, we have provided a compact response for 3 future dates.

For Category 0 (Studio), the 25th Percentile value of the Future Percentile Price for 2023-11-15 is 92.7. Similarly, the 50th Percentile value of Future Percentile Price for 2023-11-15 is 115.1.

Future Occ/New/Canc: For each bedroom category identified by the key, we provide occupancy and pickup for the future, as well as occupancy, pickup, and final occupancy from the same time last year. Similar to 'Future Percentile Prices,' labels are present in the API response for the identification of different arrays. The response structure is the same as in Future Percentile Prices. Labels for Future Occ/New/Canc Response are as follows:

 Occupancy
 New Bookings
 Canceled Bookings
 Occupancy_LY
 Occupancy_STLY
 New_Bookings_STLY
In the example mentioned, the label 'Occupancy' for category 0 on 2023-05-19 is 87.5. Similarly, 'New Bookings' for category 0 on 2023-05-19 is 0. The value of Occupancy_LY (final occupancy last year) for 2023-05-19 is 91.1765.

Summary Table Base Price: For each bedroom category identified by the key, we provide different percentile prices considering the past 180 and future 180 days.

API Response structure is the same as in Future Percentile Prices. Labels for Summary Table Base Price Response are as follows:

 25th Percentile Price
 50th Percentile Price
 75th Percentile Price
 90th Percentile Price
If the ND source is a Market Dashboard, then following additional Labels will be provided:

 Median Listed Price (USD)
 Median Booked Nightly Price (USD)
 Median Booked Weekly Price (USD)
 Median Booked Monthly Price (USD)
 Median LOS
 Median Lead Time
The Summary Table Base Price for the same category 0 can also be identified. The 25th Percentile Price of 'Summary Table Base Price' is 98. The '50th Percentile Price' of the Base price for category 0 is 126.

About Market KPI:

The market KPI JSON object stores aggregated data at a monthly level, along with data for the last 365 days and the last 730 days. It has two main keys: Category and Labels.

1. Category:
      a. This key contains sub-keys where each sub-key represents a specific bedroom type (e.g., 1 Bedroom, 2 Bedroom, etc.).
      
      b. Each bedroom type contains a data object with two keys:
      
          i. X_values: A 1-dimensional array that represents the time periods for which data is available.
          
          ii. Y_values: A 2-dimensional array with 5 rows, where each row corresponds to a specific KPI (Key Performance Indicator).
          
      c. The number of columns in Y_values matches the number of elements in X_values, indicating KPI values for the periods specified in X_values.
      
2. Labels:
  a. This key provides the names of the KPIs corresponding to the rows in Y_values. (value of this will be a  ["Total Available Days","Booking Window","LOS","Revenue","Total Booked Days"] )
  
KPI Details :

  Total Available Days : This represents the total number of days that all the listings in the area were available for booking during the specified period.
  
  Booking Window : This shows you the median number of days between when the date the booking was made and the first stay date for that booking during the specific period.
  
  LOS : This shows how many nights a clients are booking the properties per reservation during that specific period.
  Revenue : This is the total revenue generated from bookings across all listings in the area during the period.
  
  Total Booked Days : This KPI reflects the total number of days that were booked across all listings in the area during the period.
Parameters
Name	Description
pms *
string
(query)
vrm
listing_id *
string
(query)
SUNSETPROPS_OLSE___239
X-API-Key
string
(header)
{{API_KEY}}
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Examples

Neighborhood Data
Example Value
Schema
{
  "data": {
    "data": {
      "Listings Used": 350,
      "currency": "EUR",
      "lat": 48.2041,
      "lng": 16.3697,
      "source": "airbnb",
      "Future Percentile Prices": {
        "Category": {
          "0": {
            "X_values": [
              "2023-11-15",
              "2023-11-16",
              "2023-11-17"
            ],
            "Y_values": [
              [
                92.7,
                93.6,
                103.7
              ],
              [
                115.1,
                116.1,
                139
              ],
              [
                148.8,
                151.6,
                166.6
              ],
              [
                107.2,
                110.4,
                126.8
              ],
              [
                177.3,
                181.2,
                217.6
              ]
            ],
            "Listings Used": 50,
            "Active Used": 50,
            "Inactive Used": 0
          },
          "1": {
            "X_values": [
              "2023-11-15",
              "2023-11-16",
              "2023-11-17"
            ],
            "Y_values": [
              [
                99.2,
                99.2,
                108.6
              ],
              [
                129.2,
                128.2,
                147.9
              ],
              [
                166.6,
                169.4,
                194.2
              ],
              [
                125.4,
                126.3,
                147.9
              ],
              [
                215.8,
                216.2,
                240.4
              ]
            ],
            "Listings Used": 245,
            "Active Used": 245,
            "Inactive Used": 0
          },
          "-1": {
            "X_values": [
              "2023-11-15",
              "2023-11-16",
              "2023-11-17"
            ],
            "Y_values": [
              [
                60.8,
                61.8,
                58
              ],
              [
                110.4,
                116.5,
                122.1
              ],
              [
                169.4,
                194.7,
                239.8
              ],
              [
                75.8,
                78.6,
                101.1
              ],
              [
                203.8,
                242,
                288.7
              ]
            ],
            "Listings Used": 55,
            "Active Used": 55,
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
          "0": {
            "Y_values": [
              98,
              126,
              171,
              199,
              [],
              []
            ],
            "Listings Used": 50,
            "Active Used": 50,
            "Inactive Used": 0
          },
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
          "-1": {
            "Y_values": [
              58,
              99,
              199,
              244,
              [],
              []
            ],
            "Listings Used": 55,
            "Active Used": 55,
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
          "25th Percentile Price( EUR)",
          "50th Percentile Price( EUR)",
          "75th Percentile Price( EUR)",
          "90th Percentile Price( EUR)"
        ]
      },
      "Future Occ/New/Canc": {
        "Category": {
          "0": {
            "X_values": [
              "2023-05-19",
              "2023-05-20",
              "2023-05-21"
            ],
            "Y_values": [
              [
                [
                  87.5,
                  80.4878,
                  65.71430000000001
                ]
              ],
              [
                [
                  0,
                  0,
                  0
                ]
              ],
              [
                [
                  0,
                  0,
                  0
                ]
              ],
              [
                [
                  91.1765,
                  100,
                  94.1176
                ]
              ],
              [
                [
                  91.1765,
                  100,
                  94.1176
                ]
              ],
              [
                [
                  0,
                  0,
                  0
                ]
              ]
            ],
            "Listings Used": 50,
            "Active Used": 50,
            "Inactive Used": 0
          },
          "1": {
            "X_values": [
              "2023-05-19",
              "2023-05-20",
              "2023-05-21"
            ],
            "Y_values": [
              [
                [
                  88.63640000000001,
                  88.63640000000001,
                  73.7143
                ]
              ],
              [
                [
                  0,
                  0,
                  0
                ]
              ],
              [
                [
                  0,
                  0,
                  0
                ]
              ],
              [
                [
                  91.7355,
                  93.75,
                  91.0569
                ]
              ],
              [
                [
                  91.7355,
                  93.75,
                  91.0569
                ]
              ],
              [
                [
                  0,
                  0,
                  0
                ]
              ]
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
    },
    "status": "Success"
  }
}
No links
400	
Invalid request

Media type

application/json
Examples

neighborhood_data
Example Value
Schema
{
  "error": "Invalid request"
}
No links
404	
Listing Not Found

Media type

application/json
Examples

neighborhood_data
Example Value
Schema
{
  "error": "Listing not found"
}
No links
Reservations


GET
/v1/reservation_data
Get Reservations received from your PMS along with rental revenue information.



This API will return all the reservations received from the PMS connected to the PriceLabs account. If a PMS does not provide reservations, this API will not return any reservations for that PMS.Kindly note that rental_revenue is available for only those PMSs that share this information. booking_status can have only two values - booked or cancelled. The response is paginated, with limit as 100 results per page. This API call should be called to fetch more page results, until next_page = false.

Parameters
Name	Description
pms
string
(query)
igms
start_date
string
(query)
2020-01-01
end_date
string
(query)
2020-01-10
limit
string
(query)
100
offset
string
(query)
0
X-API-Key
string
(header)
{{API_KEY}}
Responses
Code	Description	Links
200	
Success

Media type

application/json
Controls Accept header.
Example Value
Schema
{
  "pms_name": "string",
  "next_page": true,
  "data": [
    {
      "listing_id": "string",
      "listing_name": "string",
      "reservation_id": "string",
      "check_in": "string",
      "check_out": "string",
      "booking_status": "booked",
      "booked_date": "string",
      "rental_revenue": "string",
      "total_cost": "string",
      "no_of_days": 0,
      "currency": "string",
      "cancelled_on": "string",
      "min_price_type": "string"
    }
  ]
}
No links
