"""
Find listings with booking data
"""

from portfolio_manager import PortfolioManager
import json

manager = PortfolioManager()
manager.refresh_all_listings()

print("\nSearching for listings with booking data...")
print("="*80)

found_bookings = []

for listing_id, listing_data in manager.listing_cache.items():
    # Check for any booking-related fields
    has_last_booked = listing_data.get('last_booked_date') is not None
    revenue = listing_data.get('revenue_past_30') or 0
    has_revenue = revenue > 0 if isinstance(revenue, (int, float)) else False
    occ = listing_data.get('occupancy_past_90')
    has_occupancy = occ not in [None, '0 %', 0, '0%'] if occ else False

    if has_last_booked or has_revenue or has_occupancy:
        found_bookings.append({
            'id': listing_id,
            'name': listing_data.get('name', 'Unknown'),
            'portfolio': listing_data.get('portfolio_name'),
            'last_booked': listing_data.get('last_booked_date'),
            'revenue_past_30': listing_data.get('revenue_past_30'),
            'revenue_next_30': listing_data.get('revenue_next_30'),
            'occupancy_past_90': listing_data.get('occupancy_past_90'),
            'occupancy_next_30': listing_data.get('occupancy_next_30'),
            'adr_past_90': listing_data.get('adr_past_90')
        })

if found_bookings:
    print(f"\n✅ Found {len(found_bookings)} listings with booking indicators")
    print(f"\nTop 5 listings with most data:")
    print("="*80)

    for listing in found_bookings[:5]:
        print(f"\n📊 {listing['name'][:50]}")
        print(f"   ID: {listing['id']}")
        print(f"   Portfolio: {listing['portfolio']}")
        print(f"   Last Booked: {listing['last_booked']}")
        print(f"   Revenue Past 30: ${listing['revenue_past_30']}")
        print(f"   Revenue Next 30: ${listing['revenue_next_30']}")
        print(f"   Occupancy Past 90: {listing['occupancy_past_90']}")
        print(f"   Occupancy Next 30: {listing['occupancy_next_30']}")
        print(f"   ADR Past 90: ${listing['adr_past_90']}")

    # Test with the first listing that has data
    print(f"\n{'='*80}")
    print(f"Testing Flask endpoint with: {found_bookings[0]['name'][:50]}")
    print(f"Listing ID: {found_bookings[0]['id']}")
    print(f"{'='*80}")

    from listing_viewer_app import app
    client = app.test_client()

    response = client.get(f'/api/reservation_data/{found_bookings[0]["id"]}')
    data = response.get_json()

    print(f"\nEndpoint Response:")
    print(json.dumps(data, indent=2))

else:
    print("\n⚠️  No listings found with booking data")
    print("This might mean:")
    print("  1. Listings don't have recent bookings")
    print("  2. PriceLabs hasn't synced booking data yet")
    print("  3. Booking data is tracked differently in the API")
