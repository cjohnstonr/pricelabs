"""
Test all listings to find which ones have working pricing and neighborhood data
"""

import json
from pricelabs_api import PriceLabsAPI
from datetime import datetime, timedelta

def test_all_listings():
    api = PriceLabsAPI()
    
    # First get all listings
    print("Getting all listings...")
    all_listings_result = api.get_all_listings(skip_hidden=False, only_syncing=False)
    
    if 'listings' not in all_listings_result:
        print("Failed to get listings")
        return
    
    listings = all_listings_result['listings']
    print(f"Found {len(listings)} total listings")
    
    # Date range for testing
    today = datetime.now().strftime('%Y-%m-%d')
    next_week = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    
    working_pricing = []
    working_neighborhood = []
    
    # Test each listing
    for i, listing in enumerate(listings):
        listing_id = listing['id']
        pms = listing['pms']
        name = listing.get('name', 'Unknown')[:50]  # Truncate long names
        push_enabled = listing.get('push_enabled', False)
        
        print(f"\n[{i+1}/{len(listings)}] Testing {listing_id} ({pms}) - {name}")
        print(f"   push_enabled: {push_enabled}")
        
        # Test pricing API
        try:
            price_request = [{
                'id': listing_id,
                'pms': pms,
                'dateFrom': today,
                'dateTo': next_week
            }]
            pricing_result = api.get_listing_prices(price_request)
            
            # Check if it's working (not an error)
            if isinstance(pricing_result, list) and len(pricing_result) > 0:
                first_result = pricing_result[0]
                if 'error' not in first_result and 'data' in first_result:
                    print(f"   ✅ PRICING WORKS - Has {len(first_result.get('data', []))} days of data")
                    working_pricing.append({
                        'id': listing_id,
                        'pms': pms,
                        'name': name,
                        'push_enabled': push_enabled,
                        'data_days': len(first_result.get('data', []))
                    })
                else:
                    error_msg = first_result.get('error', 'Unknown error')
                    print(f"   ❌ Pricing error: {error_msg}")
            else:
                print(f"   ❌ Pricing failed: Invalid response format")
                
        except Exception as e:
            print(f"   ❌ Pricing exception: {e}")
        
        # Test neighborhood API
        try:
            neighborhood_result = api.get_neighborhood_data(listing_id, pms)
            
            if 'error' not in neighborhood_result and 'data' in neighborhood_result:
                print(f"   ✅ NEIGHBORHOOD WORKS")
                working_neighborhood.append({
                    'id': listing_id,
                    'pms': pms,
                    'name': name,
                    'push_enabled': push_enabled
                })
            else:
                error_msg = neighborhood_result.get('error', 'Unknown error')
                print(f"   ❌ Neighborhood error: {error_msg}")
                
        except Exception as e:
            print(f"   ❌ Neighborhood exception: {e}")
    
    # Summary
    print(f"\n" + "="*60)
    print("SUMMARY RESULTS")
    print("="*60)
    print(f"Total listings tested: {len(listings)}")
    print(f"Listings with working PRICING data: {len(working_pricing)}")
    print(f"Listings with working NEIGHBORHOOD data: {len(working_neighborhood)}")
    
    if working_pricing:
        print(f"\nListings with WORKING PRICING:")
        for item in working_pricing:
            print(f"  {item['id']} ({item['pms']}) - {item['data_days']} days - {item['name']}")
    
    if working_neighborhood:
        print(f"\nListings with WORKING NEIGHBORHOOD:")
        for item in working_neighborhood:
            print(f"  {item['id']} ({item['pms']}) - {item['name']}")
    
    # Save results
    results = {
        'total_tested': len(listings),
        'working_pricing': working_pricing,
        'working_neighborhood': working_neighborhood,
        'test_date': datetime.now().isoformat()
    }
    
    with open('working_listings_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: working_listings_test_results.json")
    
    return results

if __name__ == '__main__':
    test_all_listings()