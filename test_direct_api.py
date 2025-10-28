"""
Quick test to verify the reservation_data API works directly
"""

from pricelabs_api import PriceLabsAPI
from portfolio_manager import PortfolioManager

print("Testing direct PriceLabs API reservation_data call...")
print("="*80)

# Get portfolio manager
manager = PortfolioManager()
manager.refresh_all_listings()

# Get first listing
first_listing_id = list(manager.portfolio_listing_map.keys())[0]
listing_info = manager.listing_cache[first_listing_id]

print(f"\nTesting with: {listing_info.get('name')}")
print(f"Listing ID: {first_listing_id}")
print(f"Portfolio: {listing_info.get('portfolio_name')}")

# Get API client
api_client = manager.get_api_client_for_listing(first_listing_id)

print("\nCalling get_reservation_data()...")
try:
    data = api_client.get_reservation_data(
        pms=None,
        start_date='2024-01-01',
        end_date='2025-12-31',
        limit=100,
        offset=0
    )

    print(f"✅ Success!")
    print(f"Response type: {type(data)}")

    if isinstance(data, dict):
        print(f"Response keys: {list(data.keys())}")

        if 'data' in data:
            reservations = data['data']
            print(f"\n📊 Total reservations: {len(reservations)}")

            if len(reservations) > 0:
                print(f"\n🔍 First reservation:")
                first = reservations[0]
                for key, value in first.items():
                    print(f"  {key}: {value}")
            else:
                print("⚠️  No reservation records in date range")
        else:
            print(f"⚠️  Unexpected structure: {data}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
