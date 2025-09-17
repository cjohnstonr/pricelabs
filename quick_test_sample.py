"""
Quick test of a sample of listings to find working ones
"""

import json
from pricelabs_api import PriceLabsAPI
from datetime import datetime, timedelta

def quick_test_sample():
    api = PriceLabsAPI()
    
    # Get all listings
    print("Getting all listings...")
    all_listings_result = api.get_all_listings(skip_hidden=False, only_syncing=False)
    
    if 'listings' not in all_listings_result:
        print("Failed to get listings")
        return
    
    listings = all_listings_result['listings']
    print(f"Found {len(listings)} total listings")
    
    # Test only listings with push_enabled = true first
    enabled_listings = [l for l in listings if l.get('push_enabled') == True]
    print(f"Found {len(enabled_listings)} listings with push_enabled=true")
    
    # Test first 10 enabled listings
    test_listings = enabled_listings[:10]
    
    # Date range for testing
    today = datetime.now().strftime('%Y-%m-%d')
    next_week = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    
    working_pricing = []
    
    for i, listing in enumerate(test_listings):
        listing_id = listing['id']
        pms = listing['pms']
        name = listing.get('name', 'Unknown')[:50]
        
        print(f"\n[{i+1}/{len(test_listings)}] Testing {listing_id} ({pms})")
        print(f"   Name: {name}")
        
        # Test pricing API
        try:
            price_request = [{
                'id': listing_id,
                'pms': pms,
                'dateFrom': today,
                'dateTo': next_week
            }]
            pricing_result = api.get_listing_prices(price_request)
            
            print(f"   Raw response: {json.dumps(pricing_result, indent=2)[:300]}...")
            
            # Check if it's working
            if isinstance(pricing_result, list) and len(pricing_result) > 0:
                first_result = pricing_result[0]
                if 'error' not in first_result and 'data' in first_result:
                    data_days = len(first_result.get('data', []))
                    print(f"   ✅ SUCCESS! Has {data_days} days of pricing data")
                    working_pricing.append({
                        'id': listing_id,
                        'pms': pms,
                        'name': name,
                        'data_days': data_days,
                        'sample_data': first_result.get('data', [])[:2]  # First 2 days
                    })
                    
                    # Save this working example immediately
                    with open(f'working_pricing_example_{listing_id}.json', 'w') as f:
                        json.dump(pricing_result, f, indent=2)
                    print(f"   Saved example to: working_pricing_example_{listing_id}.json")
                    
                else:
                    error_msg = first_result.get('error', 'Unknown error')
                    error_status = first_result.get('error_status', '')
                    print(f"   ❌ Error: {error_msg} ({error_status})")
            else:
                print(f"   ❌ Invalid response format")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    print(f"\n" + "="*50)
    print("QUICK TEST RESULTS")
    print("="*50)
    print(f"Tested {len(test_listings)} enabled listings")
    print(f"Found {len(working_pricing)} with working pricing data")
    
    if working_pricing:
        print(f"\nWORKING LISTINGS:")
        for item in working_pricing:
            print(f"  {item['id']} - {item['data_days']} days of data")
    else:
        print("\nNo working listings found in this sample. Let me try a few more...")
        
        # Try some more listings if none worked
        more_listings = enabled_listings[10:20] if len(enabled_listings) > 10 else listings[:10]
        
        for listing in more_listings:
            listing_id = listing['id']
            pms = listing['pms']
            
            print(f"\nTrying {listing_id} ({pms})...")
            
            try:
                price_request = [{
                    'id': listing_id,
                    'pms': pms,
                    'dateFrom': today,
                    'dateTo': next_week
                }]
                result = api.get_listing_prices(price_request)
                
                if (isinstance(result, list) and len(result) > 0 and 
                    'error' not in result[0] and 'data' in result[0]):
                    print(f"   ✅ FOUND WORKING LISTING: {listing_id}")
                    with open(f'working_pricing_example_{listing_id}.json', 'w') as f:
                        json.dump(result, f, indent=2)
                    break
                else:
                    print(f"   ❌ Still not working")
            except:
                print(f"   ❌ Exception")

if __name__ == '__main__':
    quick_test_sample()