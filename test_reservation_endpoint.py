"""
Test script to validate reservation_data endpoint availability and API response
This helps us understand what data is actually available before implementing the fix
"""

import requests
import json
from pricelabs_api import PriceLabsAPI
from portfolio_manager import PortfolioManager

def test_flask_endpoint_exists():
    """Test if the Flask endpoint exists on port 5050"""
    print("\n" + "="*80)
    print("TEST 1: Check if /api/reservation_data endpoint exists on Flask server")
    print("="*80)

    test_listing_id = "4305303"  # Example listing ID
    url = f"http://localhost:5050/api/reservation_data/{test_listing_id}?start_date=2025-01-01&end_date=2025-12-31"

    try:
        response = requests.get(url, timeout=5)
        print(f"✅ Endpoint responded with status: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"❌ Flask server not running on port 5050")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_pricelabs_api_directly():
    """Test if PriceLabs API has reservation data available"""
    print("\n" + "="*80)
    print("TEST 2: Check PriceLabs API reservation_data method directly")
    print("="*80)

    try:
        # Initialize portfolio manager to get API keys
        manager = PortfolioManager()
        manager.refresh_all_listings()

        # Get first available portfolio
        if not manager.portfolios:
            print("❌ No portfolios configured")
            return False

        first_portfolio_key = list(manager.portfolios.keys())[0]

        # Get API client using the correct method
        portfolio_data = manager.portfolios[first_portfolio_key]
        api_client = PriceLabsAPI(api_key=portfolio_data['api_key'])

        print(f"✅ Using portfolio: {portfolio_data['name']}")

        # Get a sample listing ID from this portfolio
        # Note: manager.refresh_all_listings() returns the data, doesn't store in manager.all_listings
        listing_data_response = {}
        for listing_id in list(manager.portfolio_listing_map.keys())[:1]:  # Get first listing
            portfolio_key = manager.portfolio_listing_map[listing_id]
            if portfolio_key == first_portfolio_key:
                listing_data_response = manager.listing_cache.get(listing_id, {})
                break

        if not listing_data_response:
            print("❌ No listings found in cache")
            return False

        listings = [listing_data_response]  # Make it a list for compatibility

        if not listings:
            print("❌ No listings found in portfolio")
            return False

        sample_listing = listings[0]
        listing_id = sample_listing.get('id')
        listing_name = sample_listing.get('name', 'Unknown')

        print(f"✅ Testing with listing: {listing_name} (ID: {listing_id})")

        # Call the API method with correct parameters
        print("\nCalling api.get_reservation_data()...")
        reservation_data = api_client.get_reservation_data(
            pms=None,
            start_date='2025-01-01',
            end_date='2025-12-31',
            limit=100,
            offset=0
        )

        print(f"\n✅ API Response received!")
        print(f"Response type: {type(reservation_data)}")

        # Analyze the response structure
        if isinstance(reservation_data, dict):
            print(f"Response keys: {list(reservation_data.keys())}")

            if 'data' in reservation_data:
                data_items = reservation_data['data']
                print(f"Number of reservation records: {len(data_items) if isinstance(data_items, list) else 'N/A'}")

                if isinstance(data_items, list) and len(data_items) > 0:
                    print(f"\n📊 Sample reservation record (first item):")
                    print(json.dumps(data_items[0], indent=2))

                    # Analyze key fields needed for calculations
                    print(f"\n🔍 Key fields present in reservation data:")
                    sample = data_items[0]
                    required_fields = [
                        'check_in',
                        'check_out',
                        'no_of_days',
                        'rental_revenue',
                        'booking_status',
                        'listing_id',
                        'reservation_id'
                    ]

                    for field in required_fields:
                        status = "✅" if field in sample else "❌"
                        value = sample.get(field, "MISSING")
                        print(f"  {status} {field}: {value}")

                    return True
                else:
                    print("⚠️  No reservation records found in date range")
                    return True  # API works, just no data
            else:
                print(f"⚠️  Unexpected response structure: {reservation_data}")
                return False
        else:
            print(f"⚠️  Response is not a dict: {reservation_data}")
            return False

    except AttributeError as e:
        print(f"❌ API method doesn't exist: {e}")
        print("\n🔍 Checking available methods on PriceLabsAPI class...")
        api_methods = [method for method in dir(PriceLabsAPI) if not method.startswith('_')]
        print(f"Available methods: {api_methods}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_neighborhood_data_structure():
    """Test the neighborhood data structure to understand percentile data format"""
    print("\n" + "="*80)
    print("TEST 3: Analyze neighborhood data structure for percentile calculations")
    print("="*80)

    try:
        manager = PortfolioManager()
        all_listings_data = manager.refresh_all_listings()

        first_portfolio_key = list(manager.portfolios.keys())[0]

        # Get API client using the correct method
        portfolio_config = manager.portfolios[first_portfolio_key]
        api_client = PriceLabsAPI(api_key=portfolio_config['api_key'])

        portfolio_data = all_listings_data.get(first_portfolio_key, {})
        listings = portfolio_data.get('listings', [])

        if not listings:
            print("❌ No listings found")
            return False

        sample_listing = listings[0]
        listing_id = sample_listing.get('id')
        pms = sample_listing.get('pms', 'airbnb')
        bedrooms = sample_listing.get('no_of_bedrooms', 1)

        print(f"Testing with listing: {sample_listing.get('name')} ({bedrooms} bedrooms)")

        # Get neighborhood data
        print("\nFetching neighborhood data...")
        neighborhood_data = api_client.get_neighborhood_data(listing_id, pms)

        if isinstance(neighborhood_data, dict) and 'data' in neighborhood_data:
            data = neighborhood_data['data']

            if 'Future Percentile Prices' in data:
                print("✅ Future Percentile Prices found")
                percentile_data = data['Future Percentile Prices']

                if 'Category' in percentile_data:
                    categories = percentile_data['Category']
                    print(f"Available bedroom categories: {list(categories.keys())}")

                    # Get data for this listing's bedroom count
                    bedroom_data = categories.get(str(bedrooms)) or categories.get('1')

                    if bedroom_data:
                        print(f"\n📊 Structure for {bedrooms}-bedroom data:")
                        print(f"Keys: {list(bedroom_data.keys())}")

                        if 'X_values' in bedroom_data:
                            dates = bedroom_data['X_values']
                            print(f"Date range: {dates[0]} to {dates[-1]} ({len(dates)} days)")

                        if 'Y_values' in bedroom_data:
                            y_vals = bedroom_data['Y_values']
                            print(f"Number of percentile series: {len(y_vals)}")
                            print(f"Percentile names/indices:")
                            print(f"  [0] = 25th percentile (length: {len(y_vals[0]) if y_vals else 0})")
                            print(f"  [1] = 50th percentile (length: {len(y_vals[1]) if len(y_vals) > 1 else 0})")
                            print(f"  [2] = 75th percentile (length: {len(y_vals[2]) if len(y_vals) > 2 else 0})")
                            print(f"  [3] = Median Booked (length: {len(y_vals[3]) if len(y_vals) > 3 else 0})")
                            print(f"  [4] = 90th percentile (length: {len(y_vals[4]) if len(y_vals) > 4 else 0})")

                            # Show sample values for first date
                            if dates and y_vals and len(y_vals) > 3:
                                print(f"\n📈 Sample prices for {dates[0]}:")
                                print(f"  25th %ile: ${y_vals[0][0]}")
                                print(f"  50th %ile: ${y_vals[1][0]}")
                                print(f"  Median Booked: ${y_vals[3][0]} ⭐ (used in calculations)")
                                print(f"  75th %ile: ${y_vals[2][0]}")
                                print(f"  90th %ile: ${y_vals[4][0]}")

                        return True

        print("❌ Expected data structure not found")
        return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_calculation_logic():
    """Test the calculation logic with sample data"""
    print("\n" + "="*80)
    print("TEST 4: Validate calculation logic with sample data")
    print("="*80)

    # Sample data based on code analysis
    market_median = 150.0  # From neighborhood data
    your_booked_rate = 165.0  # From reservation data
    current_price = 140.0  # From pricing data

    print(f"Sample inputs:")
    print(f"  Market Median Booked Price: ${market_median}")
    print(f"  Your Actual Booked Rate: ${your_booked_rate}")
    print(f"  Current Price (for tomorrow): ${current_price}")

    # Step 1: Calculate avgPercentVsMarket
    avg_percent_vs_market = ((your_booked_rate - market_median) / market_median) * 100
    print(f"\n✅ Step 1: OUR AVG VS MARKET")
    print(f"  Formula: ((165 - 150) / 150) * 100")
    print(f"  Result: {avg_percent_vs_market:+.1f}%")
    print(f"  Meaning: You typically book at {avg_percent_vs_market:+.1f}% vs market median")

    # Step 2: Calculate optimized target
    optimized_target = market_median * (1 + (avg_percent_vs_market / 100))
    print(f"\n✅ Step 2: OPTIMIZED TARGET")
    print(f"  Formula: 150 * (1 + ({avg_percent_vs_market:.1f} / 100))")
    print(f"  Result: ${optimized_target:.2f}")
    print(f"  Meaning: Recommended price based on your historical performance")

    # Step 3: Calculate adjustment percentage
    adjustment_percent = ((optimized_target - current_price) / current_price) * 100
    print(f"\n✅ Step 3: PRICE ADJUSTMENT %")
    print(f"  Formula: (({optimized_target:.2f} - {current_price}) / {current_price}) * 100")
    print(f"  Result: {adjustment_percent:+.1f}%")
    print(f"  Meaning: {'Increase' if adjustment_percent > 0 else 'Decrease'} price by {abs(adjustment_percent):.1f}%")

    # Categorization
    if adjustment_percent > 10:
        category = "increase-significant (>10%)"
    elif adjustment_percent > 2:
        category = "increase-moderate (2-10%)"
    elif adjustment_percent < -10:
        category = "decrease-significant (<-10%)"
    elif adjustment_percent < -2:
        category = "decrease-moderate (-10% to -2%)"
    else:
        category = "optimal (within 2%)"

    print(f"\n📊 Price Adjustment Category: {category}")

    return True

def main():
    """Run all validation tests"""
    print("\n" + "🔬"*40)
    print("RESERVATION DATA ENDPOINT - VALIDATION TEST SUITE")
    print("🔬"*40)

    results = {
        "Flask Endpoint": test_flask_endpoint_exists(),
        "PriceLabs API": test_pricelabs_api_directly(),
        "Neighborhood Data": test_neighborhood_data_structure(),
        "Calculation Logic": test_calculation_logic()
    }

    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    all_passed = all(results.values())

    if all_passed:
        print("\n🎉 All tests passed! Ready to implement the fix.")
    else:
        print("\n⚠️  Some tests failed. Review output above for details.")

    return all_passed

if __name__ == '__main__':
    main()
