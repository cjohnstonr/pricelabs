"""
Test the Flask endpoint directly without starting the full server
"""

from listing_viewer_app import app, portfolio_manager
import json

# Initialize test client
client = app.test_client()

# Refresh portfolio data
print("Refreshing portfolio data...")
portfolio_manager.refresh_all_listings()

# Get a test listing
first_listing_id = list(portfolio_manager.portfolio_listing_map.keys())[0]
listing_info = portfolio_manager.listing_cache[first_listing_id]

print(f"\nTesting with listing:")
print(f"  Name: {listing_info.get('name')}")
print(f"  ID: {first_listing_id}")
print(f"  Portfolio: {listing_info.get('portfolio_name')}")

# Test the endpoint
print(f"\nCalling /api/reservation_data/{first_listing_id}")
print("="*80)

response = client.get(f'/api/reservation_data/{first_listing_id}?start_date=2025-01-01&end_date=2025-12-31')

print(f"Status Code: {response.status_code}")
print(f"\nResponse:")
print(json.dumps(response.get_json(), indent=2))

if response.status_code == 200:
    data = response.get_json()
    if 'data' in data:
        print(f"\n✅ SUCCESS! Got {len(data['data'])} reservation records")
        if len(data['data']) > 0:
            print(f"\n📊 First reservation:")
            print(json.dumps(data['data'][0], indent=2))
    else:
        print(f"\n⚠️  No 'data' key in response")
else:
    print(f"\n❌ Failed with status {response.status_code}")
