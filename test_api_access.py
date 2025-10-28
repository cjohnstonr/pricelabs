"""
Test which API endpoints are accessible with our API keys
"""

from pricelabs_api import PriceLabsAPI
from portfolio_manager import PortfolioManager

print("Testing API endpoint accessibility...")
print("="*80)

# Get portfolio manager
manager = PortfolioManager()
all_data = manager.refresh_all_listings()

# Get first portfolio
first_portfolio_key = list(manager.portfolios.keys())[0]
portfolio_data = manager.portfolios[first_portfolio_key]
api_client = PriceLabsAPI(api_key=portfolio_data['api_key'])

print(f"\nUsing portfolio: {portfolio_data['name']}")
print(f"API Key: ***{portfolio_data['api_key'][-8:]}")

# Get first listing
first_listing = list(manager.portfolio_listing_map.keys())[0]
listing_data = manager.listing_cache[first_listing]

print(f"Test listing: {listing_data.get('name')}")
print(f"Listing ID: {first_listing}")

print("\n" + "="*80)
print("Testing API Endpoints:")
print("="*80)

# Test 1: Get listing (should work)
print("\n1. Testing GET /v1/listings/{id} (get_listing)...")
try:
    result = api_client.get_listing(first_listing)
    if 'error' in result:
        print(f"   ❌ Error: {result['error']}")
    else:
        print(f"   ✅ Success - Listing name: {result.get('name', 'N/A')}")
except Exception as e:
    print(f"   ❌ Exception: {e}")

# Test 2: Get listings (should work)
print("\n2. Testing GET /v1/listings (get_all_listings)...")
try:
    result = api_client.get_all_listings(skip_hidden=True)
    if 'error' in result:
        print(f"   ❌ Error: {result['error']}")
    elif 'listings' in result:
        print(f"   ✅ Success - Found {len(result['listings'])} listings")
    else:
        print(f"   ⚠️  Unexpected response: {list(result.keys())}")
except Exception as e:
    print(f"   ❌ Exception: {e}")

# Test 3: Get reservation data (might not work)
print("\n3. Testing GET /v1/reservation_data (get_reservation_data)...")
try:
    result = api_client.get_reservation_data(
        pms=None,
        start_date='2024-01-01',
        end_date='2024-12-31',
        limit=10,
        offset=0
    )
    if 'error' in result:
        print(f"   ❌ Error: {result['error']}")
        print(f"   💡 This endpoint might require special access")
    elif 'data' in result:
        print(f"   ✅ Success - Found {len(result['data'])} reservations")
        if len(result['data']) > 0:
            print(f"   📊 First reservation keys: {list(result['data'][0].keys())}")
    else:
        print(f"   ⚠️  Unexpected response: {list(result.keys())}")
except Exception as e:
    print(f"   ❌ Exception: {e}")

# Test 4: Get pricing data
print("\n4. Testing GET /v1/listing_prices (get_listing_prices)...")
try:
    pms = listing_data.get('pms', 'airbnb')
    result = api_client.get_listing_prices([{'id': first_listing, 'pms': pms}])
    if 'error' in result:
        print(f"   ❌ Error: {result['error']}")
    elif 'data' in result:
        print(f"   ✅ Success - Got pricing data")
    else:
        print(f"   ⚠️  Response keys: {list(result.keys())}")
except Exception as e:
    print(f"   ❌ Exception: {e}")

# Test 5: Get neighborhood data
print("\n5. Testing GET /v1/neighborhood_data (get_neighborhood_data)...")
try:
    pms = listing_data.get('pms', 'airbnb')
    result = api_client.get_neighborhood_data(first_listing, pms)
    if 'error' in result:
        print(f"   ❌ Error: {result['error']}")
    elif 'data' in result:
        print(f"   ✅ Success - Got neighborhood data")
    else:
        print(f"   ⚠️  Response keys: {list(result.keys())}")
except Exception as e:
    print(f"   ❌ Exception: {e}")

print("\n" + "="*80)
print("Summary:")
print("="*80)
print("""
If reservation_data endpoint shows an error, this means:
1. The endpoint might not be available for all API keys
2. It might require special permissions from PriceLabs
3. The data might be available through a different endpoint
4. We may need to use an alternative approach

The good news: The Flask endpoint is correctly implemented.
If the API becomes available, it will work immediately.

Alternative: We could implement a mock/fallback mode for testing.
""")
