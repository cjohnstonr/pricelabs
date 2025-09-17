"""
Test all PriceLabs API endpoints and generate response example documentation
"""

import json
import os
from datetime import datetime, timedelta
from pricelabs_api import PriceLabsAPI

def ensure_folder_exists(folder_path):
    """Create folder if it doesn't exist"""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")

def write_response_to_md(endpoint_name, response, folder_path):
    """Write API response to a markdown file"""
    file_path = os.path.join(folder_path, f"{endpoint_name}-api-response-example.md")
    
    with open(file_path, 'w') as f:
        f.write(f"# {endpoint_name.replace('-', ' ').title()} API Response Example\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        f.write("## Response Structure\n\n")
        f.write("```json\n")
        f.write(json.dumps(response, indent=2, default=str))
        f.write("\n```\n")
    
    print(f"✓ Written: {file_path}")
    return file_path

def test_and_document_all_endpoints():
    """Test each endpoint and generate documentation"""
    
    # Initialize API client
    api = PriceLabsAPI()
    
    # Create output folder
    folder_path = "api-response-examples"
    ensure_folder_exists(folder_path)
    
    results = []
    
    # 1. Test GET all listings
    print("\n1. Testing GET /v1/listings...")
    try:
        response = api.get_all_listings(skip_hidden=False, only_syncing=False)
        write_response_to_md("get-all-listings", response, folder_path)
        results.append(("GET /v1/listings", "Success"))
        
        # Extract a listing ID for further tests if available
        listing_id = None
        pms = None
        if 'listings' in response and len(response['listings']) > 0:
            listing_id = response['listings'][0].get('id')
            pms = response['listings'][0].get('pms', 'airbnb')
            print(f"   Using listing_id: {listing_id}, pms: {pms} for further tests")
    except Exception as e:
        results.append(("GET /v1/listings", f"Failed: {e}"))
        listing_id = "834874"  # Fallback to example ID
        pms = "airbnb"
    
    # 2. Test POST update listings
    print("\n2. Testing POST /v1/listings (update)...")
    try:
        update_data = [{
            'id': listing_id or '834874',
            'pms': pms or 'airbnb',
            'min': 100
        }]
        response = api.update_listings(update_data)
        write_response_to_md("update-listings", response, folder_path)
        results.append(("POST /v1/listings", "Success"))
    except Exception as e:
        results.append(("POST /v1/listings", f"Failed: {e}"))
    
    # 3. Test GET specific listing
    print("\n3. Testing GET /v1/listings/{listing_id}...")
    try:
        if listing_id:
            response = api.get_listing(listing_id)
            write_response_to_md("get-specific-listing", response, folder_path)
            results.append((f"GET /v1/listings/{listing_id}", "Success"))
    except Exception as e:
        results.append((f"GET /v1/listings/{listing_id}", f"Failed: {e}"))
    
    # 4. Test POST add listing data (BookingSync only)
    print("\n4. Testing POST /v1/add_listing_data...")
    try:
        response = api.add_listing_data('12345', 'bookingsync')
        write_response_to_md("add-listing-data", response, folder_path)
        results.append(("POST /v1/add_listing_data", "Success"))
    except Exception as e:
        results.append(("POST /v1/add_listing_data", f"Failed: {e}"))
    
    # 5. Test GET listing overrides
    print("\n5. Testing GET /v1/listings/{listing_id}/overrides...")
    try:
        if listing_id and pms:
            response = api.get_listing_overrides(listing_id, pms)
            write_response_to_md("get-listing-overrides", response, folder_path)
            results.append((f"GET /v1/listings/{listing_id}/overrides", "Success"))
    except Exception as e:
        results.append((f"GET /v1/listings/{listing_id}/overrides", f"Failed: {e}"))
    
    # 6. Test POST update listing overrides
    print("\n6. Testing POST /v1/listings/{listing_id}/overrides...")
    try:
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        override_data = [{
            'date': tomorrow,
            'price': '150',
            'price_type': 'fixed',
            'currency': 'USD',
            'min_stay': 2
        }]
        if listing_id and pms:
            response = api.update_listing_overrides(listing_id, pms, override_data)
            write_response_to_md("update-listing-overrides", response, folder_path)
            results.append((f"POST /v1/listings/{listing_id}/overrides", "Success"))
    except Exception as e:
        results.append((f"POST /v1/listings/{listing_id}/overrides", f"Failed: {e}"))
    
    # 7. Test DELETE listing overrides
    print("\n7. Testing DELETE /v1/listings/{listing_id}/overrides...")
    try:
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        if listing_id and pms:
            response = api.delete_listing_overrides(listing_id, pms, [tomorrow])
            write_response_to_md("delete-listing-overrides", response, folder_path)
            results.append((f"DELETE /v1/listings/{listing_id}/overrides", "Success"))
    except Exception as e:
        results.append((f"DELETE /v1/listings/{listing_id}/overrides", f"Failed: {e}"))
    
    # 8. Test POST get listing prices
    print("\n8. Testing POST /v1/listing_prices...")
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        next_month = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        price_request = [{
            'id': listing_id or '834874',
            'pms': pms or 'airbnb',
            'dateFrom': today,
            'dateTo': next_month
        }]
        response = api.get_listing_prices(price_request)
        write_response_to_md("get-listing-prices", response, folder_path)
        results.append(("POST /v1/listing_prices", "Success"))
    except Exception as e:
        results.append(("POST /v1/listing_prices", f"Failed: {e}"))
    
    # 9. Test GET fetch rate plans
    print("\n9. Testing GET /v1/fetch_rate_plans...")
    try:
        if listing_id and pms:
            response = api.fetch_rate_plans(listing_id, pms)
            write_response_to_md("fetch-rate-plans", response, folder_path)
            results.append(("GET /v1/fetch_rate_plans", "Success"))
    except Exception as e:
        results.append(("GET /v1/fetch_rate_plans", f"Failed: {e}"))
    
    # 10. Test GET neighborhood data
    print("\n10. Testing GET /v1/neighborhood_data...")
    try:
        if listing_id and pms:
            response = api.get_neighborhood_data(listing_id, pms)
            write_response_to_md("get-neighborhood-data", response, folder_path)
            results.append(("GET /v1/neighborhood_data", "Success"))
    except Exception as e:
        results.append(("GET /v1/neighborhood_data", f"Failed: {e}"))
    
    # 11. Test GET reservation data
    print("\n11. Testing GET /v1/reservation_data...")
    try:
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        response = api.get_reservation_data(
            pms=pms,
            start_date=start_date,
            end_date=end_date,
            limit=10,
            offset=0
        )
        write_response_to_md("get-reservation-data", response, folder_path)
        results.append(("GET /v1/reservation_data", "Success"))
    except Exception as e:
        results.append(("GET /v1/reservation_data", f"Failed: {e}"))
    
    # Print summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    for endpoint, status in results:
        emoji = "✅" if "Success" in status else "❌"
        print(f"{emoji} {endpoint}: {status}")
    
    print(f"\nAll response examples saved in: {os.path.abspath(folder_path)}")
    
    return results

if __name__ == '__main__':
    print("Starting PriceLabs API Testing and Documentation")
    print("="*50)
    test_and_document_all_endpoints()